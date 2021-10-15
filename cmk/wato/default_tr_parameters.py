
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

def _parameter_valuespec_default_tr():
    return Dictionary(
        elements=[
            ("hop_name", TextAscii( title=_( 'Hop name' ) ))
        ],
    )

rulespec_registry.register(
    CheckParameterRulespecWithoutItem(
        check_group_name="default_tr",
        group=RulespecGroupCheckParametersOperatingSystem,
        match_type="dict",
        parameter_valuespec=_parameter_valuespec_default_tr,
        title=lambda: _( 'Default route to arbitrary destination' )
    )
)

