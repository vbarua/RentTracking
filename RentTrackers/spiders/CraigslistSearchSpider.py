import os
import scrapy

from RentTrackers.items import Post


class CraigslistSearchSpider(scrapy.Spider):
    name = "CraigslistSearch"

    custom_settings = {
        "ITEM_PIPELINES": {
            "RentTrackers.pipelines.PostDeduplicationPipeline": 500
        }
    }

    def __init__(self):
        super().__init__()
        self.city = os.environ["CITY"]
        self.base_search_url = "https://" + self.city + ".craigslist.ca/search/apa?sort=date&"

    def start_requests(self):
        url = self.base_search_url
        yield scrapy.Request(
            url=url,
            callback=self.parse,
        )

    def parse(self, response):
        next_page = response.xpath('//link[@rel="next"]/@href').extract_first()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse,
            )

        results = response.css("li.result-row")
        for r in results:
            post = Post()
            post["url"] = r.css("a.result-title::attr(href)").extract_first()
            post["post_id"] = int(r.css("li.result-row::attr(data-pid)").extract_first())
            post["repost_id"] = r.css("li.result-row::attr(data-repost-of)").extract_first()
            yield post
