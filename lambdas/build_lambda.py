#! /usr/bin/env python3
# build_lambda.py
# Rohan Weeden, William Horn
# Created: August 1, 2017

# Script for zipping up monitor lambda function source and dependencies

import os
from argparse import ArgumentParser
from zipfile import ZIP_DEFLATED, ZipFile

import subprocess
import sys


class Logger(object):
    """Simple standin for logging module"""

    def __init__(self, level):
        self.level = level

    def info(self, *args, **kwargs):
        print(*args, **kwargs)

    def debug(self, *args, **kwargs):
        if self.level == "debug":
            print(*args, **kwargs)


log = Logger(None)


def install_dependencies(path):
    """ Install required modules to dependencies folder """
    with open(os.path.join(path, 'requirements.txt')) as f:
        for line in f.readlines():
            package = line.strip()

            log.debug('Installing {}'.format(package))
            install_package(path, package, os.path.join(path, 'dependencies'))


def install_package(path, package_name, output_dir):
    subprocess.call([sys.executable, '-m', 'pip', 'install', '--compile', '--upgrade', package_name, '-t', output_dir])


def make_zip(path, zip_name):
    """Zip all the files without any sub directories"""
    src_dir = os.path.join(path, 'src')
    with ZipFile(zip_name, 'w', compression=ZIP_DEFLATED) as zf:
        for src_file in os.listdir(src_dir):
            src_path = os.path.join(src_dir, src_file)
            if os.path.isfile(src_path):
                zf.write(src_path, arcname=src_file)
            elif os.path.isdir(src_path):
                add_folder_to_zip(src_dir, src_file, zf)

        dependencies = os.path.join(path, 'dependencies')
        for dep_dir in os.listdir(dependencies):
            full_path = os.path.join(dependencies, dep_dir)
            if '.dist-info' or '.egg-info' in full_path:
                continue
            if os.path.isdir(full_path):
                add_folder_to_zip(dependencies, dep_dir, zf)
            else:
                zf.write(full_path, arcname=dep_dir)


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
    install_dependencies(abspath)
    log.info("Creating zip file")

    make_zip(abspath, zip_name)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("source_path", help="outer folder of the function to build, if --all is set, then path to the containing folder")
    parser.add_argument("-a", "--all", help="build all functions found in source_path", action="store_true")
    parser.add_argument("-o", "--outfile", help="name of the zip file to produce")
    parser.add_argument("-v", "--verbose", help="enable additional debug output", action="store_true")
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
        for d in os.listdir(path):
            if os.path.isdir(d):
                try:
                    build_lambda_from_path(os.path.join(path, d), outfile=os.path.join(outfile, d) + ".zip")
                except FileNotFoundError:
                    continue
    else:
        build_lambda_from_path(path, outfile=outfile)


if __name__ == "__main__":
    args = parse_args()
    if args.verbose:
        log = Logger('debug')

    try:
        main(args)
    except FileNotFoundError as e:
        log.info("Missing file or directory: {}".format(e.filename))
        sys.exit(-1)
    except KeyboardInterrupt:
        log.debug("Quitting...")
