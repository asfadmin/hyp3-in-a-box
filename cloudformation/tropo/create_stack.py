# create_stack.py
# Rohan Weeden, William Horn
# Created: May 24, 2018

# Generates the CloudFormation stack json

import argparse
import json
import pathlib as pl
import re
from importlib import import_module

from template import t
from environment import environment

TEMPLATE_DIR = 'templates'


def pattern_match_hyp3_files():
    sections = {}

    templates_path = pl.Path(__file__).parent / TEMPLATE_DIR

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
    args = vars(parser.parse_args())

    set_environment_variables(args)
    make_template(args)

    if args['config']:
        generate_config_template(args['config'], args['debug'])


def set_environment_variables(args):
    for arg_name, arg_value in args.items():

        if arg_value is None or not is_env_arg(arg_name):
            continue

        print("setting ", arg_name, " to ", arg_value)
        setattr(environment, arg_name, arg_value)


def is_env_arg(arg_name):
    return arg_name in environment.__dict__


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
    parser.add_argument(
        '--config',
        help="generate a configuration template with the provided name"
    )

    for section_name in TEMPLATE_SECTIONS.keys():
        add_flag_argument(parser, section_name)

    for var_name, var_type in environment.get_variables():
        add_env_var_to(parser, var_name, var_type)

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


def add_env_var_to(parser, var_name, var_type):
    if var_type is bool:
        var_type = str2bool

    parser.add_argument(
        '--' + var_name, type=var_type,
        help="Set environment variable {}".format(var_name)
    )


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def make_template(args):
    should_make_all = get_should_make_all(args)

    add_sections_to_template(should_make_all, args)

    generate_template(args['output'], args['debug'])


def get_should_make_all(args):
    return not any(args[s] for s in TEMPLATE_SECTIONS)


def add_sections_to_template(should_make_all, args):
    for section, module_name in TEMPLATE_SECTIONS.items():
        if should_make_all or args[section]:
            import_module('templates.{}'.format(module_name))


def generate_template(output_path, debug):
    write_file(t, output_path, debug)


def generate_config_template(output_path, debug):
    params = {}
    for (param_name, param_value) in t.parameters.items():
        print("{}: ".format(param_name), end='')
        params[param_name] = input()
    config = {
        "Parameters": params
    }
    if debug:
        print(json.dumps(config, indent=4))
    else:
        with open(output_path, "w") as f:
            json.dump(config, f, indent=4)


def write_file(t, file_name, debug):
    with open(file_name, 'w') as f:
        generated_template = t.to_json()

        if debug:
            print(generated_template)

        f.write(generated_template)


if __name__ == '__main__':
    main()
