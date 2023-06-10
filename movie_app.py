import random
import statistics

import matplotlib.pyplot as plt
import requests
from colorama import Fore
from colorama import Style
from colorama import init as colorama_init
import bs4

API_KEY = "87c55f08"


class MovieApp:
    def __init__(self, storage):
        self._storage = storage

    def _command_list_movies(self, movies=None):

        """
            prints all movies in data
            :param :
            :return: None
            """
        if movies is None:
            movies = self._storage.list_movies()
        number_of_movies = len(movies)
        print(f"\n{number_of_movies} movies in total:\n")
        for key, val in movies.items():
            print(f"{key}; rating: {val['rating']}, release year: {val['year']}", end="")
            if val.get('note') is not None:
                print(f', note: {val["note"]}', end="")
            print("")
        print("\n")

    def _command_movie_stats(self):
        """
            prints stats about the movies rating:
            average, median, min and max
            :param :
            :return: None
            """
        movies_dict = self._storage.list_movies()
        movie_ratings_list = []
        for movie in movies_dict:
            movie_ratings_list.append(float(movies_dict[movie]['rating']))
        sum_movie_ratings = sum(movie_ratings_list)
        num_of_movies = len(movies_dict)

        average_ratings = sum_movie_ratings / num_of_movies
        median_ratings = statistics.median(movie_ratings_list)
        best_movie_rating = max(movie_ratings_list)
        worst_movie_rating = min(movie_ratings_list)

        print(f"Average ratings: {average_ratings}\n"
              f"Median ratings: {median_ratings}\n")

        for movie, options in movies_dict.items():
            if options['rating'] == best_movie_rating:
                print(f"Best movie: {movie}, {options['rating']}")
            if options['rating'] == worst_movie_rating:
                print(f"Worst movie: {movie}, {options['rating']}")
        print("\n")

    def _generate_website(self):
        """creates a html file from  the index_template.html file"""

        with open("index_template.html", "r") as fileobj:
            html_text = fileobj.read()
        html_title = input("insert webpage title:")
        while html_title == "":
            html_title = input("wrong input, insert webpage title:")
        print("generating website...")
        html_grid = self._get_html_grid()
        updated_title = html_text.replace("__TEMPLATE_TITLE__", html_title)
        updated_html = updated_title.replace("__TEMPLATE_MOVIE_GRID__", html_grid)
        with open(f"{html_title}.html", "w", encoding='utf-8') as fileobj:
            fileobj.write(updated_html)
        print("website generated!")

    def run(self):
        colorama_init()
        print(f"{Fore.LIGHTBLUE_EX}*************** "
              f"Welcome to your movies list! ***************\n{Style.RESET_ALL}")
        self._get_enter_key()
        self._print_menu()
        choice = self._get_input()

        while choice != '0':
            self._apply_chosen_option(choice)
            self._print_menu()
            choice = self._get_input()

        print("Bye!")

    @staticmethod
    def _print_menu():
        """prints a menu for the user"""
        print(f'''
        {Fore.LIGHTRED_EX}M{Fore.LIGHTYELLOW_EX}e{Fore.CYAN}n{Fore.LIGHTGREEN_EX}u{Fore.MAGENTA}:{Style.RESET_ALL}
        {Fore.RED}0. Exit{Style.RESET_ALL}
        {Fore.LIGHTGREEN_EX}1. Movies list
        {Fore.LIGHTYELLOW_EX}2. Add movie
        {Fore.YELLOW}3. Delete movie
        {Fore.GREEN}4. Update movie
        {Fore.BLUE}5. Stats
        {Fore.MAGENTA}6. Random movie
        {Fore.CYAN}7. Search movie
        {Fore.LIGHTBLUE_EX}8. Movies sorted by rating
        {Fore.LIGHTYELLOW_EX}9. Create rating histogram
        {Fore.LIGHTMAGENTA_EX}10. Generate web page
    
        ''')

    @staticmethod
    def _get_input():
        """get an input and returns it"""
        user_input = input(
            f'{Fore.LIGHTYELLOW_EX}Enter choice (1-10), {Fore.RED}'
            f'(0){Fore.LIGHTYELLOW_EX} to Exit:{Style.RESET_ALL} ')
        return user_input

    @staticmethod
    def _get_enter_key():
        """checks if pressed key is enter """
        enter_key_input = input(f"Press {Fore.LIGHTGREEN_EX}enter{Style.RESET_ALL} to continue")
        if enter_key_input == "":
            pass

    def _apply_chosen_option(self, choice):
        """
        get choice from user and movies data and calls
        each function depends on user choice
        """

        if not choice.isdigit():
            return None

        choice = int(choice)

        if choice == 1:
            self._command_list_movies()

        elif choice == 2:
            self.add_movie()

        elif choice == 3:

            self.delete_movie()

        elif choice == 4:
            self.update_movie()

        elif choice == 5:
            self._command_movie_stats()

        elif choice == 6:
            self._get_random_movie()

        elif choice == 7:
            self._search_movie()

        elif choice == 8:
            self._get_sorted_movies()

        elif choice == 9:
            self._get_movies_histogram()

        elif choice == 10:
            self._generate_website()

        self._get_enter_key()

    def add_movie(self):
        """
        adds a new movie to data
        :param :
        :return: None
        """
        movies = self._storage.list_movies()
        new_movie_name = input("Enter new movie name: ")
        if new_movie_name in movies.keys():
            print("Movie already exists!")
        else:
            movie_data = self._get_movies_api(new_movie_name)
            if movie_data is None:
                print("couldn't fetch data from api")
                self._add_movie_manually(new_movie_name)
                return None

            title = movie_data.get('Title')
            new_movie_release_year = movie_data.get('Year')
            new_movie_rating = movie_data.get('imdbRating')

            if title is None:
                print('Movie not found!')
                return None
            try:
                new_movie_rating = float(new_movie_rating)
            except ValueError:
                print("rating set to 0, update rating manually!")
                new_movie_rating = 0
            try:
                new_movie_release_year = int(new_movie_release_year)
            except ValueError:
                print("year set to 2023, update year manually!")
                new_movie_release_year = 2023

            self._storage.add_movie(title, new_movie_release_year, new_movie_rating)
            print(f"{new_movie_name} added")

    def _add_movie_manually(self, new_movie_name):
        """ adds movie by user inputs if api doesn't work"""

        new_movie_rating = input("Enter new movie rating: ")
        new_movie_release_year = input("Enter new movie release year: ")
        if new_movie_release_year.isdigit() and not new_movie_rating.isalpha():
            self._storage.add_movie(new_movie_name, int(new_movie_release_year), float(new_movie_rating))
            print("movie added without api")
        else:
            print("wrong inputs!")

    def delete_movie(self):
        """
        deletes a movie the user chooses from data
        :param :
        :return: None
        """
        movies = self._storage.list_movies()
        self._command_list_movies()
        movie_name = input("Enter movie name to delete: ")

        if movie_name not in movies.keys():
            print(f"{movie_name} doesn't exists!")
        else:
            self._storage.delete_movie(movie_name)
            print(f"{movie_name} deleted!")

    def update_movie(self):
        """
        update movie by user choice
        :param :
        :return: None
        """
        movies = self._storage.list_movies()
        self._command_list_movies()
        movie_name = input("Enter movie name to update: ")

        if movie_name not in movies.keys():
            print(f"{movie_name} doesn't exits!")
        else:
            movie_rating = input("Enter movie rating: ")
            movie_note = input("Enter  movie note: ")
            if not movie_rating.isalpha():
                self._storage.update_movie(movie_name, float(movie_rating), movie_note)

                print(f"{movie_name} movie successfully updated!")
            else:
                print("option is not valid!")

    def get_movies_stats(self):
        """
        prints stats about the movies rating:
        average, median, min and max
        :param :
        :return: None
        """
        movies_dict = self._storage.list_movies()
        movie_ratings_list = []
        for movie in movies_dict:
            movie_ratings_list.append(float(movies_dict[movie]['rating']))
        sum_movie_ratings = sum(movie_ratings_list)
        num_of_movies = len(movies_dict)

        average_ratings = sum_movie_ratings / num_of_movies
        median_ratings = statistics.median(movie_ratings_list)
        best_movie_rating = max(movie_ratings_list)
        worst_movie_rating = min(movie_ratings_list)

        print(f"Average ratings: {average_ratings}\n"
              f"Median ratings: {median_ratings}\n")

        for movie, options in movies_dict.items():
            if options['rating'] == best_movie_rating:
                print(f"Best movie: {movie}, {options['rating']}")
            if options['rating'] == worst_movie_rating:
                print(f"Worst movie: {movie}, {options['rating']}")
        print("\n")

    def _get_random_movie(self):
        """
        prints a random movie from movies data
        :return: None
        """
        movies_dict = self._storage.list_movies()
        random_movie, random_movie_options = random.choice(list(movies_dict.items()))
        print(f"Random movie is: {random_movie}, its rated: {random_movie_options['rating']}")

    def _search_movie(self):
        """
        search for a movie entered by user,
        if movie not found calculate edit distance
        and prints movies close to it
        :return: None
        """
        movies_dict = self._storage.list_movies()
        movie_searched = input("Enter part of movie name: ")
        is_movie_found = False
        for key in movies_dict:
            if movie_searched.lower() == key.lower():
                print(f"{key}, {movies_dict.get(key, 0)}")
                is_movie_found = True

        if not is_movie_found:
            print(f"'{movie_searched}' does not exists. Did you mean:")
            for key in movies_dict.keys():
                searched_movie_distance = self._edit_distance(movie_searched, key)
                if searched_movie_distance < 8:
                    print(f"{key}")

    # JUST WANTED TO SAY THAT I DID NOT WRITE THE CODE OF THE EDIT DISTANCE FUNCTION.###
    @staticmethod
    def _edit_distance(first_string, second_string):
        """
        calculates the difference(amount of actions needed)
         between two strings
        :param first_string:
        :param second_string:
        :return tbl[i, j]:
        """
        first_string_length = len(first_string) + 1
        second_string_length = len(second_string) + 1

        tbl = {}
        for i in range(first_string_length):
            tbl[i, 0] = i
        for j in range(second_string_length):
            tbl[0, j] = j
        for i in range(1, first_string_length):
            for j in range(1, second_string_length):
                if first_string[i - 1] == second_string[j - 1]:
                    cost = 0
                else:
                    cost = 1
                tbl[i, j] = min(tbl[i, j - 1] + 1, tbl[i - 1, j] + 1, tbl[i - 1, j - 1] + cost)

        return tbl[i, j]

    def _get_sorted_movies(self):
        """
        sort data by rating then calls get_movies_list()
        :param :
        :return: None
        """
        movies_dict = self._storage.list_movies()
        sorted_movies_dict = dict(sorted(movies_dict.items(),
                                         key=lambda x: x[1]['rating'], reverse=True))

        self._command_list_movies(sorted_movies_dict)

    def _get_movies_histogram(self):
        """
        opens a new window with a histogram of
        ratings and frequencies
        :param :
        :return None:
        """
        movies_dict = self._storage.list_movies()
        # create a list of ratings from the dictionary
        movies_ratings = [movie['rating'] for movie in movies_dict.values()]

        # create a histogram using matplotlib with custom color
        plt.hist(movies_ratings, color='lightgreen', edgecolor='black', linewidth=1)

        # add x-axis label and y-axis label
        plt.xlabel("Ratings")
        plt.ylabel("Number Of Movies")

        # add a title
        plt.title("Histogram Of Movies Ratings")

        # show the plot
        plt.show()

    @staticmethod
    def _get_movies_api(title):
        """
        connect to omdbapi and gets the api for the selected
        title and return a dictionary of the movie data
        :param title:
        :return dict_of_movie_data:
        """
        url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={title}"
        try:
            res = requests.get(url)
        except Exception as e:
            print(f"{e}\n Check connections!")
            return None
        data = res.json()
        print(data)
        return data

    def _get_html_grid(self):
        """returns a string to be created as a file later
        from the data given"""
        movies = self._storage.list_movies()

        html_grid = ""
        for title, stats in movies.items():
            movies_data = self._get_movies_api(title)
            if movies_data is None:
                print("Error fetching movie data, check connections..")
                movies_data = movies
            poster_img_url = movies_data.get('Poster')
            no_img_url = "https://upload.wikimedia.org/wikipedia/commons/6/65/No-Image-Placeholder.svg"
            if poster_img_url == 'N/A' or poster_img_url is None:
                poster_img_url = no_img_url
            year = stats.get('year')
            note = stats.get('note')
            rating = stats.get('rating')

            # fetch all data to the html elements
            rating_star = '&#11088;'
            rating_stars = rating_star * int(rating)
            website_address = self.get_movie_website_address(movies_data)
            country_raw = movies_data.get("Country")
            if website_address is not None:
                country = country_raw.split(",")[0].strip()
                country_flag_url = self.scrape_country_flag(country)

            else:
                country = ''
                country_flag_url = ''

            # create the html grid
            html_grid += '<li'
            if note is not None and note != "":
                html_grid += ' class="no-hide">\n'
            else:
                html_grid += '>\n'

            html_grid += f'<div class="movie">\n'
            if poster_img_url is not None:
                html_grid += f'<a href="{website_address}" target="_blank">' \
                             f' <img class="movie-poster" alt="{title}" \n' \
                             f'src="{poster_img_url}"/> </a>\n'
            if country_flag_url and country:
                html_grid += f'<div class="country_flag"><img src="{country_flag_url}"' \
                             f' alt="{country}_flag"' \
                             f'width="30px" height="20px"></div>\n'
            else:
                html_grid += f'<div class="country_flag"><img src="{no_img_url}"' \
                             f' alt="{country}_flag"' \
                             f'width="40px" height="25px"></div>\n'
            html_grid += f'<div class ="movie-title">{title}</div>\n'
            if year is not None:
                html_grid += f'<div class="movie-year">{year}</div>\n'
            if rating is not None:
                html_grid += f'<div class="movie-rating">{rating_stars}</div>\n'
            if note is not None and note != "":
                html_grid += f'<div class="movie-note-hide">{note}</div>\n'
            html_grid += f'</div>\n'
            html_grid += f'</li>\n'

        return html_grid

    @staticmethod
    def get_movie_website_address(movie_data):
        """
        gets data of a movie and returns its imdb address
        :param movie_data:
        :return address:
        """
        imdb_id = movie_data.get('imdbID')
        if imdb_id is None:
            return None
        address = f'https://www.imdb.com/title/{imdb_id}/'
        return address

    @staticmethod
    def _check_abbreviation(abbreviation):
        match abbreviation:
            case 'U.S.':
                return 'United States'
            case 'U.K.':
                return 'United Kingdom'
            case 'U.A.E.':
                return 'United Arab Emirates'
            case _:
                return abbreviation

    def scrape_country_flag(self, country):
        base_url = 'https://www.worldometers.info/'
        country_page_url = f'{base_url}geography/flags-of-the-world/'
        response = requests.get(country_page_url)
        content = response.content
        soup = bs4.BeautifulSoup(content, features="html.parser")
        country_containers = soup.find_all('div', {'class': 'col-md-4'})
        for country_container in country_containers:
            try:
                candidate_country = country_container.find('div').find('div').text
                candidate_country_no_alias = self._check_abbreviation(candidate_country)
                if candidate_country_no_alias.casefold() == country.casefold():
                    return f"{base_url}{country_container.find('img')['src']}"
            except AttributeError as e:
                print(e)
                continue
        return ''

    @staticmethod
    def _get_country_flag(country):
        """
        searches in the api database and returns the country flag's url
        :param country:
        :return country_flag_url:
        """
        # Country-facts api
        url = "https://country-facts.p.rapidapi.com/all"

        headers = {
            "X-RapidAPI-Key": "20737c50d5mshebaa853357f5e86p168462jsn16a8090e924d",
            "X-RapidAPI-Host": "country-facts.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers)
        print(response.text)
        # when monthly api limit reached:

        if response.ok:
            country_details = requests.get(url, headers=headers).json()
            for country in country_details:
                test_country = country_details['name']['common']
                if test_country == country:
                    country_flag_url = country_details['flag']
                    return country_flag_url

        # GeoSource API:
        url = "https://geosource-api.p.rapidapi.com/emojiFlagByCountry.php"

        querystring = {"country": country}

        headers = {
            "X-RapidAPI-Key": "20737c50d5mshebaa853357f5e86p168462jsn16a8090e924d",
            "X-RapidAPI-Host": "geosource-api.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        print(response.json())
        country_list = response.json()
        if not response.ok:
            return None
        return country_list[0]['emojiU']
