from networkStructureAttributesAndInstances import *
from networkUtil import *
import numpy as np
import random
from scipy.stats import expon
np.random.seed(100)

# Random path of a specific length
def random_path(length):
    paths = network_structure.graph.paths
    path_trim = [p for p in paths if len(p) == length]
    return random.choice(path_trim)

def insert_event_trigger(event_triggers, arrival_trigger):
    # insert by timestamp
    insertion_point = len(event_triggers)
    for i in range(len(event_triggers) - 1, -1, -1):
        if arrival_trigger[0] < event_triggers[i][0]:  # Assume all timestamps are seconds
            insertion_point -= 1
        else:
            break
    return event_triggers[0:insertion_point] + [arrival_trigger] + event_triggers[insertion_point:]

# Simulation of events in queue network
class Simulation:
    # Input:
    ## Events_O (array Events) - Observed events, with arrival time, departure time, and queue path
    ## Events_H (array Events) - Unobserved events, no infor
    ## Queue (dict Queue) - Set of Queue objects
    ## assist_style (string) - defines how servers interact with events. In {'noAssist', 'assistComplete', 'assist_partial')
    def __init__(self, Events_O, Events_H, Queues, assist_style='noAssist', verbose=False):
        # Add initial queue to every event
        self.Events_O = Events_O
        self.Events_H = Events_H
        self.Queues = Queues
        self.verbose = verbose
        self.simulation_log = []
        self.assist_style = assist_style
        if assist_style not in ('noAssist', 'assistComplete', 'assist_partial'):
            raise Exception("Assist_style must be in {'noAssist', 'assistComplete', 'assist_partial')")
        # Initial queue
        self.init_q_id = 'init'
        queue_init = Queue(self.init_q_id, 0, 1)
        self.Queues[self.init_q_id] = queue_init

        all_events = self.Events_O + self.Events_H
        # Dictionaries
        self.dict_events = {}
        for e in all_events:
            self.dict_events[e.id] = e
        self.dict_queue = {}
        for q in self.Queues:
            #            self.dict_queue[q] = q
            self.dict_queue[q] = self.Queues[q]  # This line is redundant; used for now since Queue is passed as dict. May change to array

        for e in all_events:
            e.queues = [self.init_q_id] + e.queues
            first_arrival = e.arrival_times[0]
            e.arrival_times = np.insert(e.arrival_times, 0, 0)
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
            # first departure from init = first arrival to queue
            initial_departure_trigger = (e.departure_times[0], e.id, 'Departure', 'init')
            #e.current_task += 1
            # insert by timestamp
            self.event_triggers = insert_event_trigger(self.event_triggers, initial_departure_trigger)
            log = (0, e.departure_times[0], 0, e.departure_times[0], e.id, 0, {}, 1)
            self.Queues['init'].queue_log.append(log)

        # Iterate through arrival times. At each time, simulate the new state
        t = 0
        while t < len(self.event_triggers):
            trigger = self.event_triggers[t]
            if self.verbose:
                print(trigger)
            self.simulation_log.append(str(trigger))
            trigger_time = trigger[0]
            event_id = trigger[1]
            trigger_type = trigger[2]
            event = self.dict_events[event_id]
            task = event.current_task

            queue_id = event.queues[task]
            queue = self.dict_queue[queue_id]
            if 'Arrival' in trigger_type:
                #queue_service_rate = queue.service_rate
                # TODO
                #if self.assist_style == 'noAssist':
                    #service_time = expon.rvs(scale=1/queue_service_rate)
                    #service_ready = queue.arrival(event_id, trigger_time) #, service_time=service_time)
                #elif self.assist_style == 'assistComplete':
                    # How many events are there currently on the queue?

                    #k =  np.floor(len(queue.sub_servers)/(total_events_in_queue + 1))
                    #service_time = expon.rvs(scale=1 / (queue_service_rate*k))
                service_ready = queue.arrival(event_id, trigger_time)#, service_time=service_time)
                #else:
                #    service_ready = False
                sim_trigger = 'Event {} arrived at queue {}'.format(event_id, queue_id)
                if self.verbose:
                    print(sim_trigger)
                self.simulation_log.append(sim_trigger)
                if service_ready:
                    self.service_queue(trigger_time, queue, t)

                    sim_trigger = 'Servicing event {} at queue: {}'.format(event_id, queue_id)
                    if self.verbose:
                        print(sim_trigger)
                    self.simulation_log.append(sim_trigger)

            elif 'Departure' in trigger_type:
                queue.complete_service(event_id)

                sim_trigger = 'Event {} complete at queue {}'.format(event_id, queue_id)
                if self.verbose:
                    print(sim_trigger)
                self.simulation_log.append(sim_trigger)

                # New queue for current event
                new_queue_id = event.move_queue()
                if new_queue_id: # event completed
                    # add trigger for current event, new queue
                    arrival_trigger = (trigger_time, event_id, 'Arrival', new_queue_id)
                    self.event_triggers = insert_event_trigger(self.event_triggers, arrival_trigger)

                # New event for current queue
                self.service_queue(trigger_time, queue, t)
            t += 1
                #new_queue = self.dict_queue[new_queue_id]
                #queue_service = queue.service_rate
                #service_time = expon.rvs(scale=1 / queue_service)
                #service_ready = new_queue.arrival(event_id, trigger_time, service_time=service_time)

                # if service_ready:
                #     self.service_queue(trigger_time, new_queue, t)


    def get_queue(self, queue_id):
        return self.Queues(queue_id)

    def service_queue(self, trigger_time, queue, t):
        [_, _, _, d, e, _, _, _] = queue.service_metrics(trigger_time, self.assist_style)
        if e is None:
            return
        queue_state = [server.servicing for server in queue.sub_servers]
        queue.all_servers_occupied = all(queue_state)
        event = self.dict_events[e]
        task = event.current_task
        event.departure_times[task] = d
        new_trigger = (d, e, 'Departure', queue.id)
        nt = t
        for et in range(t, len(self.event_triggers)):
            et_time = self.event_triggers[et][0]
            if et_time < d:
                nt += 1
            else:
                break
        self.event_triggers = self.event_triggers[0:nt] + [new_trigger] + self.event_triggers[nt:]

    def queuing_sample(self):
        pass
        # Events = merge_events(self.Events_O, self.Events_H)  # Ordered by first arrival time
        # for e in self.Events_H:
        #     e.queues.insert(0, self.queue_init)
        #     first_arrival = e.arrival_times[0]
        #     e.departure_times = np.insert(e.departure_times, 0, first_arrival)
        #     # events_first_arrival.append((e.id, e.arrival_times[0])) # First arrival of each event
        # # Get all departure times, in order
        # self.departure_times = []
        # for e in Events:
        #     self.departure_times = merge_id(self.departure_times, e.departure_times, e.id, e.queues)
        # self.service_times = []
        # self.wait_times = []
        # self.execute()

    def update_hidden_events(self, Events_H):
        self.Events_H = Events_H
        self.queuing_sample()

    # def execute(self):
    #     for dep_time in self.departure_times:
    #         e_id = dep_time[1]
    #         q_prev = dep_time[2]
    #         event = self.dict_events[e_id]
    #         q_next = event.move_queue()
    #         e_curr = event.current_task
    #         queue_next = self.dict_queue[q_next]
    #         queue_next.arrival(e_id, dep_time[0], event.departure_times[e_curr])
    #         queue_prev = self.dict_queue[q_prev]
    #         (s,w,e) = queue_prev.service_metrics()
    #         self.service_times.append((s,e)) # (service_time, e)
    #         self.wait_times.append((w,e)) # (wait_times, e)
    #     return [self.service_times, self.wait_times]

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
    def __init__(self, id, arrival_times, departure_times, queues, assisted=1, hidden=False):
        self.id = id
        self.arrival_times = arrival_times
        self.queues = queues
        self.departure_times = departure_times
        self.tasks = len(queues) # Number of tasks
        self.assisted = assisted
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
        if self.current_task > self.tasks:
            return ''
        else:
            queue_id = self.queues[self.current_task]
            return queue_id # Return id of next queue

