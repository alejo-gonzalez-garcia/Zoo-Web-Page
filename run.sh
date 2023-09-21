#!/usr/bin/env bash

source ./venv/bin/activate

export FLASK_APP=zoo

python -m flask --debug run
