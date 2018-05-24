#!/bin/bash

RDS_TEMPLATE=template/rds.json

python3 hyp3_rds.py $RDS_TEMPLATE

python3 -m awscli cloudformation create-stack  \
    --stack-name hyp3dbtest  \
    --template-body file://$(pwd)/$RDS_TEMPLATE \
    --parameters  \
        ParameterKey=DBUser,ParameterValue=hyp3user \
        ParameterKey=DBPassword,ParameterValue=5wzkQw8g9K
