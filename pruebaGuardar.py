import praw
from pymongo import MongoClient
from pymongo.server_api import ServerApi
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline


reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por RedSofi; propósito: extraer datos del subreddit NintendoSwitch2)"
)

uri = "mongodb+srv://adminIker:0ILhP1Eof9vBsFYs@cluster0.mbb6vij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# analyzer = SentimentIntensityAnalyzer()
sentiment_analyzer = pipeline("sentiment-analysis")

keywords = ["price", "buy", "purchase", "cost", "deal", "offer", "discount", "sale", "value", "expensive", "cheap", "affordable", "bargain", "spend", "invest", "money", "currency", "transaction", "shop", "retail", "market", "$", "switch 2 price", "pricey", "expensive", "new games prices", "cheap","costly","worth it","worth","price tag","price point","price range","price drop","price increase","price comparison","price analysis"] # Lista de palabras clave para filtrar comentarios 

def get_all_comments(comment):
    # sentiment = analyzer.polarity_scores(comment.body)
    sentiment = sentiment_analyzer(comment.body[:512])[0]  # Analizar sentimiento (máximo 512 caracteres)
    comment_data = {
        'comment_body': comment.body,
        'comment_author': str(comment.author) if comment.author else "N/A",
        'comment_score': comment.score,
        'sentiment': sentiment
    }
    replies = []
    for reply in comment.replies:
        replies.append(get_all_comments(reply))
    comment_data['replies'] = replies
    return comment_data

try:
    db = client['reddit_data_Iker']  # Nombre de la base de datos
    collection = db['nintendo_switch_posts']  # Nombre de la colección

    subreddit = reddit.subreddit("NintendoSwitch2")

    qntPosts = 10000  # Número de publicaciones a buscar
    cnt = 0  # Contador de publicaciones encontradas
    cntMax = 500  # Número máximo de publicaciones a guardar

    for post in subreddit.hot(limit=qntPosts):  # Cambia 'new' por 'hot' o 'top' si lo prefieres
        if any(keyword in post.title.lower() for keyword in keywords):  # Verificar si alguna palabra clave está en el título
            # cnt += 1
            
            post.comments.replace_more(limit=0)
            comments = []
            for comment in post.comments.list():
                if any(keyword in comment.body.lower() for keyword in keywords):
                    comments.append(get_all_comments(comment))  # Llamar a la función recursiva

            # Crear un documento para el post con sus comentarios
            post_data = {
                'post_title': post.title,
                'post_author': str(post.author) if post.author else "N/A",
                'post_url': post.url,
                'post_score': post.score,
                'comments': comments
            }
            
            # Insertar el documento del post en la colección
            if len(post.comments) > 10:
                collection.insert_one(post_data)
        # if cnt > cntMax:  # Limitar a 10 publicaciones para pruebas
        #     break

    print("Datos guardados en MongoDB.")

except Exception as e:
    print("Error al conectar a MongoDB:", e)

