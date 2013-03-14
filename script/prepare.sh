#!/usr/bin/env bash

echo "Looking for the latest corpus and seeds in corpus/"
LATEST_CORPUS=`ls corpus/corpus_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].txt | sort | tail -1`
LATEST_SEEDS=`ls corpus/seeds_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9].txt | sort | tail -1`
cp $LATEST_CORPUS input/corpus.txt
cp $LATEST_SEEDS input/seeds.txt
echo "Latest corpus: $LATEST_CORPUS"
echo "Latest seeds: $LATEST_SEEDS"
echo "These files were copied to input/ directory"
echo "----"
echo "About to parse corpus. This process may take a while."
echo "When it finishes, a copy if the generated index and urls will be copied to output/ directory."
read -p "Are you sure you want to continue? " -n 1 -r
if [[ $REPLY =~ ^[Yy]$ ]]
then
    python tools/parse_corpus.py -i input/corpus.txt -o input/index.json -s output/urls.txt -v
    cp input/index.json output/index.json
fi
