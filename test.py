import os
import whisper
import sounddevice as sd
import numpy as np
import torch
from transformers import pipeline
from gtts import gTTS
import json
from datetime import datetime
import random
import logging

# Configuración centralizada
class Config:
    WORKING_DIR = r"D:\SISTEMA01 ENTREGA PUESTO\Fabio\IA"
    AUDIO_FILE = "salida.mp3"
    ERRORS_FILE = "errores_memoria.json"
    SAMPLE_RATE = 16000
    SILENCE_THRESHOLD = 0.01
    SILENCE_DURATION = 1.2

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

os.chdir(Config.WORKING_DIR)

class AIAssistant:
    """Asistente de conversación por voz para práctica de inglés"""
    
    def __init__(self):
        """Inicializa el asistente cargando modelos y configuración"""
        self.historial = []
        self.errores_memoria = self._cargar_errores()
        self._cargar_modelos()
    
    def _cargar_modelos(self):
        """Carga todos los modelos de IA necesarios"""
        try:
            print("⏳ Cargando modelos...")
            logger.info("Iniciando carga de modelos")
            
            self.stt_model = whisper.load_model("base")
            self.chat_model = pipeline("text-generation", model="microsoft/DialoGPT-medium", 
                                     device=0 if torch.cuda.is_available() else -1)
            self.grammar_corrector = pipeline("text2text-generation", 
                                            model="prithivida/grammar_error_correcter_v1")
            self.translator_en = pipeline("translation", model="Helsinki-NLP/opus-mt-es-en")
            self.translator_es = pipeline("translation", model="Helsinki-NLP/opus-mt-en-es")
            
            logger.info("Modelos cargados exitosamente")
            print("✅ Modelos cargados correctamente")
            
        except Exception as e:
            logger.error(f"Error cargando modelos: {e}")
            print(f"❌ Error cargando modelos: {e}")
            raise
    
    def _cargar_errores(self):
        """Carga la memoria de errores desde archivo"""
        try:
            if os.path.exists(Config.ERRORS_FILE):
                with open(Config.ERRORS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error cargando errores: {e}")
            return {}
    
    def escuchar(self, silencio_seg=None, umbral=None):
        """
        Escucha audio del micrófono con detección automática de silencio
        
        Args:
            silencio_seg (float): Duración de silencio para terminar grabación
            umbral (float): Umbral de volumen para detectar silencio
            
        Returns:
            tuple: (texto_reconocido, idioma_detectado)
        """
        silencio_seg = silencio_seg or Config.SILENCE_DURATION
        umbral = umbral or Config.SILENCE_THRESHOLD
        
        try:
            fs = Config.SAMPLE_RATE
            print("\n🎙 Estoy escuchando... (habla y haz una pausa para terminar)")
            grabacion = []
            silencio_actual = 0

            while True:
                bloque = sd.rec(int(0.2 * fs), samplerate=fs, channels=1, dtype='float32')
                sd.wait()
                bloque = np.squeeze(bloque)
                grabacion.extend(bloque)

                if np.abs(bloque).mean() < umbral:
                    silencio_actual += 0.2
                    if silencio_actual >= silencio_seg:
                        break
                else:
                    silencio_actual = 0

            audio = np.array(grabacion)
            audio_tensor = torch.from_numpy(audio).float()
            audio_tensor = whisper.pad_or_trim(audio_tensor)
            mel = whisper.log_mel_spectrogram(audio_tensor).to(self.stt_model.device)

            _, probs = self.stt_model.detect_language(mel)
            idioma_detectado = max(probs, key=probs.get)

            options = whisper.DecodingOptions()
            result = whisper.decode(self.stt_model, mel, options)

            logger.info(f"Audio reconocido: {result.text.strip()}, Idioma: {idioma_detectado}")
            return result.text.strip(), idioma_detectado
            
        except Exception as e:
            logger.error(f"Error en escucha: {e}")
            print(f"❌ Error en el micrófono: {e}")
            return "", "unknown"

    def hablar(self, texto, idioma="en"):
        """
        Convierte texto a voz y lo reproduce
        
        Args:
            texto (str): Texto a convertir a voz
            idioma (str): Código de idioma para TTS
        """
        try:
            tts = gTTS(text=texto, lang=idioma)
            tts.save(Config.AUDIO_FILE)
            os.system(f"start {Config.AUDIO_FILE}")
            logger.info(f"TTS reproducido: {texto[:50]}...")
        except Exception as e:
            logger.error(f"Error en TTS: {e}")
            print(f"❌ Error en síntesis de voz: {e}")

    def guardar_errores(self):
        """Guarda la memoria de errores en archivo"""
        try:
            with open(Config.ERRORS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.errores_memoria, f, ensure_ascii=False, indent=4)
            logger.info("Errores guardados correctamente")
        except Exception as e:
            logger.error(f"Error guardando errores: {e}")

    def registrar_error(self, original, correccion):
        """
        Registra un error gramatical en la memoria
        
        Args:
            original (str): Texto original con error
            correccion (str): Texto corregido
        """
        clave = correccion.lower()
        if clave not in self.errores_memoria:
            self.errores_memoria[clave] = {"veces": 0, "ultima_fecha": None, "originales": []}
        
        self.errores_memoria[clave]["veces"] += 1
        self.errores_memoria[clave]["ultima_fecha"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.errores_memoria[clave]["originales"].append(original)
        self.guardar_errores()
        logger.info(f"Error registrado: {original} -> {correccion}")

    def corregir_ingles(self, texto):
        """
        Corrige errores gramaticales en inglés
        
        Args:
            texto (str): Texto a corregir
            
        Returns:
            str or None: Texto corregido o None si no hay errores
        """
        try:
            correccion = self.grammar_corrector(texto)[0]['generated_text']
            if correccion.lower() != texto.lower():
                self.registrar_error(texto, correccion)
                return correccion
        except Exception as e:
            logger.error(f"Error en corrección gramatical: {e}")
        return None

    def felicitar_si_mejoraste(self, texto):
        """
        Verifica si el usuario corrigió un error previo y lo felicita
        
        Args:
            texto (str): Texto del usuario a verificar
        """
        for correccion, datos in self.errores_memoria.items():
            if texto.lower() == correccion and datos["veces"] > 0:
                print(f"🎉 ¡Muy bien! Antes cometías este error y ahora lo dijiste perfecto: '{correccion}'")
                self.hablar("Great job! You corrected a past mistake.", idioma="en")
                datos["veces"] -= 1
                self.guardar_errores()
                logger.info(f"Usuario mejoró error: {correccion}")

    def responder(self, texto):
        """
        Genera una respuesta usando el modelo de chat
        
        Args:
            texto (str): Entrada del usuario
            
        Returns:
            str: Respuesta generada
        """
        try:
            contexto = " ".join(self.historial[-6:])
            entrada = contexto + " " + texto
            respuesta = self.chat_model(entrada, max_length=150, pad_token_id=50256)[0]['generated_text']
            return respuesta
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return "Sorry, I couldn't generate a response."

    def resumen_sesion(self):
        """Muestra un resumen de errores de la sesión"""
        print("\n📊 Resumen de la sesión:")
        errores_frecuentes = 0
        errores_ocasionales = 0
        
        for correccion, datos in self.errores_memoria.items():
            if datos["veces"] >= 3:
                print(f"⚠ Error frecuente: '{correccion}' ({datos['veces']} veces)")
                errores_frecuentes += 1
            elif datos["veces"] > 0:
                print(f"🔄 Error ocasional: '{correccion}' ({datos['veces']} veces)")
                errores_ocasionales += 1
        
        if errores_frecuentes == 0 and errores_ocasionales == 0:
            print("🎉 ¡Excelente! No hay errores registrados en esta sesión.")
        
        self.guardar_errores()
        logger.info(f"Resumen sesión - Frecuentes: {errores_frecuentes}, Ocasionales: {errores_ocasionales}")

    def generar_preguntas(self):
        """
        Genera preguntas adaptativas basadas en errores frecuentes
        
        Returns:
            list: Lista de preguntas para entrenamiento
        """
        preguntas_base = [
            "What did you do yesterday?",
            "Describe your favorite place.",
            "What is your dream job?",
            "Tell me about your hobbies.",
            "What is your favorite movie and why?"
        ]
        
        # Añadir preguntas específicas para errores frecuentes
        for correccion, datos in self.errores_memoria.items():
            if datos["veces"] >= 2:
                preguntas_base.append(f"Use this phrase correctly in a sentence: '{correccion}'")
        
        random.shuffle(preguntas_base)
        return preguntas_base

    def validar_comando(self, comando):
        """
        Valida si un comando es válido
        
        Args:
            comando (str): Comando a validar
            
        Returns:
            bool: True si es válido, False si no
        """
        comandos_validos = ["entrenar", "libre", "salir", "ayuda"]
        if comando not in comandos_validos:
            print(f"❌ Comando '{comando}' no válido. Usa: {', '.join(comandos_validos)}")
            return False
        return True

    def dar_feedback(self, respuesta_usuario, idioma):
        """
        Da feedback en español sobre la respuesta del usuario
        
        Args:
            respuesta_usuario (str): La respuesta del usuario
            idioma (str): Idioma detectado de la respuesta
        """
        if not respuesta_usuario:
            print("⚠ No te entendí bien, ¿puedes repetir?")
            self.hablar("No te entendí bien, puedes repetir?", idioma="es")
            return
        
        try:
            if idioma.startswith("en"):
                # Traducir al español para mostrar comprensión
                traduccion = self.translator_es(respuesta_usuario)[0]['translation_text']
                print(f"📝 Entendí que dijiste: '{respuesta_usuario}'")
                print(f"🔄 Que significa: '{traduccion}'")
                
                # Verificar si mejoró un error previo
                self.felicitar_si_mejoraste(respuesta_usuario)
                
                # Corregir gramática si es necesario
                correccion = self.corregir_ingles(respuesta_usuario)
                
                if correccion:
                    correccion_es = self.translator_es(correccion)[0]['translation_text']
                    print(f"✏ Corrección sugerida: '{correccion}'")
                    print(f"📖 Que sería: '{correccion_es}'")
                    feedback = f"Entendí que dijiste '{respuesta_usuario}', que significa '{traduccion}'. Una forma más correcta sería '{correccion}'"
                    self.hablar(feedback, idioma="es")
                else:
                    print("✅ ¡Perfecto! Tu inglés está correcto.")
                    feedback = f"¡Muy bien! Dijiste '{respuesta_usuario}' que significa '{traduccion}' y está perfecto."
                    self.hablar(feedback, idioma="es")
                    
            elif idioma.startswith("es"):
                print(f"📝 Dijiste en español: '{respuesta_usuario}'")
                print("💡 Recuerda que es mejor practicar respondiendo en inglés.")
                
                # Traducir al inglés para ayudar
                traduccion = self.translator_en(respuesta_usuario)[0]['translation_text']
                print(f"🔄 En inglés sería: '{traduccion}'")
                feedback = f"Dijiste '{respuesta_usuario}' en español. En inglés sería '{traduccion}'. Intenta responder en inglés para practicar mejor."
                self.hablar(feedback, idioma="es")
                
            else:
                print("❓ No pude identificar el idioma claramente.")
                print("💡 Intenta hablar más claro o en inglés.")
                self.hablar("No pude identificar el idioma claramente. Intenta hablar más claro o en inglés.", idioma="es")
                
        except Exception as e:
            logger.error(f"Error en feedback: {e}")
            print("❌ No pude procesar tu respuesta correctamente.")
            self.hablar("No pude procesar tu respuesta correctamente.", idioma="es")

    def modo_entrenamiento(self):
        """Ejecuta el modo de entrenamiento con preguntas adaptativas"""
        print("\n🎯 Iniciando modo entrenamiento...")
        print("💡 Responde en inglés para obtener mejor feedback")
        self.hablar("Iniciando modo entrenamiento. Responde en inglés para obtener mejor feedback.", idioma="es")
        
        preguntas = self.generar_preguntas()
        
        for i, pregunta in enumerate(preguntas[:5], 1):  # Limitar a 5 preguntas
            transiciones = ["Hmm, let's see...", "Alright, here's one for you:", "Okay, try this:"]
            print(f"\n❓ Pregunta {i}/5: {pregunta}")
            
            # Traducir la pregunta al español para mayor comprensión
            try:
                pregunta_es = self.translator_es(pregunta)[0]['translation_text']
                print(f"🔄 En español: {pregunta_es}")
            except:
                pass
            
            self.hablar(random.choice(transiciones) + " " + pregunta, idioma="en")
            
            respuesta_usuario, idioma = self.escuchar()
            
            # Dar feedback detallado en español
            self.dar_feedback(respuesta_usuario, idioma)
            
            # Pausa breve antes de la siguiente pregunta
            print("\n" + "="*50)
        
        self.resumen_sesion()

    def modo_libre(self):
        """Ejecuta el modo de conversación libre"""
        entrada, idioma_detectado = self.escuchar()
        print(f"🗣 Tú ({idioma_detectado}): {entrada}")
        
        if not entrada:
            print("⚠ No se detectó entrada de audio")
            return
        
        try:
            if idioma_detectado.startswith("es"):
                traduccion = self.translator_en(entrada)[0]['translation_text']
                print(f"🔄 En inglés: {traduccion}")
                
                salida = self.responder(traduccion)
                self.historial.append(f"Tú (ES): {entrada}")
                self.historial.append(f"Bot (EN): {salida}")
                
                # Traducir respuesta del bot al español
                try:
                    salida_es = self.translator_es(salida)[0]['translation_text']
                    print(f"🤖 Bot (EN): {salida}")
                    print(f"📖 Significa: {salida_es}")
                except:
                    print(f"🤖 Bot (EN): {salida}")
                
                self.hablar(salida, idioma="en")
                
            elif idioma_detectado.startswith("en"):
                # Dar feedback en español sobre lo que dijo en inglés
                try:
                    traduccion = self.translator_es(entrada)[0]['translation_text']
                    print(f"📝 Dijiste: '{entrada}' (que significa: '{traduccion}')")
                except:
                    print(f"📝 Dijiste: '{entrada}'")
                
                self.felicitar_si_mejoraste(entrada)
                correccion = self.corregir_ingles(entrada)
                
                if correccion:
                    try:
                        correccion_es = self.translator_es(correccion)[0]['translation_text']
                        print(f"✏ Mejor sería: '{correccion}' ('{correccion_es}')")
                    except:
                        print(f"✏ Mejor sería: '{correccion}'")
                
                salida = self.responder(entrada)
                self.historial.append(f"Tú (EN): {entrada}")
                self.historial.append(f"Bot (EN): {salida}")
                print(f"🤖 Bot (EN): {salida}")
                
                # Traducir respuesta del bot para comprensión
                try:
                    salida_es = self.translator_es(salida)[0]['translation_text']
                    print(f"📖 Significa: {salida_es}")
                except:
                    pass
                
                self.hablar(salida, idioma="en")
                
        except Exception as e:
            logger.error(f"Error en modo libre: {e}")
            print(f"❌ Error procesando entrada: {e}")

    def ejecutar(self):
        """Bucle principal del asistente"""
        print("✅ Asistente listo. Comandos: 'entrenar', 'libre', 'salir', 'ayuda'")
        
        while True:
            try:
                comando = input("\nEscribe un comando: ").strip().lower()
                
                if not self.validar_comando(comando):
                    continue
                
                if comando == "salir":
                    self.resumen_sesion()
                    print("👋 Hasta luego")
                    logger.info("Sesión terminada por el usuario")
                    break
                    
                elif comando == "entrenar":
                    self.modo_entrenamiento()
                    
                elif comando == "libre":
                    self.modo_libre()
                    
                elif comando == "ayuda":
                    print("""
📖 Comandos disponibles:
• 'entrenar' - Modo entrenamiento con preguntas adaptativas
• 'libre' - Conversación libre (español/inglés)
• 'salir' - Terminar sesión y mostrar resumen
• 'ayuda' - Mostrar esta ayuda
                    """)
                    
            except KeyboardInterrupt:
                print("\n\n⚠ Sesión interrumpida por el usuario")
                self.resumen_sesion()
                break
            except Exception as e:
                logger.error(f"Error en bucle principal: {e}")
                print(f"❌ Error inesperado: {e}")

# Inicializar y ejecutar el asistente
if __name__ == "__main__":
    try:
        asistente = AIAssistant()
        asistente.ejecutar()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        logger.critical(f"Error crítico al inicializar: {e}")
