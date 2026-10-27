import uvicorn
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

# dane trzymane w pamięci zamiast w bazie danych: {id: dane}
movies = {
    1: {"id": 1, "title": "Toy Story (1995)", "genres": "Adventure|Animation|Children|Comedy|Fantasy"},
}
links = {
    1: {"id": 1, "movie_id": 1, "imdb_id": "0114709", "tmdb_id": 862},
}
ratings = {
    1: {"id": 1, "user_id": 1, "movie_id": 1, "rating": 4.0, "timestamp": 964982703},
}
tags = {
    1: {"id": 1, "user_id": 336, "movie_id": 1, "tag": "pixar", "timestamp": 1139045764},
}


# ---------- movies ----------

@app.get("/movies")
async def get_movies():
    return list(movies.values())


@app.get("/movies/{movie_id}")
async def get_movie(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movies[movie_id]


@app.post("/movies", status_code=201)
async def create_movie(request: Request):
    data = await request.json()
    new_id = max(movies, default=0) + 1  # największe ID + 1
    movies[new_id] = {"id": new_id, "title": data["title"], "genres": data["genres"]}
    return movies[new_id]


@app.put("/movies/{movie_id}")
async def update_movie(movie_id: int, request: Request):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="Movie not found")
    data = await request.json()
    movies[movie_id] = {"id": movie_id, "title": data["title"], "genres": data["genres"]}
    return movies[movie_id]


@app.delete("/movies/{movie_id}", status_code=204)
async def delete_movie(movie_id: int):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="Movie not found")
    del movies[movie_id]


# ---------- links ----------

@app.get("/links")
async def get_links():
    return list(links.values())


@app.get("/links/{link_id}")
async def get_link(link_id: int):
    if link_id not in links:
        raise HTTPException(status_code=404, detail="Link not found")
    return links[link_id]


@app.post("/links", status_code=201)
async def create_link(request: Request):
    data = await request.json()
    new_id = max(links, default=0) + 1
    links[new_id] = {"id": new_id, "movie_id": data["movie_id"], "imdb_id": data["imdb_id"], "tmdb_id": data["tmdb_id"]}
    return links[new_id]


@app.put("/links/{link_id}")
async def update_link(link_id: int, request: Request):
    if link_id not in links:
        raise HTTPException(status_code=404, detail="Link not found")
    data = await request.json()
    links[link_id] = {"id": link_id, "movie_id": data["movie_id"], "imdb_id": data["imdb_id"], "tmdb_id": data["tmdb_id"]}
    return links[link_id]


@app.delete("/links/{link_id}", status_code=204)
async def delete_link(link_id: int):
    if link_id not in links:
        raise HTTPException(status_code=404, detail="Link not found")
    del links[link_id]


# ---------- ratings ----------

@app.get("/ratings")
async def get_ratings():
    return list(ratings.values())


@app.get("/ratings/{rating_id}")
async def get_rating(rating_id: int):
    if rating_id not in ratings:
        raise HTTPException(status_code=404, detail="Rating not found")
    return ratings[rating_id]


@app.post("/ratings", status_code=201)
async def create_rating(request: Request):
    data = await request.json()
    new_id = max(ratings, default=0) + 1
    ratings[new_id] = {"id": new_id, "user_id": data["user_id"], "movie_id": data["movie_id"],
                       "rating": data["rating"], "timestamp": data["timestamp"]}
    return ratings[new_id]


@app.put("/ratings/{rating_id}")
async def update_rating(rating_id: int, request: Request):
    if rating_id not in ratings:
        raise HTTPException(status_code=404, detail="Rating not found")
    data = await request.json()
    ratings[rating_id] = {"id": rating_id, "user_id": data["user_id"], "movie_id": data["movie_id"],
                          "rating": data["rating"], "timestamp": data["timestamp"]}
    return ratings[rating_id]


@app.delete("/ratings/{rating_id}", status_code=204)
async def delete_rating(rating_id: int):
    if rating_id not in ratings:
        raise HTTPException(status_code=404, detail="Rating not found")
    del ratings[rating_id]


# ---------- tags ----------

@app.get("/tags")
async def get_tags():
    return list(tags.values())


@app.get("/tags/{tag_id}")
async def get_tag(tag_id: int):
    if tag_id not in tags:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tags[tag_id]


@app.post("/tags", status_code=201)
async def create_tag(request: Request):
    data = await request.json()
    new_id = max(tags, default=0) + 1
    tags[new_id] = {"id": new_id, "user_id": data["user_id"], "movie_id": data["movie_id"],
                    "tag": data["tag"], "timestamp": data["timestamp"]}
    return tags[new_id]


@app.put("/tags/{tag_id}")
async def update_tag(tag_id: int, request: Request):
    if tag_id not in tags:
        raise HTTPException(status_code=404, detail="Tag not found")
    data = await request.json()
    tags[tag_id] = {"id": tag_id, "user_id": data["user_id"], "movie_id": data["movie_id"],
                    "tag": data["tag"], "timestamp": data["timestamp"]}
    return tags[tag_id]


@app.delete("/tags/{tag_id}", status_code=204)
async def delete_tag(tag_id: int):
    if tag_id not in tags:
        raise HTTPException(status_code=404, detail="Tag not found")
    del tags[tag_id]


def main():
    uvicorn.run(app)  # serwer pod http://127.0.0.1:8000, dokumentacja pod /docs


if __name__ == "__main__":
    main()
