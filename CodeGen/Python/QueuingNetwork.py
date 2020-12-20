#from CodeGen.Python.networkStructureAttributesAndInstances import *
#from CodeGen.Python.networkUtil import *
from networkStructureAttributesAndInstances import *
from networkUtil import *
#from CodeGen.Python.Simulation import *
from Simulation import *
import numpy as np
import random
import copy
import matplotlib.pyplot as plt

DECIMALS = 7

class QueueNetwork:
    def __init__(self, queue_log_dict, hidden_ids, event_triggers, K):
        self.K = K
        self.log = queue_log_dict
        self.hidden_ids = hidden_ids
        self.queue_ids = []
        self.service_rates = {}
        self.service_loss = {}
        # Construct event tuples from event trigger list:
        self.event_transition = {}
        for i in range(len(event_triggers)):
            e = event_triggers[i]
            if 'Arrival' in e[2]:
                continue
            if 'Departure' in e[2]:
                curr_queue = e[3]
                event_id = e[1]
                if i+1 < len(event_triggers) and 'Arrival' in event_triggers[i+1][2] and event_id == event_triggers[i+1][1]:
                    next_queue = event_triggers[i+1][3]
                else:
                    next_queue = None

                self.event_transition[(event_id, curr_queue)] = next_queue
        # Trim arrival, wait, service, and destination to 7 decimals
        for q in self.log:
            self.queue_ids.append(q)
            self.service_rates[q] = 1
            self.service_loss[q] = [0]*self.K
            for k in range(self.K):
                self.service_loss[q][k] = 0.5
            if q == 'init':
                self.service_loss[q] = [0]*self.K
                self.service_rates[q] = 0
            for i in range(len(self.log[q])):
                q_times = [round(self.log[q][i][t], DECIMALS) for t in range(4)]
                q_log = q_times + list(self.log[q][i][4:])
                self.log[q][i] = tuple(q_log)
        #self.update_arrival_time('')
        self.gibbs_sampling_update(initial=True)
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
        print(event_id)
        print(queue_id)
        print(new_departure)
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
        if queue_id == 'init':
            new_log = self.log[queue_id][log_id][0:3] + (new_departure,) + self.log[queue_id][log_id][4:]
            self.log[queue_id][log_id] = new_log
            return

        servicing_state = log_tuple[6] # Dict representing which subqueues are servicing which events
        # Chech new departure is valid
        if new_departure < log_tuple[0] + log_tuple[2]:
            raise Exception('Departure time is invalid.')

        # Create new log_entry with new departure

        earliest_service = log_tuple[0] + log_tuple[2]
        self.log[queue_id][log_id] = (
        log_tuple[0], new_departure - earliest_service , log_tuple[2], new_departure, log_tuple[4], log_tuple[5], servicing_state, log_tuple[7])
        departure_times_subserver[log_tuple[4]] = new_departure
        print(self.log[queue_id][log_id])
        print('Dep ' + str(departure_times_subserver))
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
            arrival_time, service_time, waiting_time, departure_time, event_id, subserver, servicing_state_new, log_tuple[7])
            print('Old ' + str(old_log[i]))
            print('New ' + str(new_log))

            compare = [new_log[t] == old_log[i][t] for t in range(len(new_log))]

            # Compare new_log with old_log
            if all(compare) and i > self.K:
                print('Stable')
                self.log[queue_id] = old_log
                return
            else:
                old_log[i] = new_log
                # Reconstruct relevant info from newest log
                log_tuple = old_log[i] #new_log
                new_departure = log_tuple[3]
                servicing_state = log_tuple[6]
                self.log[queue_id] = old_log
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
        old_log = list(self.log[queue_id])
        # Proper insert point
        entry_point = 0


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

            entry_point = 0
            for entry in range(len(old_log)):
                if new_arrival < old_log[entry][0]:
                    break
                else:
                    entry_point += 1

            servicing_state = {}
            departure_servicing = {}
            for k in range(self.K):
                servicing_state[k] = None
                departure_servicing[k] = None
            if entry_point > 0:
                servicing_state = dict(old_log[entry_point - 1][6])
            for log in old_log[0:entry_point]:
                # If previous event has already departed, remove from state
                ev_id = log[4]
                if log[3] < new_arrival:
                    for k in range(self.K):
                        if servicing_state[k] == ev_id:
                            servicing_state[k] = None
                else:
                    for k in range(self.K):
                        if servicing_state[k] == ev_id:
                            departure_servicing[k] = log[3] # state departure after new arrival
            next_deps = [departure_servicing[k] for k in range(self.K)]
            argmin_d = 0 # Earliest server available
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
            if service_time < 0:
                raise Exception('Service time must be non-negative')
            k_servers = delete_log[7]
            new_log = (new_arrival, service_time, waiting_time, old_departure_time, event_id, argmin_d, servicing_state, k_servers)
            old_log = old_log[0:entry_point] + [new_log] + old_log[entry_point:]

            print('Old ' + str(delete_log))
            print('New ' + str(new_log))
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


    # From a given log, search either forwards and backwards from a log point, and find one log per subqueue
    def surrounding_log_events(self, log_id, queue_id, forwards = True):
        queue_log = self.log[queue_id]
        log_entry_arrival = {}
        log_entry_departure = {}
        for k in range(self.K):
            log_entry_arrival[k] = None
            log_entry_departure[k] = None
        if log_id: # not none
            if forwards:
                log_id_next = log_id + 1
                while log_id_next < len(log):
                    server_k = queue_log[log_id_next][5]
                    if log_entry_arrival[server_k] is None:
                        log_entry_arrival[server_k] = queue_log[log_id_next][0]
                        log_entry_departure[server_k] = queue_log[log_id_next][3]
                    if any([log_entry_arrival[server_k] is None for k in
                            log_entry_arrival]):
                        log_id_next += 1
                    else:
                        return [log_entry_arrival, log_entry_departure]
                return [log_entry_arrival, log_entry_departure]
            else:
                log_id_prev = log_id - 1
                while log_id_prev > 0:
                    server_k = queue_log[log_id_prev][5]
                    if log_entry_arrival[server_k] is None:
                        log_entry_arrival[server_k] = queue_log[log_id_prev][0]
                        log_entry_departure[server_k] = queue_log[log_id_prev][3]
                    if any([log_entry_arrival[server_k] is None for k in
                            log_entry_arrival]):
                        log_id_prev -= 1
                    else:
                        return [log_entry_arrival, log_entry_departure]
            return [log_entry_arrival, log_entry_departure]

    def gibbs_sampling_update(self, initial=False):
        uniq_id_column = 9
        queue_column = 8
        event_column = 4
        # order all event arrival time
        arrival_times = []
        events_ordered_departure = []
        uniq_id = 0

        # Create list ordered by departure times
        for queue_id, queue_events in self.log.items():
            for event_log in queue_events:
                event_log_and_queue = [l for l in event_log]
                # event_log_and_queue = event_log
                event_log_and_queue.append(queue_id)
                events_ordered_departure.append(event_log_and_queue)

        # Order events by Departure time
        events_ordered_departure = sorted(events_ordered_departure, key=lambda x: x[3], reverse=False)
        for dep_event in events_ordered_departure:
            current_queue_id = dep_event[8]
            event_id = dep_event[4]
            if event_id not in self.hidden_ids:
                continue
            next_queue_id = self.event_transition[(event_id, current_queue_id)]

            # Index in current queue log

            log_id_cq = None
            log_id_nq = None
            #if current_queue_id != 'init':

            for idx, log in enumerate(self.log[current_queue_id]):
                if log[4] == event_id:
                    log_id_cq = idx
                    break
            if next_queue_id:
                for idx, log in enumerate(self.log[next_queue_id]):
                    if log[4] == event_id:
                        log_id_nq = idx
                        break
            ## Current queue q_pi(e)
            try:
                # Current event arrival, a_pi(e)
                current_event_current_queue_arrival = self.log[current_queue_id][log_id_cq][0] + self.log[current_queue_id][log_id_cq][2] # Earliest service time
                current_event_current_queue_departure =  self.log[current_queue_id][log_id_cq][3]  # Departure
                # Previous event departure, d_rho(pi(e))
                [previous_event_current_queue_arrival_dict, previous_event_current_queue_departure_dict] = self.surrounding_log_events(log_id_cq, current_queue_id, forwards=False)
                previous_event_current_queue_departure = None
                previous_event_current_queue_departure_nonempty = [previous_event_current_queue_departure_dict[k] for k in
                 previous_event_current_queue_departure_dict if
                 previous_event_current_queue_departure_dict[
                     k] is not None]
                if len(previous_event_current_queue_departure_nonempty) > 0:
                    previous_event_current_queue_departure = max(previous_event_current_queue_departure_nonempty)

                # Next event departure, d_rho^{-1}(pi(e))
                [next_event_current_queue_arrival_dict,
                 next_event_current_queue_departure_dict] = self.surrounding_log_events(log_id_cq, current_queue_id,
                                                                                            forwards=True)
                next_event_current_queue_departure = None
                next_event_current_queue_departure_nonempty = [next_event_current_queue_departure_dict[k] for k
                                                                   in
                                                               next_event_current_queue_departure_dict if
                                                               next_event_current_queue_departure_dict[
                                                                       k] is not None]
                if len(next_event_current_queue_departure_nonempty) > 0:
                    next_event_current_queue_departure = min(next_event_current_queue_departure_nonempty)

                # Next event arrival, a_rho^{-1}(pi(e))
                next_event_current_queue_arrival = None
                next_event_current_queue_arrival_nonempty = [next_event_current_queue_arrival_dict[k] for k
                                                               in
                                                             next_event_current_queue_arrival_dict if
                                                             next_event_current_queue_arrival_dict[
                                                                   k] is not None]
                if len(next_event_current_queue_arrival_dict) > 0:
                    next_event_current_queue_arrival = max(next_event_current_queue_arrival_nonempty)

            except:
                current_event_current_queue_arrival = 0
                previous_event_current_queue_departure = None
                next_event_current_queue_departure = None
                next_event_current_queue_arrival = None
                current_event_current_queue_departure = 0

            ## Next queue q_e

            next_event_next_queue_arrival = None
            previous_event_next_queue_arrival = None
            current_event_next_queue_departure = None
            current_event_next_queue_arrival = 0
            previous_event_next_queue_departure = None
            if log_id_nq is not None:
                # Previous event arrival, a_rho(e)
                if log_id_nq:
                    log_id_nq_prev = log_id_nq - 1
                    previous_event_next_queue_arrival_dict = {}
                    for k in range(self.K):
                        previous_event_next_queue_arrival_dict[k] = None
                    while log_id_nq_prev > 0:
                        k = self.log[current_queue_id][log_id_nq_prev][5]
                        if previous_event_next_queue_arrival_dict[k] is None:
                            previous_event_next_queue_arrival_dict[k] = self.log[current_queue_id][log_id_nq_prev][
                                3]
                        if any([previous_event_next_queue_arrival_dict[k] is None for k in
                                previous_event_next_queue_arrival_dict]):
                            log_id_nq_prev -= 1
                        else:
                            previous_event_next_queue_arrival = max(
                                [previous_event_next_queue_arrival_dict[k] for k in
                                 previous_event_next_queue_arrival_dict])
                            break
                    if all([previous_event_next_queue_arrival_dict[k] is None for k in
                            previous_event_next_queue_arrival_dict]):
                        previous_event_next_queue_arrival = None
                    elif any([previous_event_next_queue_arrival_dict[k] is None for k in
                              previous_event_next_queue_arrival_dict]):
                        previous_event_next_queue_arrival = max(
                            [previous_event_next_queue_arrival_dict[k] for k in
                             previous_event_next_queue_arrival_dict if
                             previous_event_next_queue_arrival_dict[k] is not None])



                # Next event arrival, a_rho^{-1}(e)
                log_id_nq_next = log_id_nq + 1
                while log_id_nq_next < len(self.log[next_queue_id]):
                    next_event_k = self.log[next_queue_id][log_id_nq_next][6][next_queue_server_k]
                    if next_event_k is None:
                        log_id_nq_next += 1
                    else:
                        next_event_next_queue_arrival = self.log[next_queue_id][log_id_nq_next][0]
                        break
                # Current event arrival, d_e
                current_event_next_queue_departure = self.log[next_queue_id][log_id_nq][3]
                current_event_next_queue_arrival = self.log[next_queue_id][log_id_nq][0]
                # Previous event departure, d_rho(e)
                log_id_nq_prev = log_id_nq - 1
                while log_id_nq_prev > 0:
                    next_event_k = self.log[next_queue_id][log_id_nq_prev][6][next_queue_server_k]
                    if next_event_k is None:
                        log_id_nq_prev-= 1
                    else:
                        previous_event_next_queue_departure = self.log[next_queue_id][log_id_nq_prev][0]
                        break


            # Lower bound
            lower_bound_choices = [0] + [x for x in [current_event_current_queue_arrival, previous_event_next_queue_arrival, previous_event_current_queue_departure] if x]
            upper_bound_choices = [np.infty] + [x for x in [next_event_next_queue_arrival, next_event_current_queue_departure, current_event_next_queue_departure] if x]
            lower_bound_gibbs = max(lower_bound_choices)
            upper_bound_gibbs = min(upper_bound_choices)
            print('Sample in d in [{}, {}]'.format(lower_bound_gibbs, upper_bound_gibbs))


            #partition_choices = [x for x in [next_event_current_queue_arrival, previous_event_next_queue_departure] if x]
            partition_points = []
            # Next K arrivals in current queue
            if current_queue_id != 'init':
                cg_next_log = 0
                K = len(self.log[current_queue_id][log_id_cq][6])
                while cg_next_log < K:
                    if log_id_cq + 1 + cg_next_log < len(self.log[current_queue_id]):
                        cg_log_arrival = self.log[current_queue_id][log_id_cq+1+cg_next_log][0]
                        if cg_log_arrival < upper_bound_gibbs:
                            partition_points.append(cg_log_arrival)
                            cg_next_log += 1
                        else:
                            break
                    else:
                        break
        # Previous K departures in next queue
            if next_queue_id is not None and log_id_nq is not None:
                K = len(self.log[next_queue_id][log_id_nq][6])
                nq_prev_log = 0
                while nq_prev_log < K:
                    if log_id_nq - 1 - nq_prev_log >= 0:
                        nq_log_departure = self.log[next_queue_id][log_id_nq-1-nq_prev_log][3]
                        if nq_log_departure >= upper_bound_gibbs:
                            break
                        else:
                            if nq_log_departure > lower_bound_gibbs:
                                partition_points.append(nq_log_departure)
                                nq_prev_log -=1
                            else:
                                break
                    else:
                        break
            partition_points.sort()
            print('Partition points: {}'.format(partition_points))

            # Sample from region
            # Todo with probability, region Z
            # Sample
            if initial:
                # Sample from uniform across [L, U]
                if upper_bound_gibbs == np.infty:
                    continue
                d = lower_bound_gibbs + np.random.random() * (upper_bound_gibbs-lower_bound_gibbs)
            else:
                #### Gibbs sampling
                ## Choose an interval
                cq_service_rate = self.service_rates[current_queue_id]
                if next_queue_id is not None:
                    nq_service_rate = self.service_rates[next_queue_id]
                else:
                    nq_service_rate = 0

                current_queue_current_event = [current_event_current_queue_arrival, current_event_current_queue_departure]
                next_queue_current_event = [current_event_next_queue_arrival, current_event_next_queue_departure]
                next_queue_previous_event = [previous_event_next_queue_arrival, previous_event_next_queue_departure]
                current_queue_next_event = [next_event_current_queue_arrival, next_event_current_queue_departure]

                Z = partition_probabilities(lower_bound_gibbs, upper_bound_gibbs, cq_service_rate,
                                            nq_service_rate, current_queue_current_event,
                                            next_queue_current_event, next_queue_previous_event,
                                            current_queue_next_event)
                z = 0
                u = np.random.random()
                if u < Z[0]:
                    z = 0
                elif u < Z[0] + Z[1]:
                    z = 1
                else:
                    z = 2
                d = sample_truncated_exponential_two_queues_open(z, lower_bound_gibbs, upper_bound_gibbs, cq_service_rate,
                                            nq_service_rate, current_queue_current_event,
                                            next_queue_current_event, next_queue_previous_event,
                                            current_queue_next_event)
                # self.event_transition[(event_id, queue_id)] this function gives the next queue for an event
                print('Sampling from CQ {} *[ x - {}] , NQ {} * [{} - x] from x in [{}, {}]'.format(cq_service_rate,
                                                                                                    current_event_current_queue_arrival,
                                                                                                    nq_service_rate,
                                                                                                    current_event_next_queue_departure,
                                                                                                    lower_bound_gibbs,
                                                                                                    upper_bound_gibbs))
                print('Sample d = {}'.format(d))
            self.update_departure_time(d, event_id, current_queue_id)
            if next_queue_id is not None:
                self.update_arrival_time(d, event_id, next_queue_id)




        # for queue_id, queue_events in self.log.items():
        #     for event_log in queue_events:
        #         event_log_and_queue = [l for l in event_log]
        #         event_log_and_queue.append(queue_id)
        #         event_log_and_queue.append(uniq_id)
        #         events_ordered_departure.append(event_log_and_queue)
        #         uniq_id += 1
        #         # print(event_log_and_queue)
        #
        # # find next queue for each events : sorted by event_id and by reverse arrival time to retreive next queue
        # event_list_ordered_by_event_id = sorted(events_ordered_departure, key=lambda x: (x[event_column], -x[0]), reverse=False)
        # none_list = [None] * 10
        # next_event_log = none_list
        # next_event_dict = {}
        # for event_log in event_list_ordered_by_event_id:
        #     uniq_id = event_log[uniq_id_column]
        #     if next_event_log[event_column] == event_log[event_column]:
        #         next_event_dict[uniq_id] = next_event_log
        #     else:
        #         next_event_dict[uniq_id] = none_list
        #     next_event_log = event_log
        #     # print(next_event_dict[uniq_id])
        #
        # # find within queue next events : sorted by queue_id and by reverse arrival time to retreive next queue
        # event_list_ordered_by_queue_id = sorted(events_ordered_departure, key=lambda x: (x[queue_column], -x[0]), reverse=False)
        # next_event_log = none_list
        # wq_next_event_dict = {}
        # for event_log in event_list_ordered_by_queue_id:
        #     uniq_id = event_log[uniq_id_column]
        #     if next_event_log[queue_column] == event_log[queue_column]:
        #         wq_next_event_dict[uniq_id] = next_event_log
        #     else:
        #         wq_next_event_dict[uniq_id] = none_list
        #     next_event_log = event_log
        #     # print(wq_next_event_dict[uniq_id])
        #
        # # find within queue last events : sorted by queue_id and by arrival time to retreive last queue
        # event_list_ordered_by_queue_id = sorted(events_ordered_departure, key=lambda x: (x[queue_column], x[0]), reverse=False)
        # last_event_log = none_list
        # wq_last_event_dict = {}
        # for event_log in event_list_ordered_by_queue_id:
        #     uniq_id = event_log[uniq_id_column]
        #     if last_event_log[queue_column] == event_log[queue_column]:
        #         wq_last_event_dict[uniq_id] = last_event_log
        #     else:
        #         wq_last_event_dict[uniq_id] = none_list
        #     last_event_log = event_log
        #     # print(event_log)
        #     # print(wq_last_event_dict[uniq_id])
        #
        # # find next queue next events : sorted by queue_id and by reverse arrival time to retreive last queue
        # event_list_ordered_by_queue_id = sorted(events_ordered_departure, key=lambda x: (x[queue_column], -x[0]), reverse=False)
        # next_event_log = none_list
        # nq_next_event_dict = {}
        # for e in events_ordered_departure:
        #     uniq_id = e[uniq_id_column]
        #     nq_event = next_event_dict[uniq_id]
        #     nq_event_uniq_id = nq_event[uniq_id_column]
        #     for event_log in event_list_ordered_by_queue_id:
        #         nq_next_event_uniq_id = event_log[uniq_id_column]
        #         if next_event_log[queue_column] == event_log[
        #             queue_column] and nq_next_event_uniq_id == nq_event_uniq_id:
        #             nq_next_event_dict[uniq_id] = next_event_log
        #             break
        #         else:
        #             nq_next_event_dict[uniq_id] = none_list
        #         next_event_log = event_log
        #     # print(nq_next_event_dict[uniq_id])
        #
        # # find next queue last events : sorted by queue_id and by arrival time to retreive last queue
        # event_list_ordered_by_queue_id = sorted(events_ordered_departure, key=lambda x: (x[queue_column], x[0]), reverse=False)
        # last_event_log = none_list
        # nq_last_event_dict = {}
        # for e in events_ordered_departure:
        #     uniq_id = e[uniq_id_column]
        #     nq_event = next_event_dict[uniq_id]
        #     nq_event_uniq_id = nq_event[uniq_id_column]
        #     for event_log in event_list_ordered_by_queue_id:
        #         nq_last_event_uniq_id = event_log[uniq_id_column]
        #         if last_event_log[queue_column] == event_log[
        #             queue_column] and nq_last_event_uniq_id == nq_event_uniq_id:
        #             nq_last_event_dict[uniq_id] = last_event_log
        #             break
        #         else:
        #             nq_last_event_dict[uniq_id] = none_list
        #         last_event_log = event_log
        #     # print(nq_last_event_dict[uniq_id])
        #
        # event_list_ordered_by_arrival = sorted(events_ordered_departure, key=lambda x: x[0], reverse=False)
        # # sample for each hidden event ordered by arrival
        # hidden_ids = self.hidden_ids  # [e.id for e in Events_H]
        # # print(hidden_ids)
        # for e in event_list_ordered_by_arrival:
        #     event_id = e[event_column]
        #     if event_id in hidden_ids:
        #         arrival_time, service_time, waiting_time, departure_time, event_id, argmin_d, servicing_state, k_servers, queue_id, uniq_id = e
        #         next_arrival_time, next_service_time, next_waiting_time, next_departure_time, next_event_id, next_argmin_d, next_servicing_state, next_k_servers, next_queue_id, next_uniq_id = \
        #             next_event_dict[uniq_id]
        #         wq_next_arrival_time, wq_next_service_time, wq_next_waiting_time, wq_next_departure_time, wq_next_event_id, wq_next_argmin_d, wq_next_k_servers, wq_next_servicing_state, wq_next_queue_id, wq_next_uniq_id = \
        #             wq_next_event_dict[uniq_id]
        #         wq_last_arrival_time, wq_last_service_time, wq_last_waiting_time, wq_last_departure_time, wq_last_event_id, wq_last_argmin_d, wq_next_k_servers, wq_last_servicing_state, wq_last_queue_id, wq_last_uniq_id = \
        #             wq_last_event_dict[uniq_id]
        #         nq_next_arrival_time, nq_next_service_time, nq_next_waiting_time, nq_next_departure_time, nq_next_event_id, nq_next_argmin_d, nq_next_k_servers, nq_next_servicing_state, nq_next_queue_id, nq_next_uniq_id = \
        #             nq_next_event_dict[uniq_id]
        #         nq_last_arrival_time, nq_last_service_time, nq_last_waiting_time, nq_last_departure_time, nq_last_event_id, nq_last_argmin_d, nq_next_k_servers, nq_last_servicing_state, nq_last_queue_id, nq_last_uniq_id = \
        #             nq_last_event_dict[uniq_id]
        #         print(uniq_id)
        #         print(e)
        #         print(next_event_dict[uniq_id])
        #         print(wq_next_event_dict[uniq_id])
        #         print(wq_last_event_dict[uniq_id])
        #         print(nq_next_event_dict[uniq_id])
        #         print(nq_last_event_dict[uniq_id])
        #
        #         # if wq_next_queue_id is not None:
        #         Lower_bound = self.max_min_queue_grid(departure_time, wq_last_departure_time, nq_last_arrival_time,
        #                                               maximum=1, )
        #         upper_bound = self.max_min_queue_grid(next_departure_time, nq_next_arrival_time, wq_next_departure_time,
        #                                               maximum=0)
        #         print(Lower_bound)
        #         print(upper_bound)
        #         # print(A_bound)
        #         # print(B_bound)
        #         if upper_bound < Lower_bound:
        #             continue
        #         A_bound = self.max_min_queue_grid(wq_next_arrival_time, nq_last_departure_time, maximum=0)
        #         B_bound = self.max_min_queue_grid(wq_next_arrival_time, nq_last_departure_time, maximum=1)
        #
        #         # Get all current queue next arrivals, and next queue prev_event departures
        #         partition_points = []
        #         for e in event_list_ordered_by_arrival:
        #             if (e[0] >= Lower_bound and e[0] <= upper_bound) or (e[3] >= Lower_bound and e[3] <= upper_bound):
        #                 # Check if it's valid
        #                 if e[8] == queue_id and (e[3] >= Lower_bound and e[3] <= upper_bound):
        #                     partition_points.append(e[0])
        #                 elif e[8] == next_queue_id and (e[0] >= Lower_bound and e[0] <= upper_bound):
        #                     partition_points.append(e[0])
        #         partition_points.append(Lower_bound)
        #         partition_points.append(upper_bound)
        #         partition_points.sort()
                # Sample
                # if initial:
                #     # Sample from uniform across [L, U]
                #     d = lower_bound_gibbs + np.random.random() * (upper_bound_gibbs)
                # else:
                #     #### Gibbs sampling
                #     ## Choose an interval
                #     service_rate = self.service_rates[queue_id]
                #     next_service_rate = self.service_rates[next_queue_id]
                #
                #     pass
                #     # TODO
                #     # sample_trancated_exponential(rate, start, end)
                #     # self.event_transition[(event_id, queue_id)] this function gives the next queue for an event
                # self.update_departure_time(d, event_id, queue_id)
                # self.update_arrival_time(d, event_id, next_queue_id)

    def max_min_queue_grid(self, *argv, maximum=1):
        # print("call",maximum)
        bound = 0.0 if maximum == 1 else np.infty
        for arg in argv:
            # print("another arg through *argv:", arg)
            if arg is not None:
                bound = max(bound, arg) if maximum == 1 else min(bound, arg)
                # print("max:",maximum,"bound:", bound)
        return bound


