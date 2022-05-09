import click
import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt

from usac.filters import resolve_filters, FILTERS
from usac.data.rgbd_image import RGBD_Image
from usac.clusterer import Clusterer
from usac.config import ClustererOptions, ScrollerVisualizerOptions
from usac.visualizations import resolve_visualizer

def segment_image(rgbd_img: RGBD_Image, filter_names: str, scale: float) -> (np.ndarray, np.ndarray):
    print("Segmenting Image")

    filters = resolve_filters(filter_names)
    graph_weights = {}
    for name, filter in zip(filter_names, filters):
        weights = filter.filter_image(rgbd_img)
        assert weights.shape[1:] == (rgbd_img.shape[0], rgbd_img.shape[1])
        graph_weights[name] = weights
    
    # Run clustering
    clusterer = Clusterer(ClustererOptions)
    clusters, dendogram = clusterer.cluster(graph_weights)

    return clusters, dendogram

def visualize_segmentations(viz_name: str, segmentations: np.ndarray,
        rgbd_image: RGBD_Image, dendogram: np.ndarray) -> None:
    print("Visualizing Image...")
    viz = resolve_visualizer(viz_name)
    viz.visualize(segmentations, rgb=rgbd_image.rgb,
                  depth=rgbd_image.depth, dendogram=dendogram)

@click.command()
@click.argument("folder_path", type=str)
@click.option("--filter", "filters", type=str, multiple=True, default=["all"], help="Options are color, linear, depth, normal, fpn, or all")
@click.option("--scale", default=1, type=float, help="How to scale the input image. 1 = 100%")
@click.option("--viz", default="simple", type=str, help='Options are simple, scroller, and clicksplit')
def main(folder_path, filters, scale, viz):
    if len(filters) == 1 and filters[0].lower() == 'all':
        filters = FILTERS.keys()

    rgbd_img = RGBD_Image(folder_path, scale)

    segmentations, dendogram = segment_image(rgbd_img, filters, scale)

    visualize_segmentations(viz, segmentations, rgbd_img, dendogram)

if __name__ == "__main__":
    main()
