"""Main Chainlit application"""
import chainlit as cl
from dotenv import load_dotenv
import os
from src.subscription_manager import SubscriptionManager
from src.conversation_handler import ConversationHandler, ConversationState
from src.ticket_manager import TicketManager
from src.knowledge_manager import SmartKnowledgeManager

# Load environment variables
load_dotenv()

# Initialize managers
subscription_manager = SubscriptionManager()
ticket_manager = TicketManager()
knowledge_manager = SmartKnowledgeManager()

@cl.on_chat_start
async def start():
    """Initialize chat session"""
    # Create conversation handler for this session
    conversation_handler = ConversationHandler()
    cl.user_session.set("conversation_handler", conversation_handler)
    
    # Send welcome message
    welcome = conversation_handler.get_welcome_message()
    
    actions = [
        cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], payload={"action": btn["value"]})
        for btn in welcome["buttons"]
    ]
    
    await cl.Message(
        content=welcome["message"],
        actions=actions
    ).send()

@cl.action_callback("subscription")
async def handle_subscription(action):
    """Handle subscription category selection"""
    handler = cl.user_session.get("conversation_handler")
    response = handler.handle_category_selection("subscription")
    
    await cl.Message(content=response["message"]).send()

@cl.action_callback("technical")
async def handle_technical(action):
    """Handle technical support category"""
    handler = cl.user_session.get("conversation_handler")
    response = handler.handle_category_selection("technical")
    
    actions = [
        cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], payload={"action": btn["value"]})
        for btn in response["buttons"]
    ]
    
    await cl.Message(content=response["message"], actions=actions).send()

@cl.action_callback("billing")
async def handle_billing(action):
    """Handle billing category"""
    handler = cl.user_session.get("conversation_handler")
    response = handler.handle_category_selection("billing")
    
    await cl.Message(content=response["message"]).send()

@cl.action_callback("content")
async def handle_content(action):
    """Handle content/programming category"""
    handler = cl.user_session.get("conversation_handler")
    response = handler.handle_category_selection("content")
    
    actions = [
        cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], payload={"action": btn["value"]})
        for btn in response["buttons"]
    ]
    
    await cl.Message(content=response["message"], actions=actions).send()

@cl.action_callback("general")
async def handle_general(action):
    """Handle general questions category"""
    handler = cl.user_session.get("conversation_handler")
    response = handler.handle_category_selection("general")
    
    await cl.Message(content=response["message"]).send()

@cl.action_callback("general_tech")
async def handle_general_tech(action):
    """Handle General Tech/Video Issues - Bucket 1"""
    
    template = """
**Be Specific - General Tech/Video Issues**

Hello there,

Thank you for your email. We appreciate your interest in Global TV.

To help us investigate, please be more specific on the issues you are experiencing by answering all of the questions below:

• What is the Make, Model, and OS version of your playback device(s)?
• What are you trying to watch? (please provide Show name, Season number, Episode name/number)
• What errors are you getting? At what point in the video timeline is the error displayed? (please provide a screenshot if possible)
• Did you have the same issue when trying to play other videos (older episodes, news, clips) or does it happen only on specific videos? Please test watching some videos from other shows and let us know the result.
• Are you able to watch Live TV (Live News, Global Live TV, Specialty Live Channels) without any issues?
• Who do you have an Active Cable TV Subscription with? Which Global channels are you subscribed to?
• Are you able to successfully sign-in to the Global TV website https://watch.globaltv.com/ on a computer/laptop? Please test this and let us know which Global channels you get access to.
• Which browser are you using on your computer? For testing purposes, please use different browsers (Chrome, Firefox, Edge, Safari) to sign-in to the Global TV website and watch the same video and let us know the result?

Thank you.

Regards,
The Global TV App Team
"""
    
    await cl.Message(content=template).send()
    
    # Ask if issue is resolved
    actions = [
        cl.Action(name="resolved", value="resolved", label="✅ Issue Resolved", payload={"action": "resolved"}),
        cl.Action(name="need_more_help", value="escalate", label="❌ Still Need Help", payload={"action": "escalate"})
    ]
    
    await cl.Message(
        content="Does this template help, or would you like to speak with an agent?",
        actions=actions
    ).send()

