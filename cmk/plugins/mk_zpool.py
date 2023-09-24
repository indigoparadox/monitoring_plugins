
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

ZPOOL_HEALTH = [
    'ONLINE',
    'DEGRADED',
    'FAULTED',
    'OFFLINE',
    'UNAVAIL',
    'REMOVED'
]

register.snmp_section(
    name = "mk_zpool",
    detect = exists( '.1.3.6.1.4.1.50536.1.1.1.1.2.1' ),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.50536.1.1.1.1',
        oids = [
            OIDEnd(),
            '2', # Device
            '7', # Health
            '10', # IORead
            '11' # IOWrite
        ],
    ),
)

def discover_mk_zpool( section ):
    for i in section:
        yield Service( item='{} IO'.format( i[1] ) )
        yield Service( item='{} Health'.format( i[1] ) )

def check_mk_zpool_io( idx, params, section ):

    device = section[idx][1]
    ior = float( section[idx][2] )
    iow = float( section[idx][3] )
    time_now = time.time()

    pv = get_value_store()
    pv_key_r = 'zpool_pv_{}_read'.format( device )
    pv_key_w = 'zpool_pv_{}_write'.format( device )

    # Ensure previous values exist.
    if not pv.get( 'zpool_pv_time' ):
        pv['zpool_pv_time'] = time_now
    if not pv.get( pv_key_r ):
        pv[pv_key_r] = ior
    if not pv.get( pv_key_w ):
        pv[pv_key_w] = iow

    # Perform calculations.
    time_diff = time_now - pv['zpool_pv_time']
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
    pv['zpool_pv_time'] = time_now
    pv[pv_key_r] = ior
    pv[pv_key_w] = iow

    yield Metric( "zpool_read_bytes_sec", ior_diff )
    yield Metric( "zpool_write_bytes_sec", iow_diff )
    yield Result( state=State.OK, summary='Read: {}, Write: {}'.format(
        render.iobandwidth( ior_diff ), render.iobandwidth( iow_diff ) ) )

def check_mk_zpool( item, params, section ):

    # Get the SNMP index from the pool name.
    item_arr = item.split( ' ' )
    idx = 0
    for i in section:
        if i[1] == item_arr[0]:
            break
        idx += 1

    # TODO: Handle missing device?

    if 'IO' == item_arr[1]:
        # Pass along IO results.
        for res in check_mk_zpool_io( idx, params, section ):
            yield res
    elif 'Health' == item_arr[1]:
        health = int( section[idx][2] )
        yield Result( state=State.OK if 0 == health else State.CRIT,
            summary='{}'.format( ZPOOL_HEALTH[health] ) )

register.check_plugin(
    name="mk_zpool",
    service_name="ZPool %s",
    discovery_function=discover_mk_zpool,
    check_function=check_mk_zpool,
    check_default_parameters={
        'ior_warn': 100,
        'ior_crit': 100,
        'iow_warn': 100,
        'iow_crit': 100  },
    check_ruleset_name="mk_zpool"
)

