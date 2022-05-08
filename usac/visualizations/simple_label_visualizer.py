import matplotlib.pyplot as plt
import numpy as np

class SimpleLabelVisualizer():
    def __init__(self, cfg):
        assert cfg.overlay == False, "Haven't done this yet"

    def visualize(self, labels, rgb=None, depth=None, dendogram=None) -> None:
        rgb = np.transpose(rgb, [1,2,0])
        if rgb is not None:
            cm = plt.get_cmap('tab20')
            # Apply the colormap like a function to any array:
            labels = cm(labels)[:,:,:3]

            # maximize visualization
            labels -= labels.min()
            labels /= labels.max()

        img = np.concatenate([rgb, labels])
        img = img.clip(0, 1)

        plt.imshow(img)
        plt.show()
