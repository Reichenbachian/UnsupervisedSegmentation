from usac.filters.rgb import RGBFilter
from usac.filters.linear_gradient import LinearGradient
from usac.config import RGBFilterOptions, LinearGradientOptions


FILTERS = {'rgb': (RGBFilter, RGBFilterOptions),
           'linear': (LinearGradient, LinearGradientOptions)}

def resolve_filters(filter_list):
    filters = []
    for filter_name in filter_list:
        assert filter_name in FILTERS, f"Filter {filter_name} is not implemented. Options are {FILTERS.keys()}"
        c, cfg = FILTERS[filter_name.lower()]
        filters.append(c(cfg))
    return filters
