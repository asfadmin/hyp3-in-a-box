STACK_NAME=$1

set -e
source db_creds.sh

TEMPLATE=outputs/notify-only-lambdas.json

python create_stack.py \
    --find_new \
    --should_create_db false \
    --use_name_parameters false \
    --maturity unittest \
    --lambda_bucket hyp3-in-a-box-lambdas \
    $TEMPLATE

if [ "$2" = "create" ]
then
    python3 -m awscli cloudformation create-stack  \
        --stack-name $STACK_NAME \
        --template-body file://$(pwd)/$TEMPLATE \
        --capabilities CAPABILITY_IAM \
        --tags \
            Key="Developer",Value="William Horn" \
            Key="Purpose",Value="Testing" \
        --parameters \
            ParameterKey=VerifiedSourceEmail,ParameterValue="wbhorn@alaska.edu"\
            ParameterKey=ExistingHyp3DBHostUrl,ParameterValue=$HOST \
            ParameterKey=ExistingHyp3DBName,ParameterValue=$DB \
            ParameterKey=ExistingHyp3DBUser,ParameterValue=$USER \
            ParameterKey=ExistingHyp3DBUserPassword,ParameterValue=$PASS \
            ParameterKey=ExistingHyp3DBSuperUser,ParameterValue=$USER \
            ParameterKey=ExistingHyp3DBSuperUserPassword,ParameterValue=$PASS
fi
