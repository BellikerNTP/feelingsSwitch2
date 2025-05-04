import praw
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por RedSofi; propósito: extraer datos del subreddit NintendoSwitch2)"
)

uri = "mongodb+srv://admin2:umTgpNwNGHk35Fb@cluster0.mbb6vij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

analyzer = SentimentIntensityAnalyzer()
keywords = ["switch 2 price", "pricey", "expensive", "new games prices","cheap"]
def get_all_comments(comment):
    sentiment = analyzer.polarity_scores(comment.body)
    comment_data = {
        'comentario': comment.body,
        'autor': str(comment.author) if comment.author else "N/A",
        'puntuacion': comment.score,
        'sentimiento': sentiment
    }
    replies = []
    for reply in comment.replies:
        replies.append(get_all_comments(reply))
    comment_data['respuestas'] = replies
    return comment_data

try:
    db = client['reddit_data']  # Nombre de la base de datos
    collection = db['nintendo_switch_posts']  # Nombre de la colección

    subreddit = reddit.subreddit("NintendoSwitch2")
    qntPosts = 1000  # Número de publicaciones a buscar
    cnt = 0  # Contador de publicaciones encontradas

    for post in subreddit.hot(limit=qntPosts):  # Cambia 'new' por 'hot' o 'top' si lo prefieres
        # Verificar si el título contiene alguna palabra clave
        if any(keyword.lower() in post.title.lower() for keyword in keywords):
            
            cnt += 1
            post.comments.replace_more(limit=0)
            comments = []
            for comment in post.comments.list():
                comments.append(get_all_comments(comment))  # Llamar a la función recursiva

            # Crear un documento para el post con sus comentarios
            post_data = {
                'titulo': post.title,
                'autor': str(post.author) if post.author else "N/A",
                'url': post.url,
                'puntuacion': post.score,
                'comentarios': comments
            }

            # Insertar el documento del post en la colección
            collection.insert_one(post_data)
        

    print("Datos guardados en MongoDB.")

except Exception as e:
    print("Error al conectar a MongoDB:", e)

