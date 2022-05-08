import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

from usac.visualizations.visualizer import Visualizer
from usac.visualizations.utils import labels_for_timestep
from usac.visualizations.utils import cmap_for_timestep

class ClickSplitVisualizer(Visualizer):
    def __init__(self, cfg):
        self.cfg = cfg

    def update(self, ev, ax, fig, dendogram: np.ndarray) -> None:
        x, y = int(ev.xdata), int(ev.ydata)
        label_to_split = self.current_labels[y, x]
        timestep = np.where(dendogram == label_to_split - 1)[0][0]
        labels = labels_for_timestep(dendogram, timestep, self.rows, self.cols)
        ax.imshow(labels)

        fig.canvas.draw_idle()

    def visualize(self, labels: np.ndarray,
                  rgb: np.ndarray = None,
                  depth: np.ndarray = None,
                  dendogram: np.ndarray = None) -> None:
        self.rows, self.cols = labels.shape
        self.current_labels = np.ones((self.rows, self.cols), dtype=np.int32)
        self.current_labels.fill(dendogram.max() + 1)

        fig, ax = plt.subplots()
        ax.imshow(self.current_labels)
        cid = fig.canvas.mpl_connect('button_release_event', lambda ev: self.update(ev, ax, fig, dendogram))
        plt.show()
