import pytest
from fastapi.testclient import TestClient

from lab4 import app, movies, links, ratings, tags

client = TestClient(app)


# ---------- fixtury ----------
# Każda fixtura czyści dane w pamięci i wstawia znane dane testowe,
# dzięki czemu każdy test zaczyna od tego samego stanu.

@pytest.fixture
def sample_movies():
    data = {
        1: {"id": 1, "title": "Toy Story (1995)", "genres": "Adventure|Animation|Children|Comedy|Fantasy"},
    }
    movies.clear()
    movies.update(data)
    return data


@pytest.fixture
def sample_links():
    data = {
        1: {"id": 1, "movie_id": 1, "imdb_id": "0114709", "tmdb_id": 862},
    }
    links.clear()
    links.update(data)
    return data


@pytest.fixture
def sample_ratings():
    data = {
        1: {"id": 1, "user_id": 1, "movie_id": 1, "rating": 4.0, "timestamp": 964982703},
    }
    ratings.clear()
    ratings.update(data)
    return data


@pytest.fixture
def sample_tags():
    data = {
        1: {"id": 1, "user_id": 336, "movie_id": 1, "tag": "pixar", "timestamp": 1139045764},
    }
    tags.clear()
    tags.update(data)
    return data


# ---------- movies ----------

def test_get_movies(sample_movies):
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_movies)  # tyle, ile jest w fixturze
    assert response.json() == list(sample_movies.values())


def test_get_movie(sample_movies):
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json() == sample_movies[1]

    response = client.get("/movies/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}


def test_create_movie(sample_movies):
    new_movie = {"title": "Heat (1995)", "genres": "Action|Crime|Thriller"}
    response = client.post("/movies", json=new_movie)
    assert response.status_code == 201
    assert response.json() == {"id": 2, **new_movie}
    assert len(movies) == len(sample_movies) + 1
    assert movies[2] == response.json()

    response = client.post("/movies", json={"genres": "Drama"})  # brak tytułu
    assert response.status_code == 422
    assert len(movies) == len(sample_movies) + 1


def test_update_movie(sample_movies):
    changes = {"title": "Toy Story 2 (1999)", "genres": "Animation"}
    response = client.put("/movies/1", json=changes)
    assert response.status_code == 200
    assert response.json() == {"id": 1, **changes}
    assert movies[1] == response.json()
    assert len(movies) == len(sample_movies)

    response = client.put("/movies/999", json=changes)
    assert response.status_code == 404
    assert 999 not in movies


def test_delete_movie(sample_movies):
    response = client.delete("/movies/1")
    assert response.status_code == 204
    assert 1 not in movies
    assert len(movies) == len(sample_movies) - 1
    assert client.get("/movies/1").status_code == 404

    response = client.delete("/movies/1")
    assert response.status_code == 404


# ---------- links ----------

def test_get_links(sample_links):
    response = client.get("/links")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_links)
    assert response.json() == list(sample_links.values())


def test_get_link(sample_links):
    response = client.get("/links/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json() == sample_links[1]

    response = client.get("/links/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Link not found"}


def test_create_link(sample_links):
    new_link = {"movie_id": 2, "imdb_id": "0113497", "tmdb_id": 8844}
    response = client.post("/links", json=new_link)
    assert response.status_code == 201
    assert response.json() == {"id": 2, **new_link}
    assert len(links) == len(sample_links) + 1
    assert links[2] == response.json()

    response = client.post("/links", json={"movie_id": 3, "tmdb_id": 15602})  # brak imdb_id
    assert response.status_code == 422
    assert len(links) == len(sample_links) + 1


def test_update_link(sample_links):
    changes = {"movie_id": 1, "imdb_id": "0999999", "tmdb_id": 12345}
    response = client.put("/links/1", json=changes)
    assert response.status_code == 200
    assert response.json() == {"id": 1, **changes}
    assert links[1] == response.json()
    assert len(links) == len(sample_links)

    response = client.put("/links/999", json=changes)
    assert response.status_code == 404
    assert 999 not in links


def test_delete_link(sample_links):
    response = client.delete("/links/1")
    assert response.status_code == 204
    assert 1 not in links
    assert len(links) == len(sample_links) - 1
    assert client.get("/links/1").status_code == 404

    response = client.delete("/links/1")
    assert response.status_code == 404


# ---------- ratings ----------

def test_get_ratings(sample_ratings):
    response = client.get("/ratings")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_ratings)
    assert response.json() == list(sample_ratings.values())


