import notify_only


def process_function():
    gran_poly = "POLYGON((30.45 18.59,30.77 20.10," \
        "28.40 20.53,28.10 19.02,30.45 18.59))"
    sub_poly = "POLYGON((24.20 26.37,33.43 28.63,41.07 " \
        "18.91,29.41 12.70,17.80 19.94,24.20 26.37))"

    png_path = notify_only.browse(gran_poly, sub_poly)

    print("Made png: {}".format(png_path))


if __name__ == "__main__":
    process_function()
