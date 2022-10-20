#!/usr/bin/env bash

echo "Creating log directory"
LOG_DIR="./logs"
if [ ! -d "$LOG_DIR" ]; then
    mkdir ./logs
else
    echo "$LOG_DIR already exists"
fi 

echo "Downloading virtual environment tools"
python3 -m pip install virtualenv 

echo "Creating virtual environment"
virtualenv env 

echo "Installing libraries in virtual environment"
./env/bin/python3 -m pip install -r requirements.txt

echo ""
echo "Create cloud firestore directory and fill out environment variables in .env file using .env_sample"

