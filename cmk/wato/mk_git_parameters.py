
from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    TextAscii
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithoutItem,
    rulespec_registry,
    RulespecGroupCheckParametersOperatingSystem
)

def _parameter_valuespec_mk_git():
    return Dictionary(
        elements=[
            ("new_warn", Integer(
                title=_( 'Warning above untracked files' ),
                default_value=1 )),
            ("new_crit", Integer(
                title=_( 'Critical above untracked files' ),
                default_value=5 )),
            ("mod_warn", Integer(
                title=_( 'Warning above modified files' ),
                default_value=1 )),
            ("mod_crit", Integer(
                title=_( 'Critical above modified files' ),
                default_value=5 ))
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="mk_git",
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_mk_git,
        title=lambda: _( 'git repository changes' )
    )
)

