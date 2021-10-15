#!/usr/bin/env python3

from .agent_based_api.v1 import *

def discover_default_tr( section ):
    yield Service()

def check_default_tr( params, section ):
    hop_name_found = False
    for line in section:
        if params['hop_name'] in line[1]:
            yield Result(
                state=State.OK,
                summary='Found hop: {} {} ({}ms)'.format(
                    line[1], line[2], line[3] ) )
            return
    yield Result(
        state=State.CRIT,
        summary='Could not find hop: {}'.format( params['hop_name'] ) )

register.check_plugin(
    name="default_tr",
    service_name="Default Traceroute",
    discovery_function=discover_default_tr,
    check_function=check_default_tr,
    check_default_parameters={"hop_name": "google.com"},
    check_ruleset_name="default_tr"
)

