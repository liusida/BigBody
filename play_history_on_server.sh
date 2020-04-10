#!/bin/sh

python /mnt/bluemoon/BigBody$1/latest_history.py
./VoxCAD `python /mnt/bluemoon/BigBody$1/latest_history.py`&