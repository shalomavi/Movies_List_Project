from istorage import IStorage
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
            Returns a dictionary of dictionaries that
            contains the movies information in the database.

            The function loads the information from the JSON
            file and returns the data.

            For example, the function may return:
            {
              "Titanic": {
                "rating": 9,
                "year": 1999
              },
              "..." {
                ...
              },
            }
            """
        with open(self.file_path, "r") as file:
            data = file.read()
        parsed_data = json.loads(data)
        return parsed_data

    def add_movie(self, title, year, rating):
        """
            Adds a movie to the movie's database.
            Loads the information from the JSON file, add the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies = self.list_movies()
        movies.update({title: {'rating': rating, 'year': year}})
        with open(self.file_path, "w") as fileobj:
            fileobj.write(json.dumps(movies))

    def delete_movie(self, title):
        """
            Deletes a movie from the movies database.
            Loads the information from the JSON file, deletes the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies = self.list_movies()
        movies.pop(title)
        with open(self.file_path, "w") as fileobj:
            fileobj.write(json.dumps(movies))

    def update_movie(self, title, rating, notes):
        """
            Updates a movie from the movies database.
            Loads the information from the JSON file, updates the movie,
            and saves it. The function doesn't need to validate the input.
            """
        movies = self.list_movies()
        movies[title]['rating'] = rating
        if notes is not None:
            movies[title]['note'] = notes
        with open(self.file_path, "w") as fileobj:
            fileobj.write(json.dumps(movies))



