Various systems monitoring plugins we've written for our environment.

# Check\_MK

## mk\_git

Monitors specified git respository directories and changes status if files are modified or added.

### Configuration: WATO

Create a new rule for `git repository changes` under operating system service monitoring rules in order to change thresholds for number of files to cause warning/critical status.

### Configuration: Agent

| File | Description |
| --- | --- |
| $MK\_CONFDIR/mk\_git.cfg    | Defines the configuration variables below.          |

| Variable | Description |
| --- | --- |
| $MK_GIT_DIRS | Space-separated list of git repository directories to monitor. |

## default\_tr

Monitors default route and ensures that a particular router hop is present.

### Configuration: WATO

Create a new rule for `Default route to arbitrary destination` under operating system service monitoring rules in order to specify the hop name to monitor for.

### TODO

 - [ ] Move hop target (currently google.com) into agent configuration.
 - [ ] Change rule category to network.

## mk\_weewx

Monitors WeeWX weather monitoring database and makes sure that the latest update is recent.

### Configuration: Agent

| File | Description |
| --- | --- |
| $MK\_CONFDIR/mk\_weewx.secret | Plain text file with the password for the database. |
| $MK\_CONFDIR/mk\_weewx.cfg    | Defines the configuration variables below.          |

| Variable | Description |
| --- | --- |
| $WEEWX_DB_HOST | Hostname for the WeeWX MySQL host. |
| $WEEWX_DB_USER | Username for the WeeWX MySQL account. |
| $WEEWX_DB      | Name of the WeeWX database in MySQL |
