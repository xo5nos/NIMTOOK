from fastapi.testclient import TestClient

from main3 import app, movies, links, ratings, tags

client = TestClient(app)


# ---------- fixtury: czyszczą dane i wstawiają 1 element testowy ----------

def fixture_movies():
    movies.clear()
    movies[1] = {"id": 1, "title": "Toy Story (1995)", "genres": "Adventure|Animation|Children|Comedy|Fantasy"}


def fixture_links():
    links.clear()
    links[1] = {"id": 1, "movie_id": 1, "imdb_id": "0114709", "tmdb_id": 862}


def fixture_ratings():
    ratings.clear()
    ratings[1] = {"id": 1, "user_id": 1, "movie_id": 1, "rating": 4.0, "timestamp": 964982703}


def fixture_tags():
    tags.clear()
    tags[1] = {"id": 1, "user_id": 336, "movie_id": 1, "tag": "pixar", "timestamp": 1139045764}


# ---------- movies ----------

def test_get_movies():
    fixture_movies()
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.json()) == 1  # tyle, ile jest w fixturze
    assert response.json()[0]["title"] == "Toy Story (1995)"


def test_get_movie():
    fixture_movies()
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["title"] == "Toy Story (1995)"

    response = client.get("/movies/999")
    assert response.status_code == 404


def test_create_movie():
    fixture_movies()
    response = client.post("/movies", json={"title": "Heat (1995)", "genres": "Action|Crime|Thriller"})
    assert response.status_code == 201
    assert response.json()["id"] == 2
    assert len(movies) == 2
    assert movies[2]["title"] == "Heat (1995)"


def test_update_movie():
    fixture_movies()
    response = client.put("/movies/1", json={"title": "Toy Story 2 (1999)", "genres": "Animation"})
    assert response.status_code == 200
    assert movies[1]["title"] == "Toy Story 2 (1999)"
    assert movies[1]["genres"] == "Animation"
    assert len(movies) == 1

    response = client.put("/movies/999", json={"title": "Nope", "genres": "Drama"})
    assert response.status_code == 404


def test_delete_movie():
    fixture_movies()
    response = client.delete("/movies/1")
    assert response.status_code == 204
    assert 1 not in movies
    assert len(movies) == 0

    response = client.delete("/movies/1")
    assert response.status_code == 404


# ---------- links ----------

def test_get_links():
    fixture_links()
    response = client.get("/links")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["imdb_id"] == "0114709"


def test_get_link():
    fixture_links()
    response = client.get("/links/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["tmdb_id"] == 862

    response = client.get("/links/999")
    assert response.status_code == 404


def test_create_link():
    fixture_links()
    response = client.post("/links", json={"movie_id": 2, "imdb_id": "0113497", "tmdb_id": 8844})
    assert response.status_code == 201
    assert response.json()["id"] == 2
    assert len(links) == 2
    assert links[2]["imdb_id"] == "0113497"


def test_update_link():
    fixture_links()
    response = client.put("/links/1", json={"movie_id": 1, "imdb_id": "0999999", "tmdb_id": 12345})
    assert response.status_code == 200
    assert links[1]["imdb_id"] == "0999999"
    assert links[1]["tmdb_id"] == 12345
    assert len(links) == 1

    response = client.put("/links/999", json={"movie_id": 1, "imdb_id": "1", "tmdb_id": 1})
    assert response.status_code == 404


def test_delete_link():
    fixture_links()
    response = client.delete("/links/1")
    assert response.status_code == 204
    assert 1 not in links
    assert len(links) == 0

    response = client.delete("/links/1")
    assert response.status_code == 404


# ---------- ratings ----------

def test_get_ratings():
    fixture_ratings()
    response = client.get("/ratings")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["rating"] == 4.0


def test_get_rating():
    fixture_ratings()
    response = client.get("/ratings/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["user_id"] == 1

    response = client.get("/ratings/999")
    assert response.status_code == 404


def test_create_rating():
    fixture_ratings()
    response = client.post("/ratings", json={"user_id": 10, "movie_id": 2, "rating": 5.0, "timestamp": 1700000000})
    assert response.status_code == 201
    assert response.json()["id"] == 2
    assert len(ratings) == 2
    assert ratings[2]["rating"] == 5.0


def test_update_rating():
    fixture_ratings()
    response = client.put("/ratings/1", json={"user_id": 1, "movie_id": 1, "rating": 2.5, "timestamp": 1700000000})
    assert response.status_code == 200
    assert ratings[1]["rating"] == 2.5
    assert ratings[1]["timestamp"] == 1700000000
    assert len(ratings) == 1

    response = client.put("/ratings/999", json={"user_id": 1, "movie_id": 1, "rating": 3.0, "timestamp": 1})
    assert response.status_code == 404


def test_delete_rating():
    fixture_ratings()
    response = client.delete("/ratings/1")
    assert response.status_code == 204
    assert 1 not in ratings
    assert len(ratings) == 0

    response = client.delete("/ratings/1")
    assert response.status_code == 404


# ---------- tags ----------

def test_get_tags():
    fixture_tags()
    response = client.get("/tags")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["tag"] == "pixar"


def test_get_tag():
    fixture_tags()
    response = client.get("/tags/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["tag"] == "pixar"

    response = client.get("/tags/999")
    assert response.status_code == 404


def test_create_tag():
    fixture_tags()
    response = client.post("/tags", json={"user_id": 2, "movie_id": 3, "tag": "funny", "timestamp": 1445714994})
    assert response.status_code == 201
    assert response.json()["id"] == 2
    assert len(tags) == 2
    assert tags[2]["tag"] == "funny"


def test_update_tag():
    fixture_tags()
    response = client.put("/tags/1", json={"user_id": 336, "movie_id": 1, "tag": "animation", "timestamp": 1700000000})
    assert response.status_code == 200
    assert tags[1]["tag"] == "animation"
    assert len(tags) == 1

    response = client.put("/tags/999", json={"user_id": 1, "movie_id": 1, "tag": "x", "timestamp": 1})
    assert response.status_code == 404


def test_delete_tag():
    fixture_tags()
    response = client.delete("/tags/1")
    assert response.status_code == 204
    assert 1 not in tags
    assert len(tags) == 0

    response = client.delete("/tags/1")
    assert response.status_code == 404


def main():
    test_get_movies()
    test_get_movie()
    test_create_movie()
    test_update_movie()
    test_delete_movie()

    test_get_links()
    test_get_link()
    test_create_link()
    test_update_link()
    test_delete_link()

    test_get_ratings()
    test_get_rating()
    test_create_rating()
    test_update_rating()
    test_delete_rating()

    test_get_tags()
    test_get_tag()
    test_create_tag()
    test_update_tag()
    test_delete_tag()

    print("Wszystkie testy przeszły!")


if __name__ == "__main__":
    main()
