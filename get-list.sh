#!/bin/bash
# crawls shelf and returns list

SHELF=$1
USER=$2

if [ $# -lt 2 ]; then
    echo "need to supply two arguments: get-list.sh <shelf> <user-id>"
    exit 1
fi

cd GoodreadsScraper

python3 crawl.py my-books --shelf=$SHELF   --user_id=$USER

# convert to list
cat *.jl | grep -oP 'https://www.goodreads.com/book/show/\K[^"]+' > ../$USER.txt