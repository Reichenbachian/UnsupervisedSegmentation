from usac.filters.depth import DepthFilter
from usac.filters.linear_gradient import LinearGradient
from usac.filters.color import ColorFilter
from usac.filters.normals import NormalFilter
from usac.filters.fpn import FPNFilter
from usac.config import ColorFilterOptions, LinearGradientOptions, DepthFilterOptions, NormalFilterOptions, FPNFilterOptions


FILTERS = {'color': (ColorFilter, ColorFilterOptions),
           'linear': (LinearGradient, LinearGradientOptions),
           'depth': (DepthFilter, DepthFilterOptions),
           'normal': (NormalFilter, NormalFilterOptions),
           'fpn': (FPNFilter, FPNFilterOptions)
          }

def resolve_filters(filter_list):
    filters = []
    for filter_name in filter_list:
        assert filter_name in FILTERS, f"Filter {filter_name} is not implemented. Options are {FILTERS.keys()}"
        c, cfg = FILTERS[filter_name.lower()]
        filters.append(c(cfg))
    return filters
