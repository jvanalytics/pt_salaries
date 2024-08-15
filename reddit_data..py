import praw
import pandas as pd
import json

try:
    with open('auth.json', 'r') as f:
        # Load the JSON data from the file
        credentials = json.load(f)
except FileNotFoundError:
    print("Error: auth.json file not found!")


reddit = praw.Reddit(
    client_id=credentials['client_id']
    client_secret="YOUR_SECRET_KEY",
    password="<PASSWORD>",
    user_agent="<user-agent>",
    username="YOUR_USERNAME"
)
subreddit = reddit.subreddit("<<PTOrdenado>>")


def post_parser(subreddit, posts):
    """Get posts from a subreddit"""
    for post in subreddit.hot(limit=posts):
        user_data = {
            'user': post.author._path,
            'title': post.title,
            'content': post.selftext}
        yield user_data


def to_df(subreddit, limit):
    """Store posts in a dataframe"""
    df = pd.DataFrame(list(post_parser(subreddit, limit)))
    return df
