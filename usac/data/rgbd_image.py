import cv2
import json
from PIL import Image
import numpy as np
import os
from typing import Tuple

class RGBD_Image():
    def __init__(self, root, scale: float = 1.0):
        self.rgb = self.read_rgb(root)
        self.depth = self.read_depth(root)

        if scale != 1:
            self.rgb, self.depth = self.scale_images(scale)

    def scale_images(self, scale: float) -> Tuple[np.ndarray, np.ndarray]:
        new_r, new_c = (np.array(self.shape) * scale).astype(int)
        rgb_img = np.transpose(self.rgb, [1,2,0])
        rgb_img = cv2.resize(rgb_img, dsize=(new_c, new_r), interpolation=cv2.INTER_CUBIC)
        new_rgb = np.transpose(rgb_img, [2,0,1])
        new_depth = cv2.resize(self.depth, dsize=(new_c, new_r), interpolation=cv2.INTER_NEAREST)

        return new_rgb, new_depth

    def read_rgb(self, root):
        rgb_path = os.path.join(root, "rgb/front0/000000.png")
        img = np.array(Image.open(rgb_path))
        img = img / 255
        img = np.transpose(img, [2, 0, 1])
        return img.astype(np.float32).clip(0,1)


    def read_depth(self, root):
        # It's disparity, convert to depth
        depth_path = os.path.join(root, "disp_gt/front0/000000.png")
        config_path = os.path.join(root, "disp_gt/metadata.json")

        with open(config_path, 'r') as f:
            config_data = json.load(f)

        arr = cv2.imread(os.fspath(depth_path), cv2.IMREAD_ANYDEPTH)
        arr = arr * float(config_data['resolution'])
        return arr

    @property
    def shape(self):
        assert self.rgb.shape[1:] == self.depth.shape
        return self.depth.shape
