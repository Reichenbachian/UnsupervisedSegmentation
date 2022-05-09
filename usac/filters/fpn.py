'''
Author: Alex Reichenbach
Date: May 7, 2022
'''
import cv2
import numpy as np
import torch
import torchvision


from usac.filters.filter import Filter
from usac.data.rgbd_image import RGBD_Image

class FPNFilter(Filter):
    def __init__(self, cfg):
        self.cfg = cfg
        self.model = torchvision.models.segmentation.fcn_resnet101(True, pretrained_backbone=True)

    def _filter_image(self, rgbd: RGBD_Image) -> np.ndarray:
        with torch.no_grad():
            img = torch.from_numpy(rgbd.rgb)[None]
            features = self.model(img)['out'][0].cpu().numpy()
        # Maybe a better way of doing this
        features -= features.min()
        features /= features.max()

        return features