# Test sampling
# mu1 = 0
# mu2 = 5
# np.random.seed(10)
# # exponential_test = [sample_truncated_exponential_left_fixed(mu1, 5, 15) for i in range(5000)]
# # hist, bin_edges = np.histogram(exponential_test, bins=30)
# # plt.hist(exponential_test, bins = bin_edges[:-1])
# # plt.title('Truncated Exponential Left')
# # plt.ylabel('Samples')
# # plt.show()
#
# Test sampling
# mu1 = 2
# mu2 = 1
# np.random.seed(10)
# exponential_test = [sample_truncated_exponential_two_queues_open(mu1, mu2, 2, 4, 2.1, 3) for i in range(5000)]
# hist, bin_edges = np.histogram(exponential_test, bins=30)
# plt.hist(exponential_test, bins = bin_edges[:-1])
# plt.title('Truncated Exponential, {}'.format(r'$\mu_1 = 5, \mu_2 = 7$'))
# plt.ylabel('Samples')
# plt.show()

# Test normalization factors
# Input:
## lower_bound (float) -- Truncation begin
## upper_bound (float) -- Truncation end
## service_rate_current_queue (float >= 0)
## service_rate_next_queue (float >= 0)
## current_queue_current_event ([float] size 2) -- [arrival, departure]
## next_queue_current_event ([float] size 2) -- [arrival, departure]
## next_queue_previous_event ([float] size 2) -- [arrival, departure]
## current_queue_next_event ([float] size 2) -- [arrival, departure]
# Output: Partition probabilities (array, sum to 1)
# lower_bound = 10
# upper_bound= 16
# service_rate_curr = 1
# service_rate_next = 1
# current_queue_current_event = [8, 12]
# next_queue_current_event = [12, 18]
# current_queue_next_event = [10, 16]
# next_queue_previous_event = [0, 0.5]
#
#
# # samples = []
# Z = partition_probabilities(lower_bound, upper_bound, service_rate_curr, service_rate_next,
#                                 current_queue_current_event, next_queue_current_event, next_queue_previous_event,
#                                 current_queue_next_event)
# samples = []
# for i in range(1000):
#     u = np.random.random()
#     z = 0
#     if u < Z[0]:
#         z = 0
#     elif u < Z[0] + Z[1]:
#         z = 1
#     else:
#         z = 2
#     d = sample_truncated_exponential_two_queues_open(z, lower_bound, upper_bound, service_rate_curr, service_rate_next,
#                                                      current_queue_current_event, next_queue_current_event,
#                                                      next_queue_previous_event, current_queue_next_event)
#
#     samples.append(d)
# hist, bin_edges = np.histogram(samples, bins=30)
# plt.hist(samples, bins = bin_edges[:-1])
# plt.title('Truncated Exponential, {}'.format(r'$\mu_1 = 5, \mu_2 = 7$'))
# plt.ylabel('Samples')
# plt.show()

