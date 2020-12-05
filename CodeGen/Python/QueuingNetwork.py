from CodeGen.Python.networkStructureAttributesAndInstances import *
from CodeGen.Python.networkUtil import *
#from networkStructureAttributesAndInstances import *
#from networkUtil import *
import numpy as np
import random
from scipy.stats import expon

# Random path of a specific length
def random_path(length):
    paths = network_structure.graph.paths
    path_trim = [p for p in paths if len(p) == length]
    return random.choice(path_trim)

# Simulation of events in queue network
class Simulation:
    # Input:
    ## Events_O (array Events) - Observed events, with arrival time, departure time, and queue path
    ## Events_H (array Events) - Unobserved events, no infor
    ## Queue (array Queue) - Set of Queue objects
    def __init__(self, Events_O, Events_H, Queues):
        # Initial queue
        self.queue_init = Queue(0)
        # Add initial queue to every event
        self.Events_O = Events_O
        self.Events_H = Events_H
        self.Queues = Queues

        for e in Events_O:
            e.queues.insert(0, self.queue_init)
            first_arrival = e.arrival_times[0]
            e.departure_times.insert(0, first_arrival)
        self.update_hidden_events(self.Events_H)

    def queuing_sample(self):
        Events = merge_events(self.Events_O, self.Events_H)  # Ordered by first arrival time
        for e in self.Events_H:
            e.queues.insert(0, self.queue_init)
            first_arrival = e.arrival_times[0]
            e.departure_times.insert(0, first_arrival)
            # events_first_arrival.append((e.id, e.arrival_times[0])) # First arrival of each event
        # Get all departure times, in order
        self.departure_times = []
        for e in Events:
            self.departure_times = merge_id(self.departure_times, e.departure_times, e.id, e.queues)
        # Dictionaries
        self.dict_events = {}
        for e in Events:
            self.dict_events[e.id] = e
        self.dict_queue = {}
        for q in self.Queues:
            self.dict_queue[q.id] = q
        self.service_times = []
        self.wait_times = []
        self.execute()

    def update_hidden_events(self, Events_H):
        self.Events_H = Events_H
        self.queuing_sample()

    def execute(self):
        for dep_time in self.departure_times:
            e_id = dep_time[1]
            q_prev = dep_time[2]
            event = self.dict_events[e_id]
            q_next = event.move_queue()
            e_curr = event.current_queue
            queue_next = self.dict_queue[q_next]
            queue_next.arrival(e_id, dep_time[0], event.departure_times[e_curr])
            queue_prev = self.dict_queue[q_prev]
            (s,w,e) = queue_prev.service_next()
            self.service_times.append((s,e)) # (service_time, e)
            self.wait_times.append((w,e)) # (wait_times, e)
        return [self.service_times, self.wait_times]

    # Log of joint density for set of departures, queues, transitions, and service parameters
    # Input:
    ## events (N array) - array of event ids
    ## departures (N array) - array of departure times
    ## queues (N array) - array of queues per event
    ## Transitions (Q x Q matrix) - Transition probabilities between queues
    ## theta (Q array) - distribution parameters for each queue
    # Return: joint_density_log (float)
    def joint_density_log(self, events, departures, queues, Transitions, theta):
        joint_density_log_d_q = 0
        E = len(departures)
        if len(queues) != E:
            raise Exception("d and q must be equal sizes")
        event_queues = {}
        for i in range(E):
            transition = 1
            ev_id = events[i]
            ev_queue = queues[i]
            if ev_id in event_queues.keys():
                queues_pi = event_queues[ev_id]
                transition = Transitions[ev_queue, queues_pi]
                event_queues[ev_id] = ev_queue
            service_probability = expon.pdf(departures[i], scale=theta[ev_queue])
            joint_density_log_d_q += np.log(transition) + np.log(service_probability)
        return joint_density_log_d_q

class Event:
    # Inputs
    ## id (int) - name of Event object
    ## arrival_times (array(timestamp)) - arrival times for each task in Event object
    ## departure_times (array(timestamp)) - departure times for each task in Event object
    ## queues (array(queue_id)) - queue index for queue processing each task in Event object
    ## hidden (boolean) - if False, all data is flexible, if True, data is fixed
    def __init__(self, id, arrival_times, departure_times, queues, hidden=False):
        self.id = id
        self.arrival_times = arrival_times
        self.queues = queues
        self.departure_times = departure_times
        self.tasks = len(queues)
        if len(departure_times) != self.tasks:
            raise Exception('Number of departure times does not match number of queues in task')
        if len(arrival_times) != self.tasks:
            raise Exception('Number of departure times does not match number of queues in task')
        self.current_task = 0
        self.hidden = hidden

    # Input:
    ## departure_time (timestamp) - new departure time
    ## task_id (int) - ordered id of task in Event
    def update_departure_times(self, departure_time, task_id):
        if not self.hidden:
            raise Exception("Arrival and departure of observed variables are fixed.")
        self.departure_times[task_id] = departure_time

    # Given an ordered list of queues to visit, leave current queue and move to queue of next
    def move_queue(self):
        self.current_task += 1
        if self.current_task >= self.tasks:
            return []
        else:
            queue_id = self.queues[self.current_task]
            return queue_id # Return id of next queue

class Queue:
    def __init__(self, id, service_rate):
        self.id = id
        self.service_rate = service_rate
        self.queue_events = []
        self.queue_times_arrival = []
        self.queue_times_departures = []
        self.prev_dep = 0.0
        self.waiting = 0

    # Add an event to FIFO queue, end of line
    # Input:
    ## event_task_id (string) - id of event to add to queue
    ## arrival_time (timestamp) - arrival time of new task
    ## departure_time (timestamp) - departure time of new task
    def arrival(self, event_task_id, arrival_time, departure_time):
        self.queue_events.append(event_task_id)
        self.queue_times_arrival.append(arrival_time)
        self.queue_times_departures.append(departure_time)
        self.waiting += 1

    # Given arrival and departure time, calculate service and wait time of current event
    def service_next(self):
        event = self.queue_events.pop(0)
        arrival_time = self.queue_times_arrival.pop(0)
        departure_time = self.queue_times_departures.pop(0)
        self.waiting -= 1
        earliest_service = np.max([arrival_time, self.prev_dep])
        service_time = departure_time - earliest_service
        wait_time = departure_time - service_time - arrival_time
        self.prev_departure = departure_time
        return (service_time, wait_time, event)



    #
    # def service_next(self):
    #     event = self.queue_events.pop(0)
    #     time = self.queue_times.pop(0)
    #     self.waiting -= 1
    #     service_time = np.random.exponential(1./(self.service_rate))
    #     return time + service_time




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
        Event(id, arrival_event, departure_event, event_path, hidden=True)
    else:
        Event(id, arrival_event, departure_event, event_path)

# All events are initialized with temporary values. Run a full simulation forward to fill in the remaining arrival times
# TODO

# Copy the hidden events with real values for testing
events_H_actual = events_H








# TODO - Bass
# Init simulation
#S = Simulation()
runs = 10
for i in range(runs):
    # Build sample d [departure_times]
    # build new Events_H
    Events_H = [Event()] # TODO
    [service_times, wait_times] = S.update_hidden_events(Events_H)
    # Gibbs sampling from metrics
    # Use S.joint_density_log()
