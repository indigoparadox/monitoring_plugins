#!/usr/bin/env python3

from .agent_based_api.v1 import (
    equals,
    exists,
    register,
    Service,
    SNMPTree,
    Result,
    State,
    Metric,
    render,
    OIDEnd
)

register.snmp_section(
    name = "mk_snmpsmart",
    detect = exists( '.1.3.6.1.4.1.6574.5.2.0' ),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.6574.5',
        oids = [
            OIDEnd(),
            '2', # Device
            '3', # Attribute
            '5', # Current
            '6', # Worst
            '7', # Threshold
            '8' # Raw
        ],
    ),
)

def discover_mk_snmpsmart( section ):
    found_devs = []
    for i in section:
        if i[1] not in found_devs:
            yield Service( item=i[1] )
            found_devs.append( i[1] )

def check_mk_snmpsmart( item, params, section ):

    for section_i in section:

        # Skip other device data.
        device = section_i[1]
        if device != item:
            continue

        attribute = section_i[2]
        val_cur = int( section_i[3] )
        val_worst = int( section_i[4] )
        val_threshold = int( section_i[5] )
        val_raw = -1
        try:
            val_raw = int( section_i[6] )
        except ValueError:
            pass

        # Evaluate thresholds.
        status_text = 'Value OK'
        status = State.OK
        if val_worst < val_threshold:
            status_text = 'Worst value below threshold'
            status = State.WARN
        if val_cur < val_threshold:
            status_text = 'Current value below threshold'
            status = State.CRIT

        if 0 <= val_raw:
            yield Metric( attribute, val_cur )
        yield Result( state=status,
            summary='{}: {} (Value: {}, Worst: {}{})'.format(
                attribute, status_text, val_cur, val_worst,
                ', Raw: {}'.format( val_raw ) if 0 <= val_raw else '' ) )

register.check_plugin(
    name="mk_snmpsmart",
    service_name="Disk %s SMART",
    discovery_function=discover_mk_snmpsmart,
    check_function=check_mk_snmpsmart,
    check_default_parameters={},
    check_ruleset_name="mk_snmpsmart"
)

