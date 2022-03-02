#!/usr/bin/env python3

from .agent_based_api.v1 import *

def discover_mk_git( section ):
    for line in section:
        if '/' == line[0][0]:
            yield Service( item=line[0] )

def check_mk_git( item, params, section ):
    in_section = False
    mod_count = 0
    new_count = 0
    for line in section:
        if item == line[0]:
            # Line is the sought repo name.
            in_section = True

        elif '/' == line[0][0]:
            # Line is a new repo name.
            in_section = False

        elif in_section and '?' == line[0][0]:
            # Line is a filename modified in the repo.
            new_count += 1

        elif in_section and '!' == line[0][0]:
            # Line is a filename modified in the repo.
            mod_count += 1

    # Figure out the message.
    summary_msg = ''
    if 0 == mod_count and 0 == new_count:
        summary_msg = 'No new or modified files'
    else:
        if 0 < mod_count:
            summary_msg += '{} modified files'.format( mod_count )
        if 0 < new_count:
            summary_msg += '{} new files'.format( new_count )

    if params['mod_crit'] <= mod_count or params['new_crit'] <= new_count:
        yield Result( state=State.CRIT, summary=summary_msg )
    elif params['mod_warn'] <= mod_count or params['new_warn'] <= new_count:
        yield Result( state=State.WARN, summary=summary_msg )
    else:
        yield Result( state=State.OK, summary=summary_msg )
    
register.check_plugin(
    name="mk_git",
    service_name="git Repository %s",
    discovery_function=discover_mk_git,
    check_function=check_mk_git,
    check_default_parameters={
        'mod_warn': 1,
        'mod_crit': 5,
        'new_warn': 1,
        'new_crit': 5 },
    check_ruleset_name="mk_git"
)

