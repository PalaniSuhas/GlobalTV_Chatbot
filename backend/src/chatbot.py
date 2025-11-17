"""Core chatbot logic - can be used independently of Chainlit"""
from typing import Dict, Optional, List
from .subscription_manager import SubscriptionManager
from .knowledge_manager import SmartKnowledgeManager
from .conversation_handler import ConversationHandler, ConversationState


class GlobalTVChatbot:
    """
    Core chatbot class that handles all conversation logic.
    Can be used with Chainlit, CLI, or any other interface.
    """
    
    def __init__(self):
        """Initialize chatbot with managers"""
        self.subscription_manager = SubscriptionManager()
        self.knowledge_manager = SmartKnowledgeManager()
        self.conversation_handler = ConversationHandler()
        self.session_data = {}
    
    def start_conversation(self) -> Dict:
        """Start a new conversation"""
        self.conversation_handler.reset()
        return self.conversation_handler.get_welcome_message()
    
    def process_message(self, message: str, message_type: str = "text") -> Dict:
        """
        Process user message and return response.
        
        Args:
            message: User's message text
            message_type: Type of message ("text", "button_click", etc.)
        
        Returns:
            Dictionary with response message and optional buttons
        """
        current_state = self.conversation_handler.state
        
        # Add message to history
        self.conversation_handler.add_to_history("user", message)
        
        # Route based on conversation state
        if current_state == ConversationState.WELCOME:
            return self._handle_welcome(message)
        
        elif current_state == ConversationState.CATEGORY_SELECTION:
            return self._handle_category_selection(message)
        
        elif current_state == ConversationState.SUBSCRIPTION_NAME:
            return self._handle_subscription_name(message)
        
        elif current_state == ConversationState.SUBSCRIPTION_MOBILE:
            return self._handle_subscription_mobile(message)
        
        elif current_state == ConversationState.SUBSCRIPTION_VERIFIED:
            return self._handle_subscription_verified_query(message)
        
        elif current_state == ConversationState.TECHNICAL_SUPPORT:
            return self._handle_technical_support(message)
        
        elif current_state == ConversationState.GENERAL_QUERY:
            return self._handle_general_query(message)
        
        elif current_state == ConversationState.RESOLUTION:
            return self._handle_resolution(message)
        
        elif current_state == ConversationState.FEEDBACK:
            return self._handle_feedback(message)
        
        else:
            return self._handle_general_query(message)
    
    def _handle_welcome(self, message: str) -> Dict:
        """Handle welcome state"""
        return self.conversation_handler.get_welcome_message()
    
    def _handle_category_selection(self, category: str) -> Dict:
        """Handle category selection"""
        category_lower = category.lower()
        
        # Map user input to categories
        category_mapping = {
            'subscription': 'subscription',
            'account': 'subscription',
            'billing': 'billing',
            'technical': 'technical',
            'tech': 'technical',
            'issue': 'technical',
            'problem': 'technical',
            'content': 'content',
            'show': 'content',
            'program': 'content',
            'general': 'general',
            'help': 'general',
            'question': 'general'
        }
        
        # Find matching category
        selected_category = None
        for key, value in category_mapping.items():
            if key in category_lower:
                selected_category = value
                break
        
        if selected_category:
            response = self.conversation_handler.handle_category_selection(selected_category)
            self.conversation_handler.add_to_history("assistant", response["message"])
            return response
        else:
            # Default to general
            response = self.conversation_handler.handle_category_selection("general")
            self.conversation_handler.add_to_history("assistant", response["message"])
            return response
    
    def _handle_subscription_name(self, name: str) -> Dict:
        """Handle name input for subscription verification"""
        response = self.conversation_handler.handle_subscription_name(name)
        self.conversation_handler.add_to_history("assistant", response["message"])
        return response
    
    def _handle_subscription_mobile(self, mobile: str) -> Dict:
        """Handle mobile number input and verify subscriber"""
        # Store mobile
        response = self.conversation_handler.handle_subscription_mobile(mobile)
        self.conversation_handler.add_to_history("assistant", response["message"])
        
        # Verify subscriber
        name = self.conversation_handler.context.get('name')
        mobile = self.conversation_handler.context.get('mobile')
        
        subscriber_info = self.subscription_manager.verify_subscriber(name, mobile)
        
        verification_response = self.conversation_handler.handle_subscription_verified(subscriber_info)
        self.conversation_handler.add_to_history("assistant", verification_response["message"])
        
        # If verified, add subscription details
        if subscriber_info:
            details = self.subscription_manager.get_subscription_info(subscriber_info)
            return {
                "message": verification_response["message"] + "\n\n" + details,
                "buttons": verification_response["buttons"]
            }
        
        return verification_response
    
    def _handle_subscription_verified_query(self, query: str) -> Dict:
        """Handle queries after subscription verification"""
        query_lower = query.lower()
        subscriber_info = self.conversation_handler.context.get('subscriber_info')
        
        if 'view' in query_lower or 'details' in query_lower or 'subscription' in query_lower:
            if subscriber_info:
                details = self.subscription_manager.get_subscription_info(subscriber_info)
                return {
                    "message": details,
                    "buttons": [
                        {"label": "✅ That's All I Needed", "value": "resolved"},
                        {"label": "❓ I Have Another Question", "value": "continue"}
                    ]
                }
        
        # Otherwise, use knowledge base
        return self._handle_general_query(query)
    
    def _handle_technical_support(self, query: str) -> Dict:
        """Handle technical support queries - 2 BUCKETS ONLY"""
        query_lower = query.lower()
        
        # Determine which bucket based on keywords
        ad_keywords = ['ad', 'commercial', 'freeze', 'freezing', 'crash', 'crashing', 'stuck']
        is_ad_issue = any(keyword in query_lower for keyword in ad_keywords)
        
        if is_ad_issue:
            # Bucket 2: Ad Commercials Freezing
            answer = """
**Ad Commercials Freezing and App Crashing**

Thank you for reporting this issue. To help us investigate, please provide:

• Device model and OS version
• Show name, Season, Episode having issues
• Which specific AD commercials trigger the freezing?
• Screenshot/video clip if possible

**Troubleshooting Steps:**
1. Clear app cache/data, remove app, restart device, reinstall
2. Turn off adblockers and pop-up blockers
3. Turn off VPN if using one
4. Complete pending software updates
5. Reboot WiFi router, forget network, reconnect
6. If issue persists: Power down with Hard 5 Second Hold on Pause button, reinstall app

Please try these steps and let us know the result.
"""
        else:
            # Bucket 1: General Tech/Video Issues
            answer = """
**General Tech/Video Issues**

Thank you for contacting us. To help investigate, please answer these questions:

• What is the Make, Model, and OS version of your device(s)?
• What are you trying to watch? (Show name, Season, Episode)
• What errors are you getting? At what point in the video?
• Does the issue happen with other videos or only specific ones?
• Can you watch Live TV without issues?
• Who is your Cable TV provider? Which channels are you subscribed to?
• Can you sign-in successfully at https://watch.globaltv.com/?
• Which browser are you using? Have you tried different browsers (Chrome, Firefox, Safari)?

Please provide as much detail as possible so we can assist you better.
"""
        
        self.conversation_handler.add_to_history("assistant", answer)
        
        return {
            "message": answer,
            "buttons": [
                {"label": "✅ Issue Resolved", "value": "resolved"},
                {"label": "❌ Still Need Help", "value": "escalate"}
            ]
        }
    
    def _handle_general_query(self, query: str) -> Dict:
        """Handle general queries using knowledge base"""
        # Get answer from knowledge base
        answer = self.knowledge_manager.get_answer(query)
        self.conversation_handler.add_to_history("assistant", answer)
        
        return {
            "message": answer,
            "buttons": [
                {"label": "✅ That Helped!", "value": "resolved"},
                {"label": "❓ Follow-up Question", "value": "continue"},
                {"label": "❌ Need More Help", "value": "escalate"}
            ]
        }
    
    def _handle_resolution(self, response: str) -> Dict:
        """Handle resolution response"""
        response_lower = response.lower()
        
        if any(word in response_lower for word in ['resolved', 'yes', 'helped', 'good', 'thanks']):
            return self.conversation_handler.get_feedback_message()
        elif any(word in response_lower for word in ['escalate', 'agent', 'human', 'help']):
            return self._escalate_to_agent()
        else:
            return {
                "message": "I'm here to help. What else can I assist you with?",
                "buttons": []
            }
    
    def _handle_feedback(self, feedback: str) -> Dict:
        """Handle feedback response"""
        feedback_lower = feedback.lower()
        
        if any(word in feedback_lower for word in ['positive', 'good', 'yes', 'happy']):
            return self.conversation_handler.get_end_message("positive")
        else:
            return self.conversation_handler.get_end_message("negative")
    
    def _escalate_to_agent(self) -> Dict:
        """Escalate to human agent"""
        escalation_msg = """
I understand you need additional assistance. Let me connect you with our support team.

**Please provide the following information:**
- Device details (make, model, OS version)
- Specific show/episode having issues (if applicable)
- Error messages or screenshots (if any)

**Contact Information:**
- **Phone**: 1-800-GLOBAL-TV (1-800-456-2258)
- **Email**: webmaster@globaltv.com
- **Response Time**: 1-3 business days

A support agent will contact you shortly.

Is there anything else I can help you with while you wait?
"""
        self.conversation_handler.add_to_history("assistant", escalation_msg)
        
        return {
            "message": escalation_msg,
            "buttons": [
                {"label": "✅ That's All", "value": "end"},
                {"label": "❓ Another Question", "value": "continue"}
            ]
        }
    
    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_handler.conversation_history
    
    def reset_conversation(self):
        """Reset conversation to initial state"""
        self.conversation_handler.reset()
        self.session_data = {}
    
    def get_subscription_details(self, name: str, mobile: str) -> Optional[Dict]:
        """Get subscription details for a user"""
        return self.subscription_manager.verify_subscriber(name, mobile)
    
    def search_knowledge_base(self, query: str) -> str:
        """Search knowledge base and return answer"""
        return self.knowledge_manager.get_answer(query)
    
    def get_current_state(self) -> ConversationState:
        """Get current conversation state"""
        return self.conversation_handler.state
    
    def set_state(self, state: ConversationState):
        """Set conversation state manually"""
        self.conversation_handler.state = state


