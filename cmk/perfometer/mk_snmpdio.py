#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cmk.gui.plugins.metrics import perfometer_info

perfometer_info.append({
    "type": "linear",
    "segments": ["read_bytes_sec", "write_bytes_sec"],
    "total": 2000000.0
})

