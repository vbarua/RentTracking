import os
import re
import scrapy

from RentTrackers.managers.LoggerManager import LoggerManager as logger

log_tag = "Craigslist"


def extract_area(s):
    """
    Extract area from string like: '1br 1ba 600'. Last number is area.
    
    :param s: the string to parse
    :return: an extraction of the square footage, if found, else `""`
    """
    match = re.search(r'\d+$', s)
    if match:
        return match.group()
    else:
        return ""


def extract_bedrooms(s):
    """
    Extract # of bathrooms from a string like: '1br 1ba 600'
    
    :param s: the string to parse
    :return: an extraction of the number of bedrooms, if found, else `""`
     """
    match = re.search(r'\d+br', s)
    if match:
        bedrooms = match.group()[:-2]
        return bedrooms
    else:
        return ""


def extract_bathrooms(s):
    """
    Extract # of bedrooms from a string like: '1br 1ba 600'
    
    :param s: the string to parse
    :return: an extraction of the number of bathrooms, if found, else `""`
    """
    match = re.search(r'\d+ba', s)
    if match:
        bathrooms = match.group()[:-2]
        return bathrooms
    else:
        return ""


def get_samples_directory():
    """
    Responsible for appending the OS's current working directory to
    the defined sample directory

    :return: The proper path for the samples directory
    """
    cwd = os.getcwd()
    logger.debug(__name__, "CWD: {}".format(cwd))

    sample_directory = "RentTrackers/output/Craigslist/samples/"
    logger.debug(__name__, "SAMPLES: {}".format(sample_directory))

    joined_dir = os.path.join(cwd, sample_directory)
    logger.debug(__name__, "JOINED: {}".format(joined_dir))

    return joined_dir


def extract_address(response):
    """

    :param response: 
    :return: 
    """
    address_option = response.css("span.postingtitletext small::text").extract_first()
    # Address are formatted as " (ADDRESS)"
    if address_option is None:
        return ""
    else:
        return address_option.lstrip(" (").rstrip(' )')


def extract_bdrs_bths_area(response):
    """

    :param response: 
    :return: 
    """
    raw_bdrs_bths_area = response.css("p.attrgroup span.shared-line-bubble b::text").extract()
    bdrs_bths_area = " ".join(raw_bdrs_bths_area).lower()

    area = extract_area(bdrs_bths_area)
    num_bathrooms = extract_bathrooms(bdrs_bths_area)
    num_bedrooms = extract_bedrooms(bdrs_bths_area)
    return num_bedrooms, num_bathrooms, area


def extract_housing_type(attributes):
    """
    Return the type of housing if available.

    :param attributes: 
    :return: 
    """
    return "TODO"


def extract_laundry_type(attributes):
    """
    Return the type of laundry.

    :param attributes: 
    :return: 
    """
    return "TODO"


def extract_parking_type(attributes):
    """
    Return the type of parking if available.

    :param attributes: 
    :return: 
    """
    return "TODO"


class CraigslistListingSpider(scrapy.Spider):
    """
    
    """
    name = "Craigslist"

    def start_requests(self):
        """
        Overridden method from scrapy.spiders.Spider
        Generates a series of requests with which to crawl over and parse
        
        :return: iterable of scrapy.http.request.Request
        """

        sample_dir = get_samples_directory()
        logger.debug(__name__, "Looking for sample posts in {}".format(sample_dir))
        samples = os.listdir(sample_dir)
        urls = ["file://" + sample_dir + s for s in samples]
        for url in urls:
            logger.debug(__name__, "Sampling URL: {}".format(url))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """
        Overridden method from scrapy.spiders.Spider
        Gets text response from web requests and is responsible for parsing and serializing them
        
        :param response: an instance of scrapy.http.response.Response 
        :return: Dictionary of parsed results
        """
        post_link = response.css("link::attr(href)").extract_first()
        post_id = post_link.split("/")[-1]
        post_time = response.css("time::attr(datetime)").extract_first()

        price = response.css('span.price::text').extract_first()

        latitude = response.css("#map::attr(data-latitude)").extract_first()
        longitude = response.css("#map::attr(data-longitude)").extract_first()

        address = self._extract_address(response)
        (num_bedrooms, num_bathrooms, area) = self._extract_bdrs_bths_area(response)

        attributes = " ".join(response.css("p.attrgroup span::text").extract()).lower()
        cats_allowed = "cats are ok" in attributes
        dogs_allowed = "dogs are ok" in attributes
        is_furnished = "TODO"
        laundry_type = self._extract_laundry_type(attributes)
        housing_type = self._extract_housing_type(attributes)
        no_smoking = "no smoking" in attributes
        parking_type = self._extract_parking_type(attributes)
        wheelchair_accessible = "wheelchair accessible" in attributes

        yield {
            "post_link": post_link,
            "post_id": post_id,
            "post_time": post_time,
            "address": address,
            "area": area,
            "bathrooms": "" if num_bathrooms is None else num_bathrooms,
            "bedrooms": "" if num_bedrooms is None else num_bedrooms,
            "is_furnished": is_furnished,
            "housing_type": housing_type,
            "laundry": laundry_type,
            "location": {
                "latitude": latitude,
                "longitude": longitude
            },
            "parking": parking_type,
            "pets": {
                "cats_allowed": cats_allowed,
                "dogs_allowed": dogs_allowed
            },
            "no_smoking": no_smoking,
            "wheelchair_accessible": wheelchair_accessible,
        }
