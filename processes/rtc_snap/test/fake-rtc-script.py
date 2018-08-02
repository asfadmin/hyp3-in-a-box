import argparse
import os


def main():
    args = parse_args()

    granule_zip = args['granule_zip']
    granule_safe = granule_zip.replace('.zip', '.SAFE')

    assert all(os.path.exists(f) for f in (granule_zip, granule_safe))
    assert not args['asf']


def parse_args():
    parser = argparse.ArgumentParser(description='fake-rtc-script')

    parser.add_argument(
        "granule_zip",
        help="granule zip location"
    )
    parser.add_argument(
        "-t", dest="tdir",
        help="Path to input file", metavar="DIR"
    )
    parser.add_argument(
        "-r", dest="pixsiz", help="Pixel resolution - default = 10m",
        metavar="PS", default=10.0, type=float
    )
    parser.add_argument(
        "-d", "--dem", dest="extDEM",
        help="External DEM file name", metavar="DEM"
    )
    parser.add_argument(
        "-a", "--asf", action="store_true", dest="asf", default=False,
        help="Use an ASF DEM for processing"
    )
    parser.add_argument(
        "--noorbit", action="store_true", dest="noOrb", default=False,
        help="Do not apply precise orbit information"
    )
    parser.add_argument(
        "--ns", action="store_false", dest="filter", default=True,
        help="Do not apply speckle filtering"
    )
    parser.add_argument(
        "--nf", action="store_false", dest="flattening", default=True,
        help="Do not apply terrain flattening"
    )
    parser.add_argument(
        "--tnr", action="store_true", dest="thermalNoiseRemoval",
        default=False, help="Remove thermal noise"
    )
    parser.add_argument(
        "-l", "--ls", action="store_true", dest="layover", default=False,
        help="Create layover/shadow mask"
    )
    parser.add_argument(
        "-c", "--clean", action="store_true", dest="cleanTemp", default=False,
        help="Clean intermediate files"
    )
    parser.add_argument(
        "-s", "--subset", type=float, nargs=4, dest="subset",
        metavar="ullon ullat lrlon lrlat", help="Subset to take from scene"
    )

    args = parser.parse_args()

    return vars(args)


if __name__ == "__main__":
    main()
