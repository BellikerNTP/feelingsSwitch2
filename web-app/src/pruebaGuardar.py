import praw
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from transformers import pipeline
import sys
from datetime import datetime

reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por RedSofi; propósito: extraer datos del subreddit NintendoSwitch2)"
)

uri = "mongodb+srv://adminIker:0ILhP1Eof9vBsFYs@cluster0.mbb6vij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

sentiment_analyzer = pipeline("sentiment-analysis")

keywords = ["price", "buy", "purchase", "cost", "deal", "offer", "discount", "sale", "value", "expensive", "cheap", "affordable", "bargain", "spend", "invest", "money", "currency", "transaction", "shop", "retail", "market", "$", "switch 2 price", "pricey", "expensive", "new games prices", "cheap","costly","worth it","worth","price tag","price point","price range","price drop","price increase","price comparison","price analysis"]

def get_all_comments(comment):
    sentiment = sentiment_analyzer(comment.body[:512])[0]
    comment_data = {
        'comment_body': comment.body,
        'comment_author': str(comment.author) if comment.author else "N/A",
        'comment_score': comment.score,
        'comment_date': datetime.utcfromtimestamp(comment.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
        'sentiment': sentiment
    }
    replies = []
    for reply in comment.replies:
        replies.append(get_all_comments(reply))
    comment_data['replies'] = replies
    return comment_data

try:
    db = client['reddit_data_Iker']
    collection = db['nintendo_switch_posts']

    subreddit = reddit.subreddit("NintendoSwitch2")

    qntPosts = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    cntMax = int(sys.argv[2]) if len(sys.argv) > 2 else 100
    startDate = sys.argv[3] if len(sys.argv) > 3 else None
    endDate = sys.argv[4] if len(sys.argv) > 4 else None

    start_timestamp = int(datetime.strptime(startDate, '%Y-%m-%d').timestamp()) if startDate else None
    end_timestamp = int(datetime.strptime(endDate, '%Y-%m-%d').timestamp()) if endDate else None

    cnt = 0

    for post in subreddit.hot(limit=qntPosts):
        if start_timestamp and post.created_utc < start_timestamp:
            continue
        if end_timestamp and post.created_utc > end_timestamp:
            continue

        if any(keyword in post.title.lower() for keyword in keywords):
            cnt += 1
            if cnt > cntMax:
                break
            
            post.comments.replace_more(limit=0)
            comments = []
            for comment in post.comments.list():
                if any(keyword in comment.body.lower() for keyword in keywords):
                    comments.append(get_all_comments(comment))

            post_data = {
                'post_title': post.title,
                'post_author': str(post.author) if post.author else "N/A",
                'post_url': post.url,
                'post_score': post.score,
                'post_date': datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
                'comments': comments
            }
            
            collection.insert_one(post_data)

    print("Datos guardados en MongoDB.")

except Exception as e:
    print("Error al conectar a MongoDB:", e)