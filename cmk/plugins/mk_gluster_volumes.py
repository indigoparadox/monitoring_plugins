#!/usr/bin/env python3

from .agent_based_api.v1 import register, State, Service, Result

def parse_gluster_volumes( string_table ):
    volumes_out = []
    for i in string_table:
        # Strip out "Number of volumes" line.
        if 'Number' == i[0]:
            continue
        
        # Split into dict based on |-separated k: v pairs (after patching up spaces).
        # Basically just processing raw gluster command output.
        vol_data = {x[0]: x[1].strip() for x in [y.split( ':' ) for y in ' '.join( i ).split( '|' )] if 1 < len( x ) }

        # Stuff bricks into sublist.
        vol_data['VBricks'] = []
        for j in vol_data:
            if 'Bricks' != j and j.startswith( 'Brick' ):
                vol_data['VBricks'].append( vol_data[j] )
        vol_data = {k: v for k, v in vol_data.items() if not k.startswith( 'Brick' )}
        volumes_out.append( vol_data )

    return volumes_out

def discover_gluster_volumes( section ):
    for i in section:
        yield Service( item=i['Volume Name'] )

def check_gluster_volumes( item, section ):
    for i in section:
        res = State.OK
        if 'Started' != i['Status']:
            res = State.CRIT

        yield Result( state=res, summary='{}'.format( i['Status'] ) )
    
register.check_plugin(
    name='mk_gluster_volumes',
    service_name='GlusterFS volume %s',
    discovery_function=discover_gluster_volumes,
    check_function=check_gluster_volumes
)

register.agent_section(
    name='mk_gluster_volumes',
    parse_function=parse_gluster_volumes
)