@cl.action_callback("ad_freezing")
async def handle_ad_freezing(action):
    """Handle Ad Commercials Freezing and App Crashing - Bucket 2"""
    
    template = """
**Ad Commercials Freezing and App Crashing**

Hello there,

Thank you for your email. We appreciate your interest in Global TV.

To help us investigate please be more specific on the issues you are experiencing by answering all of the questions below:

• What is the model code/number and OS version of your devices you are having this issue on?
• What are you trying to watch? (please provide Show name, Season number, Episode name/number)
• Which AD commercials in particular trigger the freezing? (please provide screenshot/video clip if possible)
• Please try the following troubleshooting steps:
  ○ Clear app cache/data, remove the app, restart your device and re-install the Global TV App and test the same videos again and let us know the result?
  ○ Turn off any adblockers, pop-up blockers, related add-ons that prevent ads from playing.
  ○ Turn off any VPN if you are using one.
  ○ Complete any pending software updates on your device and test again?
  ○ Reboot/power cycle your WiFi router, forget network on your device and make a fresh connection, launch the app and test watching again?
  ○ If the issue persists, remove the app, Power down with Hard 5 Second Hold on the Pause button, then re-install the app and test again.

Thank you.

Regards,
The Global TV App Team
"""
    
    await cl.Message(content=template).send()
    
    # Ask if issue is resolved
    actions = [
        cl.Action(name="resolved", value="resolved", label="✅ Issue Resolved", payload={"action": "resolved"}),
        cl.Action(name="need_more_help", value="escalate", label="❌ Still Need Help", payload={"action": "escalate"})
    ]
    
    await cl.Message(
        content="Does this template help, or would you like to speak with an agent?",
        actions=actions
    ).send()

@cl.action_callback("view_subscription")
async def handle_view_subscription(action):
    """Display subscription details"""
    handler = cl.user_session.get("conversation_handler")
    subscriber_info = handler.context.get('subscriber_info')
    
    if subscriber_info:
        info_message = subscription_manager.get_subscription_info(subscriber_info)
        await cl.Message(content=info_message).send()
        
        # Ask if they need more help
        actions = [
            cl.Action(name="resolved", value="resolved", label="✅ That's All I Needed", payload={"action": "resolved"}),
            cl.Action(name="need_more_help", value="more_help", label="❓ I Have Another Question", payload={"action": "more_help"})
        ]
        
        await cl.Message(
            content="Is there anything else I can help you with?",
            actions=actions
        ).send()
    else:
        await cl.Message(content="Please verify your account first.").send()

@cl.action_callback("channel_access")
async def handle_channel_access(action):
    """Handle channel access questions using subscriber info"""
    handler = cl.user_session.get("conversation_handler")
    subscriber_info = handler.context.get('subscriber_info')
    
    if subscriber_info:
        channels = subscriber_info.get('channels', 'No channel information available')
        subscription_type = subscriber_info.get('subscription_type', 'Unknown')
        provider = subscriber_info.get('provider', 'Unknown')
        
        response = f"""
**Your Channel Access**

Based on your **{subscription_type}** subscription with **{provider}**, you have access to:

{channels}

**Need help accessing a specific channel?**
1. Make sure you're signed in to the Global TV app/website
2. Verify your subscription is active with {provider}
3. Try signing out and back in
4. Clear your app cache if on mobile

Would you like help with anything else?
"""
        await cl.Message(content=response).send()
        
        actions = [
            cl.Action(name="resolved", value="resolved", label="✅ That Helped!", payload={"action": "resolved"}),
            cl.Action(name="need_more_help", value="escalate", label="❌ Still Having Issues", payload={"action": "escalate"})
        ]
        
        await cl.Message(
            content="Did this answer your question?",
            actions=actions
        ).send()
    else:
        await cl.Message(content="Please verify your account first to view your channel access.").send()

@cl.action_callback("renewal")
async def handle_renewal(action):
    """Handle subscription renewal questions"""
    handler = cl.user_session.get("conversation_handler")
    subscriber_info = handler.context.get('subscriber_info')
    
    if subscriber_info:
        end_date = subscriber_info.get('end_date', 'Unknown')
        days_remaining = subscriber_info.get('days_remaining', 0)
        provider = subscriber_info.get('provider', 'your provider')
        status = subscriber_info.get('status', 'Unknown')
        
        if status == 'Active':
            response = f"""
**Subscription Renewal Information**

Your subscription expires on **{end_date}** ({days_remaining} days remaining).

**To renew your subscription:**
1. Contact **{provider}** directly
2. Call their customer service number
3. Ask about Global TV subscription renewal options

**Note:** Global TV subscriptions are managed by your TV service provider ({provider}), not directly by Global TV.

Your subscription should auto-renew if you have automatic billing set up with {provider}.
"""
        else:
            response = f"""
**Subscription Expired**

Your subscription ended on **{end_date}**.

**To reactivate:**
1. Contact **{provider}** immediately
2. Ask to renew your Global TV subscription
3. Your access will be restored once payment is processed

**Need immediate access?** Call {provider}'s customer service.
"""
        
        await cl.Message(content=response).send()
        
        actions = [
            cl.Action(name="resolved", value="resolved", label="✅ That Helped!", payload={"action": "resolved"}),
            cl.Action(name="need_more_help", value="escalate", label="❓ More Questions", payload={"action": "escalate"})
        ]
        
        await cl.Message(
            content="Is there anything else I can help with?",
            actions=actions
        ).send()
    else:
        await cl.Message(content="Please verify your account first.").send()

