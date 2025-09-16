import sounddevice as sd
import numpy as np
import torch
import whisper
from gtts import gTTS
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Tuple
from ..interfaces.base import ISpeechToText, ITextToSpeech
from ..config.settings import Settings
import logging

logger = logging.getLogger(__name__)

class AudioRecorder:
    def __init__(self, settings: Settings):
        self.settings = settings
    
    def record_audio(self, silence_duration: float = None, threshold: float = None) -> np.ndarray:
        """Graba audio con detección de silencio"""
        silence_duration = silence_duration or self.settings.audio.silence_duration
        threshold = threshold or self.settings.audio.silence_threshold
        
        fs = self.settings.audio.sample_rate
        recording = []
        current_silence = 0
        
        print("\n🎙 Estoy escuchando... (habla y haz una pausa para terminar)")
        
        while True:
            chunk = sd.rec(int(0.2 * fs), samplerate=fs, channels=1, dtype='float32')
            sd.wait()
            chunk = np.squeeze(chunk)
            recording.extend(chunk)
            
            if np.abs(chunk).mean() < threshold:
                current_silence += 0.2
                if current_silence >= silence_duration:
                    break
            else:
                current_silence = 0
        
        return np.array(recording)

class WhisperSTT(ISpeechToText):
    def __init__(self, model_name: str = "base"):
        self.model = whisper.load_model(model_name)
        logger.info(f"Whisper model '{model_name}' loaded successfully")
    
    def recognize(self, audio_data: np.ndarray) -> Tuple[str, str]:
        """Reconoce texto y detecta idioma del audio"""
        try:
            audio_tensor = torch.from_numpy(audio_data).float()
            audio_tensor = whisper.pad_or_trim(audio_tensor)
            mel = whisper.log_mel_spectrogram(audio_tensor).to(self.model.device)
            
            # Detectar idioma
            _, probs = self.model.detect_language(mel)
            detected_language = max(probs, key=probs.get)
            
            # Transcribir
            options = whisper.DecodingOptions()
            result = whisper.decode(self.model, mel, options)
            
            return result.text.strip(), detected_language
            
        except Exception as e:
            logger.error(f"Error in speech recognition: {e}")
            return "", "unknown"

class GTTSService(ITextToSpeech):
    def __init__(self, settings: Settings):
        self.settings = settings
    
    def speak(self, text: str, language: str = "en") -> None:
        """Convierte texto a voz y lo reproduce con manejo robusto de errores"""
        try:
            tts = gTTS(text=text, lang=language)
            audio_path = self.settings.paths.working_dir / self.settings.audio.audio_file
            
            # Asegurar que el directorio existe
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Guardar archivo
            tts.save(str(audio_path))
            
            # Esperar un momento para que el archivo se escriba completamente
            time.sleep(0.5)
            
            # Verificar que el archivo existe y tiene contenido
            if not audio_path.exists() or audio_path.stat().st_size == 0:
                logger.error("Audio file was not created properly")
                return
            
            # Intentar reproducir con múltiples métodos
            if not self._play_audio_windows(audio_path):
                if not self._play_audio_fallback(audio_path):
                    logger.warning("Could not play audio file")
            
            logger.info(f"TTS played: {text[:50]}...")
            
        except Exception as e:
            logger.error(f"Error in TTS: {e}")
    
    def _play_audio_windows(self, audio_path: Path) -> bool:
        """Intenta reproducir audio usando métodos específicos de Windows"""
        try:
            # Método 1: usar start con comillas para paths con espacios
            result = subprocess.run(
                f'start "" "{audio_path}"', 
                shell=True, 
                capture_output=True, 
                timeout=5
            )
            if result.returncode == 0:
                return True
        except:
            pass
        
        try:
            # Método 2: usar PowerShell
            ps_command = f'Invoke-Item "{audio_path}"'
            result = subprocess.run(
                ["powershell", "-Command", ps_command], 
                capture_output=True, 
                timeout=5
            )
            if result.returncode == 0:
                return True
        except:
            pass
        
        try:
            # Método 3: usar explorer
            result = subprocess.run(
                ["explorer", str(audio_path)], 
                capture_output=True, 
                timeout=5
            )
            if result.returncode == 0:
                return True
        except:
            pass
        
        return False
    
    def _play_audio_fallback(self, audio_path: Path) -> bool:
        """Método de respaldo para reproducir audio"""
        try:
            # Intentar con pygame (si está instalado)
            try:
                import pygame
                pygame.mixer.init()
                pygame.mixer.music.load(str(audio_path))
                pygame.mixer.music.play()
                
                # Esperar a que termine
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                pygame.mixer.quit()
                return True
            except ImportError:
                pass
            
            # Intentar con playsound (si está instalado)
            try:
                from playsound import playsound
                playsound(str(audio_path))
                return True
            except ImportError:
                pass
            
        except Exception as e:
            logger.error(f"Fallback audio playback failed: {e}")
        
        return False