'''
Author: Alex Reichenbach
Date: May 7

Used to create the color as inputs to the ward
agglomerative clustering method
'''

import numpy as np
from skimage.color import rgb2lab

from usac.filters.filter import Filter
from usac.data.rgbd_image import RGBD_Image

class ColorFilter(Filter):
    def __init__(self, cfg):
        self.cfg = cfg

        self.convert_methods = {'rgb': self.to_rgb,
                                'lab': self.to_lab}

    def extract_hog_features(self, img):
        # Test Image
        # TO-DO: This was confusing, there should be a test to make
        # sure it's working.
        # img = np.array([[0,0,0,0],
        #                 [0,0,1,0],
        #                 [0,0,0,0],
        #                 [0,0,0,0]])

        weights = []
        for direction in self.offsets:
            r_offset, c_offset = self.offsets[direction]
            edge_weights = np.zeros(img.shape, dtype=np.float32)

            edge_weights[1 if r_offset == -1 else None:\
                               -1 if r_offset == 1 else None,
                               1 if c_offset == -1 else None:\
                               -1 if c_offset == 1 else None] = \
                           img[1 if r_offset == -1 else None:\
                               -1 if r_offset == 1 else None,
                               1 if c_offset == -1 else None:\
                               -1 if c_offset == 1 else None] - \
                           img[1 if r_offset == 1 else None:\
                               -1 if r_offset == -1 else None,
                               1 if c_offset == 1 else None:\
                               -1 if c_offset == -1 else None]


            # print(direction)
            # print("(", 1 if r_offset == -1 else None, ":",
            #         -1 if r_offset == 1 else None, ",",
            #         1 if c_offset == -1 else None, ":",
            #         -1 if c_offset == 1 else None, ") (",
            #         1 if r_offset == 1 else None, ":",
            #         -1 if r_offset == -1 else None, ",",
            #         1 if c_offset == 1 else None, ":",
            #         -1 if c_offset == -1 else None, ")")
            # print(edge_weights)

            # img[,1:] - img[,:-1]
            # # (0,1) (0,0) left of

            # img[,:-1] - img[,1:]
            # # (0,0) (0,1) right of

            # img[1:] - img[:-1]
            # # (0, 0) (1, 0) on top of


            # img[1:] - img[:-1]
            # (0,1) (0,0)

            # Collapse along rgb dimension
            edge_weights = np.linalg.norm(edge_weights, axis=0)
            weights.append(edge_weights)
        return weights

    def to_rgb(self, img: np.ndarray) -> np.ndarray:
        return img

    def to_lab(self, img: np.ndarray) -> np.ndarray:
        '''
        We use this color space because it is used in SLIC
        '''
        img = np.transpose(rgb2lab(np.transpose(img, [1,2,0])), [2,0,1])
        # Normalize between 0 and 1
        img -= img.min()
        img /= img.max()
        return img

    def _filter_image(self, rgbd_image: RGBD_Image) -> np.ndarray:
        img = self.convert_methods[self.cfg.colorspace](rgbd_image.rgb)
        return img
