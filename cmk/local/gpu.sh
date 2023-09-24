#!/bin/bash

RADEONTOP_OUT="`radeontop -d - -l 1`"

#echo $RADEONTOP_OUT | awk 'BEGIN { FS = "," } ; { print $2 }'

IFS=','
for p in $RADEONTOP_OUT; do
   if [ "gpu" = "`echo $p | awk '{ print $1 }'`" ]; then
      GPU_USAGE="`echo $p | awk '{ print $2 }' | tr -d '%'`"
      echo "P \"GPU utilization\" pipeline=$GPU_USAGE;95;100 GPU utilization"
   fi
done

