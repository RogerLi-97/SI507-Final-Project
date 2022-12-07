# Name: Ruohong Li
# Uniqname: ruohongl
# Email: ruohongl@umich.edu

# This file provides necessary open cache and save cache funtions
import json
import requests

def open_cache(file_name):
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------
    file_name: string

    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(file_name, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict


def save_cache(cache_dict, file_name):
    ''' saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
    file_name: string

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    cache_file = open(file_name, "w")
    cache_file.write(dumped_json_cache)
    cache_file.close()


def loadData(file_name, url, headers=None, params=None, key=None):
    '''load data from given url
    Parameters
    ----------
    file_name: string
        Cache file name
    url: string
        The url to request data from.
    headers: dict
        headers for request
    params: dict
        parameters for request
    key: string
        key for cache dict, if provided, use this key to cache data

    Returns
    -------
    json_data: json object
        The json object of requested data
    '''
    cache_dict = open_cache(file_name)
    json_data = None

    if key and key not in cache_dict:
        # key provided but not cached
        response = requests.get(url, headers=headers, params=params)
        cache_dict[key] = response.json()
        json_data = cache_dict[key]
    elif key:
        # key provided and already cached
        json_data = cache_dict[key]
    elif url not in cache_dict: 
        # no key
        response = requests.get(url, headers=headers, params=params)
        cache_dict[url] = response.json()
        json_data = cache_dict[url]
    else:
        # url already in cache dict
        json_data = cache_dict[url]

    save_cache(cache_dict, file_name)
    return json_data