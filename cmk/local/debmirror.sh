#!/bin/sh

# This should be set to the URL of the mirror to compare.
_osmirror_loc_url="http://debmirror.example.com/debian"
_osmirror_dist="bookworm"

# How often we should check the age of debian.org.
_osmirror_deb_fetch_interval=1000
# How old the local repo is allowed to get (default: 1 day).
_osmirror_deb_tolerance=86400

_osmirror_deb_fetched=0

# Ensure cache directories.
if [ -z "$MK_TMPDIR" ]; then
	export MK_TMPDIR="/var/run/check_mk"
fi

if [ ! -d "$MK_TMPDIR" ]; then
	mkdir -p "$MK_TMPDIR"
fi

# Check result cache.
if [ -f "$MK_TMPDIR/osmirror_last_deb_fetch" ]; then
	_osmirror_next_fetch=$(("`cat "$MK_TMPDIR/osmirror_last_deb_fetch"`" + \
		$_osmirror_deb_fetch_interval))
	if [ "$_osmirror_next_fetch" -gt "`date +'%s'`" ]; then
		# Not yet time to fetch again.
		_osmirror_deb_fetched=1
		_osmirror_deb_epoch="`cat "$MK_TMPDIR/osmirror_last_deb_res"`"
	fi
fi

# Fetch update time from local mirror.

_osmirror_osm_date="`wget $_osmirror_loc_url/dists/$_osmirror_dist/Release -O - -q | grep ^Date | sed 's/^Date: //g'`"
if [ -z "$_osmirror_osm_date" ]; then
	# Handle failure to fetch.
	exit 1
fi
_osmirror_osm_epoch="`date -j -f "%a, %d %b %Y %H:%M:%S %Z" "$_osmirror_osm_date" +"%s"`"

# Fetch update time from debian.org and cache it.

if [ $_osmirror_deb_fetched -eq 0 ]; then
	_osmirror_deb_date="`wget http://deb.debian.org/debian/dists/$_osmirror_dist/Release -O - -q | grep ^Date | sed 's/^Date: //g'`"
	if [ -z "$_osmirror_deb_date" ]; then
		# Handle failure to fetch.
		exit 1
	fi
	_osmirror_deb_epoch="`date -j -f "%a, %d %b %Y %H:%M:%S %Z" "$_osmirror_deb_date" +"%s"`"

	# Save fetched result for cache.
	date +'%s' > "$MK_TMPDIR/osmirror_last_deb_fetch"
	echo "$_osmirror_deb_epoch" > "$MK_TMPDIR/osmirror_last_deb_res"
fi
	
if [ $_osmirror_deb_epoch -gt $(($_osmirror_osm_epoch + $_osmirror_deb_tolerance)) ]
then
	# Local repo is old!
	echo "2 \"Debian Mirror\" - Out of date!"
else
	echo "0 \"Debian Mirror\" - Up to date!"
fi

