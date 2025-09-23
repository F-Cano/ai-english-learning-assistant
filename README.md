# IA English Assistant

A modular English conversation and translation assistant powered by Ollama LLM.

## Architecture

### Modular Design
```
├── main.py                 # Application entry point
├── config.py              # Centralized configuration
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── setup.py               # Optional setup script
│
├── core/                  # Application core
│   ├── __init__.py
│   ├── events.py          # Event system
│   ├── state.py           # State management
│   └── exceptions.py      # Custom exceptions
│
├── models/                # Data models
│   ├── __init__.py
│   ├── message.py         # Message model
│   ├── translation.py     # Translation model
│   └── session.py         # Session model
│
├── services/              # Business logic
│   ├── __init__.py
│   ├── ollama_service.py  # Ollama LLM service
│   ├── chat_service.py    # Chat management
│   └── translation_service.py  # Translation service
│
├── ui/                    # User interface
│   ├── __init__.py
│   ├── app.py            # Main UI application
│   ├── constants.py      # UI constants and messages
│   └── components/       # UI components
│       ├── __init__.py
│       ├── base.py       # Base component class
│       ├── header.py     # Header component
│       ├── chat_display.py  # Chat display area
│       ├── input_area.py    # Input area with buttons
│       └── footer.py        # Footer with metrics
│
├── utils/                 # Utilities
│   ├── __init__.py
│   ├── logger.py         # Logging configuration
│   └── validators.py     # Data validation
│
└── tests/                 # Tests (for future development)
    └── __init__.py
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

3. **Optional - Run setup validation**:
   ```bash
   python setup.py
   ```

4. **Run application**:
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

### Event-Driven Communication
- Loose coupling between components
- Reactive UI that updates automatically
- Centralized event management system

### State Management
- Centralized application state
- Consistent data across components
- Real-time state synchronization
- Observable state changes

### Service Layer
- Business logic separated from UI
- Reusable and testable services
- Independent service modules
- Easy mocking for testing

### Component-Based UI
- Reusable UI components
- Independent component lifecycle
- Event subscription management
- Safe UI updates

## Development

### Adding New UI Components
1. Extend `UIComponent` base class in `ui/components/base.py`
2. Implement `create()` method
3. Subscribe to relevant events/state changes
4. Register component in main application

### Adding New Services
1. Create service class in `services/` directory
2. Integrate with event system using `EventManager`
3. Update application state using `AppState`
4. Wire service into main application

### Adding New Models
1. Create data model in `models/` directory
2. Use dataclasses for structure
3. Include serialization methods (`to_dict`, `from_dict`)
4. Add validation and business logic

### Modifying Configuration
- Edit `config.py` for application settings
- Changes apply immediately on restart
- No code modification needed for basic customization
- Validate configuration with `config.validate_config()`

### Event System Usage
```python
# Subscribe to events
event_manager.subscribe(AppEvent.MESSAGE_RECEIVED, handler_function)

# Emit events
event_manager.emit(AppEvent.MESSAGE_SENT, {'message': 'Hello'})

# Cleanup subscriptions
event_manager.unsubscribe(AppEvent.MESSAGE_RECEIVED, handler_function)
```

### State Management Usage
```python
# Get state values
value = app_state.get('key', default_value)

# Set state values
app_state.set('key', new_value)

# Subscribe to state changes
app_state.subscribe('key', callback_function)

# Update multiple values
app_state.update({'key1': value1, 'key2': value2})
```

## File Structure Details

### Core Files
- `main.py`: Application entry point with validation and startup
- `config.py`: Centralized configuration with validation
- `requirements.txt`: Python dependencies (minimal)

### Core System (`core/`)
- `events.py`: Event system for component communication
- `state.py`: Centralized state management
- `exceptions.py`: Custom application exceptions

### Data Models (`models/`)
- `message.py`: Chat message data structure
- `translation.py`: Translation data structure
- `session.py`: User session data structure

### Business Services (`services/`)
- `ollama_service.py`: Direct Ollama LLM communication
- `chat_service.py`: Chat conversation management
- `translation_service.py`: Translation orchestration

### User Interface (`ui/`)
- `app.py`: Main application window and coordination
- `constants.py`: UI text messages and constants
- `components/base.py`: Base class for all UI components
- `components/header.py`: Application header with status
- `components/chat_display.py`: Chat conversation display
- `components/input_area.py`: Message input and action buttons
- `components/footer.py`: Session metrics and links

### Utilities (`utils/`)
- `logger.py`: Logging configuration and setup
- `validators.py`: Data validation functions

## Troubleshooting

### Common Issues

1. **"Import error"**: 
   - Check that all `__init__.py` files exist
   - Verify Python path includes project root
   - Run `python setup.py` to validate environment

2. **"Connection error"**: 
   - Ensure Ollama is running: `ollama serve`
   - Check Ollama is accessible: `curl http://localhost:11434/api/tags`

3. **"No models available"**: 
   - Pull models: `ollama pull mistral`
   - Verify models: `ollama list`

4. **"Configuration error"**: 
   - Check `config.py` syntax
   - Validate with `config.validate_config()`

5. **"UI not responding"**: 
   - Check console for error messages
   - Verify tkinter is available: `python -m tkinter`

### Debugging

- Check console output for detailed logs
- Enable file logging in `config.py` LOGGING_CONFIG
- Use session summary on exit for usage metrics
- Monitor event flow in debug logs

### Performance

- Event system is lightweight and fast
- State management uses efficient observers
- UI updates are scheduled safely
- Background tasks run in separate threads

## Testing

Future testing structure in `tests/` directory:
- Unit tests for individual components
- Integration tests for service interactions
- UI tests for component behavior
- Mock services for isolated testing

## Contributing

1. Follow the modular architecture principles
2. Use event system for component communication
3. Update state through centralized management
4. Add proper logging and error handling
5. Include documentation for new features

## License

This project is open source. See LICENSE file for details.
