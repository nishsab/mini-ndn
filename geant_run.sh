#!/bin/bash

NAME=$1

rm -rf /tmp/minindn/*
rm /opt/svs/logs/svs/*

if [ "x$NAME" = "x" ]; then
    python examples/geant_run_chat.py
else
    python examples/geant_run_chat.py --name $NAME
fi

