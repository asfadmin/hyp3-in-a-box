#!/bin/bash

RDS_TEMPLATE=templates/rds.json

UUID=$(uuid)

read -p 'Admin Username: ' USERNAME
echo    'Admin Password: '$UUID

python3 tropo/hyp3_rds.py $RDS_TEMPLATE

python3 -m awscli cloudformation create-stack  \
    --stack-name hyp3dbtest  \
    --template-body file://$(pwd)/$RDS_TEMPLATE \
    --parameters  \
        ParameterKey=DBUser,ParameterValue=USERNAME \
        ParameterKey=DBPassword,ParameterValue=$UUID
