#!/bin/sh

if [ -e "$MK_CONFDIR/mk_git.cfg" ]; then
	. $MK_CONFDIR/mk_git.cfg
fi

echo "<<<mk_git>>>"

for g in $MK_GIT_DIRS; do
	echo "$g"
	cd "$g"
	git status -s
done

