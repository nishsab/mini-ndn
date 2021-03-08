#!/bin/bash

cd ~/src/ndn-svs/
./waf configure --enable-static --disable-shared --with-examples --option2-just-latest
./waf
cd ~/mini-ndn
bash partial_run.sh option2-just-latest_20_05 20 topologies/geant_05.conf 5.0
#bash partial_run.sh option2-just-latest_20_05 20 topologies/geant_05.conf 5.0
#bash partial_run.sh option2-just-latest_20_05 20 topologies/geant_05.conf 5.0
bash partial_run.sh option2-just-latest_30_05 30 topologies/geant_05.conf 5.0
#bash partial_run.sh option2-just-latest_30_05 30 topologies/geant_05.conf 5.0
#bash partial_run.sh option2-just-latest_30_05 30 topologies/geant_05.conf 5.0
bash partial_run.sh option2-just-latest_40_05 40 topologies/geant_05.conf 5.0
#bash partial_run.sh option2-just-latest_40_05 40 topologies/geant_05.conf 5.0
#bash partial_run.sh option2-just-latest_40_05 40 topologies/geant_05.conf 5.0
#
cd ~/src/ndn-svs/
./waf configure --enable-static --disable-shared --with-examples --option3-latest-plus-random
./waf
cd ~/mini-ndn
bash partial_run.sh option3-latest-plus-random1_20_05 20 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random1_20_05 20 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random1_20_05 20 topologies/geant_05.conf 5.0
bash partial_run.sh option3-latest-plus-random1_30_05 30 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random1_30_05 30 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random1_30_05 30 topologies/geant_05.conf 5.0
bash partial_run.sh option3-latest-plus-random1_40_05 40 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random1_40_05 40 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random1_40_05 40 topologies/geant_05.conf 5.0
#
cd ~/src/ndn-svs/
./waf configure --enable-static --disable-shared --with-examples --option3-latest-plus-random3
./waf
cd ~/mini-ndn
bash partial_run.sh option3-latest-plus-random3_20_05 20 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random3_20_05 20 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random3_20_05 20 topologies/geant_05.conf 5.0
bash partial_run.sh option3-latest-plus-random3_30_05 30 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random3_30_05 30 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random3_30_05 30 topologies/geant_05.conf 5.0
bash partial_run.sh option3-latest-plus-random3_40_05 40 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random3_40_05 40 topologies/geant_05.conf 5.0
#bash partial_run.sh option3-latest-plus-random3_40_05 40 topologies/geant_05.conf 5.0