@cl.action_callback("show_availability")
@cl.action_callback("schedule")
@cl.action_callback("episode_availability")
@cl.action_callback("other")
async def handle_query_with_kb(action):
    """Handle queries using knowledge base"""
    query_type = action.name.replace("_", " ")
    
    await cl.Message(content=f"Let me help you with {query_type}. Please provide more details about your question.").send()

@cl.action_callback("resolved")
async def handle_resolved(action):
    """Handle when issue is resolved"""
    handler = cl.user_session.get("conversation_handler")
    feedback = handler.get_feedback_message()
    
    actions = [
        cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], payload={"action": btn["value"]})
        for btn in feedback["buttons"]
    ]
    
    await cl.Message(content=feedback["message"], actions=actions).send()

@cl.action_callback("positive")
async def handle_positive_feedback(action):
    """Handle positive feedback"""
    handler = cl.user_session.get("conversation_handler")
    end_msg = handler.get_end_message("positive")
    
    actions = [
        cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], payload={"action": btn["value"]})
        for btn in end_msg["buttons"]
    ]
    
    await cl.Message(content=end_msg["message"], actions=actions).send()

@cl.action_callback("negative")
async def handle_negative_feedback(action):
    """Handle negative feedback and create ticket"""
    handler = cl.user_session.get("conversation_handler")
    
    # Extract information for ticket
    subscriber_info = handler.context.get('subscriber_info')
    conversation_history = handler.conversation_history
    category = handler.context.get('category', 'General')
    
    # Extract details from conversation
    device_info = None
    show_details = None
    error_details = None
    
    for msg in conversation_history:
        content = msg['content'].lower()
        if any(device in content for device in ['iphone', 'android', 'samsung', 'device', 'tv', 'computer']):
            device_info = msg['content']
        if 'season' in content or 'episode' in content or 'show' in content:
            show_details = msg['content']
        if 'error' in content:
            error_details = msg['content']
    
    # Create summary
    last_user_msg = [m for m in conversation_history if m['role'] == 'user']
    issue_summary = last_user_msg[-1]['content'] if last_user_msg else "Customer feedback: Could be better"
    
    # Create ticket
    ticket_id = ticket_manager.create_ticket(
        category=category.capitalize(),
        issue_summary=issue_summary[:200],
        conversation_history=conversation_history,
        subscriber_info=subscriber_info,
        device_info=device_info,
        show_details=show_details,
        error_details=error_details,
        priority="Medium"
    )
    
    end_msg = f"""Thank you for your feedback. I'm sorry I couldn't fully meet your expectations.

**Support Ticket Created:**
**Ticket ID:** {ticket_id}
**Status:** Open
**Priority:** Medium

**What happens next:**
1. A support agent will review your conversation
2. They'll contact you within 1-3 business days
3. You can reference ticket **{ticket_id}** in any follow-up

**Need immediate help?**
- **Phone:** 1-800-GLOBAL-TV (1-800-456-2258)
- **Email:** webmaster@globaltv.com

Your feedback helps us improve. Thank you!"""
    
    actions = [
        cl.Action(name="restart", value="restart", label="🔄 Start New Conversation", 
                 payload={"action": "restart"})
    ]
    
    await cl.Message(content=end_msg, actions=actions).send()


