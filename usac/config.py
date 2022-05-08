class ColorFilterOptions:
    colorspace = 'lab'


class ClustererOptions:
    weights = {'color': 1.0,
               'linear': 0.1,
               'depth': 1.0,
               'normal': 0.1,
               'fpn': 1.0
               }

class SimpleLabelVisualizerOptions:
    overlay = False

class LinearGradientOptions:
    pass

class DepthFilterOptions:
    pass

class NormalFilterOptions:
    max_grad = 1 #200


class FPNFilterOptions:
    max_grad = 5

class ScrollerVisualizerOptions:
    pass