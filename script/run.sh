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

if [ -n "$1" ]
then
	process_options $1
else
	merge_settings
fi

scrapy crawl recipecrawler -o output/items.json -t json