def test_get_rating(sample_ratings):
    response = client.get("/ratings/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json() == sample_ratings[1]

    response = client.get("/ratings/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Rating not found"}


def test_create_rating(sample_ratings):
    new_rating = {"user_id": 10, "movie_id": 2, "rating": 5.0, "timestamp": 1700000000}
    response = client.post("/ratings", json=new_rating)
    assert response.status_code == 201
    assert response.json() == {"id": 2, **new_rating}
    assert len(ratings) == len(sample_ratings) + 1
    assert ratings[2] == response.json()

    response = client.post("/ratings", json={**new_rating, "rating": 7})  # ocena spoza 0.5 - 5.0
    assert response.status_code == 422
    assert len(ratings) == len(sample_ratings) + 1


def test_update_rating(sample_ratings):
    changes = {"user_id": 1, "movie_id": 1, "rating": 2.5, "timestamp": 1700000000}
    response = client.put("/ratings/1", json=changes)
    assert response.status_code == 200
    assert response.json() == {"id": 1, **changes}
    assert ratings[1] == response.json()
    assert len(ratings) == len(sample_ratings)

    response = client.put("/ratings/999", json=changes)
    assert response.status_code == 404
    assert 999 not in ratings


def test_delete_rating(sample_ratings):
    response = client.delete("/ratings/1")
    assert response.status_code == 204
    assert 1 not in ratings
    assert len(ratings) == len(sample_ratings) - 1
    assert client.get("/ratings/1").status_code == 404

    response = client.delete("/ratings/1")
    assert response.status_code == 404


# ---------- tags ----------

def test_get_tags(sample_tags):
    response = client.get("/tags")
    assert response.status_code == 200
    assert len(response.json()) == len(sample_tags)
    assert response.json() == list(sample_tags.values())


def test_get_tag(sample_tags):
    response = client.get("/tags/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json() == sample_tags[1]

    response = client.get("/tags/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tag not found"}


def test_create_tag(sample_tags):
    new_tag = {"user_id": 2, "movie_id": 3, "tag": "funny", "timestamp": 1445714994}
    response = client.post("/tags", json=new_tag)
    assert response.status_code == 201
    assert response.json() == {"id": 2, **new_tag}
    assert len(tags) == len(sample_tags) + 1
    assert tags[2] == response.json()

    response = client.post("/tags", json={"user_id": 2, "movie_id": 3, "timestamp": 1})  # brak tagu
    assert response.status_code == 422
    assert len(tags) == len(sample_tags) + 1


def test_update_tag(sample_tags):
    changes = {"user_id": 336, "movie_id": 1, "tag": "animation", "timestamp": 1700000000}
    response = client.put("/tags/1", json=changes)
    assert response.status_code == 200
    assert response.json() == {"id": 1, **changes}
    assert tags[1] == response.json()
    assert len(tags) == len(sample_tags)

    response = client.put("/tags/999", json=changes)
    assert response.status_code == 404
    assert 999 not in tags


def test_delete_tag(sample_tags):
    response = client.delete("/tags/1")
    assert response.status_code == 204
    assert 1 not in tags
    assert len(tags) == len(sample_tags) - 1
    assert client.get("/tags/1").status_code == 404

    response = client.delete("/tags/1")
    assert response.status_code == 404
