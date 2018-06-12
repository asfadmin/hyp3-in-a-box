import json
import pathlib as pl

from src import schedule
from src.schedule.environment import environment


def main():
    creds, granules = load_creds(), load_test_data()
    environment.set_db_creds(creds)

    schedule.hyp3_jobs(granules)


def load_creds():
    with open('tests/creds.json', 'r') as f:
        return json.load(f)


def load_test_data():
    path = pl.Path(__file__).parent / 'tests'/'data'/'new_granules.json'
    with path.open('r') as f:
        return json.load(f)


if __name__ == "__main__":
    main()
