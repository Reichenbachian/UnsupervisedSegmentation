'''
Author: Alex Reichenbach
Date: May 7, 2022
'''
import numpy as np

class Filter():
    def __init__(self, cfg):
        self.cfg = cfg

    def filter_image(self, img: np.ndarray) -> np.ndarray:
        '''
        Filters an image to augment the distances
        of the matrix.

        Input: np.ndarray (3,r,c)
        Output: np.ndarray(8,r,c)

        8 channels/connections are as follows
        
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
        # In the future this should check if it's a 
        # 4 return and augment it to an 8
        filtered = self._filter_image(img)

        assert filtered.min() >= 0 and filtered.max() <= 1, f"All filters should return values between 0 and 1. {self} failed"
        return filtered
