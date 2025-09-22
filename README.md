# IA English Assistant

**Version final - Solo Ollama, simple y confiable**

## Caracteristicas

- Solo Ollama - Sin APIs externas ni keys
- UI moderna - Interfaz grafica intuitiva  
- Chat fluido - Conversacion natural en ingles
- Traduccion - Ingles <-> Espanol
- Rapido - Respuestas en tiempo real
- Privado - Todo local, sin enviar datos

## Instalacion

1. **Instalar Ollama**
   ```bash
   # Descargar desde: https://ollama.ai
   # O usar: curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Instalar modelo**
   ```bash
   ollama pull mistral
   # o: ollama pull llama3
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements_final.txt
   ```

## Uso

1. **Iniciar Ollama**
   ```bash
   ollama serve
   ```

2. **Ejecutar aplicacion**
   ```bash
   python start_final.py
   ```

## Resolucion de problemas

### Ollama no responde
- Verifica que este ejecutandose: `ollama serve`
- Comprueba el puerto: http://localhost:11434
- Reinstala si es necesario

### Error de dependencias
```bash
pip install --upgrade requests
```

### UI no aparece
- Verifica que tkinter este instalado (viene con Python)
- En Ubuntu: `sudo apt-get install python3-tk`

## Estructura

```
├── src/
│   ├── backend/services/ai/
│   │   ├── ollama_service.py    # Conexion con Ollama
│   │   └── chat_service.py      # Logica de chat
│   └── config/
│       └── settings.py          # Configuracion
├── main_final.py                # Aplicacion principal
├── start_final.py              # Iniciador
└── requirements_final.txt       # Dependencias
```

## Comandos utiles

- **Listar modelos**: `ollama list`
- **Descargar modelo**: `ollama pull <modelo>`
- **Chat directo**: `ollama run mistral`
- **Ver logs**: `ollama logs`

Disfruta practicando ingles!
