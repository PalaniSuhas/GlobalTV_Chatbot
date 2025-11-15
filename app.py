"""Main Chainlit application - CORRECT FLOW WITH 2 ATTEMPTS"""
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
    conversation_handler = ConversationHandler()
    cl.user_session.set("conversation_handler", conversation_handler)
    cl.user_session.set("attempt_count", 0)  # Track resolution attempts
    
    welcome = conversation_handler.get_welcome_message()
    
    actions = [
        cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], payload={"action": btn["value"]})
        for btn in welcome["buttons"]
    ]
    
    await cl.Message(content=welcome["message"], actions=actions).send()


@cl.action_callback("subscription")
async def handle_subscription(action):
    """Handle subscription category selection"""
    handler = cl.user_session.get("conversation_handler")
    response = handler.handle_category_selection("subscription")
    await cl.Message(content=response["message"]).send()


@cl.action_callback("technical")
async def handle_technical(action):
    """Handle technical support category - 2 BUCKETS ONLY"""
    handler = cl.user_session.get("conversation_handler")
    handler.context['category'] = 'technical'
    
    message = """I can help with technical issues. Which describes your problem?"""
    
    actions = [
        cl.Action(name="general_tech", value="general_tech", 
                 label="🎬 Video Won't Play / Loading Issues", 
                 payload={"action": "general_tech"}),
        cl.Action(name="ad_freezing", value="ad_freezing", 
                 label="📺 Ads Freezing / App Crashing", 
                 payload={"action": "ad_freezing"})
    ]
    
    await cl.Message(content=message, actions=actions).send()


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
    await cl.Message(content=response["message"]).send()


@cl.action_callback("general")
async def handle_general(action):
    """Handle general questions category"""
    handler = cl.user_session.get("conversation_handler")
    response = handler.handle_category_selection("general")
    await cl.Message(content=response["message"]).send()


@cl.action_callback("general_tech")
async def handle_general_tech(action):
    """Handle General Tech/Video Issues - Bucket 1 - FIRST ATTEMPT"""
    handler = cl.user_session.get("conversation_handler")
    handler.context['tech_issue_type'] = 'general_tech'
    cl.user_session.set("attempt_count", 1)
    
    solution = """**Video Playback Troubleshooting**

Let's try these steps:

1. **Update & Restart**
   - Complete any pending software updates
   - Restart your device

2. **Clear App Data**
   - Clear app cache/data
   - Sign out and sign back in

3. **Network Check**
   - Reboot your WiFi router
   - Test your internet speed

4. **Reinstall App**
   - Remove the Global TV app
   - Restart device
   - Reinstall the app

Try these steps and let me know if it helps!"""
    
    await cl.Message(content=solution).send()
    
    # Ask if resolved - ATTEMPT 1
    actions = [
        cl.Action(name="resolved_attempt1", value="resolved", 
                 label="✅ Fixed!", 
                 payload={"action": "resolved", "attempt": 1}),
        cl.Action(name="not_resolved_attempt1", value="not_resolved", 
                 label="❌ Still Not Working", 
                 payload={"action": "not_resolved", "attempt": 1})
    ]
    
    await cl.Message(content="Did this fix your issue?", actions=actions).send()


@cl.action_callback("ad_freezing")
async def handle_ad_freezing(action):
    """Handle Ad Freezing Issues - Bucket 2 - FIRST ATTEMPT"""
    handler = cl.user_session.get("conversation_handler")
    handler.context['tech_issue_type'] = 'ad_freezing'
    cl.user_session.set("attempt_count", 1)
    
    solution = """**Ad Freezing / App Crashing Fix**

Try these steps:

1. **Remove Ad Blockers**
   - Turn off any adblockers
   - Turn off pop-up blockers
   - Disable VPN if using one

2. **Clear & Reinstall**
   - Clear app cache/data
   - Remove the app
   - Restart device
   - Reinstall Global TV app

3. **Hard Reset** (If still freezing)
   - Power down device
   - Hold Pause button for 5 seconds
   - Restart and reinstall app

Try these and let me know!"""
    
    await cl.Message(content=solution).send()
    
    # Ask if resolved - ATTEMPT 1
    actions = [
        cl.Action(name="resolved_attempt1", value="resolved", 
                 label="✅ Fixed!", 
                 payload={"action": "resolved", "attempt": 1}),
        cl.Action(name="not_resolved_attempt1", value="not_resolved", 
                 label="❌ Still Freezing", 
                 payload={"action": "not_resolved", "attempt": 1})
    ]
    
    await cl.Message(content="Did this fix the freezing?", actions=actions).send()


