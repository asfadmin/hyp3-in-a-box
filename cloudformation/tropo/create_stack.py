# create_stack.py
# Rohan Weeden
# Created: May 24, 2018

# Generates the CloudFormation stack json

import argparse

"""Add values here for new sections"""
TEMPLATE_SECTIONS = {
    'rds': 'from templates import hyp3_rds',
    'eb': 'from templates import hyp3_api_eb'
}


def get_parser():
    parser = argparse.ArgumentParser(
        description=('Generate select parts of the hyp3'
                     ' cloudformation template.')
    )

    add_output_folder(parser)

    for section_name in TEMPLATE_SECTIONS.keys():
        add_flag_argument(parser, section_name)

    return parser


def add_output_folder(parser):
    parser.add_argument('output', help='''Output path where the cloudformation
            template will be written''')


def add_flag_argument(parser, name):
    parser.add_argument(
        '--' + name,
        help='Build the {} portion of the template'.format(name),
        dest=name, action='store_const',
        const=True, default=False
    )


def add_templates(args):
    should_make_all = get_should_make_all(args)

    add_sections_to_template(should_make_all, args)

    generate_template(args['output'])


def get_should_make_all(args):
    for section in TEMPLATE_SECTIONS:
        if args[section]:
            return False

    return True


def add_sections_to_template(should_make_all, args):
    for section, import_stmt in TEMPLATE_SECTIONS.items():
        if should_make_all or args[section]:
            exec(import_stmt)


def generate_template(output_path):
    from template import t
    write_file(t, output_path)


def write_file(t, file_name):
    with open(file_name, 'w') as f:
        print(t.to_json())
        f.write(t.to_json())


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    add_templates(vars(args))
