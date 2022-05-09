from usac.visualizations.visualizer import Visualizer
from usac.visualizations.simple_label_visualizer import SimpleLabelVisualizer
from usac.visualizations.scroller_visualizer import ScrollerVisualizer
from usac.visualizations.click_split import ClickSplitVisualizer
from usac.config import SimpleLabelVisualizerOptions, ScrollerVisualizerOptions, ClickSplitVisualizerOptions

VIZS = {'simple': (SimpleLabelVisualizer, SimpleLabelVisualizerOptions),
        'scroller': (ScrollerVisualizer, ScrollerVisualizerOptions),
        'clicksplit': (ClickSplitVisualizer, ClickSplitVisualizerOptions)
       }

def resolve_visualizer(viz_name):
    viz_name = viz_name.lower()
    assert viz_name in VIZS, f"Filter {viz_name} is not implemented. Options are {VIZS.keys()}"
    c, cfg = VIZS[viz_name]
    return c(cfg)
