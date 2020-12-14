#from CodeGen.Python.networkStructureAttributesAndInstances import *
#from CodeGen.Python.networkUtil import *
from networkStructureAttributesAndInstances import *
from networkUtil import *
#from CodeGen.Python.Simulation import *
from Simulation import *
import numpy as np
import random
import copy

DECIMALS = 7

class QueueNetwork:
    def __init__(self, queue_log_dict, K):
        self.K = K
        self.log = queue_log_dict
        # Trim arrival, wait, service, and destination to 7 decimals
        for q in self.log:
            for i in range(len(self.log[q])):
                q_times = [round(self.log[q][i][t], DECIMALS) for t in range(4)]
                q_log = q_times + list(self.log[q][i][4:])
                self.log[q][i] = tuple(q_log)

    # For an event in a queue, return all required information.
    # Input
    ## event_id (string), id of Event
    ## queue_id (string), id of Queue
    # Return info dictionary()
    def event_log_dict(self, event_id, queue_id):
        old_log = self.log[queue_id]
        log_id = 0

        # Find index of log_entry
        while log_id < len(self.log[queue_id]):
            log_entry = self.log[queue_id][log_id]
            if log_entry[4] == event_id:
                break
            log_id += 1
        if log_id >= len(self.log[queue_id]):
            print('Event not found in queue {}'.format(queue_id))
            return
        event_log = self.log[queue_id][log_id]
        event_log_dict = {}
        event_log_dict['arrival_time'] = event_log[0]
        event_log_dict['service_time'] = event_log[1]
        event_log_dict['wait_time'] = event_log[2]
        event_log_dict['departure_time'] = event_log[3]
        event_log_dict['earliest_service_time'] = event_log[0] + event_log[2]
        return event_log_dict


    def update_departure_time(self, new_departure, event_id, queue_id):
        old_log = self.log[queue_id]
        log_id = 0
        departure_times_subserver = {}

        # Find index of log_entry
        while log_id < len(self.log[queue_id]):
            log_entry = self.log[queue_id][log_id]
            departure_times_subserver[log_entry[4]] = log_entry[3]  # event_id : departure_time
            if log_entry[4] == event_id:
                break
            log_id += 1
        if log_id >= len(self.log[queue_id]):
            print('Event not found in queue {}'.format(queue_id))
            return

        log_tuple = self.log[queue_id][log_id]
        servicing_state = log_tuple[6] # Dict representing which subqueues are servicing which events
        # Chech new departure is valid
        if new_departure < log_tuple[0] + log_tuple[2]:
            raise Exception('Departure time is invalid.')

        # Create new log_entry with new departure
        self.log[queue_id][log_id] = (
        log_tuple[0], log_tuple[1], log_tuple[2], new_departure, log_tuple[4], log_tuple[5], servicing_state)
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
        for i in range(log_id + 1, len(old_log)):
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

            waiting_time = round(earliest_service_time - arrival_time, DECIMALS)
            service_time = round(departure_time - arrival_time - waiting_time, DECIMALS)
            servicing_state_new = {}
            servicing_state_new[subserver] = event_id
            for s in servicing_state:
                if s == subserver:
                    continue
                event_id_old = servicing_state[s]
                if event_id_old and departure_times_subserver[event_id_old] > arrival_time:
                    servicing_state_new[s] = event_id_old
                else:
                    servicing_state_new[s] = None

            new_log = (
            arrival_time, service_time, waiting_time, departure_time, event_id, subserver, servicing_state_new)
            print(new_log)
            print(old_log[i])
            compare = [new_log[t] == old_log[i][t] for t in range(len(new_log))]

            # Compare new_log with old_log
            if all(compare):
                print('Stable')
                self.log[queue_id] = old_log
                return
            else:
                old_log[i] = new_log
                # Reconstruct relevant info from newest log
                log_tuple = new_log
                servicing_state = log_tuple[6]
                self.log[queue_id][log_id] = (
                    log_tuple[0], log_tuple[1], log_tuple[2], new_departure, log_tuple[4], log_tuple[5],
                    servicing_state)
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

    def update_arrival_time(self, new_arrival, event_id, queue_id):
        old_log = self.log[queue_id]
        # Proper insert point
        entry_point = 0
        for entry in range(len(old_log)):
            if new_arrival < old_log[entry][0]:
                break
            else:
                entry_point += 1

        while entry_point < len(old_log):

            # Delete old log
            delete_point = 0
            for entry in range(len(old_log)):
                if old_log[entry][4] == event_id:
                    break
                else:
                    delete_point += 1
            if delete_point >= len(old_log):
                print('Event not found in queue {}'.format(queue_id))
                return
            delete_log = old_log[delete_point]
            old_departure_time = old_log[delete_point][3]
            old_log = old_log[0:delete_point] + old_log[delete_point+1:] # Remove old log entry

            servicing_state = {}
            departure_servicing = {}
            for k in range(self.K):
                servicing_state[k] = None
            if entry_point > 0:
                servicing_state = old_log[entry_point - 1][6]
            for log in old_log[0:entry_point]:
                ev_id = log[4]
                if log[3] < new_arrival:
                    for k in range(self.K):
                        if servicing_state[k] == ev_id:
                            servicing_state[k] = None
                else:
                    for k in range(self.K):
                        if servicing_state[k] == ev_id:
                            departure_servicing[k] = log[3]
            next_deps = [departure_servicing[k] for k in range(self.K)]
            argmin_d = 0
            if all(next_deps):
                earliest_service = next_deps[0]
                argmin_d = 0
                for d in range(len(next_deps)):
                    if earliest_service > next_deps[d]:
                        earliest_service = next_deps[d]
                        argmin_d = d
            else:
                earliest_service = new_arrival
                for k in range(self.K):
                    if not servicing_state[k]:
                        argmin_d = k
                        break
            servicing_state[argmin_d] = event_id
            waiting_time = round(earliest_service - new_arrival, DECIMALS)
            service_time = round(old_departure_time - earliest_service, DECIMALS)
            new_log = (new_arrival, service_time, waiting_time, old_departure_time, event_id, argmin_d, servicing_state)
            old_log = old_log[0:entry_point] + [new_log] + old_log[entry_point:]

            print(new_log)
            print(delete_log)
            compare = [new_log[t] == delete_log[t] for t in range(len(new_log))]

            # Compare new_log with old_log
            if all(compare):
                print('Stable')
                self.log[queue_id] = old_log
                return

            entry_point += 1
            if entry_point < len(old_log):
                event_id = old_log[entry_point][4]
                new_arrival = old_log[entry_point][0]
        self.log[queue_id] = old_log






