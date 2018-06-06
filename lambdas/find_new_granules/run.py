
from src import find_new
from src.find_new import environment as env


def main():
    env.set_is_production(False)
    find_new.granules()


if __name__ == "__main__":
    main()
