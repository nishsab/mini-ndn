#!/bin/bash

WIDTH=$1
HEIGHT=$2
NAME=$3

if [ "x$WIDTH" = "x" ]; then
    echo Usage: $0 width height
    exit
fi
if [ "x$HEIGHT" = "x" ]; then
    echo Usage: $0 width height
    exit
fi

rm -rf /tmp/minindn/node_*
rm /opt/svs/logs/svs/node_*

if [ "x$NAME" = "x" ]; then
    python examples/run_chat.py --width $WIDTH --height $HEIGHT
else
    python examples/run_chat.py --width $WIDTH --height $HEIGHT --name $NAME
fi

