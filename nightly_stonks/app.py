# import valid_tickers as valid
import numpy as np
import pandas as pd
import datetime as dt
import praw
import nltk
import os
from dotenv import load_dotenv
load_dotenv()


reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                     client_secret=os.getenv("CLIENT_SECRET"),
                     user_agent=os.getenv("USER_AGENT"))


sub_reddits = reddit.subreddit('wallstreetbets')


submission_statistics = []

tickers = ["TSLA", "PTON", "CHWY", "PLTR"]


def search_subreddit(stock_tickers):
    for ticker in stock_tickers:
        for submission in reddit.subreddit('wallstreetbets').search(ticker, limit=130):
            if submission.domain != "self.wallstreetbets":
                continue

            data = {}
            data['ticker'] = ticker
            data['num_comments'] = submission.num_comments
            data['score'] = submission.score
            data['upvote_ratio'] = submission.upvote_ratio
            data['date'] = submission.created_utc
            data['domain'] = submission.domain
            data['num_crossposts'] = submission.num_crossposts
            data['author'] = submission.author

            submission_statistics.append(data)

    dfSentimentStocks = pd.DataFrame(submission_statistics)

    dfSentimentStocks.to_csv('Reddit_Sentiment_Equity.csv', index=False)


search_subreddit(tickers)
