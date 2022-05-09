import copy
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

from usac.visualizations.visualizer import Visualizer
from usac.visualizations.utils import labels_for_timestep
from usac.visualizations.utils import cmap_for_timestep

def idxs_to_coords(idxs: np.ndarray, rows: int, cols: int):
    idxs = np.array(idxs)
    assert (idxs < rows * cols).all()
    xs = idxs % cols
    ys = idxs // cols
    return xs, ys

def split_label(label: int, dendogram: np.ndarray, rows: int, cols: int):
    max_index = rows * cols
    # breakpoint()
    # print(f"exploring label {label}")
    if label < max_index:
        return label, "", [label], []

    subcluster_1, subcluster_2 = dendogram[label - max_index]

    # Right side of tree
    _, _, c1, c2 = split_label(subcluster_1, dendogram, rows, cols)
    left_cluster = c1 + c2

    # Left side of tree
    _, _, c1, c2 = split_label(subcluster_2, dendogram, rows, cols)
    right_cluster = c1 + c2

    return subcluster_1, subcluster_2, left_cluster, right_cluster

class ClickSplitVisualizer(Visualizer):
    def __init__(self, cfg):
        self.cfg = cfg

    def clicked(self, ev, ax, fig, im, dendogram: np.ndarray) -> None:
        x, y = int(ev.xdata), int(ev.ydata)
        current_label = self.current_labels[y, x]

        # print("BEFORE", np.unique(self.current_labels))

        if self.mode == 'join':
            if current_label >= self.rows*self.cols + len(dendogram):
                print("You've reached the top of the tree. Click on another color...")
            else:
                row = np.where(current_label == dendogram)[0][0]
                c1, c2 = dendogram[row]
                mask = (self.current_labels == c1) | (self.current_labels == c2)
                self.current_labels[mask] = self.rows * self.cols + row
        else:
            newlabel1, newlabel2, c1, c2 = split_label(current_label, dendogram, self.rows, self.cols)
            c1x, c1y = idxs_to_coords(c1, self.rows, self.cols)
            c2x, c2y = idxs_to_coords(c2, self.rows, self.cols)
            self.current_labels[c1y, c1x] = newlabel1
            self.current_labels[c2y, c2x] = newlabel2

        # print("AFTER", np.unique(self.current_labels))
        # print('------')

        # Reset labels to something low
        tmp_labels = self.current_labels.reshape(-1)
        unique, tmp_labels = np.unique(tmp_labels, return_inverse=True)

        im.set_data(self.cmap(tmp_labels.reshape(self.rows, self.cols)))
        im.autoscale()
        fig.canvas.draw_idle()

    def pressed(self, ev):
        if ev.key == 'p':
            print("Split mode...")
            self.mode = 'split'
        elif ev.key == 'j':
            print("Join mode...")
            self.mode = 'join'

    def visualize(self, labels: np.ndarray,
                  rgb: np.ndarray = None,
                  depth: np.ndarray = None,
                  dendogram: np.ndarray = None) -> None:
        self.rows, self.cols = labels.shape
        self.current_labels = np.ones((self.rows, self.cols), dtype=np.int32)
        self.current_labels.fill(dendogram.max() + 1)
        self.mode = 'split'
        self.cmap = plt.cm.get_cmap('tab20')

        fig, ax = plt.subplots()
        im = ax.imshow(self.cmap(self.current_labels), vmin=0, vmax=255)
        im.autoscale()
        fig.canvas.mpl_connect('button_release_event', lambda ev: self.clicked(ev, ax, fig, im, dendogram))
        fig.canvas.mpl_connect('key_press_event', lambda ev: self.pressed(ev))
        plt.show()
