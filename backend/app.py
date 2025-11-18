"""FastAPI Backend for Global TV Chatbot"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from dotenv import load_dotenv
from src.chatbot import GlobalTVChatbot
from src.ticket_manager import TicketManager

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Global TV Chatbot API",
    description="AI-powered customer support for Global TV",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chatbot instances per session
chatbot_sessions: Dict[str, GlobalTVChatbot] = {}


# Pydantic Models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    message: str
    buttons: List[Dict[str, str]] = []
    state: str


class ResetRequest(BaseModel):
    session_id: str = "default"


class SubscriptionRequest(BaseModel):
    name: str
    mobile: str
    session_id: str = "default"


def get_or_create_chatbot(session_id: str) -> GlobalTVChatbot:
    """Get existing chatbot or create new one for session"""
    if session_id not in chatbot_sessions:
        chatbot_sessions[session_id] = GlobalTVChatbot()
        # Initialize with welcome message
        chatbot_sessions[session_id].start_conversation()
    return chatbot_sessions[session_id]


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Global TV Chatbot API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat messages"""
    try:
        if not request.message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Get or create chatbot for this session
        chatbot = get_or_create_chatbot(request.session_id)
        
        # Process message
        response = chatbot.process_message(request.message)
        
        return ChatResponse(
            message=response['message'],
            buttons=response.get('buttons', []),
            state=chatbot.get_current_state().value
        )
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Sorry, I encountered an error. Please try again."
        )


@app.post("/api/reset")
async def reset(request: ResetRequest):
    """Reset conversation"""
    try:
        if request.session_id in chatbot_sessions:
            chatbot_sessions[request.session_id].reset_conversation()
            welcome = chatbot_sessions[request.session_id].start_conversation()
            return {
                'message': welcome['message'],
                'buttons': welcome.get('buttons', [])
            }
        
        raise HTTPException(status_code=404, detail="Session not found")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in reset endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error resetting conversation"
        )


@app.post("/api/subscription")
async def get_subscription(request: SubscriptionRequest):
    """Get subscription details"""
    try:
        if not request.name or not request.mobile:
            raise HTTPException(
                status_code=400,
                detail="Name and mobile are required"
            )
        
        chatbot = get_or_create_chatbot(request.session_id)
        subscriber_info = chatbot.get_subscription_details(request.name, request.mobile)
        
        if subscriber_info:
            return {
                'success': True,
                'subscriber_info': subscriber_info
            }
        else:
            return {
                'success': False,
                'message': 'Subscriber not found'
            }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in subscription endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving subscription"
        )


@app.get("/api/health")
async def health():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'active_sessions': len(chatbot_sessions)
    }


@app.get("/api/tickets/stats")
async def ticket_stats():
    """Get ticket statistics"""
    try:
        ticket_manager = TicketManager()
        stats = ticket_manager.get_ticket_stats()
        return stats
    except Exception as e:
        print(f"Error getting ticket stats: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error retrieving ticket stats"
        )


if __name__ == '__main__':
    import uvicorn
    print("=" * 60)
    print("🚀 Global TV Chatbot Backend Starting...")
    print("📡 Server running on http://localhost:5001")
    print("📚 API Documentation: http://localhost:5001/docs")
    print("🔗 Connect your Next.js frontend to this server")
    print("=" * 60)
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=5001,
        reload=True,
        log_level="info"
    )