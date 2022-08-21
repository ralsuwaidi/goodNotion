#!/bin/bash
# crawls shelf and returns list

# usage: get-list.sh <shelf> <user-id>

SHELF=$1
USER=$2

if [ $# -lt 2 ]; then
    echo "need to supply two arguments: get-list.sh <shelf> <user-id>"
    exit 1
fi


## project 1
cd GoodreadsScraper
python3 crawl.py my-books --shelf=$SHELF --user_id=$USER

cat *.jl | grep -oP 'https://www.goodreads.com/book/show/\K[^"]+' > ../$USER.txt

# make into list
BOOKS_JSON_LIST="book_"$USER".jl"


# fix files
sed -e 's/$/,/' -i $BOOKS_JSON_LIST
sed -i '1 i\[' $BOOKS_JSON_LIST
truncate -s-1  $BOOKS_JSON_LIST
truncate -s-1  $BOOKS_JSON_LIST
echo "]" >> $BOOKS_JSON_LIST
mv $BOOKS_JSON_LIST ../"book_"$USER".json"

# convert to list to take by project 2

## project 2
