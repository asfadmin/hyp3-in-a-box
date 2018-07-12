#!/bin/bash

CONF=configuration.json
BUCKET=hyp3-in-a-box
OBJ_KEY=$BUCKET/test/config/$CONF

if [ "$1" = "down" ]
then
    aws s3 cp s3://$OBJ_KEY $CONF
elif [ "$1" = "up" ]
then
    aws s3 cp $CONF s3://$OBJ_KEY
else
    echo "$0 [down|up]"
fi
