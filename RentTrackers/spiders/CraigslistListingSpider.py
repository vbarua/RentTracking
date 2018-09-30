import os
import re
import locale
import scrapy

from RentTrackers.managers.LoggerManager import LoggerManager as logger
from RentTrackers.models.HouseUnit import HouseUnit
from RentTrackers.models.LatLng import LatLng
from RentTrackers.models.Rental import Rental

log_tag = "Craigslist"


def extract_area(s):
    """
    Extract area from string like: '1br 1ba 600'. Last number is area.
    
    :param s: the string to parse
    :return: an extraction of the square footage, if found
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
    :return: an extraction of the number of bedrooms, if found
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
    :return: an extraction of the number of bathrooms, if found
    """
    match = re.search(r'\d+ba', s)
    if match:
        bathrooms = match.group()[:-2]
        return bathrooms
    else:
        return ""


def extract_price(response):
    """
    Extract price 

    :param response: the web response to parse
    :return: an extraction of the price (trimmed to an integer)
    """
    price = response.css('span.price::text').extract_first()
    decimal_point_char = locale.localeconv()['decimal_point']
    return re.sub(r'[^0-9' + decimal_point_char + r']+', '', price)


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
    return (num_bedrooms, num_bathrooms, area)


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
    return False


def extract_parking_type(attributes):
    """
    Return the type of parking if available.

    :param attributes: 
    :return: 
    """
    return 0


def get_samples_directory():
    """
    Responsible for appending the OS's current working directory to
    the defined sample directory

    :return: The proper path for the samples directory
    """
    cwd = os.getcwd()
    # assume that we are running this from the root of the repo
    sample_directory = "RentTrackers/output/Craigslist/samples/"
    return os.path.join(cwd, sample_directory)


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

        # Rental
        post_link = response.css("link::attr(href)").extract_first()
        post_id = post_link.split("/")[-1]
        post_time = response.css("time::attr(datetime)").extract_first()
        price = extract_price(response)

        # LatLng
        latitude = response.css("#map::attr(data-latitude)").extract_first()
        longitude = response.css("#map::attr(data-longitude)").extract_first()

        # HouseInfo
        address = extract_address(response)
        (num_bedrooms, num_bathrooms, area) = extract_bdrs_bths_area(response)

        attributes = " ".join(response.css("p.attrgroup span::text").extract()).lower()
        cats_allowed = "cats are ok" in attributes
        dogs_allowed = "dogs are ok" in attributes
        is_furnished = "TODO"
        laundry_type = extract_laundry_type(attributes)
        housing_type = extract_housing_type(attributes)
        no_smoking = "no smoking" in attributes
        parking_type = extract_parking_type(attributes)
        wheelchair_accessible = "wheelchair accessible" in attributes

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

        yield {
            "post_link": post_link,
            "post_id": post_id,
            "post_time": post_time,
            "price": price,
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
