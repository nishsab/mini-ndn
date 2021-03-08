#!/bin/bash

WIDTH=$1
HEIGHT=$2
NAME=$3
LOSS=$4

if [ "x$WIDTH" = "x" ]; then
    echo Usage: $0 width height name
    exit
fi
if [ "x$HEIGHT" = "x" ]; then
    echo Usage: $0 width height name
    exit
fi
if [ "x$NAME" = "x" ]; then
    echo Usage: $0 width height name
    exit
fi

rm -rf /tmp/minindn/*
rm /opt/svs/logs/svs/*
rm /opt/svs/terminal*.log

if [ "x$LOSS" = "x" ]; then
    python examples/run_chat.py --width $WIDTH --height $HEIGHT --name $NAME
else
    python examples/run_chat.py --width $WIDTH --height $HEIGHT --name $NAME --loss $LOSS
fi

