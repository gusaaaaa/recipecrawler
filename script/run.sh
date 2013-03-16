#!/usr/bin/env bash

merge_settings() {
	if [ -n "$SETTINGS" ] && [ ! -f $SETTINGS ]
	then
		echo "File not found: $SETTINGS" >& 2
		exit 2
	fi

	GLOBAL="config/global.py"
	if [ ! -f $GLOBAL ]
	then
		echo "Global configuration file not found: $GLOBAL" >& 2
		exit 2
	fi

	cat $GLOBAL $SETTINGS > "recipebot/settings.py"
}

process_options() {
	if ! [[ "$1" =~ ^[0-9]+$ ]]
	then
		echo "Argument must be a number" >& 2
		exit 1
	fi

	SETTINGS="config/custom_$1.py"

	merge_settings $SETTINGS
}

pack_output() {
	files=(tmp/*)
	if [ ${#files[@]} -gt 0 ]
	then
		CONFIGFILE="tmp/config.txt"
		touch $CONFIGFILE
		echo "# -----------------------" >> $CONFIGFILE
		echo "# GLOBAL SETTINGS -------" >> $CONFIGFILE
		echo "# -----------------------" >> $CONFIGFILE
		echo "" >> $CONFIGFILE
		cat $GLOBAL >> $CONFIGFILE
		if [ -n "$SETTINGS" ]
		then
			echo "" >> $CONFIGFILE
			echo "# -----------------------" >> $CONFIGFILE
			echo "# CUSTOM SETTINGS -------" >> $CONFIGFILE
			echo "# -----------------------" >> $CONFIGFILE
			echo "" >> $CONFIGFILE
			cat $SETTINGS >> $CONFIGFILE
		fi
		cd tmp
		ZIPFILE="results_$(date +"%Y%m%d%H%M%S").zip"
		zip -q $ZIPFILE *
		mv $ZIPFILE ../output/
		cd ..
	fi
}

GLOBAL=""
SETTINGS=""

if [ -n "$1" ]
then
	process_options $1
else
	merge_settings
fi

# remove temporary files
rm tmp/*

# execute scrapy
scrapy crawl configurable -o tmp/items.json -t json

# pack generated temporary files

pack_output
