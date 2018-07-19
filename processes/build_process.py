#! /usr/bin/env python3
# build_lambda.py
# Rohan Weeden, William Horn
# Created: August 1, 2017

# Script for zipping up monitor lambda function source and dependencies

import os
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from zipfile import ZIP_DEFLATED, ZipFile

PSYCOPG2_REPO = 'https://github.com/jkehler/awslambda-psycopg2'


class Logger(object):
    """Simple standin for logging module"""

    def __init__(self, level):
        self.level = level

    @staticmethod
    def info(*args, **kwargs):
        print(*args, **kwargs)

    def debug(self, *args, **kwargs):
        if self.level == "debug":
            print(*args, **kwargs)


log = Logger(None)


def make_zip(path, zip_name):
    """Zip all the files without any sub directories"""
    src_dir = os.path.join(path, 'src')
    with ZipFile(zip_name, 'w', compression=ZIP_DEFLATED) as zf:
        reqs_file = 'requirements.txt'
        reqs_path = os.path.join(path, reqs_file)

        zf.write(reqs_path, arcname=reqs_file)

        for src_file in os.listdir(src_dir):
            if '__pycache__' in src_file:
                continue

            src_path = os.path.join(src_dir, src_file)
            if os.path.isfile(src_path):
                zf.write(src_path, arcname=src_file)
            elif os.path.isdir(src_path):
                add_folder_to_zip(src_dir, src_file, zf)


def add_folder_to_zip(containing_dir, folder, zf):
    for fname in os.listdir(os.path.join(containing_dir, folder)):
        full_name = os.path.join(containing_dir, folder, fname)
        local_name = os.path.join(folder, fname)
        if os.path.isdir(full_name):
            add_folder_to_zip(containing_dir, local_name, zf)
        else:
            zf.write(full_name, arcname=local_name)


def build_lambda(path, zip_name):
    abspath = os.path.abspath(path)
    log.debug("path: {}".format(path))
    log.info("Installing latest version of dependencies")
    log.info("Creating zip file")

    make_zip(abspath, zip_name)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "source_path",
        help=("outer folder of the function to build, if --all"
              " is set, then path to the containing folder")
    )
    parser.add_argument(
        "-a", "--all", action="store_true",
        help="build all functions found in source_path"
    )
    parser.add_argument("-o", "--outfile",
                        help="name of the zip file to produce")
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="enable additional debug output"
    )
    return parser.parse_args()


def get_zipfile_name(source_path):
    if source_path[-1] == '/':
        source_path = source_path[:-1]
    zip_name = source_path.split("/")[-1].lower() + ".zip"
    return zip_name


def build_lambda_from_path(path, outfile=None):
    zip_name = outfile

    if zip_name is None:
        zip_name = get_zipfile_name(path)
    build_lambda(path, zip_name)


def main(args):
    path = args.source_path
    outfile = args.outfile

    if args.all:
        log.info("Building all lambdas")
        for d in os.listdir(path):
            curr_path = os.path.join(path, d)
            if os.path.isdir(curr_path):
                try:
                    build_lambda_from_path(
                        curr_path, outfile=os.path.join(outfile, d) + ".zip")
                except FileNotFoundError:
                    continue
    else:
        build_lambda_from_path(path, outfile=outfile)


if __name__ == "__main__":
    passed_args = parse_args()
    if passed_args.verbose:
        log = Logger('debug')

    try:
        main(passed_args)
    except FileNotFoundError as e:
        log.info("Missing file or directory: {}".format(e.filename))
        sys.exit(-1)
    except KeyboardInterrupt:
        log.debug("Quitting...")
