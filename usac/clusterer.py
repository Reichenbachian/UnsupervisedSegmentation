import numpy as np
from typing import List, Dict
import hdbscan
from scipy.sparse import csr_array
from sklearn.cluster import AgglomerativeClustering
from sklearn.feature_extraction.image import grid_to_graph

class Clusterer():
    offsets = [[0, -1],
               [-1, -1],
               [-1, 0],
               [-1, 1],
               [0, 1],
               [1, 1],
               [1, 0],
               [1, -1]]

    # 0) Left, (r, c - 1)
    # 1) Left up, (r - 1, c - 1)
    # 2) Up, (r - 1, c)
    # 3) Up right, (r - 1, c + 1)
    # 4) Right, (r, c + 1)
    # 5) Right Down, (r + 1, c + 1)
    # 6) Down, (r + 1, c)
    # 7) Down Left, (r + 1, c - 1)
    def __init__(self, cfg):
        self.cfg = cfg

    def cluster(self, filter_dict: Dict[str, np.ndarray]):
        '''
        Input
            - weights: A dict of {"rgb": (8, r, c)}
        Returns:
            - A dendogram in array form?
        '''
        assert len(filter_dict) > 0, "There needs to be at least one filter"

        # Grab first shape
        _, rows, cols = filter_dict[list(filter_dict.keys())[0]].shape

        # Create feature vector
        weighted_filters = []

        # Weight each of the filters
        for filter_name in filter_dict:
            weighted_filter = filter_dict[filter_name] * self.cfg.weights[filter_name]
            weighted_filters.append(weighted_filter)
        filtered_vector = np.concatenate(weighted_filters, axis=0) # (f, r, c)

        # Transpose featuer vector to correct size
        num_features = filtered_vector.shape[0]
        filtered_vector = np.transpose(filtered_vector, [1, 2, 0]) # (r, c, f)
        filtered_vector = filtered_vector.reshape(-1, num_features)

        # Run agglomerative clustering
        n_clusters = 15
        connectivity = grid_to_graph(rows, cols)
        clusterer = AgglomerativeClustering(n_clusters=n_clusters,
                                       linkage='ward',
                                       connectivity=connectivity).fit(filtered_vector)
        
        labels = clusterer.labels_.reshape(rows, cols)

        return labels, None
