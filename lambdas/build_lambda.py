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
            install_package(path, package)


def install_package(path, package_name):
    subprocess.call([sys.executable, '-m', 'pip', 'install', '--upgrade', package_name, '-t', os.path.join(path, 'dependencies')])


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


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("source_path", help="path to the function to build")
    parser.add_argument("-v", "--verbose", help="enable additional debug output", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        log = Logger('debug')

    try:
        path = args.source_path
        if path[-1] == '/':
            path = path[:-1]
        zip_name = path.split("/")[-1].lower() + ".zip"

        build_lambda(path, zip_name)
    except FileNotFoundError as e:
        log.info("Missing file or directory: {}".format(e.filename))
    except KeyboardInterrupt:
        log.debug("Quitting...")
