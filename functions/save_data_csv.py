import sys
import csv
import os


def save_data_csv(validators):
    try:
        file_path = './data/validators.csv'
        file_exists = os.path.exists(file_path)
        with open(file_path, 'a', encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(
                    ["index", "pool", "validator_address", "depositor_address"])
            for validator in validators:
                writer.writerow(
                    [validator["index"], validator["pool"], validator["validator_address"], validator["depositor_address"]])
            return True
    except NameError:
        print(NameError)
        return False


sys.modules[__name__] = save_data_csv
