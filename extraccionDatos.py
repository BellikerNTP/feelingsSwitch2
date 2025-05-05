import praw
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configurar la conexión a Reddit
reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por el equipo 5 de TEGD; propósito: extraer datos del subreddit NintendoSwitch2)"
)

# Configurar la conexión a MongoDB Atlas
uri = "mongodb+srv://admin2:umTgpNwNGHk35Fb@cluster0.mbb6vij.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))

# Inicializar el analizador de sentimientos
analyzer = SentimentIntensityAnalyzer()

# Palabras clave para buscar
keywords = ["switch 2 price", "pricey", "expensive", "new games prices", "cheap"]

# Función para analizar los comentarios
def get_all_comments(comment):
    sentiment = analyzer.polarity_scores(comment.body)
    comment_data = {
        'comentario': comment.body,
        'autor': str(comment.author) if comment.author else "N/A",
        'puntuacion': comment.score,
        'sentimiento': sentiment
    }
    return comment_data

try:
    # Configurar base de datos y colección en MongoDB
    db = client['Victor']
    collection = db['Base_Prueba']

    # Acceder al subreddit
    subreddit = reddit.subreddit("NintendoSwitch2")
    qntPosts = 100  # Número de publicaciones a buscar
    cnt = 0  # Contador de publicaciones que cumplen el criterio

    for post in subreddit.hot(limit=qntPosts):  # Cambia 'hot' por 'new' o 'top' si lo prefieres
        post.comments.replace_more(limit=0)  # Expandir comentarios anidados
        comments = post.comments.list()

        # Filtrar comentarios que contienen palabras clave
        matching_comments = [comment for comment in comments if any(keyword.lower() in comment.body.lower() for keyword in keywords)]
        match_percentage = len(matching_comments) / len(comments) if comments else 0

        # Condición: 15% de los comentarios o el título contiene palabras clave
        if any(keyword.lower() in post.title.lower() for keyword in keywords) or match_percentage >= 0.15:
            cnt += 1
            processed_comments = [get_all_comments(comment) for comment in comments]  # Analizar todos los comentarios
            post_data = {
                'titulo': post.title,
                'autor': str(post.author) if post.author else "N/A",
                'url': post.url,
                'puntuacion': post.score,
                'comentarios': processed_comments,
                'porcentaje_match': match_percentage  # Agregar el porcentaje de coincidencias
            }

            collection.insert_one(post_data)  # Guardar en la base de datos

    print(f"Se guardaron {cnt} publicaciones en MongoDB.")

except Exception as e:
    print("Error al conectar a MongoDB:", e)