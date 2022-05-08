from numba import jit
import numpy as np

@jit
def _labels_for_timestep(dendogram: np.ndarray, timestep: int,
                        rows: int, cols: int) -> np.ndarray:
    labels = np.arange(rows * cols)
    new_cluster_label = rows * cols
    for i in range(timestep):
        left_cluster, right_cluster = dendogram[i]
        labels[labels == left_cluster] = new_cluster_label
        labels[labels == right_cluster] = new_cluster_label
        new_cluster_label += 1
    return labels



def labels_for_timestep(dendogram: np.ndarray, timestep: int,
                        rows: int, cols: int) -> np.ndarray:
    labels = _labels_for_timestep(dendogram, timestep, rows, cols)
    # Reset to lower values
    unique, labels = np.unique(labels, return_inverse=True)
    print(f"Step: {timestep}, Num Clusters: {len(unique)}")
    return labels.reshape(rows, cols)
