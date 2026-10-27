import csv

from fastapi import FastAPI

app = FastAPI()


class Movie:
    def __init__(self, id, title, genres):
        self.id = id
        self.title = title
        self.genres = genres


class Link:
    def __init__(self, movie_id, imdb_id, tmdb_id):
        self.movie_id = movie_id
        self.imdb_id = imdb_id
        self.tmdb_id = tmdb_id


class Rating:
    def __init__(self, user_id, movie_id, rating, timestamp):
        self.user_id = user_id
        self.movie_id = movie_id
        self.rating = rating
        self.timestamp = timestamp


class Tag:
    def __init__(self, user_id, movie_id, tag, timestamp):
        self.user_id = user_id
        self.movie_id = movie_id
        self.tag = tag
        self.timestamp = timestamp


# dane wczytane z plików csv i trzymane w pamięci zamiast w bazie danych
movies = []
with open("movies.csv", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        movies.append(Movie(int(row["movieId"]), row["title"], row["genres"]))

links = []
with open("links.csv", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        links.append(Link(int(row["movieId"]), row["imdbId"], row["tmdbId"]))

ratings = []
with open("ratings.csv", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        ratings.append(Rating(int(row["userId"]), int(row["movieId"]), float(row["rating"]), int(row["timestamp"])))

tags = []
with open("tags.csv", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        tags.append(Tag(int(row["userId"]), int(row["movieId"]), row["tag"], int(row["timestamp"])))


@app.get("/")
async def root():
    return {"hello": "world"}


@app.get("/movies")
async def read_all_movies():
    result = []
    for movie in movies:
        result.append(movie.__dict__)
    return result


@app.get("/links")
async def read_all_links():
    result = []
    for link in links:
        result.append(link.__dict__)
    return result


@app.get("/ratings")
async def read_all_ratings():
    result = []
    for rating in ratings:
        result.append(rating.__dict__)
    return result


@app.get("/tags")
async def read_all_tags():
    result = []
    for tag in tags:
        result.append(tag.__dict__)
    return result
