# create_stack.py
# Rohan Weeden, William Horn
# Created: May 24, 2018

# Generates the CloudFormation stack json

import argparse
import os
import pathlib as pl
import re
from importlib import import_module

# Add values here for new sections
TEMPLATE_DIR = 'templates'


def pattern_match_hyp3_files():
    sections = {}

    templates_path = pl.Path(os.path.dirname(os.path.realpath(__file__))) / TEMPLATE_DIR

    for f in templates_path.iterdir():
        hyp3_file_match = re.match(r'hyp3_(.*)\.py', f.name)

        if not hyp3_file_match:
            continue

        core_name = hyp3_file_match.groups()[0]

        module_name = 'hyp3_{name}'.format(
            name=core_name
        )

        sections[core_name] = module_name

    return sections


TEMPLATE_SECTIONS = pattern_match_hyp3_files()


def main():
    parser = get_parser()
    args = parser.parse_args()

    add_templates(vars(args))


def get_parser():
    parser = argparse.ArgumentParser(
        description=('Generate select parts of the hyp3'
                     ' cloudformation template.')
    )

    add_output_folder(parser)
    add_flag_argument(
        parser, 'debug',
        desc='print out the generated template.'
    )

    for section_name in TEMPLATE_SECTIONS.keys():
        add_flag_argument(parser, section_name)

    return parser


def add_output_folder(parser):
    parser.add_argument('output', help='''Output path where the cloudformation
            template will be written''')


def add_flag_argument(parser, name, desc=None):
    if desc is None:
        desc = 'Build the {} portion of the template'.format(name)

    parser.add_argument(
        '--' + name, help=desc,
        dest=name, action='store_const',
        const=True, default=False
    )


def add_templates(args):
    should_make_all = get_should_make_all(args)

    add_sections_to_template(should_make_all, args)

    generate_template(args['output'], args['debug'])


def get_should_make_all(args):
    for section in TEMPLATE_SECTIONS:
        if args[section]:
            return False

    return True


def add_sections_to_template(should_make_all, args):
    for section, module_name in TEMPLATE_SECTIONS.items():
        if should_make_all or args[section]:
            import_module('templates.' + module_name)


def generate_template(output_path, debug):
    from template import t
    write_file(t, output_path, debug)


def write_file(t, file_name, debug):
    with open(file_name, 'w') as f:
        generated_template = t.to_json()

        if debug:
            print(generated_template)

        f.write(generated_template)


if __name__ == '__main__':
    main()
