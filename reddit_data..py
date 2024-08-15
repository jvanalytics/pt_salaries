import praw
import pandas as pd


reddit = praw.Reddit(
    client_id="YOUR_CLIENT_ID",
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
