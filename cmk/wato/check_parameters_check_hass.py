#!/usr/bin/python

group = 'activechecks'

register_rule(
    group,
    'active_checks:hass',
    Dictionary(
        title = _( 'Home Assistant API' ),
        elements = []
    )
)

