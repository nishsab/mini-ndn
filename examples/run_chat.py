# -*- Mode:python; c-file-style:"gnu"; indent-tabs-mode:nil -*- */
#
# Copyright (C) 2015-2020, The University of Memphis,
#                          Arizona Board of Regents,
#                          Regents of the University of California.
#
# This file is part of Mini-NDN.
# See AUTHORS.md for a complete list of Mini-NDN authors and contributors.
#
# Mini-NDN is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mini-NDN is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mini-NDN, e.g., in COPYING.md file.
# If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys
import os, time
import psutil

from mininet.log import setLogLevel, info, debug
from mininet.topo import Topo
from minindn.apps.application import Application

from minindn.helpers.nfdc import Nfdc
from minindn.minindn import Minindn
from minindn.util import MiniNDNCLI
from minindn.apps.app_manager import AppManager
from minindn.apps.nfd import Nfd
from minindn.helpers.ndn_routing_helper import NdnRoutingHelper

import time
from stats_logger import StatsLogger
from collections import defaultdict

def get_host_name(row, col):
    return "node_{}_{}".format(row, col)

class SvsChatApplication(Application):
    """
    Wrapper class to run the chat application from each node
    """
    def __init__(self, node):
        Application.__init__(self, node)

    def get_svs_identity(self):
        return "/ndn/{0}-site/{0}/svs_chat/{0}".format(self.node.name)

    def start(self):
        info("[{0}] Starting svs chat\n".format(self.node.name))
        identity = self.get_svs_identity()
        run_cmd = "/opt/svs/chat {} &".format(identity)
        info("[{}] Running {}\n".format(self.node.name, run_cmd))
        ret = self.node.cmd(run_cmd)
        info("pid: {}\n".format(ret))
        #self.pid = int(ret.split()[1])
    def is_running(self):
        return psutil.pid_exists(self.pid)
        #try:
        #    os.kill(self.pid, 0)
        #except OSError:
        #    return False
        #else:
        #    return True
    def cpu_percent(self):
        p = psutil.Process(self.pid)
        return p.cpu_percent()
class IdentityApplication(Application):
    """
    Small program to create an identity on each node and save the certification to a common directory
    """
    def __init__(self, node, key_dir="/opt/svs/example-security"):
        Application.__init__(self, node)
        self.key_dir = key_dir

    def get_svs_identity(self):
        return "/ndn/{0}-site/{0}/svs_chat/{0}".format(self.node.name)

    def start(self):
        info("[{0}] Starting identity application\n".format(self.node.name))

        identity = self.get_svs_identity()
        info("[{}] Creating identity {}\n".format(self.node.name, identity))
        self.node.cmd("ndnsec-key-gen -i {} -t r".format(identity))

        key_path = "{}/{}.cert".format(self.key_dir, self.node.name)
        info("[{}] saving key to {}\n".format(self.node.name, key_path))
        self.node.cmd("ndnsec cert-dump `ndnsec get-default -c -i {}` > {}".format(identity, key_path))

def count_running(pids):
    return sum(psutil.pid_exists(pid) for pid in pids)

def get_cpu_percents(processes):
    cpu_percents = []
    for p in processes:
        try:
            cpu_percents.append(p.cpu_percent())
        except:
            pass
    return cpu_percents

def get_pids():
    pids = []
    for proc in psutil.process_iter():
       try:
           pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
           # Check if process name contains the given name string.
           if "chat" in pinfo['name'].lower() :
               pids.append(pinfo['pid'])
       except (psutil.NoSuchProcess, psutil.AccessDenied , psutil.ZombieProcess) :
           pass
    return pids
                        