events = 500
p = 0.4
random.seed(events)
ns = network_structure.graph.nodes.get_nodes()
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
S = Simulation(events_O, events_H, queues, 'assistComplete')
# for e in S.event_triggers:
#     print(e[0])
print('\nDeparture times')
for e in S.Events_O:
    print(e.id)
    print(e.departure_times)

queue_log = {}
for q in S.Queues:
    print('Queue {}'.format(q))
    print('Arrival, Service, Wait, Departure, ')
    queue = queues[q]
    queue_log[q] = queue.queue_log[0:-1]
    for l in queue.queue_log: # [arrival, service, wait, departure
        print(l)
    print('\n')

queue_network = QueueNetwork(queue_log, K)
#queue_network.update_departure_time(2.00, 'e10', 'n1')
#queue_network.event_log_dict('e10', 'n1')

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

# M - Step
for q in S.Queues:
    if q == 'init':
        continue
    print('Queue {}'.format(q))
    queue = queues[q]

    sum_service_times = 0
    sum_servicers = 0
    for log in queue.queue_log: # [arrival, service, wait, departure
        k_servers = log[7]
        service_time = log[1]
        sum_service_times += service_time*k_servers
        sum_servicers += 1./k_servers
    N = len(queue.queue_log)
    print(sum_servicers / sum_service_times)
    print(N / sum_service_times)
    print(queue.service_rate)
    print('\n')