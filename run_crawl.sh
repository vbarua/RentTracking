#!/usr/bin/env bash
set -e

if test -f secrets ; then
  source secrets
fi

for city in vancouver victoria kelowna
do
    echo Crawling ${city}
    export CITY=${city}
    NOW=`date +%Y/%m/%d/%H%M%S`
    OUTPUT_LOC=output/${CITY}/${NOW}
    mkdir -p ${OUTPUT_LOC}

    #Stores listings that will be scraped in crawl. Written by CraigslistSearch, read by CraigslistListings.
    export CL_CRAWL_SET_LOCATION=${OUTPUT_LOC}/cl_crawl_set.json

    #Stores output of listings crawl.
    CL_CRAWL_OUTPUT_LOCATION=${OUTPUT_LOC}/cl_output.json
    #Stores html scraped during crawl.
    export CL_HTML_OUTPUT_LOCATION=${OUTPUT_LOC}/html

    #Logfiles
    CL_SEARCH_LOGFILE=${OUTPUT_LOC}/cl_search_log.txt
    CL_LISTING_LOGFILE=${OUTPUT_LOC}/cl_listing_log.txt

    scrapy crawl --set=DOWNLOAD_DELAY=0.25 --logfile=${CL_SEARCH_LOGFILE}  --loglevel=INFO -o ${CL_CRAWL_SET_LOCATION} CraigslistSearch
    scrapy crawl --set=DOWNLOAD_DELAY=2 --logfile=${CL_LISTING_LOGFILE} --loglevel=INFO -o ${CL_CRAWL_OUTPUT_LOCATION} CraigslistListings

    tar -zcf ${CL_HTML_OUTPUT_LOCATION}.tar.gz ${CL_HTML_OUTPUT_LOCATION}
    rm -rf ${CL_HTML_OUTPUT_LOCATION}
done