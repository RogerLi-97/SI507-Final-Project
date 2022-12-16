# Name: Ruohong Li
# Uniqname: ruohongl
# Email: ruohongl@umich.edu

# This file provides necessary function to preload raw data from corresponding API
# and caching the processed data.
import requests
import datetime
from cache_tools import *
import secret


# API_KEYS
# 1. Flixster API
X_RAPID_API_KEY = secret.X_RAPID_API_KEY
X_RAPID_API_HOST = 'flixster.p.rapidapi.com'
FLIXSTER_BASE_URL = 'https://flixster.p.rapidapi.com/movies'

# 2. Open Movie Database API
OPEN_MOVIE_API_KEY = secret.OPEN_MOVIE_API_KEY
OPEN_MOVIE_BASE_URL = 'http://www.omdbapi.com'

# 3. Google Showtimes Results API
GOOGLE_SHOWTIMES_API_KEY = secret.GOOGLE_SHOWTIMES_API_KEY
GOOGLE_SHOWTIMES_BASE_URL = 'https://serpapi.com/search.json'


# Constant
FLIXSTER_SRC_KEY = 'flixster'
DEFAULT_LOACTION = 'Ann Arbor, Michigan, United States'
DEFAULT_THEATER = 'Ann Arbor 20 IMAX'

def query_upcoming_movies():
    '''Getting and caching upcoming movie data from Flixster API

    Parameters
    ----------
    None

    Returns
    -------
    result: dict
        json object
    '''
    params = {'countryId': 'usa', 'limit': '100'}
    url = f"{FLIXSTER_BASE_URL}/get-upcoming"
    headers = {
        "X-RapidAPI-Key": X_RAPID_API_KEY,
        "X-RapidAPI-Host": X_RAPID_API_HOST
    }
    file_name = 'flixster_cache.json'
    return loadData(file_name, url, headers, params)


def build_movie_name_list(json_dict, src_key):
    '''Extract movie names from a json dict
    src_key indicate the source API of the json dict so as to determine
    the format to be used to parse the data

    Parameters
    ----------
    json_dict: dict
        The json object from a movie API
    src_key: str
        Source key for a movie api

    Returns
    -------
    name_list: list
       list of movie names
    ems_version_id_list: list
        list of ems version id for flixster API
    '''
    name_list = []
    ems_version_id_list = []
    if src_key == FLIXSTER_SRC_KEY:
        for movie in json_dict['data']['upcoming']:
            name_list.append(movie['name'])
            ems_version_id_list.append(movie['emsVersionId'])
    return (name_list, ems_version_id_list)


def preload_data():
    '''Preload movie data from API

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    # 1. load data for upcoming movies from flixster API
    data = query_upcoming_movies()
    name_list, ems_version_id_list = build_movie_name_list(
        data, FLIXSTER_SRC_KEY)
    for i in range(len(name_list)):
        query_movie_detail_from_flixster(name_list[i], ems_version_id_list[i])

    # 2. load initial showtimes data from Ann Arbor 20 IMAX theater
    query_showing_movies_by_theater()


def query_movie_detail_from_flixster(name, ems_version_id):
    '''Getting and caching movie detail info from Flixster API

    Parameters
    ----------
    name: string
        movie name
    ems_version_id: string
        Required parameter of Flixster API

    Returns
    -------
    result: dict
        json object
    '''
    params = {'emsVersionId': ems_version_id}
    url = f"{FLIXSTER_BASE_URL}/detail"
    headers = {
        "X-RapidAPI-Key": X_RAPID_API_KEY,
        "X-RapidAPI-Host": X_RAPID_API_HOST
    }
    file_name = 'flixster_movie_detail_cache.json'
    return loadData(file_name, url, headers, params, key=name)


def query_movie_detail(name, year=None):
    '''Getting and caching movie detail info from OMDb API

    Parameters
    ----------
    name: string
        Name of a movie
    year: string
        Ex: '2022'

    Returns
    -------
    result: dict
        json object
    '''
    if year:
        params = {'t': name, 'y': year, 'apikey': OPEN_MOVIE_API_KEY}
    else:
        params = {'t': name, 'apikey': OPEN_MOVIE_API_KEY}

    file_name = 'movie_detail_cache.json'
    return loadData(file_name, OPEN_MOVIE_BASE_URL, params=params, key=name)

def query_showing_movies_by_theater(name=DEFAULT_THEATER, location=DEFAULT_LOACTION):
    '''Getting and caching showtimes info from google showtimes results api

    Parameters
    ----------
    name: string
        name of theater
    location: string
        city location with format: "City, State, Country"
    
    Returns
    -------
    result: list
        list of movie dict
    '''
    params = {
        'q': name,
        'location': location,
        'hl': 'en',
        'gl': 'us',
        'api_key': GOOGLE_SHOWTIMES_API_KEY
    }

    file_name = 'showtimes_cache.json'

    # show time data need to be updated everyday
    result = loadData(file_name, GOOGLE_SHOWTIMES_BASE_URL, params=params, key=name)
    # Check update time
    try:
        update_time = result['update_time']
    except:
        # first time request
        cache_dict = open_cache(file_name)
        cache_dict[name]['update_time'] = datetime.datetime.now().strftime("%x")
        save_cache(cache_dict, file_name)
        return result['showtimes'][0]['movies'] # only return showtime result for today

    # update data if necessary
    if update_time != datetime.datetime.now().strftime("%x"):
        cache_dict = open_cache(file_name)
        cache_dict[name] = requests.get(GOOGLE_SHOWTIMES_BASE_URL, params=params).json()
        cache_dict[name]['update_time'] = datetime.datetime.now().strftime("%x")
        save_cache(cache_dict, file_name)
        result = cache_dict[name]['showtimes'][0]['movies']
    else:
        result = result['showtimes'][0]['movies']

    return result

