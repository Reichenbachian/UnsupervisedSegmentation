import numpy as np

from usac.filters.filter import Filter
from usac.data.rgbd_image import RGBD_Image

class DepthFilter(Filter):
    def _filter_image(self, rgbd_image: RGBD_Image) -> np.ndarray:
        depth_img = rgbd_image.depth
        return (depth_img / depth_img.max())[None]
