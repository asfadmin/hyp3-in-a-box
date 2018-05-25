# create_stack.py
# Rohan Weeden
# Created: May 24, 2018

# Generates the CloudFormation stack json

import sys

from templates import hyp3_api_eb
from template import t


def write_file(file_name):
    with open(file_name, 'w') as f:
        f.write(t.to_json())


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} out_file_name".format(sys.argv[0]))
        sys.exit(0)
    write_file(sys.argv[1])
