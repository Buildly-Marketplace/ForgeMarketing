import requests
import random
import time
import json
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from config.config_loader import config_loader

def get_twitter_headers(brand_name='buildly'):
    """Get Twitter API headers with credentials from database"""
    creds = config_loader.get_twitter_credentials(brand_name)
    bearer_token = creds.get('bearer_token', '')
    
    if not bearer_token:
        raise ValueError(
            f"Twitter bearer token not configured for {brand_name}. "
            "Please configure via admin panel at http://localhost:8002/admin"
        )
    
    return {
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json',
    }

# Get headers from secure configuration
headers = get_twitter_headers()

# Function to create a tweet
def create_tweet(text):
    url = 'https://api.twitter.com/2/tweets'
    payload = {
        'text': text
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Define the ad variations
ads = [
    "Elevate Your Software Development with #Buildly Insights & Our Partner Marketplace 🚀 Join our private beta today! https://insights.buildly.io",
    "Transform your development journey with #Buildly - AI-driven project management & expert development community. Discover more https://insights.buildly.io",
    "#BuildlyMarketplace connects you to expert agencies for efficient software solutions. Explore our Bounty Hunter feature! https://insights.buildly.io",
    "Streamline your software projects with #Buildly Insights and access quick fixes through our Partner Marketplace. Join now! https://insights.buildly.io",
    "Innovate with #Buildly's AI-Based Idea Translation & Product Roadmaps. Connect with experts on our marketplace. https://insights.buildly.io",
    # Additional ad variations go here
    "Discover how #Buildly's cloud-based solutions can accelerate your startup's growth. Explore our features today! https://insights.buildly.io",
    "Maximize productivity with #Buildly Insights. AI-powered project management for modern teams. Learn more https://insights.buildly.io",
    "Join the #Buildly revolution! Seamless project management and a vibrant expert community await. https://insights.buildly.io",
    "Revolutionize your software development with #Buildly. Cutting-edge tools for startups and enterprises. https://insights.buildly.io",
    "Efficiency meets innovation with #Buildly. Dive into our AI-driven platform and marketplace today! https://insights.buildly.io"
]

# Function to post tweets
def post_tweet():
    ad = random.choice(ads)
    try:
        response = create_tweet(ad)
        print(f"Tweet posted successfully: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Loop to post tweets every hour
for _ in range(200):
    post_tweet()
    time.sleep(3600)  # Wait for 1 hour

