#!/bin/bash
cd ~
git clone https://github.com/Han-xox/15-418-final.git
sudo apt-get update
sudo apt-get install python-pip python-dev -y
pip install virtualenv
cd ./15-418-final
virtualenv --no-site-packages venv
source ./venv/bin/activate
pip install -r requirements.txt
