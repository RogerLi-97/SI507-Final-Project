# Name: Ruohong Li
# Uniqname: ruohongl
# Email: ruohongl@umich.edu

# This is the main driver file for my SI507 Final Project
import datetime
import webbrowser
from original_data_loader import *
from tree import *

# Constants
MAX_MAIN_MENU_NUM = 5
MAX_SHOWTIME_MENU_NUM = 3
MAX_PLAYING_MOVIE_MENU_NUM = 2

SEARCH_BY_THEATER_OPTION = 1
LIST_PLAYING_MOVIES_OPTION = 2
SEARCH_BY_TITLE_OPTION = 3
LIST_UPCOMING_OPTION = 4
EXIT_OPTION = 5

PRINT_TREE_OPTION = 1
SAVE_TREE_OPTION = 2
BACK_OPTION = 3

GET_WEB_INFO_OPTION = 1
MAIN_MENU_OPTION = 2

CHROME_PATH = 'open -a /Applications/Google\ Chrome.app %s'


def print_main_menu():
    print("1. Search Movie Showtime by Theater")
    print("2. List Currently Playing Movies")
    print("3. Search Movie Info by Title")
    print("4. List upcoming movies")
    print("5. Exit")


def request_input(max):
    '''request user input, error checking by max option #
    Parameters
    ----------
    max: int
        max option number
    '''
    choice = input('Please input a valid number: ')
    while True:
        if choice.isnumeric() and 1 <= int(choice) <= max:
            return int(choice)
        else:
            choice = input('Invalid input, please give a valid option: ')


def search_movies_by_theater():
    '''search movie info by theater and location
    '''
    print()
    print("Example:")
    print(f"Theater Name: {DEFAULT_THEATER}")
    print(f"Location: {DEFAULT_LOACTION}")
    print()
    location = input(
        "Please specify your location in format [City, State, Country]: ")
    theater_name = input("Please specify the theater name: ")
    while location == "" or theater_name == "":
        print("Insufficient information, please specify both location and theater name")
        location = input(
            "Please specify your location in format [City, State, Country]: ")
        theater_name = input("Please specify the theater name: ")
    movie_list = query_showing_movies_by_theater(theater_name, location)
    movie_tree = build_tree(movie_list)
    print("Movie showtime results have been loaded in a tree, sorted by showtime amount\n")
    while True:
        print_showtime_result_menu()
        choice = request_input(MAX_SHOWTIME_MENU_NUM)
        if choice == PRINT_TREE_OPTION:
            print()
            movie_tree.print_tree()
        elif choice == SAVE_TREE_OPTION:
            save_tree(movie_tree)
            print("Save Successful\n")
        else:
            break


def print_showtime_result_menu():
    print("1. Print detail showtime info")
    print("2. Save tree into \"tree.json\"")
    print("3. Back to main menu")


def list_currently_playing_movies():
    '''Use default theater showtime info to list currently playing movies
    '''
    movie_list = query_showing_movies_by_theater()
    print()
    for i in range(len(movie_list)):
        print(f"({i}) {movie_list[i]['name']}")
    print()
    while True:
        print_playing_movies_menu()
        choice = request_input(MAX_PLAYING_MOVIE_MENU_NUM)
        if choice == GET_WEB_INFO_OPTION:
            movie_idx = input(
                f"Please select a movie number listed above (0-{len(movie_list) - 1}): ")
            link = movie_list[int(movie_idx)]['link']
            name = movie_list[int(movie_idx)]['name']
            print(f"\nLaunching \"{name}\" Page in Web Browser...\n")
            webbrowser.get(CHROME_PATH).open(link)
        else:
            break


def print_playing_movies_menu():
    print("1. Get movie showtime info on web browser")
    print("2. Back to main menu")


def search_movie_by_title():
    '''Using Open Movie Database API to search movie detail info by title
    '''
    print()
    while True:
        name = input(
            "Please input a valid movie title or input nothing to go back to the main menu: ")
        if name == '':
            break
        else:
            movie_dict = query_movie_detail(name)
            if movie_dict['Response'] == 'False':
                print('...Movie Not Found!\n')
            else:
                print()
                print_movie_detail(movie_dict)
                print()


def print_movie_detail(movie_dict):
    '''print a movie detail info by a movie_dict from OMDB API
    '''
    print(f"  Title: {movie_dict['Title']}")
    print(f"  Released: {movie_dict['Released']}")
    print(f"  Rated: {movie_dict['Rated']}")
    print(f"  Runtime: {movie_dict['Runtime']}")
    print(f"  Director: {movie_dict['Director']}")
    print(f"  Actors: {movie_dict['Actors']}")
    print(f"  Language: {movie_dict['Language']}")
    print(f"  Awards: {movie_dict['Awards']}")
    print(f"  Plot: {movie_dict['Plot']}")

def list_upcoming_movies():
    '''list upcoming movies, data from flixster api
    '''
    upcoming_dict = query_upcoming_movies()
    movie_list = upcoming_dict['data']['upcoming']
    print(f"\nThere are {len(movie_list)} movies in total, how many you want to list")
    list_num = request_input(len(movie_list))
    for i in range(list_num):
        print(f"  Title: {movie_list[i]['name']}")
        print(f"  Release Date: {movie_list[i]['releaseDate']}")
        print()



if __name__ == "__main__":
    # 1. start program, preload data
    print('-' * 60)
    print("Welcome to SI507 Final Project -- Movie showtime!")
    print("Author: Ruohong Li")
    time = datetime.datetime.now()
    print("Date for today:", time.strftime("%x"))
    print('-' * 60)
    preload_data()

    # 2. request user input, interaction
    while True:
        print()
        print_main_menu()
        choice = request_input(MAX_MAIN_MENU_NUM)
        if choice == SEARCH_BY_THEATER_OPTION:
            search_movies_by_theater()
        elif choice == LIST_PLAYING_MOVIES_OPTION:
            list_currently_playing_movies()
        elif choice == SEARCH_BY_TITLE_OPTION:
            search_movie_by_title()
        elif choice == LIST_UPCOMING_OPTION:
            list_upcoming_movies()
        else:
            break

    print("Thank you for using my program!")
