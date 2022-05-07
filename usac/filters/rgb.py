import numpy as np

from usac.filters.filter import Filter
from usac.data.rgbd_image import RGBD_Image

class RGBFilter(Filter):
    offsets = {"left": [0, -1],
               "left up": [-1, -1],
               "up": [-1, 0],
               "up right": [-1, 1],
               "right": [0, 1],
               "right down": [1, 1],
               "down": [1, 0],
               "down left": [1, -1]}

    # The graph connection to (ie to the left)
    # 0) Left, (r, c - 1)
    # 1) Left up, (r - 1, c - 1)
    # 2) Up, (r - 1, c)
    # 3) Up right, (r - 1, c + 1)
    # 4) Right, (r, c + 1)
    # 5) Right Down, (r + 1, c + 1)
    # 6) Down, (r + 1, c)
    # 7) Down Left, (r + 1, c - 1)

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

    def _filter_image(self, rgbd_image: RGBD_Image) -> np.ndarray:
        return rgbd_image.rgb 