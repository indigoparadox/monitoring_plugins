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
    OIDEnd,
    get_value_store
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

def check_mk_snmpsmart_thresh( val_cur, val_worst, val_threshold ):
    
    ''' Evaluate thresholds. '''

    status_text = 'Value OK'
    status = State.OK
    if val_worst < val_threshold:
        status_text = 'Worst value below threshold'
        status = State.WARN
    if val_cur < val_threshold:
        status_text = 'Current value below threshold'
        status = State.CRIT

    return status, status_text

def check_mk_snmpsmart( item, params, section ):

    pv = get_value_store()
    report_success = []
    if not item in pv:
        pv[item] = {}
    for section_i in section:

        # Skip other device data.
        device = section_i[1]
        if device != item:
            continue

        # Fail and keep moving on bad lines.
        if 'echo: write error on stdout' in section_i:
            return

        if '' in section_i:
            continue

        # Translate section columns to variables.
        attribute = section_i[2]
        val_cur = int( section_i[3] ) if '' != section_i[3] else -1
        val_worst = int( section_i[4] ) if '' != section_i[4] else -1
        val_threshold = int( section_i[5] ) if '' != section_i[5] else -1
        val_raw = int( section_i[6] )

        assert 0 <= val_cur
        assert 0 <= val_worst
        assert 0 <= val_threshold
        assert 0 <= val_raw
        assert '' != attribute

        status, status_text = \
            check_mk_snmpsmart_thresh( val_cur, val_worst, val_threshold )

        yield Metric( attribute, val_cur )

        yield Result( state=status,
            summary='{}: {} (Value: {}, Worst: {}, Raw: {})'.format(
                attribute, status_text, val_cur, val_worst, val_raw ) )

        # Report was successful, so cache value and add to success list.
        report_success.append( attribute )
        if not attribute in pv[device]:
            pv[device][attribute] = {
                'value': val_cur,
                'val_worst': val_worst,
                'val_raw': val_raw,
                'val_threshold': val_threshold }

    # Report cached values for any missing from the last stanza.
    # TODO: Expire cache based on age?
    for attribute in pv[item]:
        if not attribute in report_success:
            status, status_text = check_mk_snmpsmart_thresh(
                pv[device][attribute]['value'],
                pv[device][attribute]['val_worst'],
                pv[device][attribute]['val_threshold'] )
            yield Result( state=status,
                summary='{} (Cached): {} (Value: {}, Worst: {}, Raw: {})'.format(
                    attribute,
                    status_text,
                    pv[device][attribute]['value'],
                    pv[device][attribute]['val_worst'],
                    pv[device][attribute]['val_raw'] ) )

register.check_plugin(
    name="mk_snmpsmart",
    service_name="Disk %s SMART",
    discovery_function=discover_mk_snmpsmart,
    check_function=check_mk_snmpsmart,
    check_default_parameters={},
    check_ruleset_name="mk_snmpsmart"
)

