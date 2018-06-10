#!/bin/bash
source "$1bin/activate"
python $2manage.py clearsessions
python $2maintance/clearusers.py