@cl.action_callback("need_more_help")
@cl.action_callback("escalate")
@cl.action_callback("not_resolved")
async def handle_escalation(action):
    """Handle escalation to human agent with ticket creation"""
    handler = cl.user_session.get("conversation_handler")
    subscriber_info = handler.context.get('subscriber_info')
    
    # Extract device/show/error info
    device_info = None
    show_details = None
    error_details = None
    
    for msg in handler.conversation_history:
        content = msg['content'].lower()
        if any(device in content for device in ['iphone', 'android', 'samsung', 'device', 'tv']):
            device_info = msg['content'][:500]  # Limit length
        if 'season' in content or 'episode' in content:
            show_details = msg['content'][:500]
        if 'error' in content:
            error_details = msg['content'][:500]
    
    # Create ticket
    ticket_id = ticket_manager.create_ticket(
        category=handler.context.get('category', 'General').capitalize(),
        issue_summary="Customer requested human agent assistance",
        conversation_history=handler.conversation_history,
        subscriber_info=subscriber_info,
        device_info=device_info,
        show_details=show_details,
        error_details=error_details,
        priority="High"
    )
    
    escalation_msg = f"""I understand you need additional support. Let me connect you with our team.

**Support Ticket Created:**
**Ticket ID:** {ticket_id}
**Status:** Open - Escalated to Support Team  
**Priority:** High

**What you can expect:**
✓ Full conversation review by support agent
✓ Response within 1-3 business days
✓ Direct follow-up via email or phone

**Urgent issues? Contact us now:**
📞 **Phone:** 1-800-GLOBAL-TV (1-800-456-2258)
📧 **Email:** webmaster@globaltv.com

When contacting, mention ticket **{ticket_id}** for faster service."""
    
    await cl.Message(content=escalation_msg).send()
    
    # Ask for final feedback
    actions = [
        cl.Action(name="positive", value="positive", label="👍 Thanks for the help", 
                 payload={"action": "positive"}),
        cl.Action(name="restart", value="restart", label="🔄 New Issue", 
                 payload={"action": "restart"})
    ]
    
    await cl.Message(content="Would you like to provide any feedback before you go?", actions=actions).send()


@cl.action_callback("restart")
@cl.action_callback("main_menu")
async def handle_restart(action):
    """Restart conversation"""
    handler = cl.user_session.get("conversation_handler")
    handler.reset()
    
    welcome = handler.get_welcome_message()
    actions = [
        cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], payload={"action": btn["value"]})
        for btn in welcome["buttons"]
    ]
    
    await cl.Message(content=welcome["message"], actions=actions).send()

@cl.action_callback("more_help")
async def handle_more_help(action):
    """Handle request for more help"""
    await cl.Message(content="What else can I help you with?").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages with context awareness"""
    handler = cl.user_session.get("conversation_handler")
    current_state = handler.state
    user_message = message.content
    
    # Add to conversation history
    handler.add_to_history("user", user_message)
    
    if current_state == ConversationState.SUBSCRIPTION_NAME:
        response = handler.handle_subscription_name(user_message)
        await cl.Message(content=response["message"]).send()
        
    elif current_state == ConversationState.SUBSCRIPTION_MOBILE:
        response = handler.handle_subscription_mobile(user_message)
        await cl.Message(content=response["message"]).send()
        
        name = handler.context.get('name')
        mobile = handler.context.get('mobile')
        subscriber_info = subscription_manager.verify_subscriber(name, mobile)
        
        verification_response = handler.handle_subscription_verified(subscriber_info)
        
        actions = [
            cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], 
                     payload={"action": btn["value"]})
            for btn in verification_response["buttons"]
        ]
        
        await cl.Message(content=verification_response["message"], actions=actions).send()
        
    elif current_state == ConversationState.SUBSCRIPTION_VERIFIED or \
         current_state == ConversationState.GENERAL_QUERY or \
         current_state == ConversationState.TECHNICAL_SUPPORT:
        
        subscriber_info = handler.context.get('subscriber_info')
        user_message_lower = user_message.lower()
        
        # Check for subscription-specific queries
        if subscriber_info and any(keyword in user_message_lower for keyword in [
            'channel', 'subscription', 'access', 'package', 'provider', 
            'what do i have', 'my subscription', 'my channels'
        ]):
            channels = subscriber_info.get('channels', 'No information available')
            subscription_type = subscriber_info.get('subscription_type', 'Unknown')
            provider = subscriber_info.get('provider', 'Unknown')
            
            answer = f"""Based on your verified subscription:

**Subscription Type:** {subscription_type}
**Provider:** {provider}
**Your Channels:** {channels}

These are the Global TV channels included in your current subscription package."""
            
            handler.add_to_history("assistant", answer)
            await cl.Message(content=answer).send()
        else:
            # Use SMART knowledge base with conversation history
            answer = knowledge_manager.get_answer(
                user_message, 
                conversation_history=handler.conversation_history
            )
            handler.add_to_history("assistant", answer)
            await cl.Message(content=answer).send()
        
        # Ask if issue is resolved
        actions = [
            cl.Action(name="resolved", value="resolved", label="✅ That Helped!", 
                     payload={"action": "resolved"}),
            cl.Action(name="need_more_help", value="escalate", label="❌ Need More Help", 
                     payload={"action": "escalate"})
        ]
        
        await cl.Message(content="Did that answer your question?", actions=actions).send()
    
    else:
        # Default: use smart knowledge base
        answer = knowledge_manager.get_answer(
            user_message, 
            conversation_history=handler.conversation_history
        )
        handler.add_to_history("assistant", answer)
        await cl.Message(content=answer).send()