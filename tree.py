# Name: Ruohong Li
# Uniqname: ruohongl
# Email: ruohongl@umich.edu

# This file contains the BST tree for my program to sort movies
# by showtime
from cache_tools import *

# Constants
TREE_FILE_NAME = 'tree.json'


class MovieTreeNode:
    '''a tree node for movie, contains detail info

    Instance Attributes
    -------------------
    name: string
        movie name
    link: string
        showtime google link for this movie
    showtime_list: list
        list of showing time, category by type
    showtime_num: int
        number of available showtime for this movie
    '''

    def __init__(self, name, link, showtime_list, left=None, right=None):
        self.name = name
        self.link = link
        self.showtime_list = showtime_list
        self.showtime_num = self._calculate_showtime_num()
        self.left = left
        self.right = right

    def _calculate_showtime_num(self):
        num = 0
        for showtime in self.showtime_list:
            num += len(showtime['time'])
        return num

    def __str__(self):
        result = f"Movie Name: {self.name}\n"
        result += f"Showtime ({self.showtime_num} available times):\n"
        for showtime in self.showtime_list:
            result += f"    {showtime['type']}: "
            for time in showtime['time']:
                result += f"{time.replace(' ', '')} "
            result += '\n'
        return result


class MovieTree:
    '''a binary search tree contains movie information,
    sorted by # of showtime

    Instance Attributes
    -------------------
    root: MovieTreeNode
        root node of tree initially None
    size: int
    '''

    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self, node):
        '''insert new node to tree, sort by showtime_num
        '''
        self.root = self._insert(node, self.root)
        self.size += 1

    def _insert(self, node, current_node):
        # base case
        if current_node == None:
            return node

        if node.showtime_num < current_node.showtime_num:
            current_node.left = self._insert(node, current_node.left)
        else:
            current_node.right = self._insert(node, current_node.right)

        return current_node

    def print_tree(self):
        '''print tree by in-order, with right sub-tree before left sub-tree,
        so as to get the result in descending order of showtime_num
        '''
        self._print_tree(self.root)

    def _print_tree(self, current_node):
        # base case
        if current_node == None:
            return

        self._print_tree(current_node.right)
        print(current_node)
        self._print_tree(current_node.left)


def build_tree(movie_list):
    '''using a movie list to build a movie tree
    Parameters
    ----------
    movie_list: list
        a list of dict, each dict contains necessary keys for a movie
        (name, link, showing)
    Returns
    -------
    tree: MovieTree object
    '''
    tree = MovieTree()
    for movie in movie_list:
        node = MovieTreeNode(movie['name'], movie['link'], movie['showing'])
        tree.insert(node)
    return tree


def save_tree(movie_tree):
    '''save tree to a json file
    Parameters
    ----------
    movie_tree: MovieTree object
    '''
    movies = []
    _save_tree(movie_tree.root, movies)
    file_obj = open(TREE_FILE_NAME, 'w')
    file_obj.write(json.dumps(movies))
    file_obj.close()


def _save_tree(current_node, movies):
    if current_node == None:
        return

    _save_tree(current_node.right, movies)
    movie_dict = {'name': current_node.name,
                  'link': current_node.link,
                  'showing': current_node.showtime_list
                  }
    movies.append(movie_dict)
    _save_tree(current_node.left, movies)

def load_tree():
    '''reconstruct a tree from a json file
    '''
    try:
        tree_file = open(TREE_FILE_NAME, 'r')
        tree = build_tree(json.loads(tree_file.read()))
        tree_file.close()
    except:
        tree = MovieTree()
    return tree


if __name__ == "__main__":
    cache_dict = open_cache('showtimes_cache.json')
    movie_tree = build_tree(
        cache_dict['Ann Arbor 20 IMAX']['showtimes'][0]['movies'])
    movie_tree.print_tree()
    save_tree(movie_tree)
    movie_tree = load_tree()
    movie_tree.print_tree()
