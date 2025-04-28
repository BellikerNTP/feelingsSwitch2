import praw
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Configurar la conexión a la API de Reddit
reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por RedSofi; propósito: extraer datos del subreddit NintendoSwitch2)"
)

# Conectar a MongoDB
uri = "mongodb+srv://admin1:RvIOEjPqjEfNUMtM@cluster0.9byophz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

analyzer = SentimentIntensityAnalyzer()

# Seleccionar la base de datos y la colección
db = client['reddit_data']  # Nombre de la base de datos
collection = db['nintendo_switch_comments']  # Nombre de la colección

# Acceder al subreddit (por ejemplo, NintendoSwitch2)
subreddit = reddit.subreddit("NintendoSwitch2")
contador = 0 
for post in subreddit.new(limit=100):  # Cambia 'new' por 'hot' o 'top' si lo prefieres
     if contador >= 5:
            break  # Salir del bucle si se han procesado 5 publicaciones   
     if "price" in post.title.lower() or "buy" in post.title.lower():

        contador=contador+1      
              
        print(f"Título de la publicación: {post.title}")  

        post.comments.replace_more(limit=5)
        comments = []
        for comment in post.comments.list():
           # print(f"Comentario: {comment.body}")
           # print(f"Autor: {comment.author}")
           # print(f"Score: {comment.score}")
           # print("-" * 50)
           sentiment_scores = analyzer.polarity_scores(comment.body)
           sentiment = sentiment_scores['compound']  # Valor entre -1 y 1

            # Agregar cada comentario al arreglo
        comments.append({
                'comment_body': comment.body,
                'comment_author': str(comment.author) if comment.author else "N/A",
                'comment_score': comment.score,
                'sentiment': sentiment  # Agregar el sentimiento al comentario
            })

        # Crear un documento para el post con sus comentarios
        post_data = {
            'post_title': post.title,
            'post_author': str(post.author) if post.author else "N/A",
            'post_url': post.url,
            'post_score': post.score,
            'comments': comments
        }

        # Insertar el documento del post en la colección
        collection.insert_one(post_data)
        

print("Datos guardados en MongoDB.")