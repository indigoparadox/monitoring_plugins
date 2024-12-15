#!/usr/bin/env python3

from .agent_based_api.v1 import register, State, Service, Result

def parse_gluster_peers( string_table ):
    peers_out = []
    for i in string_table:
        # Strip out "Number of Peers" line.
        if 'Number' == i[0]:
            continue
        
        # Split into dict based on |-separated k: v pairs (after patching up spaces).
        # Basically just processing raw gluster command output.
        peers_out.append( {x[0]: x[1].strip() for x in [y.split( ':' ) for y in ' '.join( i ).split( '|' )] if 1 < len( x ) } )

    return peers_out

def discover_gluster_peers( section ):
    if( 0 < len( section ) ):
        yield Service()

def check_gluster_peers( section ):
    for i in section:
        res = State.OK
        if 'Peer in Cluster (Connected)' != i['State']:
            res = State.CRIT

        yield Result( state=res, summary='{}: {}'.format( i['Hostname'], i['State'] ) )
    
register.check_plugin(
    name='mk_gluster_peers',
    service_name='GlusterFS peers',
    discovery_function=discover_gluster_peers,
    check_function=check_gluster_peers
)

register.agent_section(
    name='mk_gluster_peers',
    parse_function=parse_gluster_peers
)
