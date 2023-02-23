import numpy as np

def rgb2hex(rgb: np.ndarray):
    ''' Converts an N X 3 numpy array of RGB values into a list of hex strings'''
    hex_list = list(map(lambda x: '#%02x%02x%02x' % tuple(x), rgb))
    return hex_list