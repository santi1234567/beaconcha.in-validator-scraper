import sys


def get_validator_data(soup):
    pool, validator_address, depositor_address = None, None, None

    pool_element = soup.find('abbr', {
        'title': 'This name has been set by the owner of this validator. Pool tags have been set by the beaconcha.in team.'})
    if pool_element:  # If not, validator doesn't have a pool identified and None value remains
        # Remove excess text and return pool name
        pool = pool_element.text.replace("Pool: ", "")

    validator_address_element = soup.find(
        'div', {'class': 'text-monospace text-secondary text-truncate text-sm mb-0'})
    if validator_address_element:
        validator_address = validator_address_element.text

    depositor_address_element = soup.find(
        'a', {'class': 'text-monospace'})
    if depositor_address_element:
        depositor_address = depositor_address_element['href'].replace(
            "/address/", "")  # Find "a" element, get its href and remove excess string

    return pool, validator_address, depositor_address


sys.modules[__name__] = get_validator_data