events = 500
p = 0.4
random.seed(events)
ns = network_structure.graph.nodes.get_nodes()
queues = {}
K = 1
for node in ns:
    service_rate = 15*np.random.random()
    service_loss = []
    for k in range(K):
        sl =  (k+1)*service_rate*np.random.random()
        service_loss.append(sl)
    queues[node] = Queue(node, service_rate, K, service_loss)

arrival_rate = 10
arrivals = np.zeros(events)
arrivals[0] = 0.0
for e in range(1, events):
    arrivals[e] = arrivals[e-1] + np.random.exponential(1/arrival_rate)
departures = np.zeros(events)

all_events = []
events_O = []
events_H = []

# Build events
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
events_O_copy = copy.deepcopy(events_O)
events_H_copy = copy.deepcopy(events_H)
queues_copy = copy.deepcopy(queues)
random.seed(events)
S = Simulation(events_O_copy, events_H_copy, queues_copy)
# Copy the hidden events with real values for testing. Deep copy creates new objects with their own references
events_H_actual = copy.deepcopy(events_H)
hidden_ids = []
for h in events_H_actual:
    hidden_ids.append(h.id)
# for e in S.event_triggers:
#     print(e[0])
# print('\nDeparture times')
# for e in S_no_assist.Events_O:
#     print(e.id)
#     print(e.departure_times)

