import requests
import sys
import math
import time
from bs4 import BeautifulSoup
from functions import get_validator_data, save_data_csv, get_last_validator_saved
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# TODO: Handle error when GET request doesn't return code 200

SCRAPE_COOLDOWN = 0.01  # seconds
FIRST_VALIDATOR_ARGUMENT_INDEX = 1
LAST_VALIDATOR_ARGUMENT_INDEX = 2
FREE_RUN_MODE_BATCH_SIZE = 50


def scrape_url(index):  # make a GET request to the URL
    url = 'https://beaconcha.in/validator/'+str(index)+'#deposits'
    return requests.get(url), index


if __name__ == "__main__":
    max_pools = cpu_count()
    start_time = time.time()
    first_validator_index = 0
    last_validator_index = 0
    free_run = False
    match len(sys.argv):
        case 1:
            first_validator_index = int(get_last_validator_saved())
            if first_validator_index > 0:  # If no validators are saved, start at 0
                first_validator_index += 1
            last_validator_index = first_validator_index + \
                FREE_RUN_MODE_BATCH_SIZE
            free_run = True
        case 2:
            first_validator_index = int(
                sys.argv[FIRST_VALIDATOR_ARGUMENT_INDEX])
            last_validator_index = first_validator_index
        case 3:
            first_validator_index = int(
                sys.argv[FIRST_VALIDATOR_ARGUMENT_INDEX])
            last_validator_index = int(
                sys.argv[LAST_VALIDATOR_ARGUMENT_INDEX]) + 1  # add one to include the last one
            if first_validator_index >= last_validator_index:
                raise Exception(
                    "First validator index must be lower than last validator index")
        case _:
            raise Exception(
                "Script should only recieve one or two arguments."
            )
    while (True):  # Will continue if free_run mode is active
        validators = []

        for i in tqdm(range(0, math.ceil((last_validator_index-first_validator_index)/max_pools))):
            number_of_pools = max_pools

            # Case that the amount of validators to fetch aren't divisible by MAX_POOLS
            if first_validator_index+(i+1)*max_pools > last_validator_index:
                number_of_pools = max_pools - \
                    (first_validator_index + (i+1)*max_pools-last_validator_index)

            indexes = range(first_validator_index+i*max_pools,
                            first_validator_index+i*max_pools+number_of_pools)

            with Pool(number_of_pools) as p:
                for response, index in p.map(scrape_url, indexes):
                    if response.status_code == 200:
                        # parse the HTML content of the response using BeautifulSoup
                        soup = BeautifulSoup(response.content, 'html.parser')

                        pool, validator_address, depositor_address = get_validator_data(
                            soup)
                        if validator_address and depositor_address:
                            if not pool:  # validator isn't labeled
                                pool = "undefined"
                            validators.append({
                                "index": index,
                                "pool": pool,
                                "validator_address": validator_address,
                                "depositor_address": depositor_address})
                        else:
                            print(
                                "Validator doesn't yet exist or page format changed")
                            free_run = False  # End free run because there are no more validators to fetch
                    else:
                        print("Failed to scrape page. Error code:",
                              response.status_code)

        save_data_csv(validators)
        if not free_run:
            break
        first_validator_index = last_validator_index
        last_validator_index = first_validator_index + \
            FREE_RUN_MODE_BATCH_SIZE + 1
    print("--- %s seconds ---" % (time.time() - start_time))
