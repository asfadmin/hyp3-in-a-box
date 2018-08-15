REPO_PATH=/home/ubuntu/hyp3-in-a-box

python3.6 -m pip install -e \
    $REPO_PATH/modules/hyp3_events
python3.6 -m pip install -e \
    $REPO_PATH/modules/hyp3_process


if [ "$1" = "dummy" ]
then
    echo "Using dummy handler function"
    HANDLER_PATH=./ec2/worker/hyp3_dummy_handler.py
elif [ "$1" = "copy" ]
then
    echo "Using copy handler function"
    HANDLER_PATH=./ec2/worker/hyp3_copy_handler.py
else
    echo "Using rtc_snap handler function"
    HANDLER_PATH=./processes/rtc_snap/src/hyp3_handler.py
fi


cp \
    $HANDLER_PATH
    ./ec2/worker/src/hyp3_handler.py


if [ -n "$RTC_SNAP_HANDLER" ]
then
    echo "Using rtc handler function"
    cp \
        $REPO_PATH/processes/rtc_snap/src/hyp3_handler.py \
        $REPO_PATH/ec2/worker/src/
else
    echo "Using dummy handler function"
fi

cp $REPO_PATH/ec2/worker/hyp3.service /etc/systemd/system/

cp $REPO_PATH/ec2/worker/src/hyp3_handler.py /opt/hyp3/
cp $REPO_PATH/ec2/worker/src/hyp3_daemon.py /opt/hyp3/
chmod +x /opt/hyp3/hyp3_daemon.py