@cl.action_callback("resolved_attempt1")
async def handle_resolved_attempt1(action):
    """Handle resolution after first attempt"""
    feedback_msg = "Great! Glad that worked. Quick feedback?"
    
    actions = [
        cl.Action(name="positive", value="positive", label="👍 Helpful!", 
                 payload={"action": "positive"}),
        cl.Action(name="negative", value="negative", label="👎 Could improve", 
                 payload={"action": "negative"}),
        cl.Action(name="restart", value="restart", label="🏠 Main Menu", 
                 payload={"action": "restart"})
    ]
    
    await cl.Message(content=feedback_msg, actions=actions).send()


@cl.action_callback("not_resolved_attempt1")
async def handle_not_resolved_attempt1(action):
    """Handle when first attempt didn't work - TRY SECOND SOLUTION"""
    handler = cl.user_session.get("conversation_handler")
    tech_issue_type = handler.context.get('tech_issue_type', 'general_tech')
    cl.user_session.set("attempt_count", 2)
    
    if tech_issue_type == 'general_tech':
        # ALTERNATE SOLUTION for General Tech
        solution = """Let's try a different approach:

**Advanced Troubleshooting:**

1. **Test on Different Device**
   - Try watching on another device (phone, tablet, computer)
   - This helps identify if it's device-specific

2. **Check Browser (if on computer)**
   - Try different browsers (Chrome, Firefox, Safari)
   - Disable browser extensions
   - Clear browser cache/cookies

3. **Verify Subscription**
   - Go to https://watch.globaltv.com/ on computer
   - Sign in with your TV provider credentials
   - Check if you can play Live TV
   - Verify which channels you have access to

4. **Contact Your Provider**
   - Sometimes the issue is with your TV provider's authentication
   - Contact them to verify your Global TV subscription is active

Try these steps and let me know!"""
    else:
        # ALTERNATE SOLUTION for Ad Freezing
        solution = """Let's try these additional steps:

**Advanced Ad Freezing Fix:**

1. **Identify Specific Ad**
   - Note which specific commercial causes the freeze
   - Try different shows to see if same ad appears

2. **Device-Specific Reset**
   - For Smart TVs: Unplug TV for 60 seconds
   - For streaming devices: Factory reset the device
   - Reinstall Global TV app

3. **Network Optimization**
   - Connect device directly via Ethernet (if possible)
   - Reduce other devices using WiFi
   - Contact your internet provider if speeds are slow

4. **Alternative Viewing**
   - Try watching via https://watch.globaltv.com/ on computer
   - This helps identify if it's app-specific

Try these and let me know the result!"""
    
    await cl.Message(content=solution).send()
    
    # Ask if resolved - ATTEMPT 2
    actions = [
        cl.Action(name="resolved_attempt2", value="resolved", 
                 label="✅ This Fixed It!", 
                 payload={"action": "resolved", "attempt": 2}),
        cl.Action(name="not_resolved_attempt2", value="not_resolved", 
                 label="❌ Still Having Issues", 
                 payload={"action": "not_resolved", "attempt": 2})
    ]
    
    await cl.Message(content="Did this resolve it?", actions=actions).send()


@cl.action_callback("resolved_attempt2")
async def handle_resolved_attempt2(action):
    """Handle resolution after second attempt"""
    feedback_msg = "Excellent! So glad we got it working. Quick feedback?"
    
    actions = [
        cl.Action(name="positive", value="positive", label="👍 Very Helpful!", 
                 payload={"action": "positive"}),
        cl.Action(name="negative", value="negative", label="👎 Could improve", 
                 payload={"action": "negative"}),
        cl.Action(name="restart", value="restart", label="🏠 Main Menu", 
                 payload={"action": "restart"})
    ]
    
    await cl.Message(content=feedback_msg, actions=actions).send()


@cl.action_callback("not_resolved_attempt2")
async def handle_not_resolved_attempt2(action):
    """Handle when both attempts failed - AUTO-CREATE TICKET"""
    handler = cl.user_session.get("conversation_handler")
    
    # AUTO-CREATE TICKET (user shouldn't need to ask)
    await auto_create_ticket(handler, "Technical issue unresolved after 2 attempts")


async def auto_create_ticket(handler, issue_summary):
    """Automatically create ticket when solutions don't work"""
    subscriber_info = handler.context.get('subscriber_info')
    conversation_history = handler.conversation_history
    category = handler.context.get('category', 'Technical')
    tech_issue_type = handler.context.get('tech_issue_type', 'general')
    
    # Extract device, show, error details from conversation
    device_info = None
    show_details = None
    error_details = None
    
    for msg in conversation_history:
        content = msg['content']
        content_lower = content.lower()
        
        # Look for device info
        if any(keyword in content_lower for keyword in 
               ['iphone', 'android', 'samsung', 'tv', 'device', 'ios', 'tizen', 'fire stick', 'roku']):
            if not device_info or len(content) > len(device_info or ''):
                device_info = content[:500]
        
        # Look for show/episode info
        if any(keyword in content_lower for keyword in ['season', 'episode', 'show', 's0', 's1', 's2']):
            if not show_details:
                show_details = content[:500]
        
        # Look for error messages
        if 'error' in content_lower or 'message' in content_lower:
            if not error_details:
                error_details = content[:500]
    
    # Create ticket
    ticket_id = ticket_manager.create_ticket(
        category=category.capitalize(),
        issue_summary=f"{tech_issue_type}: {issue_summary}"[:200],
        conversation_history=conversation_history,
        subscriber_info=subscriber_info,
        device_info=device_info,
        show_details=show_details,
        error_details=error_details,
        priority="High"
    )
    
    # Show ticket confirmation
    ticket_msg = f"""I've tried two solutions but the issue persists. I've automatically created a support ticket for you.

**🎫 Support Ticket Created**

**Ticket ID:** {ticket_id}
**Status:** Open - Escalated to Technical Team
**Priority:** High

**What Happens Next:**
✓ Our technical team will review your case
✓ You'll receive a response within 1-3 business days
✓ They'll have your full conversation and troubleshooting history

**Need Immediate Help?**
📞 Phone: 1-800-GLOBAL-TV (1-800-456-2258)
📧 Email: webmaster@globaltv.com

**Important:** Please reference ticket **{ticket_id}** when contacting support.

A support specialist will reach out to you soon!"""
    
    await cl.Message(content=ticket_msg).send()
    
    # Final feedback
    actions = [
        cl.Action(name="positive", value="positive", 
                 label="👍 Thanks for trying to help", 
                 payload={"action": "positive"}),
        cl.Action(name="restart", value="restart", 
                 label="🔄 Start Over", 
                 payload={"action": "restart"})
    ]
    
    await cl.Message(content="Anything else before you go?", actions=actions).send()


@cl.action_callback("view_subscription")
async def handle_view_subscription(action):
    """Display subscription details"""
    handler = cl.user_session.get("conversation_handler")
    subscriber_info = handler.context.get('subscriber_info')
    
    if subscriber_info:
        info_message = subscription_manager.get_subscription_info(subscriber_info)
        await cl.Message(content=info_message).send()
        
        actions = [
            cl.Action(name="resolved", value="resolved", label="✅ That's All", 
                     payload={"action": "resolved"}),
            cl.Action(name="need_more_help", value="more_help", label="❓ Another Question", 
                     payload={"action": "more_help"})
        ]
        await cl.Message(content="Anything else?", actions=actions).send()
    else:
        await cl.Message(content="Please verify your account first.").send()


@cl.action_callback("channel_access")
async def handle_channel_access(action):
    """Handle channel access"""
    handler = cl.user_session.get("conversation_handler")
    subscriber_info = handler.context.get('subscriber_info')
    
    if subscriber_info:
        channels = subscriber_info.get('channels', 'No info')
        subscription_type = subscriber_info.get('subscription_type', 'Unknown')
        provider = subscriber_info.get('provider', 'Unknown')
        
        response = f"""**Your Channel Access**

**{subscription_type}** with **{provider}**

**Your Channels:** {channels}

**Quick Fix:**
1. Sign in to Global TV app/website
2. Verify subscription active with {provider}
3. Clear app cache and sign in again"""
        
        await cl.Message(content=response).send()
        
        actions = [
            cl.Action(name="resolved", value="resolved", label="✅ Got it!", 
                     payload={"action": "resolved"}),
            cl.Action(name="not_resolved", value="not_resolved", label="❌ Still issues", 
                     payload={"action": "not_resolved"})
        ]
        await cl.Message(content="Did this help?", actions=actions).send()
    else:
        await cl.Message(content="Please verify your account first.").send()


