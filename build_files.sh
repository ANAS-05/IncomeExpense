#!/bin/bash

# build_files.sh

echo "Installing the required Python packages"
# Install the required Python packages
pip install -r requirements.txt

echo "Collecting the static files"
# Collect static files without user input
python3.9 manage.py collectstatic --noinput