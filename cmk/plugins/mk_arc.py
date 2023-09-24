#!/usr/bin/env python4

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
    name = "mk_zfs_arc",
    detect = exists( '.1.3.6.1.4.1.50536.1.4.1.0' ),
    fetch = SNMPTree(
        base = '.1.3.6.1.4.1.50536.1.4',
        oids = [
            OIDEnd(),
            '1', # Size
            '2', # Metadata Size
            '3', # Data Size
            '9', # Cache Hit Ratio
            '10' # Cache Miss Ratio
        ],
    ),
)

def discover_mk_zfs_arc( section ):
    yield Service()

def check_mk_zfs_state( val, prefix, label, rendered, params ):
    status = State.OK
    if 0 < params['{}_warn'.format( prefix )] and \
    val > params['{}_warn'.format( prefix )]:
        status = State.WARN
    elif 0 < params['{}_crit'.format( prefix )] and \
    val > params['{}_crit'.format( prefix )]:
        status = State.CRIT
    return Result( state=status, summary='{}: {}'.format( label, rendered ) )

def check_mk_zfs_arc( params, section ):

    arc_sz = int( section[0][1] )
    arc_meta_sz = int( section[0][2] )
    arc_data_sz = int( section[0][3] )
    arc_chit_rat = float( section[0][4] )
    arc_cmiss_rat = float( section[0][5] )

    # ARC SNMP calls seem to give sizes in kilobytes, metrics need bytes.
    yield Metric( "arc_sz", arc_sz * 1024 )
    yield Metric( "arc_meta_sz", arc_meta_sz * 1024 )
    yield Metric( "arc_cache_hit_ratio", arc_chit_rat )
    yield Metric( "arc_cache_miss_ratio", arc_cmiss_rat )

    # ARC SNMP calls seem to give sizes in kilobytes, render funcs need bytes.
    yield check_mk_zfs_state( arc_sz, 'sz', 'Size',
        render.bytes( arc_sz * 1024 ), params )
    yield check_mk_zfs_state( arc_meta_sz, 'meta', 'Metadata',
        render.bytes( arc_meta_sz * 1024 ), params )
    yield check_mk_zfs_state( arc_data_sz, 'data', 'Data',
        render.bytes( arc_data_sz * 1024 ), params )
    yield check_mk_zfs_state( arc_chit_rat, 'chit', 'Cache Hit Ratio',
        render.percent( arc_chit_rat ), params )
    yield check_mk_zfs_state( arc_cmiss_rat, 'cmiss', 'Cache Miss Ratio',
        render.percent( arc_cmiss_rat ), params )

register.check_plugin(
    name="mk_zfs_arc",
    service_name="ZFS ARC",
    discovery_function=discover_mk_zfs_arc,
    check_function=check_mk_zfs_arc,
    check_default_parameters={
        'cmiss_warn': 25,
        'cmiss_crit': 50,
        'chit_warn': 0,
        'chit_crit': 0,
        'meta_warn': 0,
        'meta_crit': 0,
        'data_warn': 0,
        'data_crit': 0,
        'sz_warn': 0,
        'sz_crit': 0  },
    check_ruleset_name="mk_zfs_arc"
)

