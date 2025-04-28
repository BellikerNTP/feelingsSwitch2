import praw
import csv

# Configurar la conexión a la API de Reddit
reddit = praw.Reddit(
    client_id="vel1HuEjohqoEGEQDgutyQ",
    client_secret="s1cTjaqVaiwnpqvju1MsXRs070GufA",
    user_agent="TEGD/1.0 (Desarrollado por RedSofi; propósito: extraer datos del subreddit NintendoSwitch2)"
)

# Acceder al subreddit (por ejemplo, NintendoSwitch2)
subreddit = reddit.subreddit("NintendoSwitch2")

# Crear y abrir el archivo CSV para guardar los datos
with open("reddit_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Escribir el encabezado del archivo CSV
    writer.writerow(["Título de la publicación", "Autor de la publicación", "URL", "Puntaje", "Comentario", "Autor del comentario"])

    # Filtrar publicaciones recientes y buscar comentarios
    for post in subreddit.new(limit=10):  # Cambia 'new' por 'hot' o 'top' si lo prefieres
        print(f"Título de la publicación: {post.title}")

        # Manejar comentarios anidados
        post.comments.replace_more(limit=0)
        for comment in post.comments.list():
            if "price" in comment.body.lower():  # Convertir a minúsculas para evitar errores
                print(f"Comentario: {comment.body}")
                print(f"Autor: {comment.author}")
                print(f"Score: {comment.score}")
                print("-" * 50)

                # Guardar en el CSV
                writer.writerow([post.title, post.author, post.url, post.score, comment.body, comment.author])