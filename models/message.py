"""
Message data model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class MessageType(Enum):
    """Message type enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    ERROR = "error"
    TRANSLATION = "translation"


class MessageStatus(Enum):
    """Message status enumeration"""
    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    ERROR = "error"


@dataclass
class Message:
    """Message data model"""
    content: str
    message_type: MessageType
    timestamp: datetime = None
    status: MessageStatus = MessageStatus.PENDING
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        
        if self.metadata is None:
            self.metadata = {}
    
    @property
    def formatted_timestamp(self) -> str:
        """Get formatted timestamp string"""
        return self.timestamp.strftime("%H:%M:%S")
    
    @property
    def is_user_message(self) -> bool:
        """Check if message is from user"""
        return self.message_type == MessageType.USER
    
    @property
    def is_assistant_message(self) -> bool:
        """Check if message is from assistant"""
        return self.message_type == MessageType.ASSISTANT
    
    @property
    def is_system_message(self) -> bool:
        """Check if message is system message"""
        return self.message_type == MessageType.SYSTEM
    
    def to_dict(self) -> dict:
        """Convert message to dictionary"""
        return {
            'content': self.content,
            'message_type': self.message_type.value,
            'timestamp': self.timestamp.isoformat(),
            'status': self.status.value,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Message':
        """Create message from dictionary"""
        return cls(
            content=data['content'],
            message_type=MessageType(data['message_type']),
            timestamp=datetime.fromisoformat(data['timestamp']),
            status=MessageStatus(data['status']),
            metadata=data.get('metadata', {})
        )
    
    def __str__(self) -> str:
        return f"[{self.formatted_timestamp}] {self.message_type.value}: {self.content}"