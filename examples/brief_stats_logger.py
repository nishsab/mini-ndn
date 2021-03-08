#!/usr/bin/python

import glob
from datetime import datetime
from collections import defaultdict

class StatsLogger:
    stats_directory = "/opt/svs/stats"
    log_files_path = "/opt/svs/logs/svs/*"
    def __init__(self, name, width, height, load_averages, cpu_percents):
        self.width = width
        self.height = height
        self.load_averages = load_averages
        self.cpu_percents = cpu_percents
        self.name = name
    def get_filename(self):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        return "{}/stats_{}_{}_{}_{}.txt".format(StatsLogger.stats_directory, self.name, timestamp, self.width, self.height)
    def readlines(self):
        sv_lines = []
        stats_lines = []
        for logfile in glob.glob(StatsLogger.log_files_path):
            print("Reading {}".format(logfile))
            with open(logfile) as fd:
                sv_lines.extend([ line.rstrip() for line in fd.readlines()])
            stats_lines.append(sv_lines.pop())
        sv_lines.sort()
        return sv_lines, stats_lines
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
        sv_lines, stats_lines = self.readlines()
        node_counts = self.get_node_counts()
        print("node counts: {}".format(node_counts))
        load_stats = self.get_load_stats()
        print("load stats: {}".format(load_stats))
        event_counts = self.count_events(stats_lines)
        print("event counts: {}".format(event_counts))
        state_vector_stats = self.assess_state_vector(sv_lines)
        print("state vector stats: {}".format(state_vector_stats))
        self.write_to_file(filename, node_counts + load_stats + event_counts + state_vector_stats)
        return filename
    def get_node_counts(self):
        return [ ("num nodes", self.width * self.height), ("width", self.width), ("height", self.height) ]
    def get_load_stats(self):
        average_load_average = sum(self.load_averages) / len(self.load_averages)
        average_cpu_percent = sum(self.cpu_percents) / len(self.cpu_percents)
        return [ ("average load average", average_load_average), ("average cpu percent", average_cpu_percent) ] 
    def assess_state_vector(self, lines):
        last_state_vector = {}
        for line in lines:
            if "state vector" in line:
                tokens = line.split("\t")
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
            tokens = line.split(",")
            for token in tokens:
                try:
                    term, value = token.split(":")
                    event_counts[term] += int(value)
                except:
                    print line
        return [ (term, event_counts[term]) for term in terms ] 
    
    def count_events_old(self, lines):
        terms = ["outbound sync interest", "inbound sync interest", "outbound sync ack", "inbound sync ack", "sync nack", "sync timeout", "inbound data interest", "outbound data interest", "outbound data timeout retry", "inbound data packet"]
        event_counts = defaultdict(int)
        for line in lines:
            for term in terms:
                if term in line:
                    event_counts[term] += 1
        return [ (term, event_counts[term]) for term in terms ] 

        
