import praw
import pandas as pd
import json
import datetime


try:
    with open('auth.json', 'r') as f:
        credentials = json.load(f)
except FileNotFoundError:
    print("Error: auth.json file not found!")

reddit = praw.Reddit(
    client_id=credentials['client_id'],
    client_secret=credentials['client_secret'],
    password=credentials['password'],
    user_agent=credentials['user_agent'],
    username=credentials['username']
)


def post_parser(subreddit, posts):
    """Get posts from a subreddit"""
    data = []
    for post in subreddit.new(limit=posts):
        data.append({
            'title': post.title,
            'author': post.author.name if post.author else None,
            'created_utc': post.created_utc,
            'content': post.selftext
        })
    return data


limit = 10000
subreddit = reddit.subreddit('PTOrdenado')


post_data = post_parser(subreddit, limit)


# Get the current date and time
now = datetime.datetime.now()
date_str = now.strftime('%Y-%m-%d_%H-%M-%S')


def to_df(data):
    """Store posts in a dataframe"""
    df = pd.json_normalize(data).replace('\n', '+++', regex=True)
    return df


def to_json(data):
    """Store posts in a JSON file"""
    with open(f'posts{date_str}.json', 'w') as f:
        json.dump(data, f)


to_json(post_data)


df = to_df(post_data)
print(df.head())
df.to_csv(f'posts{date_str}.csv', index=False, lineterminator='')
