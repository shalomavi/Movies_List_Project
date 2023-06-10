from istorage import IStorage


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path

    def list_movies(self):
        """
            Returns a dictionary of dictionaries that
            contains the movies information in the database.

            The function loads the information from the CSV
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
            data = file.readlines()
        parsed_data = {}
        for movie_raw in data[1:]:
            splitted_movie = movie_raw.strip().split(",")
            if len(splitted_movie) == 3:
                title, rating, year = splitted_movie
                parsed_data.update({title: {"rating": float(rating), "year": int(year)}})
            else:
                title, rating, year, note = splitted_movie
                parsed_data.update({title: {"rating": float(rating), "year": int(year), "note": note}})
        return parsed_data

    def add_movie(self, title, year, rating):
        """
            Adds a movie to the movie's database.
            Loads the information from the CSV file, add the movie,
            and saves it. The function doesn't need to validate the input.
            """
        with open(self.file_path, "r") as fileobj:
            data = fileobj.read()

        with open(self.file_path, "w") as fileobj:
            fileobj.write(f"{data.strip()}\n{title},{rating},{year}")

    def delete_movie(self, title):
        """
            Deletes a movie from the movies database.
            Loads the information from the CSV file, deletes the movie,
            and saves it. The function doesn't need to validate the input.
        """
        with open(self.file_path, "r") as fileobj:
            data = fileobj.readlines()
        new_data = ""
        for line in data:
            if title not in line:
                new_data += line
        with open(self.file_path, "w") as fileobj:
            fileobj.write(new_data)

    def update_movie(self, title, rating, notes):
        """
            Updates a movie from the movies database.
            Loads the information from the CSV file, updates the movie,
            and saves it. The function doesn't need to validate the input.
            """

        with open(self.file_path, "r") as fileobj:
            data = fileobj.readlines()
        print(data)

        new_data = ""
        for line in data:
            if title in line:
                if len(line.split(",")) == 3:
                    new_data += line.strip() + "," + notes
                else:
                    new_line_without_notes = line.split(",")[:-1]
                    new_line = new_line_without_notes[0] + "," + new_line_without_notes[1] + "," \
                        + new_line_without_notes[2]
                    new_data += new_line.strip() + "," + notes
            else:
                new_data += line
        print("new", data)

        with open(self.file_path, "w") as fileobj:
            fileobj.write(new_data)
