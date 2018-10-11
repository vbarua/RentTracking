import locale
import re


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
    if price:
        decimal_point_char = locale.localeconv()['decimal_point']
        return re.sub(r'[^0-9' + decimal_point_char + r']+', '', price)
    else:
        return ""


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


VALID_HOUSING_TYPES = {
    "apartment",
    "condo",
    "cottage/cabin",
    "duplex",
    "flat",
    "house",
    "in-law",
    "loft",
    "townhouse",
    "manufactured",
    "land",
    "assisted living",
}

VALID_LAUNDRY_TYPES = {
    "w/d in unit",
    "w/d hookups",
    "laundry in bldg",
    "laundry on site",
    "no laundry on site",

}

VALID_PARKING_TYPES = {
    "carport",
    "attached garage",
    "detached garage",
    "off-street parking",
    "street parking",
    "valet parking",
    "no parking",
}


def extract_unstructured_attributes(response):
    attrs = response.css("p.attrgroup span::text").extract()
    attrs = [a.lower() for a in attrs]
    results = {}
    for a in attrs:
        if a in VALID_HOUSING_TYPES:
            results["housing_type"] = a
            break
        if a in VALID_LAUNDRY_TYPES:
            results["laundry_type"] = a
            break
        if a in VALID_PARKING_TYPES:
            results["parking_type"] = a
            break
        if a is "no smoking":
            results["is_no_smoking"] = True
            break
        if a is "wheelchair accessible":
            results["is_wheelchair_accessible"] = True
            break
        if a is "furnished":
            results["is_furnished"] = True
            break
        if a is "dogs are ok":
            results["dogs_allowed"] = True
            break
        if a is "cats are ok":
            results["cats_allowed"] = True

    return results
