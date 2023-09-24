#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.i18n import _
from cmk.gui.plugins.metrics import metric_info

metric_info["read_bytes_sec"] = {
    "title": _( "Read Bytes/sec" ),
    "unit": "bytes/s",
    "color": "#00ff88",
}

metric_info["write_bytes_sec"] = {
    "title": _( "Write Bytes/sec" ),
    "unit": "bytes/s",
    "color": "#0088ff",
}

