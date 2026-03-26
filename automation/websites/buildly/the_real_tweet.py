from requests_oauthlib import OAuth1Session
import webbrowser
import os
import json
import random
import time


# In your terminal please set your environment variables by running the following lines of code.
# export 'CONSUMER_KEY'='<your_consumer_key>'
# export 'CONSUMER_SECRET'='<your_consumer_secret>'

consumer_key = os.environ.get('TWITTER_CONSUMER_KEY', '')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET', '')


# Be sure to add replace the text of the with the text you wish to Tweet. You can also add parameters to post polls, quote Tweets, Tweet with reply settings, and Tweet to Super Followers in addition to other features.
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

# Get request token
request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

try:
    fetch_response = oauth.fetch_request_token(request_token_url)
except ValueError:
    print(
        "There may have been an issue with the consumer_key or consumer_secret you entered."
    )

resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")
print("Got OAuth token: %s" % resource_owner_key)

# Get authorization
base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
webbrowser.open(authorization_url)
verifier = input("Paste the PIN here: ")

# Get the access token
access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

# Make the request
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

# Make the request with OAuth session and tweet text
def post_tweet(oauth_session, text):
    response = oauth_session.post("https://api.twitter.com/2/tweets", json={"text": text})
    if response.status_code != 201:
        raise Exception(f"Request returned an error: {response.status_code} {response.text}")
    print("Tweet posted successfully!")

# Post tweets every hour, up to 1000 times
for _ in range(1000):
    ad = random.choice(ads)
    post_tweet(oauth, ad)
    time.sleep(3600)  # Wait for 1 hour