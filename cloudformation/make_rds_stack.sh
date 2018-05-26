#!/bin/bash

RDS_TEMPLATE=outputs/rds.json

PASS=$(pwgen 13 1)

$PASS > dbpass.txt

read -p 'VpcId: ' VPCID
read -p 'Admin Username: ' USERNAME
echo    'Admin Password: '$PASS

python3 tropo/hyp3_rds.py $RDS_TEMPLATE

python3 -m awscli cloudformation create-stack  \
    --stack-name hyp3dbtest  \
    --template-body file://$(pwd)/$RDS_TEMPLATE \
    --parameters  \
        ParameterKey=DBUser,ParameterValue=$USERNAME \
        ParameterKey=DBPassword,ParameterValue=$PASS
        ParameterKey=MyVpcId,ParameterValue=$VPCID
