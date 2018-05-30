#!/bin/bash

RDS_TEMPLATE=tropo/outputs/rds.json

PASS=$(pwgen 13 1)

echo $PASS > dbpass.txt

read -p 'Admin Username: ' USERNAME
echo    'Admin Password: '$PASS

python tropo/create_stack.py --rds --vpc $RDS_TEMPLATE

python3 -m awscli cloudformation create-stack  \
    --stack-name hyp3dbtest  \
    --template-body file://$(pwd)/$RDS_TEMPLATE \
    --parameters \
        ParameterKey=Hyp3DBUser,ParameterValue=$USERNAME \
        ParameterKey=Hyp3DBPassword,ParameterValue=$PASS
