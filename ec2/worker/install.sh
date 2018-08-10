REPO_PATH=/home/ubuntu/hyp3-in-a-box

python3.6 -m pip install -e \
    $REPO_PATH/modules/hyp3_events 
python3.6 -m pip install -e \
    $REPO_PATH/modules/hyp3_process

cp $REPO_PATH/ec2/worker/hyp3.service /etc/systemd/system/ 
cp $REPO_PATH/ec2/worker/src/hyp3_daemon.py /opt/hyp3/
