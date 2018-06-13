#!/bin/bash
source "$1bin/activate"
python $2manage.py clearsessions
python $2manage.py clearusers
