# beaconcha.in-validator-scraper

The scraper grabs validator data from beachoncha.in and stores it in csv format.

The script can be run to get a single validator:

```sh
python scraper.py VALIDATOR_INDEX
```

or to get multiple validators:

```sh
python scraper.py FIRST_VALIDATOR_INDEX LAST_VALIDATOR_INDEX
```

or also in free_run mode:

```sh
python scraper.py
```
