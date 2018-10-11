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
        area = match.group()
        return {"area": area}
    else:
        return {}


def extract_bedrooms(s) -> dict:
    """
    Extract # of bathrooms from a string like: '1br 1ba 600'

    :param s: the string to parse
    :return: an extraction of the number of bedrooms, if found
     """
    match = re.search(r'\d+br', s)
    if match:
        bedrooms = match.group()[:-2]
        return {"bedrooms": bedrooms}
    else:
        return {}


def extract_bathrooms(s) -> dict:
    """
    Extract # of bedrooms from a string like: '1br 1ba 600', '1br sharedba 400'

    :param s: the string to parse
    :return: an extraction of the number of bathrooms, if found
    """
    num_match = re.search(r'\d(\.\d)?ba', s)
    if num_match:
        bathrooms = num_match.group()[:-2]
        return {"bathrooms": bathrooms}
    type_match = re.search(r'[a-z]+ba', s)
    if type_match:
        bathrooms = type_match.group()[:-2]
        return {"bathrooms": bathrooms}
    return {}


def extract_price(response) -> dict:
    """
    Extract price

    :param response: the web response to parse
    :return: an extraction of the price (trimmed to an integer)
    """
    price = response.css('span.price::text').extract_first()
    if price:
        decimal_point_char = locale.localeconv()['decimal_point']
        formatted_price = re.sub(r'[^0-9' + decimal_point_char + r']+', '', price)
        return {"price": formatted_price}
    else:
        return {}


def extract_address(response) -> dict:
    """

    :param response:
    :return:
    """
    address_option = response.css("span.postingtitletext small::text").extract_first()
    # Address are formatted as " (ADDRESS)"
    if address_option is None:
        return {}
    else:
        clean_address = address_option.lstrip(" (").rstrip(' )')
        return {"address": clean_address}


def extract_bdrs_bths_area(response: dict):
    """

    :param response:
    :return:
    """
    raw_bdrs_bths_area = response.css("p.attrgroup span.shared-line-bubble b::text").extract()
    bdrs_bths_area = " ".join(raw_bdrs_bths_area).lower()

    results = {}
    results.update(extract_area(bdrs_bths_area))
    results.update(extract_bathrooms(bdrs_bths_area))
    results.update(extract_bedrooms(bdrs_bths_area))
    return results


def extract_lat_long(response) -> dict:
    latitude = response.css("#map::attr(data-latitude)").extract_first()
    longitude = response.css("#map::attr(data-longitude)").extract_first()
    return {
        "latitude": latitude,
        "longitude": longitude
    }


def extract_attributes(response) -> dict:
    results = {}
    results.update(extract_price(response))
    results.update(extract_address(response))
    results.update(extract_lat_long(response))
    results.update(extract_bdrs_bths_area(response))
    results.update(extract_unstructured_attributes(response))
    return results


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
