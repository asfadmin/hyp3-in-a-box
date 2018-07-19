#! /bin/bash

PY_VERSION=3.6.5

install_apt_packages() {
    sudo apt update -y && apt upgrade -y
    sudo apt install -y unzip python3-pip
}


install_python_prereqs() {
    sudo apt update -y && sudo apt upgrade -y

    sudo apt install -y  \
        build-essential libffi-dev python-dev libssl-dev zlib1g-dev \
        libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
        libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev tk-dev
}

download_python() {
    wget https://www.python.org/ftp/python/$PY_VERSION/Python-$PY_VERSION.tar.xz
    tar xf Python-$PY_VERSION.tar.xz
}


install_python() {
    pushd Python-$PY_VERSION
        ./configure --enable-optimizations
        make -j 8
        sudo make altinstall
    popd
}

install_python36_from_source() {
    install_python_prereqs

    download_python
    install_python
}


main() {
    install_apt_packages
    install_python36_from_source
}

main
