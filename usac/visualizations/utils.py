from numba import jit
import numpy as np

CACHE = {}

@jit(nopython=True, nogil=True, cache=True, fastmath=True, parallel=True)
def _labels_for_timestep(dendogram: np.ndarray, timestep: int,
                        rows: int, cols: int) -> np.ndarray:
    labels = np.arange(rows * cols)
    new_cluster_label = rows * cols
    for i in range(timestep):
        left_cluster, right_cluster = dendogram[i]
        mask = (labels == left_cluster) | (labels == right_cluster)
        labels[mask] = new_cluster_label
        new_cluster_label += 1
    return labels



def labels_for_timestep(dendogram: np.ndarray, timestep: int,
                        rows: int, cols: int) -> np.ndarray:
    if timestep in CACHE:
        return CACHE[timestep]

    labels = _labels_for_timestep(dendogram, timestep, rows, cols)
    # Reset to lower values
    unique, labels = np.unique(labels, return_inverse=True)
    print(f"Step: {timestep}, Num Clusters: {len(unique)}")
    res = labels.reshape(rows, cols)
    CACHE[timestep] = res
    return res


def cmap_for_timestep(dendogram: np.ndarray, timestep: int,
                      rows: int, cols: int) -> np.ndarray:
    pass