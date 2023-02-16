import sys
import csv
import json


def save_data_csv(validators):
    for pool in validators:
        try:
            with open(f'./data/{pool}.csv', 'a') as file:
                file.truncate(0)  # Delete file contents
                writer = csv.writer(file)
                writer.writerow(
                    ["index", "validator_address", "depositor_address"])
                for validator in validators[pool]:
                    writer.writerow(
                        [validator["index"], validator["validator_address"], validator["depositor_address"]])
                return True
        except NameError:
            print(NameError)
            return False


sys.modules[__name__] = save_data_csv
