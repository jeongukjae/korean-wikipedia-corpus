#!/bin/sh

pip install wikiextractor
python -m wikiextractor.WikiExtractor $WIKI_FILE
