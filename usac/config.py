class ColorFilterOptions:
    colorspace = 'lab'


class ClustererOptions:
    weights = {'color': 1.0,
               'linear': 0.2,
               'depth': 0.5,
               'normal': 0.5,
               'fpn': 0.1
               }

class LinearGradientOptions:
    pass

class DepthFilterOptions:
    pass

class NormalFilterOptions:
    max_grad = 1 #200


class FPNFilterOptions:
    max_grad = 5

## Visualizers
class SimpleLabelVisualizerOptions:
    overlay = False

class ScrollerVisualizerOptions:
    pass

class ClickSplitVisualizerOptions:
    pass

