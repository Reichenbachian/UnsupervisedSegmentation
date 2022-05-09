import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

from usac.visualizations.visualizer import Visualizer
from usac.visualizations.utils import labels_for_timestep



class ScrollerVisualizer(Visualizer):
    def update_labels(self, val: float, dendogram:np.ndarray, fig, ax, rows: int, cols: int):
        base = 1.5
        largest_val = np.log(10) / np.log(base)
        multiplier = (self.rows * self.cols - 1) / largest_val
        self.timestep = int(np.log(val) * multiplier / np.log(base))
        labels = labels_for_timestep(dendogram, self.timestep, self.rows, self.cols)
        plt.gca().set_prop_cycle(None)
        ax.imshow(labels, cmap='tab20')
        fig.canvas.draw_idle()

    def on_press(self, event, dendogram: np.ndarray, fig, ax, im):
        if event.key == 'd':
            self.timestep += 1
        elif event.key == 'u':
            self.timestep -= 1
        labels = labels_for_timestep(dendogram, self.timestep, self.rows, self.cols)
        # ax.imshow(labels, cmap='tab20')
        im.set_data(self.cmap(labels))
        fig.canvas.draw_idle()

    def visualize(self, labels: np.ndarray,
                  rgb: np.ndarray = None,
                  depth: np.ndarray = None,
                  dendogram: np.ndarray = None) -> None:
        self.rows, self.cols = labels.shape
        self.timestep = len(dendogram) - 5
        self.cmap = plt.cm.get_cmap('tab20')

        labels = labels_for_timestep(dendogram, self.timestep, self.rows, self.cols)
        fig, ax = plt.subplots()
        axcolor = 'lightgoldenrodyellow'
        axmin = fig.add_axes([0.25, 0.1, 0.65, 0.03])
        slider_position = Slider(axmin, "Log step", 1, 10, self.timestep)
        im = ax.imshow(self.cmap(labels))
        # update function called using on_changed() function
        slider_position.on_changed(lambda x: self.update_labels(x, dendogram, fig, ax, self.rows, self.cols))
        fig.canvas.mpl_connect('key_press_event', lambda ev: self.on_press(ev, dendogram, fig, ax, im))
        plt.show()

