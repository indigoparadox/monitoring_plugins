#!/usr/bin/env python3

import time
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
    name = "mk_snmpdio",
    detect = exists( '.1.3.6.1.4.1.2021.13.15.1.1.2.0' ),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.2021.13.15.1.1',
        oids = [
            OIDEnd(),
            '2', # Device
            '3', # IORead
            '4' # IOWrite
        ],
    ),
)

def discover_mk_snmpdio( section ):
    for i in section:
        yield Service( item=str( i[1] ) )

def check_mk_snmpdio( item, params, section ):

    idx = 0
    for i in section:
        if i[1] == item:
            break
        idx += 1

    device = section[idx][1]
    ior = float( section[idx][2] )
    iow = float( section[idx][3] )
    time_now = time.time()

    # TODO: Handle missing device?

    pv = get_value_store()
    pv_key_r = 'snmpdio_pv_{}_read'.format( device )
    pv_key_w = 'snmpdio_pv_{}_write'.format( device )

    # Ensure previous values exist.
    if not pv.get( 'snmpdio_pv_time' ):
        pv['snmpdio_pv_time'] = time_now
    if not pv.get( pv_key_r ):
        pv[pv_key_r] = ior
    if not pv.get( pv_key_w ):
        pv[pv_key_w] = iow

    # Perform calculations.
    time_diff = time_now - pv['snmpdio_pv_time']
    ior_diff = 0
    iow_diff = 0
    if 0 < time_diff:
        ior_diff = ior - pv[pv_key_r]
        ior_diff = ior_diff / time_diff
        # Handle int32 rollover?
        if 0 > ior_diff:
            ior_diff = 0
        iow_diff = iow - pv[pv_key_w]
        if 0 > iow_diff:
            iow_diff = 0
        iow_diff = iow_diff / time_diff

    # Update stored values.
    pv['snmpdio_pv_time'] = time_now
    pv[pv_key_r] = ior
    pv[pv_key_w] = iow

    yield Metric( "read_bytes_sec", ior_diff )
    yield Metric( "write_bytes_sec", iow_diff )
    yield Result( state=State.OK, summary='Read: {}/s, Write: {}/s'.format( render.bytes( ior_diff ), render.bytes( iow_diff ) ) )

register.check_plugin(
    name="mk_snmpdio",
    service_name="Disk IO %s",
    discovery_function=discover_mk_snmpdio,
    check_function=check_mk_snmpdio,
    check_default_parameters={
        'ior_warn': 100,
        'ior_crit': 100,
        'iow_warn': 100,
        'iow_crit': 100  },
    check_ruleset_name="mk_snmpdio"
)

