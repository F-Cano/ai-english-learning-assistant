# IA English Assistant - Copilot Instructions

## Architecture Overview

This is a **Tkinter-based bilingual English learning assistant** that integrates with local Ollama LLM service. The AI assistant adapts intelligently between Spanish and English based on user needs. The architecture follows a clean separation with:

- **Entry Point**: `main.py` - Environment validation → UI initialization
- **Core System**: Event-driven architecture with centralized state management
- **UI Layer**: Component-based Tkinter interface with consistent theming
- **Service Layer**: Ollama integration for AI conversations

## Key Patterns & Conventions

### Configuration Management
- **Single source of truth**: All settings in `config.py` using `Config` class
- **Theme system**: Dark theme defined in `Config.COLORS` with semantic color names
- **Font system**: Font tuples accessible via `Config.get_font()` and `Config.get_font_tuple()`
- **UI dimensions**: Centralized in `Config.UI_CONFIG` and `Config.WINDOW_CONFIG`

### Component Architecture
All UI components inherit from `ui/components/base.py:UIComponent`:
```python
class MyComponent(UIComponent):
    def create(self) -> tk.Frame:
        # Required: Create and return main frame
        pass
```

Components receive: `parent`, `colors`, `event_manager`, `app_state` in constructor.

### State Management
- **Centralized state**: `core/app_state.py:AppState` singleton
- **Reactive updates**: State changes trigger subscriber notifications
- **Session tracking**: Built-in metrics (messages_sent, translations_made, etc.)

### Event System
- **Type-safe events**: `core/events.py:AppEvent` enum defines all events
- **Loop prevention**: Built-in duplicate subscription and rate limiting
- **Debug mode**: Extensive logging for event flow debugging

### Service Integration
- **Ollama dependency**: Requires local Ollama server at `localhost:11434`
- **Models**: Configured for `mistral` (primary) and `llama2` fallback
- **Connection handling**: Automatic reconnection and model validation
- **AI Behavior**: Bilingual assistant that adapts response language intelligently based on user input and learning context

## Development Workflows

### Running the Application
```bash
python main.py
```
Environment validation runs first - check logs if startup fails.

### Adding New UI Components
1. Inherit from `UIComponent` in `ui/components/base.py`
2. Implement `create()` method returning `tk.Frame`
3. Use `self.colors` for theming, `self.app_state` for data
4. Register in main app's component initialization

### Debugging Event Issues
- Events logged to `logs/ia_assistant.log`
- Check for subscription loops in EventManager debug output
- Use `_event_count` tracking for rate limit issues

### Extending Ollama Integration
- Models configured in `OllamaService.available_models`
- API calls use streaming for better UX
- Connection status propagated via `OLLAMA_CONNECTED/DISCONNECTED` events

## Critical Dependencies

### External Services
- **Ollama**: Must be running locally with models installed
  ```bash
  ollama pull mistral
  ollama serve
  ```

### Python Dependencies
- `requests` (HTTP client for Ollama API)
- `tkinter` (UI framework - included with Python)

### Development Setup
No build system required - direct Python execution. Logging automatically configured on startup.

## Common Gotchas

- **Event loops**: EventManager has built-in loop prevention - don't circumvent it
- **State mutations**: Always use `app_state.set()` to trigger notifications
- **Component lifecycle**: Call `component.create()` before adding to parent
- **Ollama models**: App fails gracefully if models unavailable, but shows connection errors
- **Threading**: Ollama calls run in background threads - UI updates must use thread-safe patterns

## File Structure Significance

- `core/`: Business logic and state - no UI imports allowed
- `ui/components/`: Reusable UI pieces following UIComponent pattern  
- `ui/simple_app.py`: Main application orchestrator
- `config.py`: Single configuration source - modify here for UI changes
- `logs/`: Auto-created runtime logs with rotation