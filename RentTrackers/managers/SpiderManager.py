
from RentTrackers import settings


class SpiderManager:
    def __init__(self):
        """

        """

        super().__init__()


def get_spiders():
    """
    Gets the registered Spiders for Scrapy

    :return: settings.SPIDER_MODULES
    """
    return settings.SPIDER_MODULES
