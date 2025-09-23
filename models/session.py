"""
Session data model
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from .message import Message
from .translation import Translation


@dataclass
class Session:
    """Session data model"""
    session_id: str
    start_time: datetime = None
    end_time: Optional[datetime] = None
    messages: List[Message] = field(default_factory=list)
    translations: List[Translation] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    
    def __post_init__(self):
        if self.start_time is None:
            self.start_time = datetime.now()
    
    @property
    def duration(self) -> datetime:
        """Get session duration"""
        end = self.end_time or datetime.now()
        return end - self.start_time
    
    @property
    def message_count(self) -> int:
        """Get total message count"""
        return len(self.messages)
    
    @property
    def translation_count(self) -> int:
        """Get total translation count"""
        return len(self.translations)
    
    @property
    def user_message_count(self) -> int:
        """Get user message count"""
        return len([msg for msg in self.messages if msg.is_user_message])
    
    @property
    def assistant_message_count(self) -> int:
        """Get assistant message count"""
        return len([msg for msg in self.messages if msg.is_assistant_message])
    
    def add_message(self, message: Message) -> None:
        """Add message to session"""
        self.messages.append(message)
    
    def add_translation(self, translation: Translation) -> None:
        """Add translation to session"""
        self.translations.append(translation)
    
    def end_session(self) -> None:
        """End the session"""
        self.end_time = datetime.now()
    
    def get_recent_messages(self, count: int = 10) -> List[Message]:
        """Get recent messages"""
        return self.messages[-count:] if self.messages else []
    
    def get_recent_translations(self, count: int = 5) -> List[Translation]:
        """Get recent translations"""
        return self.translations[-count:] if self.translations else []
    
    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        return {
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'messages': [msg.to_dict() for msg in self.messages],
            'translations': [trans.to_dict() for trans in self.translations],
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Session':
        """Create session from dictionary"""
        session = cls(
            session_id=data['session_id'],
            start_time=datetime.fromisoformat(data['start_time']),
            end_time=datetime.fromisoformat(data['end_time']) if data['end_time'] else None,
            metadata=data.get('metadata', {})
        )
        
        session.messages = [Message.from_dict(msg_data) for msg_data in data.get('messages', [])]
        session.translations = [Translation.from_dict(trans_data) for trans_data in data.get('translations', [])]
        
        return session