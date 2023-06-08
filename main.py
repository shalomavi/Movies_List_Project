from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv


def main():
    # storage = StorageCsv('data.csv')
    storage = StorageJson('data.json')
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
