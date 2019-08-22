import logging
import os
from scrapy.exceptions import DropItem

from RentTrackers.utils import IdCache, send_email


class PostDeduplicationPipeline(object):

    def __init__(self):
        city = os.environ["CITY"]
        post_id_cache_location = os.path.join("output", city, "cl_post_id_cache.txt")
        self.post_id_cache = IdCache(post_id_cache_location)

    def close_spider(self, spider):
        logging.info("Writing Post ID Cache")
        self.post_id_cache.write_cache()

    def process_item(self, item, spider):
        post_id = item.get("post_id")
        if not post_id:
            raise DropItem("Post Id Not Populated")

        if self.post_id_cache.contains(post_id):
            raise DropItem("Post has already been scraped")
        else:
            return item


class EmailNotificationPipeline(object):
    """
    Sends an email with the total item count on scrape completion.
    """

    def __init__(self):
        self.city = os.environ["CITY"]
        self.counter = 0

    def close_spider(self, spider):
        logging.info("Closing Email Notification Pipeline")
        if not os.environ.get("TEST"):
            logging.info("Send Scrape Email")
            send_email(self.city, self.counter)

    def process_item(self, item, spider):
        self.counter += 1
        return item
