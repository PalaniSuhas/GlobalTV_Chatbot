"""Subscription management module"""
import pandas as pd
from datetime import datetime
from typing import Optional, Dict

class SubscriptionManager:
    def __init__(self, csv_path: str = 'data/subscribers.csv'):
        self.csv_path = csv_path
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Load subscriber data from CSV"""
        try:
            self.df = pd.read_csv(self.csv_path)
            self.df['purchase_date'] = pd.to_datetime(self.df['purchase_date'])
            self.df['end_date'] = pd.to_datetime(self.df['end_date'])
        except FileNotFoundError:
            print(f"Warning: {self.csv_path} not found. Please run generate_subscribers.py first.")
            self.df = pd.DataFrame()
    
    def verify_subscriber(self, name: str, mobile: str) -> Optional[Dict]:
        """Verify subscriber by name and mobile number"""
        if self.df is None or self.df.empty:
            return None
        
        # Normalize inputs
        name = name.strip().lower()
        mobile = ''.join(filter(str.isdigit, mobile))  # Keep only digits
        
        # Search for matching subscriber
        for idx, row in self.df.iterrows():
            db_name = row['name'].strip().lower()
            db_mobile = ''.join(filter(str.isdigit, row['mobile']))
            
            if name in db_name or db_name in name:
                if mobile in db_mobile or db_mobile in mobile:
                    return self._format_subscriber_info(row)
        
        return None
    
    def _format_subscriber_info(self, row) -> Dict:
        """Format subscriber information"""
        today = datetime.now().date()
        end_date = row['end_date'].date()
        days_remaining = (end_date - today).days
        
        return {
            'name': row['name'],
            'mobile': row['mobile'],
            'email': row['email'],
            'provider': row['provider'],
            'subscription_type': row['subscription_type'],
            'channels': row['channels'],
            'purchase_date': row['purchase_date'].strftime('%Y-%m-%d'),
            'end_date': row['end_date'].strftime('%Y-%m-%d'),
            'is_active': row['is_active'],
            'account_number': row['account_number'],
            'days_remaining': days_remaining if days_remaining > 0 else 0,
            'status': 'Active' if row['is_active'] else 'Expired'
        }
    
    def get_subscription_info(self, subscriber_info: Dict) -> str:
        """Generate formatted subscription information message"""
        info = f"""
**Subscription Details**

**Account Holder:** {subscriber_info['name']}
**Account Number:** {subscriber_info['account_number']}
**Status:** {subscriber_info['status']}

**Provider:** {subscriber_info['provider']}
**Subscription Type:** {subscriber_info['subscription_type']}

**Subscribed Channels:**
{subscriber_info['channels']}

**Subscription Period:**
- Start Date: {subscriber_info['purchase_date']}
- End Date: {subscriber_info['end_date']}
"""
        
        if subscriber_info['is_active']:
            info += f"- Days Remaining: {subscriber_info['days_remaining']} days\n"
        else:
            info += f"\n⚠️ Your subscription has expired. Please contact your provider to renew.\n"
        
        return info