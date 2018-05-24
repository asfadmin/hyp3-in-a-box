RDS_TEMPLATE=templates/rds.json

PASS=$(pwgen 13 1)

read -p 'Admin Username: ' USERNAME
echo    'Admin Password: '$PASS

python3 tropo/hyp3_rds.py $RDS_TEMPLATE

python3 -m awscli cloudformation create-stack  \
    --stack-name hyp3dbtest  \
    --template-body file://$(pwd)/$RDS_TEMPLATE \
    --parameters  \
        ParameterKey=DBUser,ParameterValue=$USERNAME \
        ParameterKey=DBPassword,ParameterValue=$PASS
