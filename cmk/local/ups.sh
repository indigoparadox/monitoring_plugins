#!/bin/bash

IFS=$'\n'
for l in `apcaccess`; do
   UPS_FIELD="`echo $l | awk '{print $1}'`"
   if [ "STATUS" = "$UPS_FIELD" ]; then
      UPS_STATUS="`echo $l | awk '{print $3}'`"
   elif [ "LINEV" = "$UPS_FIELD" ]; then
      UPS_LINEV="`echo $l | awk '{print $3}'`"
   elif [ "LOADPCT" = "$UPS_FIELD" ]; then
      UPS_LOADPCT="`echo $l | awk '{print $3}'`"
   elif [ "BCHARGE" = "$UPS_FIELD" ]; then
      UPS_BCHARGE="`echo $l | awk '{print $3}'`"
   elif [ "TIMELEFT" = "$UPS_FIELD" ]; then
      UPS_TIMELEFT="`echo $l | awk '{print $3}'`"
   elif [ "MODEL" = "$UPS_FIELD" ]; then
      UPS_MODEL="`echo $l | awk 'BEGIN {FS = ":" } {print $2}' | sed -e 's/^ //g'`"
   fi
done

if [ "ONLINE" = "$UPS_STATUS" ]; then
   UPS_OK="P"
else
   UPS_OK=2
fi

echo "$UPS_OK \"UPS status\" line_voltage=$UPS_LINEV;105:125;100:130|load_percent=$UPS_LOADPCT;80;90|battery_charge=$UPS_BCHARGE;50:105;25:110|time_left=$UPS_TIMELEFT;10:1000;5:2000 $UPS_MODEL"

