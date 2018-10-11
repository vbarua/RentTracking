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
