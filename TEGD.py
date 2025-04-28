import praw

# Configurar la conexión a la API de Reddit
reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por RedSofi; propósito: extraer datos del subreddit NintendoSwitch2)"
)

# Acceder al subreddit (por ejemplo, NintendoSwitch2)
subreddit = reddit.subreddit("NintendoSwitch2")

# Filtrar publicaciones recientes y buscar comentarios
for post in subreddit.new(limit=10):  # Cambia 'new' por 'hot' o 'top' si lo prefieres
    print(f"Título de la publicación: {post.title}")
    
    # Obtener comentarios de la publicación
    post.comments.replace_more(limit=0)  # Para manejar comentarios anidados
    for comment in post.comments.list():
        if "precio" in comment.body.lower():  # Convertir a minúsculas para evitar errores
            print(f"Comentario: {comment.body}")
            print(f"Autor: {comment.author}")
            print(f"Score: {comment.score}")
            print("-" * 50)