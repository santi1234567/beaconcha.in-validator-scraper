import requests
import sys
import time
from bs4 import BeautifulSoup
from functions import get_validator_data, save_data_csv


# TODO: Handle error when GET request doesn't return code 200

SCRAPE_COOLDOWN = 1  # seconds
FIRST_VALIDATOR_ARGUMENT_INDEX = 1
LAST_VALIDATOR_ARGUMENT_INDEX = 2


first_validator_index = 0
last_validator_index = 0
match len(sys.argv):
    case 1:
        raise Exception(
            "No arguments passed. Script must recieve at least first_validator_index ")
    case 2:
        first_validator_index = int(sys.argv[FIRST_VALIDATOR_ARGUMENT_INDEX])
        last_validator_index = first_validator_index
    case 3:
        first_validator_index = int(sys.argv[FIRST_VALIDATOR_ARGUMENT_INDEX])
        last_validator_index = int(sys.argv[LAST_VALIDATOR_ARGUMENT_INDEX])
        if first_validator_index >= last_validator_index:
            raise Exception(
                "First validator index must be lower than last validator index")
    case _:
        raise Exception(
            "Script should only recieve one or two arguments."
        )

validators = []
for i in range(first_validator_index, last_validator_index+1):
    # specify the URL to scrape
    url = 'https://beaconcha.in/validator/'+str(i)+'#deposits'

    # make a GET request to the URL
    response = requests.get(url)

    if response.status_code == 200:
        # parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        pool, validator_address, depositor_address = get_validator_data(soup)
        if validator_address and depositor_address:
            if not pool:  # validator isn't labeled
                pool = "undefined"
            validators.append({
                "index": i,
                "pool": pool,
                "validator_address": validator_address,
                "depositor_address": depositor_address})
        else:
            print("Validator doesn't yet exist or page format changed")

        time.sleep(SCRAPE_COOLDOWN)
    else:
        print("Failed to scrape page. Error code:", response.status_code)


save_data_csv(validators)
