import matplotlib.pyplot as plt
import numpy as np

class SimpleLabelVisualizer():
    def __init__(self, cfg):
        assert cfg.overlay == False, "Haven't done this yet"
        pass

    def visualize(self, labels, rgb_img=None, depth_img=None) -> None:
        # rgb_img = np.transpose(rgb_img, [1,2,0])
        # if rgb_img is not None:
        #     cm = plt.get_cmap('viridis')
        #     # Apply the colormap like a function to any array:
        #     labels = cm(labels)[:,:,:3]

        #     # maximize visualization
        #     labels -= labels.min()
        #     labels /= labels.max()

        plt.imshow(labels)
        plt.show()

        breakpoint()
        img = np.concatenate([rgb_img, labels])

        plt.imshow(img)
        plt.show()
