
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.metrics import metric_info

metric_info["arc_sz"] = {
    "title": _( "ARC Size" ),
    "unit": "bytes",
    "color": "#ffff88",
}

metric_info["arc_meta_sz"] = {
    "title": _( "ARC Metadata Size" ),
    "unit": "bytes",
    "color": "#0088ff",
}

metric_info["arc_data_sz"] = {
    "title": _( "ARC Data Size" ),
    "unit": "bytes",
    "color": "#00ff88",
}

metric_info["arc_cache_hit_ratio"] = {
    "title": _( "ARC Cache Hit Ratio" ),
    "unit": "%",
    "color": "#00ff88",
}

metric_info["arc_cache_miss_ratio"] = {
    "title": _( "ARC Cache Miss Ratio" ),
    "unit": "%",
    "color": "#ff8888",
}

