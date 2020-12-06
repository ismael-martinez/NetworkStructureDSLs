from CodeGen.Python.networkStructureAttributesAndInstances import *
from CodeGen.Python.networkUtil import *
#from networkStructureAttributesAndInstances import *
#from networkUtil import *
from CodeGen.Python.Simulation import *
from Simulation import *
import numpy as np
import random
import copy

events = 50
p = 0.4
random.seed(events)
ns = network_structure.graph.nodes
queues = {}
for node in ns:
    service_rate = 5*np.random.random()
    queues[node] = Queue(node, service_rate)

arrival_rate = 3
arrivals = np.zeros(events)
arrivals[0] = 0.0
for e in range(1, events):
    arrivals[e] = arrivals[e-1] + np.random.exponential(1/arrival_rate)
departures = np.zeros(events)

all_events = []
events_O = []
events_H = []

for e in range(events):
    tasks = np.random.randint(1, 3)
    event_path = random_path(tasks)
    arrival_event = np.zeros(tasks)
    departure_event = np.zeros(tasks)
    arrival_event[0] = arrivals[e]
    id = 'e' + str(e)
    p_sample = np.random.rand()
    if p_sample < p:
        events_H.append(Event(id, arrival_event, departure_event, event_path, hidden=True))
    else:
        events_O.append(Event(id, arrival_event, departure_event, event_path))
# Init calls execution_initial() internally
S = Simulation(events_O, events_H, queues)
for e in S.event_triggers:
    print(e[0])

# Copy the hidden events with real values for testing. Deep copy creates new objects with their own references
events_H_actual = copy.deepcopy(events_H)

# TODO - Bass
# Init simulation
#S = Simulation()
runs = 10
for i in range(runs):
    # Build sample d [departure_times]

    [service_times, wait_times] = S.update_hidden_events(events_H)
    # Gibbs sampling from metrics
    # Use S.joint_density_log()
