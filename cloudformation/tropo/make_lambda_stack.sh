source db_creds.sh

TEMPLATE=outputs/lambdas.json

python3 create_stack.py \
    --find_new \
    --scheduler \
    --send_email \
    --lambda_bucket hyp3-in-a-box-lambdas \
    --maturity test \
    --db_host $HOST \
    --db_pass $PASS \
    --db_user $USER \
    --db_name $DB \
    $TEMPLATE

python3 -m awscli cloudformation create-stack  \
    --stack-name $1 \
    --template-body file://$(pwd)/$TEMPLATE \
    --capabilities CAPABILITY_IAM \
    --tags \
        Key="Developer",Value="William Horn" \
        Key="Purpose",Value="Testing" \
    --parameters \
        ParameterKey=VerifiedSourceEmail,ParameterValue="wbhorn@alaska.edu"\
        ParameterKey=FindNewName,ParameterValue=Hyp3FindNewGranules1 \
        ParameterKey=SchedulerName,ParameterValue=Hyp3Scheduler1 \
        ParameterKey=SendEmailName,ParameterValue=Hyp3SendEmail1
