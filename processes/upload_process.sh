MATURITY=local-testing
S3_PATH=s3://asf-hyp3-in-a-box-source/$MATURITY

update_process() {
    PROCESS_NAME=$(basename $1)
    echo "updating $PROCESS_NAME"
    echo "  building"
    python3 build_process.py $PROCESS_NAME > /dev/null
    aws s3 cp $PROCESS_NAME.zip $S3_PATH/$PROCESS_NAME.zip > /dev/null
}


if [ $# -eq 0 ]
then
    for process in $(ls -d */)
    do
        update_process $process
    done
else
    for process in "$@"
    do
        update_process $process
    done
fi



