"""
Chat service for managing conversations
"""
from typing import Optional, List
from datetime import datetime
from core.events import EventManager, AppEvent
from core.state import AppState
from models.message import Message, MessageType, MessageStatus
from models.session import Session
from services.ollama_service import OllamaService
from utils.logger import logger
from utils.validators import validate_message


class ChatService:
    """Service for managing chat conversations"""
    
    def __init__(self, event_manager: EventManager = None, app_state: AppState = None):
        self.event_manager = event_manager
        self.app_state = app_state
        self.ollama_service = OllamaService(event_manager=event_manager)
        self.current_session: Optional[Session] = None
        
        # Initialize session
        self._create_new_session()
        
        logger.info("ChatService initialized")
    
    def _create_new_session(self) -> None:
        """Create a new chat session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.current_session = Session(session_id=session_id)
        logger.info(f"New session created: {session_id}")
    
    def send_message(self, message_content: str) -> Message:
        """Send a user message and get assistant response"""
        if not validate_message(message_content):
            raise ValueError("Invalid message content")
        
        # Create user message
        user_message = Message(
            content=message_content,
            message_type=MessageType.USER,
            status=MessageStatus.SENT
        )
        
        # Add to session
        if self.current_session:
            self.current_session.add_message(user_message)
        
        # Update state
        if self.app_state:
            self.app_state.set('last_message', message_content)
            self.app_state.increment('messages_sent')
        
        # Emit sent event
        if self.event_manager:
            self.event_manager.emit(AppEvent.MESSAGE_SENT, {
                'message': message_content,
                'timestamp': user_message.timestamp
            })
        
        try:
            # Get response from Ollama
            response_content = self.ollama_service.generate_response(message_content)
            
            # Create assistant message
            assistant_message = Message(
                content=response_content,
                message_type=MessageType.ASSISTANT,
                status=MessageStatus.DELIVERED
            )
            
            # Add to session
            if self.current_session:
                self.current_session.add_message(assistant_message)
            
            # Update state
            if self.app_state:
                self.app_state.set('last_response', response_content)
            
            logger.info("Message processed successfully")
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error processing message: {e}"
            logger.error(error_msg)
            
            # Create error message
            error_message = Message(
                content=error_msg,
                message_type=MessageType.ERROR,
                status=MessageStatus.ERROR
            )
            
            # Add to session
            if self.current_session:
                self.current_session.add_message(error_message)
            
            # Update error count
            if self.app_state:
                self.app_state.increment('errors_count')
            
            return error_message
    
    def get_conversation_history(self, count: int = 10) -> List[Message]:
        """Get recent conversation history"""
        if not self.current_session:
            return []
        
        return self.current_session.get_recent_messages(count)
    
    def clear_conversation(self) -> None:
        """Clear current conversation"""
        self._create_new_session()
        logger.info("Conversation cleared")
    
    def is_online(self) -> bool:
        """Check if chat service is online"""
        return self.ollama_service.is_online()
    
    def get_status(self) -> dict:
        """Get chat service status"""
        ollama_status = self.ollama_service.get_status()
        
        session_info = {}
        if self.current_session:
            session_info = {
                'session_id': self.current_session.session_id,
                'message_count': self.current_session.message_count,
                'duration': str(self.current_session.duration)
            }
        
        return {
            'online': ollama_status['online'],
            'session': session_info,
            'ollama': ollama_status
        }
    
    def export_session(self) -> dict:
        """Export current session data"""
        if not self.current_session:
            return {}
        
        return self.current_session.to_dict()