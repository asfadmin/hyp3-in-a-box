#!/bin/bash

BUCKET=$(cat .config.json | jq -r '.processes_bucket')
KEY=$(cat .config.json | jq -r '.default_processes_key')
OBJ_KEY=$BUCKET/$KEY

if [ "$1" = "down" ]
then
    aws s3 cp s3://$OBJ_KEY $(basename $KEY)
elif [ "$1" = "up" ]
then
    aws s3 cp $(basename $KEY) s3://$OBJ_KEY
else
    echo "$0 [down|up]"
fi
