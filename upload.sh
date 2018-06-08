
docs() {
    cd docs && make html && cd ..
    aws s3 cp --recursive docs/_build/html s3://asf-docs/hyp3-in-a-box
}

if [ "$1" = "docs" ]
then
    docs
else
    echo "upload.sh [docs]"
fi
