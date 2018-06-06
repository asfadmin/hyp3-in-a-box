
docs() {
    cd docs && make clean html && cd ..
    aws s3 sync docs/_build/html s3://asf-docs/hyp3-in-a-box
}

if [ "$1" = "docs" ]
then
    docs
else
    echo "upload.sh [docs]"
fi
