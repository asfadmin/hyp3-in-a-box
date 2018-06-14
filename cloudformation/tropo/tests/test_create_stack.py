import os

import boto3

from create_stack import make_template

client = boto3.client('cloudformation')

def test_create_stack():
    template_file = 'template.json'
    make_template({'maturity': 'test', 'output': template_file})

    assert os.path.isfile(template_file)

    os.remove(template_file)


def test_create_stack_makes_valid_stack():
    template_file = 'template.json'
    make_template({'maturity': 'test', 'output': template_file})

    with open(template_file, 'r') as f:
        template = f.read()

    response = client.validate_template(
        TemplateBody=template
    )

    assert response
    print(response)
    os.remove(template_file)
