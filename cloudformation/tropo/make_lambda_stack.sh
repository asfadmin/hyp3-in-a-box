STACK_NAME=$1

set -e
source db_creds.sh

TEMPLATE=outputs/lambdas.json

python3 create_stack.py \
    --find_new \
    --scheduler \
    --send_email \
    --lambda_bucket hyp3-in-a-box-lambdas \
    --maturity test \
    --db_host $HOST \
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
            ParameterKey=FindNewName,ParameterValue=Hyp3FindNewGranules1 \
            ParameterKey=SchedulerName,ParameterValue=Hyp3Scheduler1 \
            ParameterKey=SendEmailName,ParameterValue=Hyp3SendEmail1 \
            ParameterKey=Hyp3DBName,ParameterValue=$DB \
            ParameterKey=Hyp3DBUser,ParameterValue=$USER \
            ParameterKey=Hyp3DBPassword,ParameterValue=$PASS
fi
