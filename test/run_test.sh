#!/bin/bash

pip install -r requirements.txt -r requirements-dev.txt
python -m pytest
