"""Ticket management system for unresolved issues"""
import pandas as pd
from datetime import datetime
import os
from typing import Dict, Optional
import random
import string

class TicketManager:
    def __init__(self, tickets_dir: str = 'data/tickets'):
        self.tickets_dir = tickets_dir
        self.tickets_file = os.path.join(tickets_dir, 'support_tickets.csv')
        self._ensure_directory()
        self._initialize_tickets_file()
    
    def _ensure_directory(self):
        """Create tickets directory if it doesn't exist"""
        if not os.path.exists(self.tickets_dir):
            os.makedirs(self.tickets_dir)
            print(f"Created tickets directory: {self.tickets_dir}")
    
    def _initialize_tickets_file(self):
        """Initialize tickets CSV file if it doesn't exist"""
        if not os.path.exists(self.tickets_file):
            df = pd.DataFrame(columns=[
                'ticket_id',
                'created_at',
                'status',
                'category',
                'priority',
                'customer_name',
                'customer_mobile',
                'customer_email',
                'provider',
                'subscription_type',
                'issue_summary',
                'conversation_history',
                'device_info',
                'show_details',
                'error_details',
                'resolution_notes',
                'resolved_at',
                'assigned_to'
            ])
            df.to_csv(self.tickets_file, index=False)
            print(f"Initialized tickets file: {self.tickets_file}")
    
    def _generate_ticket_id(self) -> str:
        """Generate unique ticket ID"""
        timestamp = datetime.now().strftime('%Y%m%d')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"GT-{timestamp}-{random_suffix}"
    
    def create_ticket(self, 
                     category: str,
                     issue_summary: str,
                     conversation_history: list,
                     subscriber_info: Optional[Dict] = None,
                     device_info: Optional[str] = None,
                     show_details: Optional[str] = None,
                     error_details: Optional[str] = None,
                     priority: str = "Medium") -> str:
        """
        Create a new support ticket
        
        Args:
            category: Issue category (technical, subscription, billing, etc.)
            issue_summary: Brief summary of the issue
            conversation_history: List of conversation messages
            subscriber_info: Customer subscription details (if available)
            device_info: Device information
            show_details: Show/episode details (if applicable)
            error_details: Error messages or codes
            priority: Low, Medium, High, Critical
        
        Returns:
            ticket_id: Generated ticket ID
        """
        ticket_id = self._generate_ticket_id()
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Extract customer info
        customer_name = "Unknown"
        customer_mobile = "Unknown"
        customer_email = "Unknown"
        provider = "Unknown"
        subscription_type = "Unknown"
        
        if subscriber_info:
            customer_name = subscriber_info.get('name', 'Unknown')
            customer_mobile = subscriber_info.get('mobile', 'Unknown')
            customer_email = subscriber_info.get('email', 'Unknown')
            provider = subscriber_info.get('provider', 'Unknown')
            subscription_type = subscriber_info.get('subscription_type', 'Unknown')
        
        # Format conversation history
        conversation_text = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}" 
            for msg in conversation_history
        ])
        
        # Create ticket entry
        ticket_data = {
            'ticket_id': ticket_id,
            'created_at': created_at,
            'status': 'Open',
            'category': category,
            'priority': priority,
            'customer_name': customer_name,
            'customer_mobile': customer_mobile,
            'customer_email': customer_email,
            'provider': provider,
            'subscription_type': subscription_type,
            'issue_summary': issue_summary,
            'conversation_history': conversation_text,
            'device_info': device_info or 'Not provided',
            'show_details': show_details or 'Not provided',
            'error_details': error_details or 'Not provided',
            'resolution_notes': '',
            'resolved_at': '',
            'assigned_to': 'Unassigned'
        }
        
        # Append to CSV
        df = pd.read_csv(self.tickets_file)
        df = pd.concat([df, pd.DataFrame([ticket_data])], ignore_index=True)
        df.to_csv(self.tickets_file, index=False)
        
        print(f"Created ticket: {ticket_id}")
        return ticket_id
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Retrieve ticket by ID"""
        try:
            df = pd.read_csv(self.tickets_file)
            ticket = df[df['ticket_id'] == ticket_id]
            if not ticket.empty:
                return ticket.iloc[0].to_dict()
            return None
        except Exception as e:
            print(f"Error retrieving ticket: {e}")
            return None
    
    def update_ticket_status(self, ticket_id: str, status: str, resolution_notes: str = ""):
        """Update ticket status"""
        try:
            df = pd.read_csv(self.tickets_file)
            mask = df['ticket_id'] == ticket_id
            df.loc[mask, 'status'] = status
            
            if resolution_notes:
                df.loc[mask, 'resolution_notes'] = resolution_notes
            
            if status.lower() in ['resolved', 'closed']:
                df.loc[mask, 'resolved_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            df.to_csv(self.tickets_file, index=False)
            print(f"Updated ticket {ticket_id} to status: {status}")
        except Exception as e:
            print(f"Error updating ticket: {e}")
    
    def get_open_tickets(self) -> pd.DataFrame:
        """Get all open tickets"""
        try:
            df = pd.read_csv(self.tickets_file)
            return df[df['status'] == 'Open']
        except Exception as e:
            print(f"Error retrieving open tickets: {e}")
            return pd.DataFrame()
    
    def get_ticket_stats(self) -> Dict:
        """Get ticket statistics"""
        try:
            df = pd.read_csv(self.tickets_file)
            stats = {
                'total': len(df),
                'open': len(df[df['status'] == 'Open']),
                'resolved': len(df[df['status'] == 'Resolved']),
                'closed': len(df[df['status'] == 'Closed']),
                'by_category': df['category'].value_counts().to_dict(),
                'by_priority': df['priority'].value_counts().to_dict()
            }
            return stats
        except Exception as e:
            print(f"Error getting ticket stats: {e}")
            return {}