import click
import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt

from usac.filters import resolve_filters
from usac.data.rgbd_image import RGBD_Image
from usac.clusterer import Clusterer
from usac.config import ClustererOptions, SimpleLabelVisualizerOptions
from usac.visualizations import SimpleLabelVisualizer

def segment_image(rgbd_img: RGBD_Image, filter_names: str, scale: float) -> np.ndarray:
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

	return clusters

def visualize_segmentations(segmentations: np.ndarray, rgbd_image: RGBD_Image) -> None:
	print("Visualizing Image...")
	viz = SimpleLabelVisualizer(SimpleLabelVisualizerOptions)
	viz.visualize(segmentations, rgbd_image.rgb)

@click.command()
@click.argument("folder_path", type=str)
@click.option("--filter", "filters", type=str, multiple=True, default=["rgb", "linear"])
@click.option("--scale", default=1, type=float)
def main(folder_path, filters, scale):
	rgbd_img = RGBD_Image(folder_path, scale)

	segmentations = segment_image(rgbd_img, filters, scale)

	visualize_segmentations(segmentations, rgbd_img)

if __name__ == "__main__":
	main()