queue_log = {}
for q in S.Queues:
    # if q == 'init':
    #     continue
    print('Queue {}'.format(q))
    print('Arrival, Service, Wait, Departure, ')
    queue = S.Queues[q]
    queue_log[q] = queue.queue_log[0:-1]
    for l in queue.queue_log: # [arrival, service, wait, departure
        print(l)
    print('\n')

queue_network = QueueNetwork(queue_log, hidden_ids, S.event_triggers, K)


def service_rate_k(n, eta, sum_s, sum_sk):
    service_rate = n + eta*sum_s
    service_rate = service_rate/sum_sk
    return service_rate


runs = 10
for i in range(runs):
    print('E-step')
    queue_network.gibbs_sampling_update()

    # M - Step
    for queue_id, queue_log in queue_network.log.items():
        if queue_id == 'init':
            continue
        print('Queue {}'.format(queue_id))

        sum_service_times = 0
        sum_servicers = 0

        sk_sums = [0]*K
        obs = [0]*K
        s_sums = [0]*K
        for log in queue_log: # [arrival, service, wait, departure
            k_servers = int(log[7])
            service_time = log[1]
            if service_time == np.infty:
                continue
            sk_sums[k_servers] += service_time*k_servers
            obs[k_servers] += 1
            s_sums[k_servers] += service_time

        service_rate_observed = sum( service_rate_k(obs[k], queue_network.service_loss[queue_id][k], s_sums[k], sk_sums[k]) for k in range(K))
        print('Update service time estimation')
        queue_network.service_rates[queue_id] = service_rate_observed # M step update, service rate

        # Update eta, service loss
        print('Update service loss estimation')
        for k in range(K):
            service_loss_estimation = service_rate_observed*(k+1) - obs[k]/s_sums[k]
            queue_network.service_loss[queue_id][k] = service_loss_estimation






