CLONE_TOKEN=$(aws ssm get-parameter --name /CodeBuild/GITHUB_HYP3_API_CLONE_TOKEN --output text --with-decryption | awk {'print $6'})

rm -rf ./hyp3-in-a-box

git clone --single-branch -b dev https://$CLONE_TOKEN@github.com/asfadmin/hyp3-in-a-box --depth=1

pushd hyp3-in-a-box

python3.6 -m pip install -e \
    ./modules/hyp3_events
python3.6 -m pip install -e \
    ./modules/hyp3_process

pushd ./processes/$PROCESS/.
sudo python3.6 install.py $CLONE_TOKEN

cp src/hyp3_handler.py build

popd
popd
