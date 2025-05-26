import praw
import os
from dotenv import load_dotenv
from transformers import pipeline

# load environment variables from .env
load_dotenv()
client_id = os.getenv('REDDIT_CLIENT_ID')
client_secret = os.getenv('REDDIT_CLIENT_SECRET')
user_agent = os.getenv('REDDIT_USER_AGENT')
# check for all env vars
if not all([client_id, client_secret, user_agent]):
    raise EnvironmentError("Please set REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT in .env. See README for more information.")


# setup read-only reddit client
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)


# create a summarization model
# facebook/bart-large-cnn is the top HuggingFace summarization model
# max input length of 1024 tokens
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


# get top comments from hot posts in a given subreddit
# returns a list of tuples of post titles and lists of the top comments on each post
def get_post_comments(subreddit_name='AskReddit', post_limit=1, comment_limit=25):
    subreddit = reddit.subreddit(subreddit_name)
    # loop through posts in the given subreddit
    comments = []
    for post in subreddit.hot(limit=post_limit):
        # replace the MoreComments instances in the CommentForest with the actual comments
        # limit the number of API calls based on the number of comments we want - estimate as comment_limit/10 replacements
        post.comments.replace_more(limit=int(comment_limit/10))
        # filter out any pinned comments
        top_comments = [comment.body for comment in post.comments[:comment_limit] if not comment.stickied]
        # store a tuple of the post title and a list of the top comments on that post
        comments.append((post.title, top_comments))
    return comments

# combines and summarizes a list of strings
def summarize_comments(comments_list, max_words=512, min_output=25, max_output=100):
    # first, summarize long comments individually
    # allow each comment up to an equal portion of the max words
    max_words_per_comment = max_words // len(comments_list)
    comments_list_summarized = []
    for comment in comments_list:
        # if the comment is shorter than allowed, don't modify it
        if len(comment.split()) <= max_words_per_comment:
            comments_list_summarized.append(comment)
        # if the comment is longer than allowed, summarize it
        else:
            comment_summary = summarizer(comment, min_length=max_words_per_comment//2, max_length=max_words_per_comment)
            comments_list_summarized.append(comment_summary[0]['summary_text'])

    # combine comments into one string
    text = "\n".join(comments_list_summarized)
    # summarize all comments together
    summary = summarizer(text, min_length=min_output, max_length=max_output)
    return summary[0]['summary_text']



if __name__ == "__main__":
    subreddit_name = 'r/ChangeMyView'
    comment_limit = 10
    posts = get_post_comments(subreddit_name=subreddit_name, post_limit=2, comment_limit=comment_limit)
    print(f"Posts from r/{subreddit_name}:")
    for title, comments in posts:
        print(f"{title}\nSummary of the top {comment_limit} comments:")
        print(summarize_comments(comments))
        print()
