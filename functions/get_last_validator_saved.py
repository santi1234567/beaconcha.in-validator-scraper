import csv
import sys
import os


def get_last_validator_saved():
    try:
        file_path = './data/validators.csv'
        file_exists = os.path.exists(file_path)
        last_validator_saved = 0
        if file_exists:
            with open(file_path, 'r', encoding="utf-8") as file:
                # Last line is empty so grab the one before
                final_line = file.readlines()[-2]
                last_validator_saved = final_line.split(',')[0]
        return last_validator_saved
    except NameError:
        raise Exception(NameError)


sys.modules[__name__] = get_last_validator_saved
