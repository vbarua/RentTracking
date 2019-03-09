#!/usr/bin/env bash
now=`date +%Y-%m-%d.%H:%M:%S`

export TEST=true
export CITY=test
export CL_CRAWL_SET_LOCATION=dummy

OUTPUT_LOC=test_output
rm -rf ${OUTPUT_LOC}
export CL_HTML_OUTPUT_LOCATION=${OUTPUT_LOC}/html

scrapy crawl --set=DOWNLOAD_DELAY=0 CraigslistListings