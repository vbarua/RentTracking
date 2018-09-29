import os
import re
import scrapy

#sample_directory = "/home/vbarua/Dropbox/Projects/VTU/Samples/Craigslist/"
sample_directory = "/output/Samples/Craigslist/"


def extract_area(s):
    """
    Extract area from string like: '1br 1ba 600'. Last number is area.
    
    :param s: 
    :return: 
    """
    match = re.search(r'\d+$', s)
    if match:
        return match.group()
    else:
        return ""


def extract_bedrooms(s):
    """
    Extract # of bathrooms from a string like: '1br 1ba 600'
    
    :param s: 
    :return: 
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
    
    :param s: 
    :return: 
    """
    match = re.search(r'\d+ba', s)
    if match:
        bathrooms= match.group()[:-2]
        return bathrooms
    else:
        return ""


class CraigslistListingSpider(scrapy.Spider):
    """
    
    """
    name = "Craigslist"

    def start_requests(self):
        samples = os.listdir(sample_directory)
        urls = ["file://" + sample_directory + s for s in samples]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def _extract_address(self, response):
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

    def _extract_bdrs_bths_area(self, response):
        """
        
        :param response: 
        :return: 
        """
        raw_bdrs_bths_area = response.css("p.attrgroup span.shared-line-bubble b::text").extract()
        bdrs_bths_area = " ".join(raw_bdrs_bths_area).lower()

        area = extract_area(bdrs_bths_area)
        num_bathrooms = extract_bathrooms(bdrs_bths_area)
        num_bedrooms = extract_bedrooms(bdrs_bths_area)
        return(num_bedrooms, num_bathrooms, area)

    def _extract_housing_type(self, attributes):
        """
        Return the type of housing if available.
        
        :param attributes: 
        :return: 
        """
        return "TODO"

    def _extract_laundry_type(self, attributes):
        """
        Return the type of laundry.
        
        :param attributes: 
        :return: 
        """
        return "TODO"

    def _extract_parking_type(self, attributes):
        """
        Return the type of parking if available.
        
        :param attributes: 
        :return: 
        """
        return "TODO"

    def parse(self, response):
        """
        
        :param response: 
        :return: 
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
