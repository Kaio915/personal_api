from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from security import get_current_user
from .message_service import MessageService, MessageResponse, MessageCreate
from .message_repository import MessageRepository

router = APIRouter(prefix="/messages", tags=["messages"])

def get_message_service(db: Session = Depends(get_db)) -> MessageService:
    repository = MessageRepository(db)
    return MessageService(repository)

@router.post("/", response_model=MessageResponse)
async def send_message(
    message_data: MessageCreate,
    current_user = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    """
    Send a message to another user
    """
    print(f"💬 Sending message from user {current_user.id} to user {message_data.receiver_id}")
    
    try:
        message = service.send_message(
            sender_id=current_user.id,
            receiver_id=message_data.receiver_id,
            content=message_data.content
        )
        print(f"✅ Message sent successfully: {message.id}")
        return message
    except Exception as e:
        print(f"❌ Error sending message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error sending message: {str(e)}"
        )

@router.get("/conversation/{other_user_id}", response_model=List[MessageResponse])
async def get_conversation(
    other_user_id: int,
    current_user = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    """
    Get all messages between current user and another user
    """
    print(f"📥 Loading conversation between user {current_user.id} and user {other_user_id}")
    
    try:
        messages = service.get_messages_between_users(current_user.id, other_user_id)
        print(f"✅ Found {len(messages)} messages")
        return messages
    except Exception as e:
        print(f"❌ Error loading messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading messages: {str(e)}"
        )

@router.get("/conversations", response_model=List[int])
async def get_conversations(
    current_user = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    """
    Get list of user IDs that have conversations with current user
    """
    print(f"📋 Loading conversations for user {current_user.id}")
    
    try:
        user_ids = service.get_conversations(current_user.id)
        print(f"✅ Found {len(user_ids)} conversations")
        return user_ids
    except Exception as e:
        print(f"❌ Error loading conversations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading conversations: {str(e)}"
        )

@router.patch("/read/{sender_id}")
async def mark_as_read(
    sender_id: int,
    current_user = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    """
    Mark all messages from sender to current user as read
    """
    print(f"✔️ Marking messages from user {sender_id} to user {current_user.id} as read")
    
    try:
        success = service.mark_as_read(sender_id, current_user.id)
        if success:
            print(f"✅ Messages marked as read")
            return {"message": "Messages marked as read"}
        else:
            print(f"ℹ️ No unread messages found")
            return {"message": "No unread messages"}
    except Exception as e:
        print(f"❌ Error marking messages as read: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error marking messages as read: {str(e)}"
        )

@router.get("/unread/count")
async def get_unread_count(
    current_user = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    """
    Get total unread message count for current user
    """
    try:
        count = service.get_unread_count(current_user.id)
        return {"count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting unread count: {str(e)}"
        )

@router.get("/unread/count/{other_user_id}")
async def get_unread_count_with_user(
    other_user_id: int,
    current_user = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    """
    Get unread message count from specific user
    """
    try:
        count = service.get_unread_count_between_users(current_user.id, other_user_id)
        return {"count": count}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting unread count: {str(e)}"
        )

@router.delete("/conversation/{other_user_id}")
async def delete_conversation(
    other_user_id: int,
    current_user = Depends(get_current_user),
    service: MessageService = Depends(get_message_service)
):
    """
    Delete all messages between current user and another user
    """
    print(f"🗑️ Deleting conversation between user {current_user.id} and user {other_user_id}")
    
    try:
        success = service.delete_conversation(current_user.id, other_user_id)
        if success:
            print(f"✅ Conversation deleted")
            return {"message": "Conversation deleted"}
        else:
            print(f"ℹ️ No messages found")
            return {"message": "No messages found"}
    except Exception as e:
        print(f"❌ Error deleting conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )
