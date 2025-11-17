"""Flask Backend for Global TV Chatbot"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from src.chatbot import GlobalTVChatbot

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for Next.js frontend

# Store chatbot instances per session
chatbot_sessions = {}


def get_or_create_chatbot(session_id: str) -> GlobalTVChatbot:
    """Get existing chatbot or create new one for session"""
    if session_id not in chatbot_sessions:
        chatbot_sessions[session_id] = GlobalTVChatbot()
        # Initialize with welcome message
        chatbot_sessions[session_id].start_conversation()
    return chatbot_sessions[session_id]


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        message = data.get('message', '')
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create chatbot for this session
        chatbot = get_or_create_chatbot(session_id)
        
        # Process message
        response = chatbot.process_message(message)
        
        return jsonify({
            'message': response['message'],
            'buttons': response.get('buttons', []),
            'state': chatbot.get_current_state().value
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'message': 'Sorry, I encountered an error. Please try again.',
            'buttons': []
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation"""
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        
        if session_id in chatbot_sessions:
            chatbot_sessions[session_id].reset_conversation()
            welcome = chatbot_sessions[session_id].start_conversation()
            return jsonify({
                'message': welcome['message'],
                'buttons': welcome.get('buttons', [])
            })
        
        return jsonify({
            'message': 'Session not found',
            'buttons': []
        }), 404
    
    except Exception as e:
        print(f"Error in reset endpoint: {e}")
        return jsonify({
            'message': 'Error resetting conversation',
            'buttons': []
        }), 500


@app.route('/api/subscription', methods=['POST'])
def get_subscription():
    """Get subscription details"""
    try:
        data = request.json
        name = data.get('name', '')
        mobile = data.get('mobile', '')
        session_id = data.get('session_id', 'default')
        
        if not name or not mobile:
            return jsonify({'error': 'Name and mobile are required'}), 400
        
        chatbot = get_or_create_chatbot(session_id)
        subscriber_info = chatbot.get_subscription_details(name, mobile)
        
        if subscriber_info:
            return jsonify({
                'success': True,
                'subscriber_info': subscriber_info
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Subscriber not found'
            })
    
    except Exception as e:
        print(f"Error in subscription endpoint: {e}")
        return jsonify({
            'success': False,
            'message': 'Error retrieving subscription'
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'active_sessions': len(chatbot_sessions)
    })


@app.route('/api/tickets/stats', methods=['GET'])
def ticket_stats():
    """Get ticket statistics"""
    try:
        from src.ticket_manager import TicketManager
        ticket_manager = TicketManager()
        stats = ticket_manager.get_ticket_stats()
        return jsonify(stats)
    except Exception as e:
        print(f"Error getting ticket stats: {e}")
        return jsonify({'error': 'Error retrieving ticket stats'}), 500


if __name__ == '__main__':
    print("🚀 Global TV Chatbot Backend Starting...")
    print("📡 Server running on http://localhost:5001")
    print("🔗 Connect your Next.js frontend to this server")
    app.run(host='0.0.0.0', port=5001, debug=True)