#!/usr/bin/env bash

now=`date +%Y-%m-%d.%H:%M:%S`
export CITY=vancouver
export CRAWL_SET_LOCATION=output/crawl-set-$now.json

scrapy crawl -set=DOWNLOAD_DELAY=1 -o ${CRAWL_SET_LOCATION} CraigslistSearch