# CLI interface for testing
def main():
    """CLI interface for testing the chatbot"""
    print("=" * 60)
    print("Global TV Support Chatbot - CLI Interface")
    print("=" * 60)
    print()
    
    chatbot = GlobalTVChatbot()
    
    # Start conversation
    welcome = chatbot.start_conversation()
    print(f"Bot: {welcome['message']}\n")
    
    if welcome.get('buttons'):
        print("Options:")
        for i, btn in enumerate(welcome['buttons'], 1):
            print(f"  {i}. {btn['label']}")
        print()
    
    # Main conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nBot: Thank you for contacting Global TV support. Goodbye!")
                break
            
            if user_input.lower() == 'reset':
                chatbot.reset_conversation()
                welcome = chatbot.start_conversation()
                print(f"\nBot: {welcome['message']}\n")
                continue
            
            # Process message
            response = chatbot.process_message(user_input)
            
            print(f"\nBot: {response['message']}\n")
            
            # Show buttons if available
            if response.get('buttons'):
                print("Quick Options:")
                for i, btn in enumerate(response['buttons'], 1):
                    print(f"  {i}. {btn['label']}")
                print()
            
        except KeyboardInterrupt:
            print("\n\nBot: Conversation interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again or type 'reset' to restart.\n")


if __name__ == "__main__":
    main()