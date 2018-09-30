from RentTrackers.managers import SpiderManager

spiders = []


class RentTrackers:


    def __init__(self):
        """
        
        """

        super().__init__()

        self.spiders = SpiderManager.get_spiders()


def crawl_sources:
    for spider in spiders:
        print(spider)





