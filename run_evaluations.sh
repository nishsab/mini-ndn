#!/bin/bash

NAME=$1
if [ "x$NAME" = "x" ]; then
    echo Usage: $0 name
    exit
fi

#bash partial_run.sh ${NAME}_20_00 20 topologies/geant.conf 0.0
#bash partial_run.sh ${NAME}_20_00 20 topologies/geant.conf 0.0
#bash partial_run.sh ${NAME}_20_00 20 topologies/geant.conf 0.0
#bash partial_run.sh ${NAME}_25_00 25 topologies/geant.conf 0.0
#bash partial_run.sh ${NAME}_25_00 25 topologies/geant.conf 0.0
#bash partial_run.sh ${NAME}_25_00 25 topologies/geant.conf 0.0
bash partial_run.sh ${NAME}_30_00 30 topologies/geant.conf 0.0
bash partial_run.sh ${NAME}_30_00 30 topologies/geant.conf 0.0
bash partial_run.sh ${NAME}_30_00 30 topologies/geant.conf 0.0
#bash partial_run.sh ${NAME}_25_05 25 topologies/geant_05.conf 5.0
#bash partial_run.sh ${NAME}_25_05 25 topologies/geant_05.conf 5.0
#bash partial_run.sh ${NAME}_25_05 25 topologies/geant_05.conf 5.0
#bash partial_run.sh ${NAME}_25_10 25 topologies/geant_10.conf 10.0
#bash partial_run.sh ${NAME}_25_10 25 topologies/geant_10.conf 10.0
#bash partial_run.sh ${NAME}_25_10 25 topologies/geant_10.conf 10.0
#bash partial_run.sh ${NAME}_25_15 25 topologies/geant_15.conf 15.0
#bash partial_run.sh ${NAME}_25_15 25 topologies/geant_15.conf 15.0
#bash partial_run.sh ${NAME}_25_15 25 topologies/geant_15.conf 15.0

