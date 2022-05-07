'''
Author: Alex Reichenbach
Date: May 7, 2022
'''
import numpy as np
from usac.filters.filter import Filter

class LinearGradient(Filter):
    def __init__(self, cfg):
        self.cfg = cfg

    def _filter_image(self, img: np.ndarray) -> np.ndarray:
        '''
        r, c = i, j are origin 

        0) Left, (r, c - 1)
        1) Left up, (r - 1, c - 1)
        2) Up, (r - 1, c)
        3) Up right, (r - 1, c + 1)
        4) Right, (r, c + 1)
        5) Right Down, (r + 1, c + 1)
        6) Down, (r + 1, c)
        7) Down Left, (r + 1, c - 1)
        '''
        rows, cols = img.shape
        c_coords, r_coords = np.meshgrid(np.arange(cols), np.arange(rows))

        return np.array()
