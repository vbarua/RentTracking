import json
import logging
import os
import scrapy
from scrapy import signals

from .utils import send_email, IdCache
import RentTrackers.spiders.CraigslistParsingUtilities as CPU


def get_samples() -> list:
    """
    "Retrieve scraping samples from sample directory.

    :return: List of file urls.
    """
    cwd = os.getcwd()
    # Assume that we are running this from the root of the repo
    sample_dir = os.path.join(cwd, "testing/samples/CraigslistListings/")
    samples = os.listdir(sample_dir)
    urls = ["file://" + sample_dir + s for s in samples]
    return urls


class CraigslistListingSpider(scrapy.Spider):
    name = "CraigslistListings"

    def __init__(self):
        super().__init__()
        self.post_count = 0
        self.city = os.environ["CITY"]
        post_id_cache_location = os.path.join("output", self.city, "cl_post_id_cache.txt")
        self.post_id_cache = IdCache(post_id_cache_location)
        self.html_output_path = os.environ["CL_HTML_OUTPUT_LOCATION"]
        os.makedirs(self.html_output_path)
        self.crawl_set_location = os.environ["CL_CRAWL_SET_LOCATION"]
        self.test_mode = False
        if os.environ.get("TEST"):
            self.test_mode = True


    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        Attaching the spider_closed method to the spider_closed signal.
        """
        spider = super(CraigslistListingSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def item_scraped(self, item, spider):
        self.post_count += 1

    def spider_closed(self, spider):
        """
        Operations to perform once the spider terminates.
        """
        if not self.test_mode:
            logging.info("Writing Post ID Cache")
            self.post_id_cache.write_cache()
            logging.info("Send Scrape Email")
            send_email(self.city, self.post_count)

    def start_requests(self):
        """
        Overridden method from scrapy.spiders.Spider
        Generates a series of requests with which to crawl over and parse

        :return: iterable of scrapy.http.request.Request
        """
        if self.test_mode:
            urls = get_samples()
            for url in urls:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )
        else:
            with open(self.crawl_set_location, 'r') as f:
                crawl_list = json.load(f)

            logging.info("Starting Craigslist Crawl")
            for i in crawl_list:
                post_id = i["post_id"]
                url = i["url"]
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )

    def parse(self, response):
        """
        Parses the contents of a Craigslist listing page. Returns a dictionary of the contents.

        :param response: an instance of scrapy.http.response.Response
        :return: Dictionary of parsed results
        """

        is_deleted = response.css("div.removed")
        if is_deleted:
            return {}

        # Rental
        post_link = response.css("link::attr(href)").extract_first()
        post_id = int(post_link.split("/")[-1][:-5])
        post_time = response.css("time::attr(datetime)").extract_first()

        body = response.text
        with open(os.path.join(self.html_output_path, str(post_id) + ".html"), "w") as f:
            f .write(body)

        results = CPU.extract_attributes(response)

        base_results = {
            "post_link": post_link,
            "post_id": post_id,
            "post_time": post_time,
        }
        base_results.update(results)

        self.post_id_cache.add(post_id)
        yield base_results
