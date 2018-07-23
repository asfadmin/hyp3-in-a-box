import os

import boto3
from hypothesis import given, settings, strategies as st

from create_stack import make_template

client = boto3.client('cloudformation')


@given(st.fixed_dictionaries({
    'maturity': st.sampled_from(['test', 'unittest', 'prod']),
    'use_name_parameters': st.booleans(),
    'should_create_db': st.booleans()
}))
def test_create_stack(params):
    template_file = 'template.json'
    params['output'] = template_file
    make_template(params)

    assert os.path.isfile(template_file)


@settings(max_examples=3, deadline=2000)
@given(st.fixed_dictionaries({
    'maturity': st.sampled_from(['test', 'unittest', 'prod']),
    'use_name_parameters': st.booleans(),
    'should_create_db': st.booleans()
}))
def test_create_stack_makes_valid_stack(params):
    template_file = 'template.json'
    params['output'] = template_file
    make_template(params)
    print('validating template')

    with open(template_file, 'r') as f:
        template = f.read()

    response = client.validate_template(
        TemplateBody=template
    )

    assert response
