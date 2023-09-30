#!/bin/sh

snmp_trim_oid() {
	# Trim off provided OID from testing OID.
   OID_END="`echo $2 | sed "s/^$1//g"`"
   if [ -n "$OID_END" ]; then
      # Strip leading "." off of specified OID end.
      OID_END="`echo $OID_END | sed 's/^\.//g'`"
   fi
}

snmp_proc_once() {
	SNMP_PROC_ONCE=0
	if [ "$1" = "-g" ]; then
		snmp_trim_oid "$SNMP_OID" "$2"
		if [ -z "$OID_END"  ]; then
			echo NONE
		else
			snmp_test "$SNMP_OID" "$OID_END"
		fi
		SNMP_PROC_ONCE=1
	elif [ "$1" = "-n" ]; then
		snmp_trim_oid "$SNMP_OID" "$2"
		snmp_test "$SNMP_OID" "$OID_END" "NEXT"
		SNMP_PROC_ONCE=1
	fi
}

snmp_proc_persist() {
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
			snmp_trim_oid "$SNMP_OID" "$REPLY"

			if [ 0 -eq $SNMP_MODE ] && [ -n "$OID_END" ]; then
				# Simple GET request.
				snmp_test "$SNMP_OID" "$OID_END"
				OID_END=""

			elif [ 1 -eq $SNMP_MODE ] && [ -z "$OID_END" ]; then
				# GETNEXT request with no OID.
				snmp_test "$SNMP_OID" "" "NEXT"

			elif [ 1 -eq $SNMP_MODE ]; then
				# GETNEXT request with specified OID.
				snmp_test "$SNMP_OID" "$OID_END" "NEXT"
				OID_END=""
			else
				echo NONE
			fi
		fi
	done
}

