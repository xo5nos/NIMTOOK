import csv

from fastapi import FastAPI
from sqlalchemy import create_engine, select, String, Integer, Float, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

app = FastAPI()

# baza danych sqlite zapisywana w pliku movies.db
engine = create_engine("sqlite:///movies.db")


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String)
    genres: Mapped[str] = mapped_column(String)


class Link(Base):
    __tablename__ = "links"

    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), primary_key=True)
    # imdb_id i tmdb_id jako tekst, bo imdb ma zera na początku a tmdb czasem jest puste
    imdb_id: Mapped[str] = mapped_column(String)
    tmdb_id: Mapped[str] = mapped_column(String)


class Rating(Base):
    __tablename__ = "ratings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    rating: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[int] = mapped_column(Integer)


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))
    tag: Mapped[str] = mapped_column(String)
    timestamp: Mapped[int] = mapped_column(Integer)


# tworzy tabele w bazie jeśli jeszcze ich nie ma
Base.metadata.create_all(engine)


# wczytuje dane z plików csv do bazy, ale tylko jak baza jest jeszcze pusta
def load_data():
    with Session(engine) as session:
        if session.scalars(select(Movie)).first() is not None:
            print("Dane są już w bazie, nie wczytuję ich drugi raz")
            return

        with open("movies.csv", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                session.add(Movie(id=int(row["movieId"]), title=row["title"], genres=row["genres"]))

        with open("links.csv", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                session.add(Link(movie_id=int(row["movieId"]), imdb_id=row["imdbId"], tmdb_id=row["tmdbId"]))

        with open("ratings.csv", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                session.add(Rating(user_id=int(row["userId"]), movie_id=int(row["movieId"]), rating=float(row["rating"]), timestamp=int(row["timestamp"])))

        with open("tags.csv", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                session.add(Tag(user_id=int(row["userId"]), movie_id=int(row["movieId"]), tag=row["tag"], timestamp=int(row["timestamp"])))

        session.commit()
        print("Załadowano dane z plików csv do bazy")


load_data()


@app.get("/")
def root():
    return {"hello": "world"}


@app.get("/movies")
def read_all_movies():
    result = []
    with Session(engine) as session:
        movies = session.scalars(select(Movie)).all()
        for movie in movies:
            result.append({"id": movie.id, "title": movie.title, "genres": movie.genres})
    return result


@app.get("/links")
def read_all_links():
    result = []
    with Session(engine) as session:
        links = session.scalars(select(Link)).all()
        for link in links:
            result.append({"movie_id": link.movie_id, "imdb_id": link.imdb_id, "tmdb_id": link.tmdb_id})
    return result


@app.get("/ratings")
def read_all_ratings():
    result = []
    with Session(engine) as session:
        ratings = session.scalars(select(Rating)).all()
        for rating in ratings:
            result.append({"user_id": rating.user_id, "movie_id": rating.movie_id, "rating": rating.rating, "timestamp": rating.timestamp})
    return result


@app.get("/tags")
def read_all_tags():
    result = []
    with Session(engine) as session:
        tags = session.scalars(select(Tag)).all()
        for tag in tags:
            result.append({"user_id": tag.user_id, "movie_id": tag.movie_id, "tag": tag.tag, "timestamp": tag.timestamp})
    return result
