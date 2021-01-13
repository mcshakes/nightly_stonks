# import valid_tickers as valid
import numpy as np
import pandas as pd
import datetime as dt
import praw
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os
from dotenv import load_dotenv
load_dotenv()


reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                     client_secret=os.getenv("CLIENT_SECRET"),
                     user_agent=os.getenv("USER_AGENT"))


sub_reddits = reddit.subreddit('wallstreetbets')


submission_statistics = []

tickers = ["TSLA", "PTON", "CHWY", "PLTR", "MT"]


def comment_sentiment(ticker, url):
    subComments = []
    bodyComment = []

    try:
        check = reddit.submission(url=url)
        subComments = check.comments
    except:
        return 0

    for comment in subComments:
        try:
            bodyComment.append(comment.body)
        except:
            return 0

    analyzer = SentimentIntensityAnalyzer()
    results = []

    for line in bodyComment:
        # import code
        # code.interact(local=dict(globals(), **locals()))

        scores = analyzer.polarity_scores(line)
        scores["headline"] = line
        results.append(scores)

    df = pd.DataFrame.from_records(results)
    df.head()
    df['label'] = 0

    try:
        df.loc[df['compound'] > 0.1, 'label'] = 1
        df.loc[df['compound'] < -0.1, 'label'] = -1
    except:
        return 0

    averageScore = 0
    position = 0

    while position < len(df.label)-1:
        averageScore = averageScore + df.label[position]
        position += 1

    averageScore = averageScore/len(df.label)

    return(averageScore)


def search_subreddit(stock_tickers):
    for ticker in stock_tickers:
        for submission in reddit.subreddit('wallstreetbets').search(ticker, limit=10):
            if submission.domain != "self.wallstreetbets":
                continue

            data = {}
            data['ticker'] = ticker
            data['num_comments'] = submission.num_comments

            data['comment_sentiment_average'] = comment_sentiment(
                ticker, submission.url)
            if data['comment_sentiment_average'] == 0.000000:
                continue

            data['score'] = submission.score
            data['upvote_ratio'] = submission.upvote_ratio
            data['date'] = submission.created_utc
            data['domain'] = submission.domain
            data['num_crossposts'] = submission.num_crossposts
            data['author'] = submission.author

            submission_statistics.append(data)

    dfSentimentStocks = pd.DataFrame(submission_statistics)

    dfSentimentStocks.to_csv('WSB_Sentiment_Equity.csv', index=False)


search_subreddit(tickers)
