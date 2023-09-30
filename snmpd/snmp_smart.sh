#!/bin/sh

CACHE_UPDATE_SECONDS=60
CACHE_REFRESH=0

SNMP_OID=".1.3.6.1.4.1.6574.5"
SNMP_OID_COL_TYPES="na string string integer integer integer integer integer"

snmp_smart() {
   for i in /dev/ada?; do
      /usr/local/sbin/smartctl -a $i | grep '^\s\?[0-9]' | sed "s/^/`basename $i` /g"
   done
}

SMART_LINES="`snmp_smart`"
SMART_UPDATE="`date +%s`"
SMART_LINE_CT="`echo "$SMART_LINES" | wc -l`"
SMART_LINE_CT_LAST="`echo "$SMART_LINES" | wc -l`"

snmp_test() {
   COL_COL="`echo "$2" | sed 's/^\([0-9]*\).[0-9]*$/\1/g'`"
   COL_END="`echo "$2" | sed 's/^[0-9]*.\([0-9]*\)$/\1/g'`"

   # Refresh SMART data if it's old.
   if [ $(($SMART_UPDATE + $CACHE_UPDATE_SECONDS)) -lt `date +%s` ]; then
      CACHE_REFRESH=1
   fi

   while [ $CACHE_REFRESH -eq 1 ]; do
      SMART_LINES="`snmp_smart`"
      SMART_UPDATE="`date +%s`"
      SMART_LINE_CT_LAST="$SMART_LINE_CT"
      SMART_LINE_CT="`echo "$SMART_LINES" | wc -l`"
      CACHE_REFRESH=0
      if echo "$SMART_LINES" | grep 'echo: write error on stdout' || \
      [ $SMART_LINE_CT -lt $SMART_LINE_CT_LAST ] ||
      echo "$SMART_LINES" | grep '^ada[0-9]*$'; then
         SMART_LINES_TEMPFILE="/tmp/snmp_smart_error.log"
         echo "$SMART_LINES" >> $SMART_LINES_TEMPFILE
         echo "check write failed: $SMART_LINES_TEMPFILE" | /usr/bin/logger -t snmpd
         CACHE_REFRESH=1
      fi
   done

   # Start at first column if next is specified, or fail.
   if [ "NEXT" = "$3" ] && [ -z "$2" ]; then
      COL_COL=2
   elif [ -z "$COL_COL" ] && [ -z "$COL_END" ]; then
      # Couldn't extract from $2... pattern mismatch?
      COL_COL="`echo "$2" | sed 's/^\([0-9]*\)$/\1/g'`"
      COL_END=-1
   elif [ -z "$3" ] && [ -z "$COL_COL" ]; then
      COL_COL=-1
   fi

   # Start at first index if next is specified (-1 + 1 below=0), or fail.
   if [ -z "$COL_END" ]; then
      COL_END=-1
   fi

   # Iterate into next section if at the end of this one, or just get next
   # index if next is specified.
   if [ "NEXT" = "$3" ] && \
   [ $COL_END -eq $(($SMART_LINE_CT - 1)) ] && \
   [ $COL_COL -le 8 ]; then
      COL_COL="$(($COL_COL + 1))"
      COL_END=0
   elif [ "NEXT" = "$3" ] && [ $COL_END -lt $SMART_LINE_CT ]; then
      COL_END="$(($COL_END + 1))"
   fi

   # Figure out print index for awk.
   if [ $COL_COL -eq 2 ]; then
      COL_PRINT_IDX=1
   elif [ $COL_COL -eq 3 ]; then
      COL_PRINT_IDX=3
   elif [ $COL_COL -eq 4 ]; then
      COL_PRINT_IDX=2
   elif [ $COL_COL -eq 5 ]; then
      COL_PRINT_IDX=5
   elif [ $COL_COL -eq 6 ]; then
      COL_PRINT_IDX=6
   elif [ $COL_COL -eq 7 ]; then
      COL_PRINT_IDX=7
   elif [ $COL_COL -eq 8 ]; then
      COL_PRINT_IDX=11
   else
      COL_PRINT_IDX=""
   fi

   # If column/end is valid, display value.
   if [ $COL_END -ge 0 ] && [ $COL_END -lt $SMART_LINE_CT ] && [ $COL_COL -ge 0 ] && [ $COL_COL -lt 9 ]; then
      echo $SNMP_OID.$COL_COL.$COL_END
      echo $SNMP_OID_COL_TYPES | awk "{print \$$COL_COL}"
      echo "$SMART_LINES" | head -$(($COL_END + 1)) | tail -1 | awk "{print \$$COL_PRINT_IDX}"
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

