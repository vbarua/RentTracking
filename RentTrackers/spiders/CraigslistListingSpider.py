import json
import os
import scrapy
from scrapy import signals

from RentTrackers.spiders.JsonCache import JsonCache
from RentTrackers.managers.LoggerManager import LoggerManager as logger
import RentTrackers.spiders.CraigslistParsingUtilities as cpu

log_tag = "Craigslist"


def get_samples_directory():
    """
    Responsible for appending the OS's current working directory to
    the defined sample directory

    :return: The proper path for the samples directory
    """
    cwd = os.getcwd()
    # assume that we are running this from the root of the repo
    sample_directory = "testing/samples/CraigslistListings/"
    return os.path.join(cwd, sample_directory)


class CraigslistListingSpider(scrapy.Spider):
    """
    
    """
    name = "CraigslistListings"

    post_id_cache_location = "output/post_cache.txt"

    def __init__(self):
        super().__init__()
        self.crawl_list_location = os.environ["CRAWL_SET_LOCATION"]
        self.post_id_cache = JsonCache(self.post_id_cache_location)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        """
        Attaching the spider_closed method to the spider_closed signal.
        """
        spider = super(CraigslistListingSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        """
        Operations to perform once the spider terminates.
        """
        logger.info(__name__, "Writing Post ID Cache")
        self.post_id_cache.write_cache()

    def start_requests(self):
        """
        Overridden method from scrapy.spiders.Spider
        Generates a series of requests with which to crawl over and parse
        
        :return: iterable of scrapy.http.request.Request
        """

        use_samples = os.environ.get("TEST")
        if use_samples:
            sample_dir = get_samples_directory()
            samples = os.listdir(sample_dir)
            urls = ["file://" + sample_dir + s for s in samples]
            for url in urls:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )
        else:
            with open(self.crawl_list_location, 'r') as f:
                crawl_list = json.load(f)

            logger.info(__name__, "Starting Craigslist Crawl")
            for i in crawl_list:
                post_id = i["post_id"]
                if self.post_id_cache.contains(post_id):
                    break

                url = i["url"]
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                )

    def parse(self, response):
        """
        Parses the contents of a Craiglist listing page. Returns a dictionary of the contents.

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

        results = cpu.extract_attributes(response)

        # TODO: Use models
        #latlng = LatLng(latitude=latitude, longitude=longitude)
        # house_unit = HouseUnit(
        #     type="rental",
        #     location=latlng,
        #     address=address,
        #     bedrooms=num_bedrooms,
        #     bathrooms=num_bathrooms,
        #     area=area,
        #     parking_spots=parking_type,
        #     smoking_allowed=no_smoking,
        #     wheelchair_access=wheelchair_accessible,
        #     laundry_onsite=laundry_type
        # )
        #
        # rental = Rental(
        #     url=post_link,
        #     id=post_id,
        #     # TODO: add post_time (post model?)
        #     city="",
        #     price=price,
        #     house_unit=house_unit
        # )
        #
        # yield rental

        base_results = {
            "post_link": post_link,
            "post_id": post_id,
            "post_time": post_time,
        }
        base_results.update(results)

        self.post_id_cache.add(post_id)

        yield base_results
