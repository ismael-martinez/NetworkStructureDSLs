from CodeGen.Python.networkStructureAttributesAndInstances import *
from CodeGen.Python.networkUtil import *
from networkStructureAttributesAndInstances import *
from networkUtil import *
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
    ## Queue (dict Queue) - Set of Queue objects
    def __init__(self, Events_O, Events_H, Queues):
        # Add initial queue to every event
        self.Events_O = Events_O
        self.Events_H = Events_H
        self.Queues = Queues
        # Initial queue
        self.init_q_id = 'init'
        queue_init = Queue(self.init_q_id, 1)
        self.Queues[self.init_q_id] = queue_init

        all_events = self.Events_O + self.Events_H
        for e in all_events:
            e.queues.insert(0, self.init_q_id)
            first_arrival = e.arrival_times[0]
            e.departure_times = np.insert(e.departure_times, 0, first_arrival)
        self.event_triggers = []
        self.execute_initial()
        #self.update_hidden_events(self.Events_H)

    # The initial simulation of events, based on arrival times and service rates.
    # This initializes all departure times
    def execute_initial(self):
        # event_triggers = [(timestamp, event_id, type)]
        ## type in [('Arrival', 'Departure']
        all_Events = self.Events_O + self.Events_H
        # Insert all initial departure times (arrival into the system)
        for e in all_Events:
            # first arrival
            arrival_trigger = (e.departure_times[0], e.id, 'Arrival')
            # insert by timestamp
            insertion_point = len(self.event_triggers)
            for i in range(len(self.event_triggers)-1, -1, -1):
                if arrival_trigger[0] <= self.event_triggers[i][0]: # Assume all timestamps are seconds
                    insertion_point -= 1
                else:
                    break
            self.event_triggers = self.event_triggers[0:insertion_point] + [arrival_trigger] + self.event_triggers[insertion_point:]

        # Iterate through arrival times. At each time, simulate the new state
        #for e in self.event_triggers:



    def queuing_sample(self):
        Events = merge_events(self.Events_O, self.Events_H)  # Ordered by first arrival time
        for e in self.Events_H:
            e.queues.insert(0, self.queue_init)
            first_arrival = e.arrival_times[0]
            e.departure_times = np.insert(e.departure_times, 0, first_arrival)
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
#            self.dict_queue[q] = q
            self.dict_queue[q] = self.Queues[q] # This line is redundant; used for now since Queue is passed as dict. May change to array
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
            e_curr = event.current_task
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
        self.tasks = len(queues) # Number of tasks
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