@cl.action_callback("renewal")
async def handle_renewal(action):
    """Handle renewal questions"""
    handler = cl.user_session.get("conversation_handler")
    subscriber_info = handler.context.get('subscriber_info')
    
    if subscriber_info:
        end_date = subscriber_info.get('end_date', 'Unknown')
        days_remaining = subscriber_info.get('days_remaining', 0)
        provider = subscriber_info.get('provider', 'your provider')
        status = subscriber_info.get('status', 'Unknown')
        
        if status == 'Active':
            response = f"""**Renewal Info**

Expires: **{end_date}** ({days_remaining} days)
Contact **{provider}** to renew
Should auto-renew if you have automatic billing"""
        else:
            response = f"""**Subscription Expired**

Ended: **{end_date}**
Contact **{provider}** to reactivate"""
        
        await cl.Message(content=response).send()
        
        actions = [
            cl.Action(name="resolved", value="resolved", label="✅ Thanks!", 
                     payload={"action": "resolved"}),
            cl.Action(name="more_help", value="more_help", label="❓ More Questions", 
                     payload={"action": "more_help"})
        ]
        await cl.Message(content="Anything else?", actions=actions).send()
    else:
        await cl.Message(content="Please verify your account first.").send()


@cl.action_callback("positive")
async def handle_positive_feedback(action):
    """Handle positive feedback"""
    end_msg = "Thank you for your feedback! Have a great day! 🎉"
    actions = [
        cl.Action(name="restart", value="restart", label="🔄 New Conversation", 
                 payload={"action": "restart"})
    ]
    await cl.Message(content=end_msg, actions=actions).send()


@cl.action_callback("negative")
async def handle_negative_feedback(action):
    """Handle negative feedback"""
    handler = cl.user_session.get("conversation_handler")
    
    # Create ticket for negative feedback
    await auto_create_ticket(handler, "Customer feedback: Experience could be improved")


@cl.action_callback("restart")
@cl.action_callback("main_menu")
async def handle_restart(action):
    """Restart conversation"""
    handler = cl.user_session.get("conversation_handler")
    handler.reset()
    cl.user_session.set("attempt_count", 0)
    
    welcome = handler.get_welcome_message()
    actions = [
        cl.Action(name=btn["value"], value=btn["value"], label=btn["label"], 
                 payload={"action": btn["value"]})
        for btn in welcome["buttons"]
    ]
    await cl.Message(content=welcome["message"], actions=actions).send()


@cl.action_callback("more_help")
async def handle_more_help(action):
    """Handle more help request"""
    await cl.Message(content="What else can I help with?").send()


@cl.on_message
async def main(message: cl.Message):
    """Handle user messages"""
    handler = cl.user_session.get("conversation_handler")
    current_state = handler.state
    user_message = message.content
    
    # Add to history
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
        
    elif current_state in [ConversationState.SUBSCRIPTION_VERIFIED, ConversationState.GENERAL_QUERY]:
        # Use smart knowledge base with context
        answer = knowledge_manager.get_answer(user_message, 
                                              conversation_history=handler.conversation_history)
        handler.add_to_history("assistant", answer)
        await cl.Message(content=answer).send()
        
        # Ask if resolved
        actions = [
            cl.Action(name="resolved", value="resolved", label="✅ That Helped!", 
                     payload={"action": "resolved"}),
            cl.Action(name="not_resolved", value="not_resolved", label="❌ Need More Help", 
                     payload={"action": "not_resolved"})
        ]
        await cl.Message(content="Did that answer your question?", actions=actions).send()
    
    else:
        # Default: use knowledge base
        answer = knowledge_manager.get_answer(user_message, 
                                              conversation_history=handler.conversation_history)
        handler.add_to_history("assistant", answer)
        await cl.Message(content=answer).send()


@cl.action_callback("resolved")
async def handle_resolved(action):
    """Handle general resolved action"""
    feedback_msg = "Great! Quick feedback?"
    actions = [
        cl.Action(name="positive", value="positive", label="👍 Helpful!", 
                 payload={"action": "positive"}),
        cl.Action(name="negative", value="negative", label="👎 Could improve", 
                 payload={"action": "negative"}),
        cl.Action(name="restart", value="restart", label="🏠 Main Menu", 
                 payload={"action": "restart"})
    ]
    await cl.Message(content=feedback_msg, actions=actions).send()


@cl.action_callback("not_resolved")
async def handle_not_resolved(action):
    """Handle general not resolved - create ticket"""
    handler = cl.user_session.get("conversation_handler")
    await auto_create_ticket(handler, "Customer issue not resolved")