class SubQueue:
    # Input
    ## sub_id (int) 1...K
    ## service_rate (float) - Exponential parameter of service
    def __init__(self, sub_id, service_rate):
        self.id = sub_id
        self.service_rate = service_rate
        self.servicing = None


class Queue:
    # K (int) - Number of servers
    # service_loss (array size K) - loss for k server collaboration
    def __init__(self, id, service_rate, K, service_loss):
        self.id = id
        self.service_rate = service_rate
        self.queue_events = []
        self.queue_times_arrival = []
        self.queue_times_departures = []
        self.queue_times_service = []
        self.prev_dep = 0.0
        self.waiting = 0
        self.all_servers_occupied = False
        self.queue_log = []
        self.sub_servers = []
        self.K = K
        if len(service_loss) != K:
            raise Exception('Service loss needs to be of size K')
        for k in range(K):
            if service_loss[k] > service_rate*(k+1):
                raise Exception('Service loss from k servers cannot be greater than service rate by k servers')
        self.service_loss = service_loss
        for k in range(K):
            self.sub_servers.append(SubQueue(k, self.service_rate))

    # Add an event to FIFO queue, end of line
    # Input:
    ## event_task_id (string) - id of event to add to queue
    ## arrival_time (timestamp) - arrival time of new task
    ## departure_time (timestamp) - departure time of new task
    # return bool - service_next
    def arrival(self, event_task_id, arrival_time, departure_time=-1, service_time=-1):
        self.queue_events.append(event_task_id)
        self.queue_times_arrival.append(arrival_time)
        # if departure_time >= 0:
        #     self.queue_times_departures.append(departure_time)
        # # todo Move this?
        # if service_time >= 0:
        #     self.queue_times_service.append(service_time)
        self.waiting += 1
        service_ready = False
        queue_state = [server.servicing for server in self.sub_servers]
        self.all_servers_occupied = all(queue_state)
        if not self.all_servers_occupied:
            service_ready = True
        return service_ready

    def complete_service(self, event_id):
        for k in range(self.K):
            if self.sub_servers[k].servicing == event_id:
                self.sub_servers[k].servicing = None
                break
        queue_state = [server.servicing for server in self.sub_servers]
        self.all_servers_occupied = all(queue_state)
        return

    # Given arrival and departure time, calculate service and wait time of current event
    def service_metrics(self, event_time, assist_style):
        if len(self.queue_events) < 1:
            return [None]*8
        event = self.queue_events.pop(0)
        arrival_time = self.queue_times_arrival.pop(0)
        service_time = 0
        wait_time = 0
        departure_time = 0
        sub_id = 0
        for k in range(self.K):
            if not self.sub_servers[k].servicing:
                self.sub_servers[k].servicing = event
                sub_id = k
                break
        #self.servicing = event
        # This is never called
        # if len(self.queue_times_departures) > 0:
        #     departure_time = self.queue_times_departures.pop(0)
        #     earliest_service = np.max([arrival_time, self.prev_dep])
        #     service_time = departure_time - earliest_service
        #     wait_time = departure_time - service_time - arrival_time
        #     self.prev_departure = departure_time
        # if len(self.queue_times_service) > 0:
        total_events_in_queue = sum(server.servicing is not None for server in self.sub_servers)
        if assist_style == 'assistComplete':
            k_servers = np.floor(len(self.sub_servers) / (total_events_in_queue))
        else:
            k_servers = 1
        service_loss_k = self.service_loss[k_servers]
        service_time = expon.rvs(scale=1 / (self.service_rate*k_servers - service_loss_k))
        #service_time =     #self.queue_times_service.pop(0)
        wait_time = event_time - arrival_time
        departure_time = event_time + service_time
        self.waiting -= 1
        # self.servicing = event
        servicing_state = {}
        for sq in self.sub_servers:
            servicing_state[sq.id] = sq.servicing
        log = (arrival_time, service_time, wait_time, departure_time, event, sub_id, servicing_state, k_servers)
        self.queue_log.append(log)
        return log
