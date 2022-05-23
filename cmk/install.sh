#!/bin/sh

PLUGIN_NAME=""
DO_LINK=0
DO_FORCE=0
PLUGINS_DIR="$OMD_ROOT/local/lib/check_mk/base/plugins/agent_based"
WATO_DIR="$OMD_ROOT/local/share/check_mk/web/plugins/wato"
SCRIPT_PATH="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P)"

if [ -z "$OMD_ROOT" ]; then
	echo "No OMD_ROOT defined. Must be run from omd su!"
	exit 1
fi

while [ "$1" ]; do
	case "$1" in
		"-l")
			DO_LINK=1
			;;

      "-f")
         DO_FORCE=1
         ;;

		*)
			if [ -z "$PLUGIN_NAME" ]; then
				PLUGIN_NAME="$1"
			fi
	 		;;
	esac
	shift
done

if [ -z "$PLUGIN_NAME" ]; then
   echo "usage: $0 [-l] [-f] <plugin_name>"
   echo
   echo "-l    Link files instead of copying them."
   echo "-f    Force copy/link even if file is older."
fi

do_install_file() {
   INSTALL_SRC="$1"
   INSTALL_DEST="$2"

   if [ $DO_FORCE = 1 ] && [ $DO_LINK = 1 ] && [ -f "$INSTALL_DEST" ]; then
      rm -fv "$INSTALL_DEST"
      ln -sv "$INSTALL_SRC" "$INSTALL_DEST"

   elif [ $DO_LINK = 1 ] && [ -f "$INSTALL_DEST" ] && [ ! -L "$INSTALL_DEST" ]
   then
      echo "$INSTALL_DEST is file\nskipping..."

   elif [ $DO_LINK = 1 ] && [ ! -L "$INSTALL_DEST" ] && [ ! -f "$INSTALL_DEST" ]
   then
      ln -sv "$INSTALL_SRC" "$INSTALL_DEST"

   elif [ $DO_LINK = 1 ]; then
      echo "$INSTALL_DEST linked\nskipping..."

   elif [ ! -f "$INSTALL_DEST" ]; then
      cp -vp "$INSTALL_SRC" "$INSTALL_DEST"

   elif [ "$INSTALL_SRC" -nt "$INSTALL_DEST" ]; then
      # Copy the file if updated.
      cp -vp "$INSTALL_SRC" "$INSTALL_DEST"

   elif [ $DO_FORCE = 1 ]; then
      # Copy the file regardless.
      rm -fv "$INSTALL_DEST"
      cp -vp "$INSTALL_SRC" "$INSTALL_DEST"

   else
      echo "$INSTALL_DEST exists\nskipping..."

   fi

}

if [ -f "$SCRIPT_PATH/plugins/$PLUGIN_NAME.py" ]; then
   do_install_file \
      "$SCRIPT_PATH/plugins/$PLUGIN_NAME.py" \
      "$PLUGINS_DIR/$PLUGIN_NAME.py"
fi

if [ -f "$SCRIPT_PATH/wato/${PLUGIN_NAME}_parameters.py" ]; then
   do_install_file \
      "$SCRIPT_PATH/wato/${PLUGIN_NAME}_parameters.py" \
      "$WATO_DIR/${PLUGIN_NAME}_parameters.py"
fi

