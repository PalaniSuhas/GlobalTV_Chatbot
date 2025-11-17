"""Core chatbot logic - Clean responses, auto-ticketing, no repetition"""
from typing import Dict, Optional, List
from .subscription_manager import SubscriptionManager
from .knowledge_manager import SmartKnowledgeManager
from .conversation_handler import ConversationHandler, ConversationState
from .ticket_manager import TicketManager


class GlobalTVChatbot:
    """
    Core chatbot class with clean responses and smart escalation
    """
    
    def __init__(self):
        """Initialize chatbot with managers"""
        self.subscription_manager = SubscriptionManager()
        self.knowledge_manager = SmartKnowledgeManager()
        self.conversation_handler = ConversationHandler()
        self.ticket_manager = TicketManager()
        self.session_data = {}
        
        # Track information and attempts
        self.collected_info = {
            'device_info': None,
            'show_details': None,
            'error_details': None,
            'provider': None
        }
        
        # Track resolution attempts
        self.resolution_attempts = 0
        self.max_attempts = 2  # Auto-escalate after 2 failed attempts
        self.ticket_created = False
    
    def start_conversation(self) -> Dict:
        """Start a new conversation"""
        self.conversation_handler.reset()
        self.collected_info = {
            'device_info': None,
            'show_details': None,
            'error_details': None,
            'provider': None
        }
        self.resolution_attempts = 0
        self.ticket_created = False
        return self.conversation_handler.get_welcome_message()
    
    def _extract_info_from_message(self, message: str):
        """Extract and store information from user messages"""
        message_lower = message.lower()
        
        # Extract device info
        devices = ['iphone', 'android', 'samsung', 'tv', 'ipad', 'tablet', 'computer', 'laptop', 'mac', 'windows', 'ios', 'tizen']
        if any(device in message_lower for device in devices):
            if not self.collected_info['device_info']:
                # Extract just the relevant part
                for device in devices:
                    if device in message_lower:
                        start = message_lower.find(device)
                        end = min(start + 100, len(message))
                        self.collected_info['device_info'] = message[start:end].split('.')[0].strip()
                        break
        
        # Extract show details
        show_keywords = ['season', 'episode', 'show', 'series', 'morning show', 'west block', 's2', 'e5']
        if any(word in message_lower for word in show_keywords):
            if not self.collected_info['show_details']:
                for keyword in show_keywords:
                    if keyword in message_lower:
                        start = message_lower.find(keyword)
                        end = min(start + 80, len(message))
                        self.collected_info['show_details'] = message[start:end].split('.')[0].strip()
                        break
        
        # Extract error details
        error_keywords = ['freeze', 'crash', 'stop', 'error', 'minute', 'mark', 'stuck', 'loading']
        if any(word in message_lower for word in error_keywords):
            if not self.collected_info['error_details']:
                for keyword in error_keywords:
                    if keyword in message_lower:
                        start = max(0, message_lower.find(keyword) - 30)
                        end = min(message_lower.find(keyword) + 80, len(message))
                        self.collected_info['error_details'] = message[start:end].strip()
                        break
        
        # Extract provider
        providers = ['rogers', 'bell', 'shaw', 'telus', 'videotron', 'cogeco']
        if any(provider in message_lower for provider in providers):
            if not self.collected_info['provider']:
                for provider in providers:
                    if provider in message_lower:
                        self.collected_info['provider'] = provider.capitalize()
                        break
    
    def process_message(self, message: str, message_type: str = "text") -> Dict:
        """Process user message and return response"""
        current_state = self.conversation_handler.state
        
        # Extract info from message
        self._extract_info_from_message(message)
        
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
            response = self.conversation_handler.handle_category_selection("general")
            self.conversation_handler.add_to_history("assistant", response["message"])
            return response
    
    def _handle_subscription_name(self, name: str) -> Dict:
        """Handle name input"""
        response = self.conversation_handler.handle_subscription_name(name)
        self.conversation_handler.add_to_history("assistant", response["message"])
        return response
    
    def _handle_subscription_mobile(self, mobile: str) -> Dict:
        """Handle mobile number input"""
        response = self.conversation_handler.handle_subscription_mobile(mobile)
        self.conversation_handler.add_to_history("assistant", response["message"])
        
        name = self.conversation_handler.context.get('name')
        mobile = self.conversation_handler.context.get('mobile')
        
        subscriber_info = self.subscription_manager.verify_subscriber(name, mobile)
        verification_response = self.conversation_handler.handle_subscription_verified(subscriber_info)
        self.conversation_handler.add_to_history("assistant", verification_response["message"])
        
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
        
        return self._handle_general_query(query)
    
    def _handle_technical_support(self, query: str) -> Dict:
        """Handle technical support - Clean responses only"""
        query_lower = query.lower()
        
        # Check if user said issue not resolved
        if any(word in query_lower for word in ['still', 'not', "didn't", 'no', 'same', 'persist']):
            self.resolution_attempts += 1
            
            # Auto-escalate after 2 attempts
            if self.resolution_attempts >= self.max_attempts and not self.ticket_created:
                return self._auto_escalate()
        
        # Determine issue type
        if query_lower in ['general tech', 'general_tech']:
            is_ad_issue = False
        elif query_lower in ['ad freezing', 'ad_freezing', 'ad commercials']:
            is_ad_issue = True
        else:
            ad_keywords = ['ad', 'commercial', 'freeze', 'freezing', 'crash', 'crashing', 'stuck']
            is_ad_issue = any(keyword in query_lower for keyword in ad_keywords)
        
        # Check if we have enough info
        has_device = self.collected_info['device_info'] is not None
        has_show = self.collected_info['show_details'] is not None
        
        if is_ad_issue:
            # Ad issue - give solution immediately
            answer = """**Troubleshooting Steps for Ad Freezing/Crashing:**

1. Clear app cache/data → Remove app → Restart device → Reinstall app
2. Turn off ad blockers and pop-up blockers
3. Disable VPN if you're using one
4. Install any pending software updates
5. Reboot your WiFi router, forget the network, then reconnect
6. If issue persists: Hold Pause button for 5 seconds (hard power down), then reinstall app

Please try these steps and let me know if the issue is resolved."""
        
        elif has_device or has_show:
            # We have some info - give general solution
            answer = """**Troubleshooting Steps:**

1. Clear browser cache and cookies (or clear app data on mobile)
2. Try a different browser (Chrome, Firefox, Safari)
3. Temporarily disable any ad blockers or VPN
4. Check your internet connection speed
5. Try watching a different episode to see if the issue is content-specific
6. Sign out and sign back in to your account

Try these steps and let me know if it helps."""
        
        else:
            # Need basic info
            answer = """**To help you better, I need:**

• What device are you using? (e.g., iPhone 14, Samsung Smart TV)
• Which show/episode is having issues?

Once I have this info, I can provide specific troubleshooting steps."""
        
        self.conversation_handler.add_to_history("assistant", answer)
        
        return {
            "message": answer,
            "buttons": [
                {"label": "✅ Issue Resolved", "value": "resolved"},
                {"label": "❌ Still Need Help", "value": "escalate"}
            ]
        }
    
    def _handle_general_query(self, query: str) -> Dict:
        """Handle general queries - with smart escalation"""
        query_lower = query.lower()
        
        # Check if user is frustrated or issue not resolved
        if any(word in query_lower for word in ['still', 'not working', 'same problem', 'again', 'frustrated']):
            self.resolution_attempts += 1
            
            if self.resolution_attempts >= self.max_attempts and not self.ticket_created:
                return self._auto_escalate()
        
        # Try knowledge base
        answer = self.knowledge_manager.get_answer(
            query, 
            conversation_history=self.conversation_handler.conversation_history
        )
        
        # Check if answer is generic "contact support" response
        if "webmaster@globaltv.com" in answer and "knowledge base" in answer.lower():
            # Knowledge base doesn't have answer - escalate immediately
            return self._auto_escalate()
        
        self.conversation_handler.add_to_history("assistant", answer)
        
        return {
            "message": answer,
            "buttons": [
                {"label": "✅ That Helped!", "value": "resolved"},
                {"label": "❓ Follow-up Question", "value": "continue"},
                {"label": "❌ Need More Help", "value": "escalate"}
            ]
        }
    
    def _auto_escalate(self) -> Dict:
        """Automatically escalate and create ticket"""
        if not self.ticket_created:
            # Create ticket
            subscriber_info = self.conversation_handler.context.get('subscriber_info')
            
            # Build issue summary
            issue_parts = []
            if self.collected_info['device_info']:
                issue_parts.append(f"Device: {self.collected_info['device_info']}")
            if self.collected_info['show_details']:
                issue_parts.append(f"Content: {self.collected_info['show_details']}")
            if self.collected_info['error_details']:
                issue_parts.append(f"Issue: {self.collected_info['error_details']}")
            
            issue_summary = " | ".join(issue_parts) if issue_parts else "Technical issue requiring escalation"
            
            # Create ticket
            ticket_id = self.ticket_manager.create_ticket(
                category="Technical Support",
                issue_summary=issue_summary,
                conversation_history=self.conversation_handler.conversation_history,
                subscriber_info=subscriber_info,
                device_info=self.collected_info['device_info'],
                show_details=self.collected_info['show_details'],
                error_details=self.collected_info['error_details'],
                priority="High"
            )
            
            self.ticket_created = True
            
            message = f"""I've created a support ticket for you.

**Ticket ID:** {ticket_id}

Our technical team will review your case and contact you within 24 hours.

**Contact Options:**
📞 **Phone:** 1-800-GLOBAL-TV (1-800-456-2258)
📧 **Email:** webmaster@globaltv.com

Please reference your ticket ID when contacting us.

Is there anything else I can help you with?"""
        
        else:
            # Ticket already created
            message = """A support ticket has already been created for your issue.

Our technical team will contact you soon.

**Need immediate help?**
📞 Call: 1-800-GLOBAL-TV (1-800-456-2258)

Is there anything else I can help you with?"""
        
        self.conversation_handler.add_to_history("assistant", message)
        
        return {
            "message": message,
            "buttons": [
                {"label": "✅ That's All", "value": "end"},
                {"label": "❓ New Question", "value": "continue"}
            ]
        }
    
    def _handle_resolution(self, response: str) -> Dict:
        """Handle resolution response"""
        response_lower = response.lower()
        
        if any(word in response_lower for word in ['resolved', 'yes', 'helped', 'good', 'thanks', 'thank', 'fixed', 'worked']):
            return self.conversation_handler.get_feedback_message()
        elif any(word in response_lower for word in ['escalate', 'agent', 'human', 'help', 'no', 'still', 'not']):
            return self._auto_escalate()
        else:
            return {
                "message": "I'm here to help. What else can I assist you with?",
                "buttons": []
            }
    
    def _handle_feedback(self, feedback: str) -> Dict:
        """Handle feedback response"""
        feedback_lower = feedback.lower()
        
        if any(word in feedback_lower for word in ['positive', 'good', 'yes', 'happy', 'thank']):
            return self.conversation_handler.get_end_message("positive")
        else:
            return self.conversation_handler.get_end_message("negative")
    
    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_handler.conversation_history
    
    def reset_conversation(self):
        """Reset conversation to initial state"""
        self.conversation_handler.reset()
        self.session_data = {}
        self.collected_info = {
            'device_info': None,
            'show_details': None,
            'error_details': None,
            'provider': None
        }
        self.resolution_attempts = 0
        self.ticket_created = False
    
    def get_subscription_details(self, name: str, mobile: str) -> Optional[Dict]:
        """Get subscription details for a user"""
        return self.subscription_manager.verify_subscriber(name, mobile)
    
    def search_knowledge_base(self, query: str) -> str:
        """Search knowledge base and return answer"""
        return self.knowledge_manager.get_answer(
            query,
            conversation_history=self.conversation_handler.conversation_history
        )
    
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
    print("Global TV Support Chatbot - CLEAN VERSION")
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