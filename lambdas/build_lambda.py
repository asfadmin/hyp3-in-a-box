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


def install_dependencies(path):
    """ Install required modules to dependencies folder """
    req_file = os.path.join(path, 'requirements.txt')
    deps_dir = os.path.join(path, 'dependencies')

    subprocess.check_call([
        sys.executable, '-m', 'pip', 'install', '--compile', '-r',
        req_file, '-t', deps_dir
    ], cwd=path
    )

    if psycopg2_is_dependency(deps_dir):
        shutil.rmtree(os.path.join(deps_dir, 'psycopg2'))
        install_lambda_compatible_psycopg2(path)


def psycopg2_is_dependency(deps_dir):
    return any(dep for dep in os.listdir(deps_dir) if 'psycopg2' in dep)


def install_lambda_compatible_psycopg2(path):
    print('installing psycopg2...')
    repo = 'psycopg2'
    subprocess.check_call([
        'git', 'clone', '--depth', '1', PSYCOPG2_REPO, repo
    ], cwd=path)

    repo_path = os.path.join(path, repo)

    src = os.path.join(repo_path, 'psycopg2-3.6')
    dest = os.path.join(path, 'dependencies', 'psycopg2')

    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    shutil.rmtree(repo_path)


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
            if '.dist-info' in full_path or '.egg-info' in full_path:
                continue
            if os.path.isdir(full_path):
                add_folder_to_zip(dependencies, dep_dir, zf)
            else:
                zf.write(full_path, arcname=dep_dir)

        print('removing dependencies folder')
        shutil.rmtree(dependencies)


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

            lambda_file = os.path.join(curr_path, "src/lambda_function.py")
            if os.path.isdir(curr_path) and os.path.isfile(lambda_file):
                try:
                    build_lambda_from_path(
                        curr_path, outfile=os.path.join(outfile, d) + ".zip"
                    )
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
