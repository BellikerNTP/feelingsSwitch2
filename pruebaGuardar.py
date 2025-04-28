import praw
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por RedSofi; propósito: extraer datos del subreddit NintendoSwitch2)"
)

uri = "mongodb+srv://admin2:6KGOOvnArpdZbnKt@cluster0.9byophz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

analyzer = SentimentIntensityAnalyzer()

def get_all_comments(comment):
    sentiment = analyzer.polarity_scores(comment.body)
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
    qntPosts = 200  # Número de publicaciones a buscar
    cnt = 0  # Contador de publicaciones encontradas

    for post in subreddit.hot(limit=qntPosts):  # Cambia 'new' por 'hot' o 'top' si lo prefieres
        if "price" in post.title.lower() or "buy" in post.title.lower():  # Convertir a minúsculas para evitar errores
            cnt += 1
            
            post.comments.replace_more(limit=0)
            comments = []
            for comment in post.comments.list():
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
            collection.insert_one(post_data)
        if cnt > 10:  # Limitar a 10 publicaciones para pruebas
            break

    print("Datos guardados en MongoDB.")

except Exception as e:
    print("Error al conectar a MongoDB:", e)

