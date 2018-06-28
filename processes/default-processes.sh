#!/bin/bash

BUCKET=$(jq -r '.processes_bucket' < .config.json)
KEY=$(jq -r '.default_processes_key' < .config.json)
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
