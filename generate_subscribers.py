"""Generate fake subscriber database for testing"""
from faker import Faker
import pandas as pd
from datetime import datetime, timedelta
import random

fake = Faker('en_CA')
Faker.seed(42)
random.seed(42)

def generate_subscribers(num_subscribers=100):
    """Generate fake subscriber data"""
    subscribers = []
    
    subscription_types = [
        'Basic Cable',
        'Premium Cable',
        'Global TV Only',
        'Global + Specialty Channels',
        'Ultimate Package'
    ]
    
    providers = [
        'Rogers',
        'Bell',
        'Shaw',
        'Telus',
        'Videotron',
        'Cogeco'
    ]
    
    global_channels = {
        'Basic Cable': ['Global TV'],
        'Premium Cable': ['Global TV', 'Global News'],
        'Global TV Only': ['Global TV'],
        'Global + Specialty Channels': ['Global TV', 'Global News', 'Showcase', 'HISTORY', 'Food Network', 'HGTV'],
        'Ultimate Package': ['Global TV', 'Global News', 'Showcase', 'HISTORY', 'Food Network', 'HGTV', 'W Network', 'Slice', 'Lifetime', 'National Geographic']
    }
    
    for _ in range(num_subscribers):
        subscription_type = random.choice(subscription_types)
        purchase_date = fake.date_between(start_date='-2y', end_date='today')
        
        # Some subscriptions are active, some expired
        if random.random() < 0.8:  # 80% active
            end_date = purchase_date + timedelta(days=random.randint(365, 730))
        else:  # 20% expired
            end_date = purchase_date + timedelta(days=random.randint(30, 300))
        
        is_active = end_date > datetime.now().date()
        
        subscriber = {
            'name': fake.name(),
            'mobile': fake.phone_number(),
            'email': fake.email(),
            'provider': random.choice(providers),
            'subscription_type': subscription_type,
            'channels': ', '.join(global_channels[subscription_type]),
            'purchase_date': purchase_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'is_active': is_active,
            'account_number': fake.bothify(text='ACC-########'),
        }
        subscribers.append(subscriber)
    
    df = pd.DataFrame(subscribers)
    df.to_csv('data/subscribers.csv', index=False)
    print(f"Generated {num_subscribers} subscribers")
    print(f"Active subscriptions: {df['is_active'].sum()}")
    print(f"Expired subscriptions: {(~df['is_active']).sum()}")
    print("\nSample data:")
    print(df.head())
    return df

if __name__ == "__main__":
    generate_subscribers(100)