import praw
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from transformers import pipeline
import torch

# Configuración inicial
device = "cuda" if torch.cuda.is_available() else "cpu"
sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    device=deviceg
)

# Configuración de Reddit
reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por RedSofi; propósito: extraer datos del subreddit NintendoSwitch2)"
)

# Conexión a MongoDB
uri = "mongodb+srv://admin2:umTgpNwNGHk35Fb@cluster0.mbb6vij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

keywords = ["switch 2 price", "pricey", "expensive", "new games prices", "cheap"]

def analyze_sentiment(text):
    try:
        # Limitar la longitud del texto para el modelo
        max_length = 512
        if len(text) > max_length:
            text = text[:max_length]
        
        result = sentiment_analyzer(text)
        return {
            'label': result[0]['label'],
            'score': result[0]['score']
        }
    except Exception as e:
        print(f"Error al analizar sentimiento: {e}")
        return {
            'label': 'NEUTRAL',
            'score': 0.0
        }

def get_all_comments(comment):
    sentiment = analyze_sentiment(comment.body)
    comment_data = {
        'comentario': comment.body,
        'autor': str(comment.author) if comment.author else "N/A",
        'puntuacion': comment.score,
        'sentimiento': sentiment  # Ahora usa el analizador de transformers
    }
    replies = []
    for reply in comment.replies:
        replies.append(get_all_comments(reply))
    comment_data['respuestas'] = replies
    return comment_data

try:
    db = client['Nii']
    collection = db['Gger']

    subreddit = reddit.subreddit("NintendoSwitch2")
    qntPosts = 300
    cnt = 0

    for post in subreddit.hot(limit=qntPosts):
        if any(keyword.lower() in post.title.lower() for keyword in keywords):
            cnt += 1
            post.comments.replace_more(limit=0)
            comments = []
            for comment in post.comments.list():
                comments.append(get_all_comments(comment))

            post_data = {
                'titulo': post.title,
                'autor': str(post.author) if post.author else "N/A",
                'url': post.url,
                'puntuacion': post.score,
                'comentarios': comments
            }

            collection.insert_one(post_data)

    print(f"Se procesaron {cnt} posts. Datos guardados en MongoDB.")

except Exception as e:
    print("Error:", e)
finally:
    client.close()