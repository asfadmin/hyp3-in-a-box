#!/bin/bash

CONF=configuration.json
BUCKET=asf-hyp3-in-a-box-source
OBJ_KEY=$BUCKET/test/config/$CONF

if [ "$1" = "down" ]
then
    aws s3 cp s3://$OBJ_KEY $CONF
elif [ "$1" = "up" ]
then
    aws s3 cp $CONF s3://$OBJ_KEY
else
    echo "cloudformation-config.sh [down|up]"
fi
