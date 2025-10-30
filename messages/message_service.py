from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from .message_repository import MessageRepository

class MessageResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    is_read: bool
    timestamp: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "sender_id": 4,
                "receiver_id": 3,
                "content": "Olá, gostaria de agendar um treino!",
                "is_read": False,
                "timestamp": "2024-01-15T10:30:00"
            }
        }

class MessageCreate(BaseModel):
    receiver_id: int
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "receiver_id": 3,
                "content": "Olá, gostaria de agendar um treino!"
            }
        }

class ConversationResponse(BaseModel):
    user_id: int
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
    unread_count: int

class MessageService:
    def __init__(self, repository: MessageRepository):
        self.repository = repository

    def send_message(self, sender_id: int, receiver_id: int, content: str) -> MessageResponse:
        """Send a message from one user to another"""
        message = self.repository.create_message(sender_id, receiver_id, content)
        return MessageResponse(
            id=message.id,
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            content=message.content,
            is_read=message.is_read,
            timestamp=message.created_at
        )

    def get_messages_between_users(self, user_id1: int, user_id2: int) -> List[MessageResponse]:
        """Get all messages between two users"""
        messages = self.repository.get_messages_between_users(user_id1, user_id2)
        return [
            MessageResponse(
                id=msg.id,
                sender_id=msg.sender_id,
                receiver_id=msg.receiver_id,
                content=msg.content,
                is_read=msg.is_read,
                timestamp=msg.created_at
            )
            for msg in messages
        ]

    def get_conversations(self, user_id: int) -> List[int]:
        """Get list of user IDs that have conversations with given user"""
        return self.repository.get_conversations(user_id)

    def mark_as_read(self, sender_id: int, receiver_id: int) -> bool:
        """Mark all messages from sender to receiver as read"""
        count = self.repository.mark_messages_as_read(sender_id, receiver_id)
        return count > 0

    def get_unread_count(self, user_id: int) -> int:
        """Get total unread message count for a user"""
        return self.repository.get_unread_count(user_id)

    def get_unread_count_between_users(self, current_user_id: int, other_user_id: int) -> int:
        """Get unread message count from other user to current user"""
        return self.repository.get_unread_count_between_users(current_user_id, other_user_id)

    def delete_conversation(self, user_id1: int, user_id2: int) -> bool:
        """Delete all messages between two users"""
        count = self.repository.delete_conversation(user_id1, user_id2)
        return count > 0
