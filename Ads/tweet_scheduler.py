import requests
from requests_oauthlib import OAuth1Session
import webbrowser
import random
import time
import os

# Twitter credentials - set via environment variables
consumer_key = os.environ.get('TWITTER_CONSUMER_KEY', '')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET', '')
bearer_token = os.environ.get('TWITTER_BEARER_TOKEN', '')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN', '')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')

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

# Initialize OAuth
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)
fetch_response = oauth.fetch_request_token("https://api.twitter.com/oauth/request_token")
resource_owner_key = fetch_response.get('oauth_token')
resource_owner_secret = fetch_response.get('oauth_token_secret')

# Authorization
full_authorize_url = oauth.authorization_url("https://api.twitter.com/oauth/authorize")
webbrowser.open(full_authorize_url)
verifier = input('Please enter the PIN: ')

# Obtain Access Token
oauth = OAuth1Session(consumer_key,
                      client_secret=consumer_secret,
                      resource_owner_key=resource_owner_key,
                      resource_owner_secret=resource_owner_secret,
                      verifier=verifier)
oauth_tokens = oauth.fetch_access_token("https://api.twitter.com/oauth/access_token")

access_token = oauth_tokens['oauth_token']
access_token_secret = oauth_tokens['oauth_token_secret']

# Function to post tweets
def post_tweet(oauth_session, text):
    response = oauth_session.post("https://api.twitter.com/2/tweets", json={"text": text})
    if response.status_code == 201:
        print("Tweet posted successfully!")
    else:
        print("Failed to post tweet:", response.content)

# Post tweets every hour
oauth = OAuth1Session(consumer_key,
                      client_secret=consumer_secret,
                      resource_owner_key=access_token,
                      resource_owner_secret=access_token_secret)

for i in range(1000):
    post_tweet(oauth, random.choice(ads))
    time.sleep(3600)  # Wait for 1 hour
