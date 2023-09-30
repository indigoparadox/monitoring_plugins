#!/bin/sh

OS_NAME="`uname -o`"
SNMP_OID=.1.3.6.1.2.1.25.1.8
snmp_test() {
   CPU_IDX="$2"
   if [ -z "$2" ] && [ "NEXT" = "$3" ]; then
      CPU_IDX=0
   elif [ -n "$2" ] && [ "NEXT" = "$3" ]; then
      CPU_IDX="$(($2 + 1))"
   elif [ -z "$2" ] || [ $2 -ge 8 ]; then
      CPU_IDX=-1
   fi

   if [ $CPU_IDX -ge 0 ] && [ $CPU_IDX -lt 8 ]; then
      echo $1.$CPU_IDX
      echo gauge
      if [ "FreeBSD" = "$OS_NAME" ]; then
         sysctl -n dev.cpu.$CPU_IDX.temperature | cut -c 1,2,4
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

