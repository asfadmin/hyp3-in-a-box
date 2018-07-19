#! /bin/bash

# Based on python3 ami

PROCESS=notify_only
MATURITY=local-testing
PROCESS_ZIP=$PROCESS.zip

install_aws_cli() {
    python3.6 -m pip awscli
}


install_notify_only_source() {
    mkdir $PROCESS

    pushd $PROCESS
        aws s3 cp s3://asf-hyp3-in-a-box-source/$MATURITY/$PROCESS_ZIP .
        unzip $PROCESS_ZIP
        rm $PROCESS_ZIP
        python3.6 -m pip install -r requirements.txt --user
    popd
}


main() {
    install_aws_cli
    install_notify_only_source
}

main
