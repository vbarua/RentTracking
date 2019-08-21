import scrapy


class Post(scrapy.Item):
    url = scrapy.Field()
    post_id = scrapy.Field()
    repost_id = scrapy.Field()
