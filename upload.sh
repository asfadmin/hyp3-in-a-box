#! /bin/bash

docs() {
    cd docs && make clean html && cd ..
    aws s3 cp docs/_build/html s3://asf-docs/hyp3-in-a-box --recursive
}

if [ "$1" = "docs" ]
then
    docs
else
    echo "upload.sh [docs]"
fi
