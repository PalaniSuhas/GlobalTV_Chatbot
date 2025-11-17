"""Conversation flow handler"""
from enum import Enum
from typing import Dict, Optional

class ConversationState(Enum):
    WELCOME = "welcome"
    CATEGORY_SELECTION = "category_selection"
    SUBSCRIPTION_NAME = "subscription_name"
    SUBSCRIPTION_MOBILE = "subscription_mobile"
    SUBSCRIPTION_VERIFIED = "subscription_verified"
    TECHNICAL_SUPPORT = "technical_support"
    GENERAL_QUERY = "general_query"
    RESOLUTION = "resolution"
    FEEDBACK = "feedback"
    END = "end"

class ConversationHandler:
    def __init__(self):
        self.state = ConversationState.WELCOME
        self.context = {}
        self.conversation_history = []
    
    def reset(self):
        """Reset conversation state"""
        self.state = ConversationState.WELCOME
        self.context = {}
        self.conversation_history = []
    
    def get_welcome_message(self) -> Dict:
        """Get welcome message with quick action buttons"""
        self.state = ConversationState.CATEGORY_SELECTION
        
        return {
            "message": "Hi! How can I help you today?",
            "buttons": [
                {"label": "Account & Subscription", "value": "subscription"},
                {"label": "Technical Issues", "value": "technical"},
                {"label": "Billing Questions", "value": "billing"},
                {"label": "Content & Programming", "value": "content"},
                {"label": "General Questions", "value": "general"}
            ]
        }
    
    def handle_category_selection(self, category: str) -> Dict:
        """Handle category selection - SIMPLIFIED TO 2 BUCKETS"""
        self.context['category'] = category
        
        if category == "subscription":
            self.state = ConversationState.SUBSCRIPTION_NAME
            return {
                "message": "To access your subscription information, I'll need to verify your account. Please provide your full name as it appears on your account.",
                "buttons": []
            }
        elif category == "technical":
            self.state = ConversationState.TECHNICAL_SUPPORT
            return {
                "message": "I can help you with technical issues. Please select which type:",
                "buttons": [
                    {"label": "General Tech/Video Issues", "value": "general_tech"},
                    {"label": "Ad Commercials Freezing/App Crashing", "value": "ad_freezing"}
                ]
            }
        elif category == "billing":
            self.state = ConversationState.SUBSCRIPTION_NAME
            return {
                "message": "For billing questions, I'll need to verify your account first. Please provide your full name as it appears on your account.",
                "buttons": []
            }
        elif category == "content":
            self.state = ConversationState.GENERAL_QUERY
            return {
                "message": "I can help with questions about shows, schedules, and programming. What would you like to know?",
                "buttons": []
            }
        else:
            self.state = ConversationState.GENERAL_QUERY
            return {
                "message": "Please describe your question or concern, and I'll do my best to help.",
                "buttons": []
            }
    
    def handle_subscription_name(self, name: str) -> Dict:
        """Handle name input for subscription verification"""
        self.context['name'] = name
        self.state = ConversationState.SUBSCRIPTION_MOBILE
        
        return {
            "message": f"Thank you, {name}. Now please provide your mobile number (the one associated with your account).",
            "buttons": []
        }
    
    def handle_subscription_mobile(self, mobile: str) -> Dict:
        """Handle mobile number input"""
        self.context['mobile'] = mobile
        self.state = ConversationState.SUBSCRIPTION_VERIFIED
        
        return {
            "message": "Verifying your account...",
            "buttons": []
        }
    
    def handle_subscription_verified(self, subscriber_info: Optional[Dict]) -> Dict:
        """Handle subscription verification result"""
        if subscriber_info:
            self.context['subscriber_info'] = subscriber_info
            self.state = ConversationState.GENERAL_QUERY
            
            return {
                "message": "Account verified! How can I assist you with your subscription?",
                "buttons": [
                    {"label": "View Subscription Details", "value": "view_subscription"},
                    {"label": "Channel Access Issues", "value": "channel_access"},
                    {"label": "Subscription Renewal", "value": "renewal"},
                    {"label": "Other Question", "value": "other"}
                ]
            }
        else:
            self.state = ConversationState.CATEGORY_SELECTION
            return {
                "message": "I couldn't find an account matching that information. Please verify your name and mobile number are correct, or contact your TV service provider directly.",
                "buttons": [
                    {"label": "Try Again", "value": "subscription"},
                    {"label": "Main Menu", "value": "main_menu"}
                ]
            }
    
    def determine_resolution_type(self, message: str) -> str:
        """Determine if issue can be resolved by bot"""
        escalation_keywords = [
            "speak to agent", "talk to human", "representative",
            "not working", "still broken", "doesn't help",
            "not satisfied", "angry", "frustrated"
        ]
        
        message_lower = message.lower()
        for keyword in escalation_keywords:
            if keyword in message_lower:
                return "escalate"
        
        return "resolved"
    
    def get_feedback_message(self) -> Dict:
        """Get feedback collection message"""
        self.state = ConversationState.FEEDBACK
        
        return {
            "message": "Was I able to help you today?",
            "buttons": [
                {"label": "👍 Yes, thank you!", "value": "positive"},
                {"label": "👎 No, I need more help", "value": "negative"}
            ]
        }
    
    def get_end_message(self, feedback: str) -> Dict:
        """Get session end message"""
        self.state = ConversationState.END
        
        if feedback == "positive":
            message = "Thank you for contacting Global TV support! Have a great day!"
        else:
            message = "I'm sorry I couldn't fully resolve your issue. A support agent will contact you shortly. Thank you for your patience."
        
        return {
            "message": message,
            "buttons": [
                {"label": "Start New Conversation", "value": "restart"}
            ]
        }
    
    def add_to_history(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content
        })