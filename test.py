from movie_app import MovieApp
from storage_json import StorageJson
import pytest


def test_list_movies_normal():
    storage = StorageJson("test.json")
    assert storage.list_movies() == {"test": {"test1": "test1"}}


def test_list_movies_not_exit():
    storage = StorageJson("test1.json")
    with pytest.raises(Exception):
        storage.list_movies()


def test_add_movie_normal():
    storage = StorageJson("test.json")
    storage.add_movie("m", "1999", "8.8")
    assert storage.list_movies() == {"test": {"test1": "test1"},
                                     "m": {"year": 1999, "rating": 8.8}}
    storage.delete_movie("m")


def test_delete_movie_normal():
    storage = StorageJson("test.json")
    storage.add_movie("m", "1999", "8.8")
    storage.delete_movie("m")
    assert storage.list_movies() == {"test": {"test1": "test1"}}

def test_delete_movie_not_exits():
    storage = StorageJson("test.json")
    test = MovieApp(storage)
    test.delete_movie()





def test_update_movie_normal():
    storage = StorageJson("test.json")
    storage.add_movie("m", "1999", "8.8")
    storage.update_movie("m", "9.0", "test")
    assert storage.list_movies() == {"test": {"test1": "test1"},
                                     "m": {"year": 1999, "rating": 9.0, "note": "test"}}
    storage.delete_movie("m")


pytest.main()
