import numpy as np

class Visualizer:
    def __init__(self, cfg):
        self.cfg = cfg

    def visualize(self, labels,
                  rgb: np.ndarray = None,
                  depth: np.ndarray = None,
                  dendogram: np.ndarray = None) -> None:
        raise NotImplementedError()