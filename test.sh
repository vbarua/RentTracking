#!/usr/bin/env bash

# Unused But Required Exports
export CL_CRAWL_SET_LOCATION=dummy

# Test Setting
export TEST=true
export CITY=test

NOW=`date +%Y/%m/%d/%H%M%S`
OUTPUT_LOC=output/${CITY}/${NOW}
CL_CRAWL_OUTPUT_LOCATION=${OUTPUT_LOC}/cl_output.json
export CL_HTML_OUTPUT_LOCATION=${OUTPUT_LOC}/html

# Test CraigslistListings Crawler
scrapy crawl --set=DOWNLOAD_DELAY=0 CraigslistListings -o ${CL_CRAWL_OUTPUT_LOCATION}
tar -zcf ${CL_HTML_OUTPUT_LOCATION}.tar.gz ${CL_HTML_OUTPUT_LOCATION}
rm -rf ${CL_HTML_OUTPUT_LOCATION}
