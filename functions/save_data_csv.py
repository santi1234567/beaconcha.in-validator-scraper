import sys
import csv


def save_data_csv(validators):
    try:
        with open(f'./data/validators.csv', 'a') as file:
            file.truncate(0)  # Delete file contents
            writer = csv.writer(file)
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
