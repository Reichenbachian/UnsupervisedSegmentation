'''
Author: Alex Reichenbach
Date: May 7, 2022
'''
import cv2
import numpy as np

from usac.filters.filter import Filter
from usac.data.rgbd_image import RGBD_Image

class FPNFilter(Filter):
    def __init__(self, cfg):
        self.cfg = cfg

    def _filter_image(self, rgbd: RGBD_Image) -> np.ndarray:
        raise NotImplementedError()
