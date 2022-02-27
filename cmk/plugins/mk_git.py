#!/usr/bin/env python3

from .agent_based_api.v1 import *

def discover_mk_git( section ):
    for line in section:
        if '/' == line[0][0]:
            yield Service( item=line[0] )

def check_mk_git( item, section ):
    in_section = False
    mod_count = 0
    for line in section:
        if item == line[0]:
            # Line is the sought repo name.
            in_section = True

        elif '/' == line[0][0]:
            # Line is a new repo name.
            in_section = False

        elif in_section:
            # Line is a filename modified in the repo.
            mod_count += 1

    if 0 == mod_count:
        yield Result(
            state=State.OK,
            summary='No modified files in repo.' )
    else:
        yield Result(
            state=State.WARN,
            summary='{} modified files in repo'.format( mod_count ) )
    
register.check_plugin(
    name="mk_git",
    service_name="git Repository %s",
    discovery_function=discover_mk_git,
    check_function=check_mk_git
)

