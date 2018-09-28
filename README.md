# Rent Trackers
A collection of web scrapers for use in tracking rental prices.

Makes use of the  [Scrapy]( https://github.com/scrapy/scrapy) web crawling and scraping framework.

Please scrape responsibly.

## Craigslist
```scrapy crawl Craigslist -o output.json```
This command runs the Craigslist scraper to extract rental data.

### TODO
- Implement page caching to avoid making unnecessary requests to Craigslist.
- Implement date cutoff to only scrape new postings.
- Switch from crawling pages that have been saved locally to crawling the live Craigslist website.

## Disclaimer
This project is for non-commercial use.
