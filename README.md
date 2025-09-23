# IA English Assistant

A modular English conversation and translation assistant powered by Ollama LLM.

## Architecture

### Modular Design
```
├── main.py                 # Application entry point
├── config.py              # Centralized configuration
├── requirements.txt       # Dependencies
│
├── core/                  # Application core
│   ├── events.py          # Event system
│   ├── state.py           # State management
│   └── exceptions.py      # Custom exceptions
│
├── models/                # Data models
│   ├── message.py         # Message model
│   ├── translation.py     # Translation model
│   └── session.py         # Session model
│
├── services/              # Business logic
│   ├── ollama_service.py  # Ollama LLM service
│   ├── chat_service.py    # Chat management
│   └── translation_service.py  # Translation service
│
├── ui/                    # User interface
│   ├── app.py            # Main UI application
│   ├── constants.py      # UI constants
│   └── components/       # UI components
│       ├── base.py       # Base component
│       ├── header.py     # Header component
│       ├── chat_display.py  # Chat display
│       ├── input_area.py    # Input area
│       └── footer.py        # Footer
│
└── utils/                 # Utilities
    ├── logger.py         # Logging setup
    └── validators.py     # Data validation
```

## Features

- **Natural English Conversation**: Practice English with an AI assistant
- **Smart Translation**: Multi-model translation with automatic fallback
- **Real-time Status**: Live connection monitoring and status updates
- **Session Metrics**: Track messages, translations, and session time
- **Event-Driven**: Reactive UI with centralized event system
- **Modular Architecture**: Independent, replaceable components

## Requirements

- Python 3.8+
- Ollama installed and running locally
- tkinter (usually included with Python)

## Installation

1. **Install Ollama**:
   ```bash
   # Visit https://ollama.ai for installation instructions
   # Pull recommended models:
   ollama pull mistral
   ollama pull llama2
   ```

2. **Clone and setup**:
   ```bash
   git clone <repository>
   cd IA
   pip install -r requirements.txt
   ```

3. **Run application**:
   ```bash
   python main.py
   ```

## Configuration

Edit `config.py` to customize:

- **Window settings**: Size, title, appearance
- **Ollama settings**: URL, timeouts, retry logic
- **Model preferences**: Preferred models, parameters
- **UI settings**: Colors, fonts, layout
- **AI prompts**: System prompts for chat and translation

## Usage

1. **Start Ollama**: Ensure Ollama is running on `localhost:11434`
2. **Run application**: Execute `python main.py`
3. **Chat**: Type messages and press Send or Ctrl+Enter
4. **Translate**: Click Translate to translate the last assistant response
5. **Monitor**: Watch connection status and session metrics in real-time

## Architecture Benefits

### Modularity
- Each component can be modified independently
- Easy to add new features or replace components
- Clear separation of concerns

### Event-Driven
- Loose coupling between components
- Reactive UI that updates automatically
- Easy to debug and extend

### State Management
- Centralized application state
- Consistent data across components
- Real-time state synchronization

### Service Layer
- Business logic separated from UI
- Reusable services
- Easy testing and mocking

## Development

### Adding New Components
1. Extend `UIComponent` base class
2. Implement required methods
3. Subscribe to relevant events/state
4. Register in main application

### Adding New Services
1. Create service class in `services/`
2. Integrate with event system
3. Update state as needed
4. Wire into application

### Modifying Configuration
- Edit `config.py` for application settings
- Changes apply immediately on restart
- No code modification needed for basic customization

## Troubleshooting

### Common Issues

1. **"Connection error"**: Ensure Ollama is running
2. **"No models available"**: Pull models with `ollama pull <model>`
3. **"Import error"**: Check Python path and dependencies
4. **"UI not responding"**: Check console for error messages

### Debugging

- Check console output for detailed logs
- Enable file logging in `config.py`
- Use session summary for usage metrics

## License

This project is open source. See LICENSE file for details.
