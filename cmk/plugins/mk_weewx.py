#!/usr/bin/env python3

from .agent_based_api.v1 import *
from datetime import datetime, timedelta

def discover_mk_weewx( section ):
    yield Service()

def check_mk_weewx( section ):
    # Agent should provide timestamp of the last entry date as a string.
    try:
        entry_date = datetime.fromtimestamp( int( section[0][0] ) )

        if entry_date < datetime.now() - timedelta( minutes=10 ):
            yield Result(
                state=State.CRIT,
                summary='Last update was at {}'.format( entry_date ) )
        else:
            yield Result(
                state=State.OK,
                summary='Last update was at {}'.format( entry_date ) )

    except KeyError:
        yield Result(
            state=State.CRIT,
            summary='No updates found' )

register.check_plugin(
    name="mk_weewx",
    service_name="WeeWX Database",
    discovery_function=discover_mk_weewx,
    check_function=check_mk_weewx
)

