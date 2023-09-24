#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.plugins.metrics import perfometer_info

perfometer_info.append({
    "type": "linear",
    "segments": ["zpool_read_bytes_sec", "zpool_write_bytes_sec"],
    "total": 2000000.0
})

