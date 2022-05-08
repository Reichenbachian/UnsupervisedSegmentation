# Unsupervised Segmentation through Agglomerative Clustering

Supervised image segmentation is a well studied problem. Recently, convolutional neural networks (CNNs) have become the most common method for supervised image segmentation. However, in most cases, CNNs require supervised data in order to train segmentation models. We present USAC (Unsupervised Segmentation through Agglomerative Clustering). Our method uses several novel signals to augment the conventional methodology, including incorporating depth images. Unsupervised segmentation is a naturally ill-posed problem, there are many possible output segmentations for a single input image. Thus, we include an interactive framework that intelligently let's users increase or decrease the specificity of a specific labelling. All our work is publicly available and open source.

![Example Segmentation](doc_imgs/Figure_1.png)

This project is an unsupervised segmentation approach that augments the process via interactivity and depth.

Future Features:
	-  Can blur first before RGBFilter
	-  Add option for normalizing color per channel
