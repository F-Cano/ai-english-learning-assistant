"""
Translation data model
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class TranslationStatus(Enum):
    """Translation status enumeration"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Translation:
    """Translation data model"""
    original_text: str
    translated_text: Optional[str] = None
    source_language: str = "en"
    target_language: str = "es"
    status: TranslationStatus = TranslationStatus.PENDING
    model_used: Optional[str] = None
    timestamp: datetime = None
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    @property
    def is_completed(self) -> bool:
        """Check if translation is completed"""
        return self.status == TranslationStatus.COMPLETED
    
    @property
    def is_failed(self) -> bool:
        """Check if translation failed"""
        return self.status == TranslationStatus.FAILED
    
    @property
    def formatted_timestamp(self) -> str:
        """Get formatted timestamp string"""
        return self.timestamp.strftime("%H:%M:%S")
    
    def mark_completed(self, translated_text: str, model_used: str = None) -> None:
        """Mark translation as completed"""
        self.translated_text = translated_text
        self.status = TranslationStatus.COMPLETED
        if model_used:
            self.model_used = model_used
    
    def mark_failed(self, error_message: str) -> None:
        """Mark translation as failed"""
        self.status = TranslationStatus.FAILED
        self.error_message = error_message
    
    def to_dict(self) -> dict:
        """Convert translation to dictionary"""
        return {
            'original_text': self.original_text,
            'translated_text': self.translated_text,
            'source_language': self.source_language,
            'target_language': self.target_language,
            'status': self.status.value,
            'model_used': self.model_used,
            'timestamp': self.timestamp.isoformat(),
            'error_message': self.error_message
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Translation':
        """Create translation from dictionary"""
        return cls(
            original_text=data['original_text'],
            translated_text=data.get('translated_text'),
            source_language=data.get('source_language', 'en'),
            target_language=data.get('target_language', 'es'),
            status=TranslationStatus(data['status']),
            model_used=data.get('model_used'),
            timestamp=datetime.fromisoformat(data['timestamp']),
            error_message=data.get('error_message')
        )