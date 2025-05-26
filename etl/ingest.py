import praw
import os
from dotenv import load_dotenv

# setup read-only reddit client
def create_reddit_client():
    # load environment variables from .env
    load_dotenv()
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')
    # check for all env vars
    if not all([client_id, client_secret, user_agent]):
        raise EnvironmentError("Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT in .env. See README for more information.")
    # create reddit client
    return praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

# validate a subreddit name and create a subreddit object
def access_subreddit(reddit_client, subreddit_name):
    try:
        subreddit = reddit_client.subreddit(subreddit_name)
        # accessing `.id` forces a request
        subreddit.id
        return subreddit
    except Exception as e:
        raise RuntimeError(f"Subreddit 'r/{subreddit_name}' is not valid.")


# get top comments from hot posts in a given subreddit
def fetch_post_data(subreddit_name='AskReddit', post_limit=1, comment_limit=25):
    reddit = create_reddit_client()
    subreddit = access_subreddit(reddit, subreddit_name)
    # loop through posts in the given subreddit
    posts_comments = []
    for post in subreddit.hot(limit=post_limit):
        # replace the MoreComments instances in the CommentForest with the actual comments
        # limit the number of API calls based on the number of comments we want - estimate as comment_limit/10 replacements
        post.comments.replace_more(limit=int(comment_limit/10))
        # filter out any pinned comments
        comments = [comment.body for comment in post.comments[:comment_limit] if not comment.stickied]
        # save the post title, post body, a list of the top comments on that post, and the post ID
        posts_comments.append({
            'title': post.title,
            'body': post.selftext,
            'comments': comments,
            'post_id': post.id
        })
    return posts_comments
