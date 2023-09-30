#!/bin/sh

OS_NAME="`uname -o`"
SNMP_OID=.1.3.6.1.2.1.25.1.9
snmp_test() {
   if [ "FreeBSD" = "$OS_NAME" ]; then
      HDD_COUNT=`ls /dev/ada? | wc -l`
      SMARTCTL_PATH="/usr/local/sbin/smartctl"
   else
      HDD_COUNT=`ls /dev/sd? | wc -l`
      SMARTCTL_PATH="/usr/sbin/smartctl"
   fi
   HDD_IDX="$2"

   if [ -z "$2" ] && [ "NEXT" = "$3" ]; then
      HDD_IDX=0
   elif [ -n "$2" ] && [ "NEXT" = "$3" ]; then
      HDD_IDX="$(($2 + 1))"
   elif [ -z "$2" ] || [ $2 -ge 8 ]; then
      HDD_IDX=-1
   fi

	if [ $HDD_IDX -ge 0 ] && [ $HDD_IDX -lt 5 ]; then
		echo .1.3.6.1.2.1.25.1.9.$1
		echo gauge
      if [ "FreeBSD" = "$OS_NAME" ]; then
         $SMARTCTL_PATH -A $1 | grep Temperature | awk '{print $10}'
      else
         # TODO: Translate number to letter for Linux disk path.
      fi
	else
		echo NONE
	fi
}

SCRIPT_DIR_PATH="`dirname "$0"`"
. "`realpath "$SCRIPT_DIR_PATH"`/snmplib.sh"

snmp_proc_once $@
if [ $SNMP_PROC_ONCE -eq 1 ]; then
   exit
else
   snmp_proc_persist
fi