if __name__ == '__main__':
    setLogLevel('info')

    Minindn.cleanUp()
    Minindn.verifyDependencies()

    parser = argparse.ArgumentParser()
    parser.add_argument('--face-type', dest='faceType', default='udp', choices=['udp', 'tcp'])
    parser.add_argument('--routing', dest='routingType', default='link-state',
                         choices=['link-state', 'hr', 'dry'],
                         help='''Choose routing type, dry = link-state is used
                                 but hr is calculated for comparision.''')
    parser.add_argument('--svs-prefix', dest='svsPrefix', default='/ndn/svs',
                        help='''prefix for nfd multicast strategy.''')
    parser.add_argument('--width', dest='width', type=int, required=True,
                         help='''number of nodes in width''')
    parser.add_argument('--height', dest='height', type=int, required=True,
                         help='''number of nodes in height''')
    
    topo = Topo()

    args = parser.parse_args()
    height, width = args.height, args.width
    print height, width

    info("Creating a grid topology of height {} and width {}\n".format(height, width))

    hosts = [ [ None for col in range(width) ] for row in range(height) ]

    for row in range(height):
        for col in range(width):
            host_name = get_host_name(row, col)
            info(host_name + '\n')
            hosts[row][col] = topo.addHost(host_name)

    routes = defaultdict(list)
    for row in range(height):
        for col in range(width):
            if row + 1 < height:
                topo.addLink(hosts[row][col], hosts[row+1][col], delay='10ms')
                routes[hosts[row][col]].append([hosts[row+1][col], "1", hosts[row+1][col]])
                routes[hosts[row+1][col]].append([hosts[row][col], "1", hosts[row][col]])
            if col + 1 < width:
                topo.addLink(hosts[row][col], hosts[row][col+1], delay='10ms')
                routes[hosts[row][col]].append([hosts[row][col+1], "1", hosts[row][col+1]])
                routes[hosts[row][col+1]].append([hosts[row][col], "1", hosts[row][col]])

    ndn = Minindn(parser=parser, topo=topo)

    ndn.start()

    info('Starting NFD on nodes\n')
    nfds = AppManager(ndn, ndn.net.hosts, Nfd)

    info('Setting NFD strategy to multicast on all nodes with prefix {}\n'.format(ndn.args.svsPrefix))
    for node in ndn.net.hosts:
        #Nfdc.setStrategy(node, ndn.args.svsPrefix, Nfdc.STRATEGY_MULTICAST)
        Nfdc.setStrategy(node, "/", Nfdc.STRATEGY_MULTICAST)

    info('Adding static routes to NFD\n')
    grh = NdnRoutingHelper(ndn.net, ndn.args.faceType, ndn.args.routingType)
    for row in range(height):
        for col in range(width):
            host_name = get_host_name(row, col)
            grh.addOrigin([ndn.net[host_name]], ["/ndn/svs"])

    start = int(time.time() * 1000)
    #grh.calculateNPossibleRoutes()
    #grh.calculateRoutes()
    grh.routes = routes
    grh.globalRoutingHelperHandler()
    end = int(time.time() * 1000)
    info('Added static routes to NFD in {} ms\n'.format(end - start))

    info('Route addition to NFD completed\n')
    identity_app = AppManager(ndn, ndn.net.hosts, IdentityApplication)
    svs_chat_app = AppManager(ndn, ndn.net.hosts, SvsChatApplication)
    time.sleep(5)

    pids = get_pids()
    info("pids: {}\n".format(pids))
    count = count_running(pids)
    processes = [ psutil.Process(pid) for pid in pids ]
    cpu_percents = get_cpu_percents(processes)

    load_averages = []
    total_cpu_percents = []
    while count > 0:
        info("{} nodes are runnning\n".format(count))
        load_average = os.getloadavg()
        load_averages.append(load_average[0])
        info("load average: {}\n".format(load_average))
        cpu_percents = get_cpu_percents(processes)
        total_cpu_percents.extend(cpu_percents)
        info("cpu percents: {}\n".format(cpu_percents))
        time.sleep(5)
        count = count_running(pids)
    stats_logger = StatsLogger(width, height, load_averages, total_cpu_percents)
    logfile = stats_logger.log_stats()
    info("summary located at {}\n".format(logfile))
             
    #MiniNDNCLI(ndn.net)

    ndn.stop()