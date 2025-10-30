from sqlalchemy.orm import Session
from typing import List, Optional
from .message_models import Message

class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, sender_id: int, receiver_id: int, content: str) -> Message:
        """Create a new message"""
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_between_users(self, user_id1: int, user_id2: int) -> List[Message]:
        """Get all messages between two users"""
        return self.db.query(Message).filter(
            ((Message.sender_id == user_id1) & (Message.receiver_id == user_id2)) |
            ((Message.sender_id == user_id2) & (Message.receiver_id == user_id1))
        ).order_by(Message.created_at).all()

    def get_conversations(self, user_id: int) -> List[int]:
        """Get list of user IDs that have conversation with given user"""
        sent_to = self.db.query(Message.receiver_id).filter(
            Message.sender_id == user_id
        ).distinct().all()
        
        received_from = self.db.query(Message.sender_id).filter(
            Message.receiver_id == user_id
        ).distinct().all()
        
        # Combine and deduplicate
        user_ids = set([r[0] for r in sent_to] + [r[0] for r in received_from])
        return list(user_ids)

    def mark_messages_as_read(self, sender_id: int, receiver_id: int) -> int:
        """Mark all messages from sender to receiver as read"""
        result = self.db.query(Message).filter(
            Message.sender_id == sender_id,
            Message.receiver_id == receiver_id,
            Message.is_read == False
        ).update({Message.is_read: True})
        self.db.commit()
        return result

    def get_unread_count(self, user_id: int) -> int:
        """Get total unread message count for a user"""
        return self.db.query(Message).filter(
            Message.receiver_id == user_id,
            Message.is_read == False
        ).count()

    def get_unread_count_between_users(self, current_user_id: int, other_user_id: int) -> int:
        """Get unread message count from other user to current user"""
        return self.db.query(Message).filter(
            Message.sender_id == other_user_id,
            Message.receiver_id == current_user_id,
            Message.is_read == False
        ).count()

    def get_last_message(self, user_id1: int, user_id2: int) -> Optional[Message]:
        """Get the last message between two users"""
        return self.db.query(Message).filter(
            ((Message.sender_id == user_id1) & (Message.receiver_id == user_id2)) |
            ((Message.sender_id == user_id2) & (Message.receiver_id == user_id1))
        ).order_by(Message.created_at.desc()).first()

    def delete_conversation(self, user_id1: int, user_id2: int) -> int:
        """Delete all messages between two users"""
        result = self.db.query(Message).filter(
            ((Message.sender_id == user_id1) & (Message.receiver_id == user_id2)) |
            ((Message.sender_id == user_id2) & (Message.receiver_id == user_id1))
        ).delete()
        self.db.commit()
        return result
