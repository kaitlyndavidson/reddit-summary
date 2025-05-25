import praw
import os
from dotenv import load_dotenv

# load environment variables from .env
load_dotenv()

# setup read-only reddit client
reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent=os.getenv('REDDIT_USER_AGENT')
)

if __name__ == "__main__":
    # test - print the titles of the 5 hottest submissions in r/AskReddit
    subreddit = reddit.subreddit("AskReddit")
    for submission in subreddit.hot(limit = 5):
        print(submission.title)