#!/usr/bin/python

import glob
from datetime import datetime
from collections import defaultdict

def to_milliseconds(timestr):
    d = datetime.strptime(timestr, '%Y/%m/%d %H:%M:%S.%f').strftime('%s.%f')
    return int(float(d) * 1000)

class StatsLogger:
    stats_directory = "/opt/svs/stats"
    log_files_path = "/opt/svs/logs/svs/*"
    def __init__(self, name, width, height, load_averages, cpu_percents, loss=0.0):
        self.width = width
        self.height = height
        self.load_averages = load_averages
        self.cpu_percents = cpu_percents
        self.name = name
        self.loss = loss
    def get_filename(self):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        return "{}/stats_{}_{}_{}_{}.txt".format(StatsLogger.stats_directory, self.name, timestamp, self.width, self.height)
    def readlines(self):
        lines = []
        for logfile in glob.glob(StatsLogger.log_files_path):
            print("Reading {}".format(logfile))
            with open(logfile) as fd:
                lines.extend([ line.rstrip() for line in fd.readlines()])
        lines.sort()
        return lines
    def write_to_file(self, filename, events):
        headers = ",".join(event[0] for event in events)
        data = ",".join(str(event[1]) for event in events)
        print(headers)
        print(data)
        with open(filename, 'w') as fd:
            fd.write(headers + "\n")
            fd.write(data + "\n")
    def log_stats(self):
        filename = self.get_filename()
        print("Saving stats to {}".format(filename))
        lines = self.readlines()
        node_counts = self.get_node_counts()
        print("node counts: {}".format(node_counts))
        load_stats = self.get_load_stats()
        print("load stats: {}".format(load_stats))
        event_counts = self.count_events(lines)
        print("event counts: {}".format(event_counts))
        state_vector_stats = self.assess_state_vector(lines)
        print("state vector stats: {}".format(state_vector_stats))
        delay_stats = self.get_delay_stats(lines)
        print("delay stats: {}".format(delay_stats))
        self.write_to_file(filename, node_counts + load_stats + event_counts + state_vector_stats + delay_stats)
        return filename
    def get_node_counts(self):
        return [ ("num nodes", self.width * self.height), ("width", self.width), ("height", self.height), ("loss", self.loss) ]
    def get_load_stats(self):
        average_load_average = sum(self.load_averages) / len(self.load_averages)
        average_cpu_percent = sum(self.cpu_percents) / len(self.cpu_percents)
        return [ ("average load average", average_load_average), ("average cpu percent", average_cpu_percent) ] 
    def assess_state_vector(self, lines):
        last_state_vector = {}
        for line in lines:
            if "state vector" in line:
                tokens = line.split("\t") + [""]
                name, state_vector = tokens[1], tokens[3]
                last_state_vector[name] = state_vector
        sequence_numbers = []
        for state_vector in last_state_vector.values():
            sequence_numbers.extend([int(state.split(":")[1]) for state in state_vector.split()])
        average_sequence_number = sum(sequence_numbers) / len(sequence_numbers)
        return [ ("min sequence number", min(sequence_numbers)), ("average sequence number", average_sequence_number) ]
    def count_events(self, lines):
        terms = ["outbound sync interest", "inbound sync interest", "outbound sync ack", "inbound sync ack", "sync nack", "sync timeout", "inbound data interest", "outbound data interest", "outbound data timeout retry", "inbound data packet"]
        event_counts = defaultdict(int)
        for line in lines:
            for term in terms:
                if term in line:
                    event_counts[term] += 1
        return [ (term, event_counts[term]) for term in terms ]
    def get_delay_stats(self, lines):
        first, last = defaultdict(int), defaultdict(int)
        for line in lines:
            if "new data" in line:
                ts, node, _, node_seq = line.split("\t")
                millis = to_milliseconds(ts)
                last[node_seq] = millis
            elif "publish data" in line:
                ts, node, _, seq = line.split("\t")
                millis = to_milliseconds(ts)
                node_seq = "{}:{}".format(node, seq)
                first[node_seq] = millis
        delays = [last[node_seq] - first[node_seq] for node_seq in last if node_seq in first]
        ave_delay = sum(delays) / len(delays)
        max_delay = max(delays)
        #for l in last:
        #    print l, last[l], first[l], last[l] - first[l]


        return [ ("average delay", ave_delay), ("max delay", max_delay) ]
        

        
