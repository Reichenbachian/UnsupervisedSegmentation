import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np

from usac.visualizations.visualizer import Visualizer

class ScrollerVisualizer(Visualizer):
    def visualize(self, labels: np.ndarray,
                  rgb: np.ndarray = None,
                  depth: np.ndarray = None,
                  dendogram: np.ndarray = None) -> None:

        # Setting Plot and Axis variables as subplots() function returns tuple(fig, ax)
        fig, axs = plt.subplots()
         
        # Adjust the bottom size according to the requirement of the user
        plt.subplots_adjust(bottom=0.25)
         
        # Set the x and y axis to some dummy data
        t = np.arange(0.0, 100.0, 0.1)
        s = np.sin(2*np.pi*t)
         
        # plot the x and y using plot function
        l = plt.plot(t, s)
         
        # Set the axis and slider position in the plot
        axis_position = plt.axes([0.2, 0.1, 0.65, 0.03],
                                 facecolor = 'White')
        slider_position = Slider(axis_position,
                                 'Pos', 0.1, 90.0)
         
        # update() function to change the graph when the
        # slider is in use
        def update(val):
            pos = slider_position.val
            axs.axis([pos, pos+10, -1, 1])
            fig.canvas.draw_idle()
         
        # update function called using on_changed() function
        slider_position.on_changed(update)
         
        # Display the plot
        plt.show()



        # import itertools
        # ii = itertools.count(198 * 288)
        # for x in dendogram:
        #     print({'node_id': next(ii), 'left': x[0], 'right':x[1]})
        # breakpoint()

        # rgb_img = np.transpose(rgb_img, [1,2,0])
        # if rgb_img is not None:
        #     cm = plt.get_cmap('tab20')
        #     # Apply the colormap like a function to any array:
        #     labels = cm(labels)[:,:,:3]

        #     # maximize visualization
        #     labels -= labels.min()
        #     labels /= labels.max()

        # img = np.concatenate([rgb_img, labels])

        # plt.imshow(img)
        plt.show()
