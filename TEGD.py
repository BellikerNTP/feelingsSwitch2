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
# Crear y abrir el archivo CSV
with open("reddit_data.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Escribir el encabezado del archivo CSV
    writer.writerow(["Titulo", "Autor", "URL", "Puntaje", "Texto", "Tipo", "Autor_Comentario"])

    # Lista de palabras clave para buscar
    keywords = ["Switch 2", "price", "expensive", "New games"]

    # Filtrar publicaciones recientes y buscar comentarios
    for post in subreddit.new(limit=10):  # Cambia 'new' por 'hot' o 'top' si lo prefieres
        # Verificar si el título contiene alguna palabra clave
        if any(keyword.lower() in post.title.lower() for keyword in keywords):
            print(f"Titulo: {post.title}")
            writer.writerow([post.title, post.author, post.url, post.score, post.title, "Publicacion", "N/A"])

        # Obtener comentarios de la publicación
        post.comments.replace_more(limit=0)  # Expandir comentarios anidados
        for comment in post.comments.list():
            if any(keyword.lower() in comment.body.lower() for keyword in keywords):
                print(f"Comentario: {comment.body}")
                writer.writerow([post.title, post.author, post.url, post.score, comment.body, "Comentario", comment.author])
