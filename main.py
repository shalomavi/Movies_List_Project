from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv
import sys


def main():
    try:
        storage_file = sys.argv[1]
        if storage_file.split(".")[1] == "csv":
            storage = StorageCsv(storage_file)
        else:
            storage = StorageJson(storage_file)

        movie_app = MovieApp(storage)
        movie_app.run()
    except IndexError:
        storage = StorageCsv('data.csv')
        storage = StorageJson('data.json')
        movie_app = MovieApp(storage)
        movie_app.run()


if __name__ == "__main__":
    main()
