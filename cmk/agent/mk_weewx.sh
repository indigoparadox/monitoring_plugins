#!/bin/sh

if [ -e "$MK_CONFDIR/mk_weewx.cfg" ]; then
        . $MK_CONFDIR/mk_weewx.cfg
fi

WEEWX_DB_PWD="`cat $MK_CONFDIR/mk_weewx.secret`"

echo "<<<mk_weewx>>>"

echo "select dateTime from archive order by dateTime desc limit 1;" | mysql -h$WEEWX_DB_HOST -u$WEEWX_DB_USER $WEEWX_DB -p$WEEWX_DB_PWD | tail -1

