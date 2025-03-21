#!/bin/bash

DHCP_RETVAL=0
DHCP_ROGUE=""
DHCP_GOOD="192.168.0.2"

for d in `nmap --script broadcast-dhcp-discover -e eth0 | grep "Server Identifier:" | awk '{print $4}'`; do
	if [ "$DHCP_GOOD" != "$d" ]; then
		DHCP_RETVAL=2
		DHCP_ROGUE="$d"
	fi
done

if [ $DHCP_RETVAL -ne 0 ]; then
	echo "$DHCP_RETVAL \"DHCP Server\" - Rogue DHCP server: $DHCP_ROGUE"
else
	echo "0 \"DHCP Server\" - No rogue DHCP server found."
fi

