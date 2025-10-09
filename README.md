# 🤖 IA English Assistant

> **Tu asistente bilingüe inteligente para aprender inglés de forma natural**

Un asistente de conversación desarrollado en Python que utiliza IA local (Ollama) para ayudarte a practicar y mejorar tu inglés. **Completamente bilingüe** - se adapta automáticamente a tu idioma y nivel.

## ✨ Características Principales

🗣️ **Conversación Bilingüe Inteligente**
- Responde en español cuando escribes en español
- Cambia a inglés cuando practicas en inglés
- Se adapta automáticamente a tu nivel y contexto

🎯 **Aprendizaje Personalizado**
- Correcciones gentiles y educativas
- Explicaciones claras de gramática
- Traducciones contextuales cuando las necesitas

🖥️ **Interfaz Limpia y Moderna**
- Tema oscuro elegante
- Chat fluido y responsivo
- Botones de traducción rápida

⚡ **Tecnología Local**
- Funciona completamente offline con Ollama
- Sin dependencias de APIs externas
- Rápido y privado

## 🚀 Instalación Rápida

### Prerrequisitos

1. **Python 3.8+**
2. **Ollama** instalado y ejecutándose

```bash
# Instalar Ollama (si no lo tienes)
# Visita: https://ollama.ai

# Descargar modelos requeridos
ollama pull mistral
ollama pull llama2
```

### Instalación del Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/F-Cano/ai-english-learning-assistant.git
cd ai-english-learning-assistant

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## 🎮 Uso

1. **Inicia Ollama** en tu sistema
2. **Ejecuta la aplicación** con `python main.py`
3. **¡Empieza a conversar!** En español o inglés, el asistente se adaptará

### Ejemplos de Uso

```
👤 Usuario: "Hola, ¿cómo puedo mejorar mi pronunciación?"
🤖 Alex: "¡Hola! Para mejorar tu pronunciación, te recomiendo..."

👤 Usuario: "Hello, how are you today?"
🤖 Alex: "Hello! I'm doing great, thank you for asking..."
```

## 📁 Estructura del Proyecto

```
├── 📄 main.py                 # Punto de entrada de la aplicación
├── ⚙️ config.py              # Configuración centralizada
├── 📁 core/                  # Sistema central
│   ├── 🧠 app_state.py       # Gestión de estado
│   ├── 📡 events.py          # Sistema de eventos
│   ├── 📝 logging_setup.py   # Configuración de logs
│   └── 📁 services/
│       └── 🔗 ollama_service.py  # Integración con Ollama
├── 📁 ui/                    # Interfaz de usuario
│   ├── 🖼️ simple_app.py      # Aplicación principal
│   └── 📁 components/        # Componentes UI
│       ├── 🧩 base.py        # Componente base
│       ├── 📋 header.py      # Cabecera
│       ├── 💬 chat_display.py # Área de chat
│       ├── ⌨️ input_area.py   # Entrada de texto
│       └── 📊 footer.py      # Pie de página
└── 📁 logs/                  # Archivos de registro
```

## ⚙️ Configuración

Personaliza la aplicación editando `config.py`:

- **🎨 Colores del tema**: Modifica `Config.COLORS`
- **📝 Fuentes**: Ajusta `Config.FONTS`
- **📐 Dimensiones**: Cambia `Config.WINDOW_CONFIG`
- **🔧 Logs**: Configura `Config.LOGGING_CONFIG`

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: Amazing Feature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🐛 Reportar Problemas

Si encuentras algún problema:

1. Revisa los logs en `logs/ia_assistant.log`
2. Verifica que Ollama esté ejecutándose
3. Abre un issue en GitHub con detalles del error

## 📜 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **Ollama** por proporcionar IA local potente y eficiente
- **Tkinter** por la interfaz gráfica nativa de Python
- La comunidad de código abierto por las herramientas increíbles

---

<div align="center">

**¿Te gusta el proyecto? ¡Dale una ⭐ en GitHub!**

Made with ❤️ by [F-Cano](https://github.com/F-Cano)

</div>