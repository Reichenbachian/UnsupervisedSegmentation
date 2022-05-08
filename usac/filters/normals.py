'''
Author: Alex Reichenbach
Date: May 7, 2022
'''
import cv2
import numpy as np

from usac.filters.filter import Filter
from usac.data.rgbd_image import RGBD_Image

class NormalFilter(Filter):
    def __init__(self, cfg):
        self.cfg = cfg

    def _filter_image(self, rgbd: RGBD_Image) -> np.ndarray:
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
        rows, cols = rgbd.depth.shape

        # zx = cv2.Sobel(rgbd.depth, cv2.CV_64F, 1, 0, ksize=5)     
        # zy = cv2.Sobel(rgbd.depth, cv2.CV_64F, 0, 1, ksize=5)

        zx, zy = np.gradient(rgbd.depth)

        zx = zx.clip(-self.cfg.max_grad, self.cfg.max_grad)
        zy = zy.clip(-self.cfg.max_grad, self.cfg.max_grad)

        zx -= zx.min()
        zy -= zy.min()
        zx /= zx.max()
        zy /= zy.max()


        # import matplotlib.pyplot as plt
        # plt.imshow(zx)
        # plt.show()

        breakpoint()

        return np.stack([zx, zy])
