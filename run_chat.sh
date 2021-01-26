#!/bin/bash

WIDTH=$1
HEIGHT=$2

if [ "x$WIDTH" = "x" ]; then
    echo Usage: $0 width height
    exit
fi
if [ "x$HEIGHT" = "x" ]; then
    echo Usage: $0 width height
    exit
fi

rm -rf /tmp/minindn/node_*
rm /home/ubuntu/logs/svs/node_*
python examples/run_chat.py --width $WIDTH --height $HEIGHT
