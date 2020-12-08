from CodeGen.Python.networkStructureAttributesAndInstances import *
from CodeGen.Python.networkUtil import *
#from networkStructureAttributesAndInstances import *
#from networkUtil import *
from CodeGen.Python.Simulation import *
from Simulation import *
import numpy as np
import random
import copy

class QueueNetwork:
    def __init__(self, queue_log_dict, K):
        self.K = K
        self.log = queue_log_dict
        # Trim arrival, wait, service, and destination to 7 decimals
        for q in self.log:
            for i in range(len(self.log[q])):
                q_times = [round(self.log[q][i][t], 7) for t in range(4)]
                q_log = q_times + list(self.log[q][i][4:])
                self.log[q][i] = tuple(q_log)


    def update_deparrture_time(self, new_departure, event_id, queue_id):
        old_log = self.log[queue_id]
        print('Old')
        for l in self.log[queue_id]:
            print(l)
        print('test')
        log_id = 0
        departure_times_subserver = {}

        for i in range(len(self.log[queue_id])):
            log_entry = self.log[queue_id][i]
            departure_times_subserver[log_entry[4]] = log_entry[3] # event_id : departure_time
            if log_entry[4] == event_id:
                log_id = i
                break
        log_tuple = self.log[queue_id][log_id]
        servicing_state = log_tuple[6]
        self.log[queue_id][log_id] = (log_tuple[0], log_tuple[1], log_tuple[2], new_departure, log_tuple[4], log_tuple[5], servicing_state)
        departure_times_subserver[log_tuple[4]] = new_departure
        print(self.log[queue_id][log_id])
        print(departure_times_subserver)
        queue_events = []
        servicing = [servicing_state[q] for q in servicing_state if servicing_state[q]]
        if all(servicing):
            queue_departures = [departure_times_subserver[event] for event in servicing]
            for i in range(log_id + 1, len(old_log)):
                arrival_waiting = [old_log[i][0] < dep for dep in queue_departures]
                if all(arrival_waiting):
                    queue_events.append(old_log[i][4])
                else:
                    break

        # Rearrange log entries after the changed log
        for i in range(log_id+1, len(old_log)):
            event_id = old_log[i][4]
            arrival_time = old_log[i][0]
            departure_time = old_log[i][3]
            earliest_service_time = arrival_time
            servicing_events = [servicing_state[event] for event in servicing_state]
            if all(servicing_events):
                queue_available = [max(departure_times_subserver[event], arrival_time) for event in servicing_events]
                earliest_service_time = min(queue_available)
                subserver = 0
                for s in range(len(queue_available)):  # First argmin if multiple
                    if queue_available[s] == earliest_service_time:
                        subserver = s
                        break
            else:
                earliest_service_time = arrival_time
                subserver = 0
                for s in servicing_state:
                    sub_event = servicing_state[s]
                    if not sub_event or departure_times_subserver[sub_event] < arrival_time:
                        subserver = s
                        break

            waiting_time = round(earliest_service_time - arrival_time, 7)
            service_time = round(departure_time - arrival_time - waiting_time, 7)
            servicing_state_new = {}
            servicing_state_new[subserver] = event_id
            for s in servicing_state:
                if s == subserver:
                    continue
                event_id_old = servicing_state[s]
                if  event_id_old and departure_times_subserver[event_id_old] > arrival_time:
                    servicing_state_new[s] = event_id_old
                else:
                    servicing_state_new[s] = None

            new_log = (arrival_time, service_time, waiting_time, departure_time, event_id, subserver, servicing_state_new)
            print(new_log)
            print(old_log[i])
            compare = [new_log[t] == old_log[i][t] for t in range(len(new_log))]

            # Compare new_log with old_log
            if all(compare):
                print('Stable')
                return
            else:
                # Reconstruct relevant info from newest log
                log_tuple = new_log
                servicing_state = log_tuple[6]
                self.log[queue_id][log_id] = (
                log_tuple[0], log_tuple[1], log_tuple[2], new_departure, log_tuple[4], log_tuple[5], servicing_state)
                departure_times_subserver[log_tuple[4]] = new_departure
                queue_events = []
                servicing = [servicing_state[q] for q in servicing_state if servicing_state[q]]
                if all(servicing):
                    queue_departures = [departure_times_subserver[event] for event in servicing]
                    for i in range(log_id + 1, len(old_log)):
                        arrival_waiting = [old_log[i][0] < dep for dep in queue_departures]
                        if all(arrival_waiting):
                            queue_events.append(old_log[i][4])
                        else:
                            break



events = 50
p = 0.4
random.seed(events)
ns = network_structure.graph.nodes
queues = {}
K = 2
for node in ns:
    service_rate = 5*np.random.random()
    queues[node] = Queue(node, service_rate, K)

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
    event_path = list(random_path(tasks)) # Make copy
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
# for e in S.event_triggers:
#     print(e[0])
print('\nDeparture times')
for e in S.Events_O:
    print(e.id)
    print(e.departure_times)

queue_log = {}
for q in S.Queues:
    print('Queue {}'.format(q))
    queue = queues[q]
    queue_log[q] = queue.queue_log
    for l in queue.queue_log: # [arrival, service, wait, departure
        print(l)
    print('\n')

queue_network = QueueNetwork(queue_log, K)
queue_network.update_deparrture_time(2.32, 'e9', 'n4')

# Copy the hidden events with real values for testing. Deep copy creates new objects with their own references
events_H_actual = copy.deepcopy(events_H)

# TODO - Bass
# Init simulation
#S = Simulation()
runs = 10
#for i in range(runs):
    # Build sample d [departure_times]

    #[service_times, wait_times] = S.update_hidden_events(events_H)
    # Gibbs sampling from metrics
    # Use S.joint_density_log()
