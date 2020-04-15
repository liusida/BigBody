#!/bin/sh

python /mnt/bluemoon/$1/latest_history.py
./VoxCAD `python /mnt/bluemoon/$1/latest_history.py`&