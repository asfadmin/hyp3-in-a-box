#!/bin/bash

TEMPLATE=tropo/outputs/find-new.json

python3 tropo/create_stack.py --find_new $TEMPLATE

python3 -m awscli cloudformation create-stack  \
    --stack-name hyp3lambdatest  \
    --template-body file://$(pwd)/$TEMPLATE \
    --capabilities CAPABILITY_IAM \
    --tags \
        Key="Developer",Value="William Horn" \
        Key="Purpose",Value="Testing"
