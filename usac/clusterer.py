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

        # Weighted sum of weights
        edge_weights = np.zeros((rows, cols))
        for filter_name in filter_dict:
            weights = weight_dict[filter_name]
            filter_weight = self.cfg.weights[filter_name]
            edge_weights += filter_weight * weights
        
        # Edge weights are size (r, c)
        breakpoint()

        # # A grid of X=()
        # c_coords, r_coords = np.meshgrid(np.arange(cols), np.arange(rows))
        # c_coords = c_coords.astype(np.int32).reshape(-1)
        # r_coords = r_coords.astype(np.int32).reshape(-1)
        # edge_weights = edge_weights.reshape(8, -1) # Flatten image

        # from_idxs = [] 
        # to_idxs = []
        # data = []

        # for (r_offset, c_offset), directional_data in zip(self.offsets, edge_weights):
        #     # Position in array is r*cols + c 
        #     from_coord = r_coords * cols + c_coords

        #     offset_c_arr = c_coords + c_offset
        #     offset_r_arr = r_coords + r_offset
        #     to_coord = offset_r_arr * cols + offset_c_arr

        #     # Some indices are invalid
        #     valid_mask = ~((offset_c_arr < 0) | (offset_c_arr >= cols) | \
        #                    (offset_r_arr < 0) | (offset_r_arr >= rows))
        #     from_coord = from_coord[valid_mask]
        #     to_coord = to_coord[valid_mask]
        #     directional_data = directional_data[valid_mask]


        #     from_idxs.append(from_coord)
        #     to_idxs.append(to_coord)
        #     data.append(directional_data)

        # # Duplicate for a symmetric graph
        # row_idxs = np.concatenate(from_idxs + to_idxs)
        # col_idxs = np.concatenate(to_idxs + from_idxs)
        # data = np.concatenate(data + data)


        # Shape of CSR array is r*c, r*c
        distance_matrix = csr_array((data, (row_idxs, col_idxs)), shape=(rows*cols, rows*cols))

        n_clusters = 15
        connectivity = grid_to_graph((rows, cols))
        breakpoint()
        clusterer = AgglomerativeClustering(n_clusters=n_clusters,
                                       linkage='ward',
                                       connectivity=connectivity).fit()
        
        label = ward.labels_.reshape(rows, cols)

        clusterer = hdbscan.HDBSCAN(min_cluster_size=10,
                                    # min_sample=10,
                                    max_dist=1000000,
                                    metric="precomputed",
                                    core_dist_n_jobs=-1)
        labels = clusterer.fit_predict(distance_matrix)

        breakpoint()

        # from sklearn.cluster import SpectralClustering
        # clusterer = SpectralClustering(n_clusters=3,
        #                                n_neighbors=3,
        #                                affinity='precomputed_nearest_neighbors')

        # clusterer = AgglomerativeClustering(n_clusters=10,
        #                                     affinity="precomputed")
        # labels = clusterer.fit_predict(distance_matrix)
        # import matplotlib.pyplot as plt
        # clusterer.condensed_tree_.plot()
        # plt.show()
        tree = clusterer.condensed_tree_.to_numpy()
        return labels.reshape(rows, cols), tree
