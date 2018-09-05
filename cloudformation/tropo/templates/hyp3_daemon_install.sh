CLONE_TOKEN=$(aws ssm get-parameter --name /CodeBuild/GITHUB_HYP3_API_CLONE_TOKEN --output text --with-decryption | awk {'print $6'})

cd /home/ubuntu
rm -rf ./hyp3-in-a-box

git clone --single-branch -b dev https://$CLONE_TOKEN@github.com/asfadmin/hyp3-in-a-box --depth=1

pushd hyp3-in-a-box/processes/rtc_snap/.
    sudo python3.6 install.py $CLONE_TOKEN
popd

pushd hyp3-in-a-box/ec2/worker/.
    sudo ./install.sh
popd

sudo systemctl daemon-reload
echo "-Xmx32G" > /usr/local/snap/bin/gpt.vmoptions
