#!/bin/sh

snmp_hdd_temp() {
	if [ $1 -lt 5 ]; then
		echo .1.3.6.1.2.1.25.1.9.$1
		echo gauge
		/usr/local/sbin/smartctl -A /dev/ada$1 | grep Temperature | awk '{print $10}'
	else
		echo NONE
	fi
}

if [ "$1" = "-g" ]; then
	OID_END="`echo $2 | sed 's/\.1\.3\.6\.1\.2\.1\.25\.1\.9//g'`"
	if [ -n "$OID_END" ]; then
		# Strip leading "." off of specified OID end.
		OID_END="`echo $OID_END | sed 's/^\.//g'`"
	else
		OID_END=0
	fi
	snmp_hdd_temp $OID_END
	exit
elif [ "$1" = "-n" ]; then
	OID_END="`echo $2 | sed 's/\.1\.3\.6\.1\.2\.1\.25\.1\.9//g'`"
	if [ -n "$OID_END" ]; then
		# Strip leading "." off of specified OID end.
		OID_END="`echo $OID_END | sed 's/^\.//g'`"
		OID_END=$(($OID_END + 1))
	else
		OID_END=0
	fi
	snmp_hdd_temp $OID_END
	exit
fi

SNMP_MODE=0 # 0 GET, 1 NEXT
while read -r REPLY; do
	if [ "PING" = "$REPLY" ]; then
		echo PONG
	elif [ "getnext" = "$REPLY" ]; then
		SNMP_MODE=1
	elif [ "get" = "$REPLY" ]; then
		SNMP_MODE=0
	else
		# Probably an OID?
		OID_END="`echo $REPLY | sed 's/\.1\.3\.6\.1\.2\.1\.25\.1\.9//g'`"
		if [ -n "$OID_END" ]; then
			# Strip leading "." off of specified OID end.
			OID_END="`echo $OID_END | sed 's/^\.//g'`"
		fi

		if [ $SNMP_MODE -eq 0 ] && [ -n "$OID_END" ]; then
			# Simple GET request.
			snmp_hdd_temp $OID_END
			OID_END=""

		elif [ $SNMP_MODE -eq 1 ] && [ -z "$OID_END" ]; then
			# GETNEXT request with no OID.
			snmp_hdd_temp 0

		elif [ $SNMP_MODE -eq 1 ]; then
			# GETNEXT request with specified OID.
			snmp_hdd_temp $(($OID_END + 1))
			OID_END=""
		else
			echo NONE
		fi
	fi
done

