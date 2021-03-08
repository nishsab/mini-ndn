#!/bin/bash

NAME=$1
NUM_NODES=$2
TOPO_FILE=$3
LOSS_TAG=$4

if [ "x$NAME" = "x" ]; then
    echo Usage: $0 name num_nodes topo_file
    exit
fi
if [ "x$NUM_NODES" = "x" ]; then
    echo Usage: $0 name num_nodes topo_file
    exit
fi
if [ "x$TOPO_FILE" = "x" ]; then
    echo Usage: $0 name num_nodes topo_file
    exit
fi


rm -rf /tmp/minindn/*
rm /opt/svs/logs/svs/*
rm /opt/svs/terminal.log

python examples/geant_split.py --name $NAME --num_nodes $NUM_NODES --topo_file $TOPO_FILE --loss_tag $LOSS_TAG