def plot_service_time_histograms(events_O, events_H, queues):

    random.seed(50)
    events_O_copy = copy.deepcopy(events_O)
    events_H_copy = copy.deepcopy(events_H)
    queues_copy = copy.deepcopy(queues)
    S_w_assist = Simulation(events_O_copy, events_H_copy, queues_copy, 'assistComplete')
    for q in S_w_assist.Queues:
        q_log = S_w_assist.Queues[q].queue_log
        service_mean = 1/S_w_assist.Queues[q].service_rate
        service_times = []
        for log in q_log:
            service_times.append(log[1])
        plt.boxplot(service_times)
        plt.axhline(service_mean, color='r', label='Expected service time {}'.format(q))
        plt.title('Service gains from collaborative processing  K = 3')
        plt.ylabel('Service time')
        plt.xticks([1], ['Queue ' + q])
        plt.legend()
        plt.show()


    # Plots Histograms
    no_assist_service = {}
    w_assist_service = {}
    true_service = {}

    for i in range(200):
        events_O_copy = copy.deepcopy(events_O)
        events_H_copy = copy.deepcopy(events_H)
        queues_copy = copy.deepcopy(queues)
        random.seed(i)
        S_no_assist = Simulation(events_O_copy, events_H_copy, queues_copy)
        random.seed(i)
        events_O_copy = copy.deepcopy(events_O)
        events_H_copy = copy.deepcopy(events_H)
        queues_copy = copy.deepcopy(queues)
        S_w_assist = Simulation(events_O_copy, events_H_copy, queues_copy, 'assistComplete')

        for q in S_w_assist.Queues:
            if q == 'init':
                continue
            print('Queue {}'.format(q))
            queue = S_w_assist.Queues[q]
            true_service[q] = queue.service_rate
            if q not in w_assist_service:
                w_assist_service[q] = []
            # Modified congestion
            sum_service_times = 0
            sum_servicers = 0
            for log in queue.queue_log: # [arrival, service, wait, departure
                k_servers = log[7]
                service_time = log[1]
                sum_service_times += service_time*k_servers
            mod_rate_estimator = len(queue.queue_log) / sum_service_times
            w_assist_service[q].append(mod_rate_estimator)

        for q in S_no_assist.Queues:
            if q == 'init':
                continue
            print('Queue {}'.format(q))
            queue = S_no_assist.Queues[q]
            # standard congestion
            if q not in no_assist_service:
                no_assist_service[q] = []
            sum_service_times = 0
            for log in queue.queue_log: # [arrival, service, wait, departure
                service_time = log[1]
                sum_service_times += service_time
            mod_rate_estimator = len(queue.queue_log) / sum_service_times
            no_assist_service[q].append(mod_rate_estimator)

    print(no_assist_service)
    print(w_assist_service)
    queue_keys = []
    for key in no_assist_service:
        queue_keys.append(key)
    for key in queue_keys:
        service_estimations_no_assist = no_assist_service[key]
        hist, bin_edges = np.histogram(service_estimations_no_assist, bins=30)
        plt.hist(service_estimations_no_assist, bins = bin_edges[:-1], alpha=0.5, label='No collaboration', edgecolor='black')
        ymax = max(hist)+1
        #plt.vlines(true_service[key], ymin=0, ymax=ymax, color='red', label='True service rate')
        plt.legend()
        plt.yticks(range(0, ymax+1, 5))
        plt.title('Service time estimation, standard processing; Queue {}, K = 3'.format(key))
        plt.xlabel('Service time estimation')
        #plt.show()

        service_estimations_w_assist = w_assist_service[key]
        hist, bin_edges = np.histogram(service_estimations_w_assist, bins=30)
        plt.hist(service_estimations_w_assist, bins=bin_edges[:-1], alpha=0.5, label='With collaboration', edgecolor='black')
        ymax = max(ymax, max(hist)+1)
        plt.vlines(true_service[key], ymin=0, ymax=ymax, color='red', label='True service rate')
        plt.legend()
        plt.yticks(range(0, ymax+1, 5))
        plt.title('Service time estimation, collaborative processing; Queue {}, K = 3'.format(key))
        plt.xlabel('Service time estimation')
        plt.show()

plot_service_time_histograms(events_O, events_H, queues)