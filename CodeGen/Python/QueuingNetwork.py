# from CodeGen.Python.networkStructureAttributesAndInstances import *
# from CodeGen.Python.networkUtil import *
from networkStructureAttributesAndInstances import *
from networkUtil import *
# from CodeGen.Python.Simulation import *
from Simulation import *
import numpy as np
import random
import copy
from scipy.stats import expon
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
                if i + 1 < len(event_triggers) and 'Arrival' in event_triggers[i + 1][2] and event_id == \
                        event_triggers[i + 1][1]:
                    print(event_triggers[i])
                    print(event_triggers[i + 1])
                    next_queue = event_triggers[i + 1][3]
                else:
                    next_queue = None

                self.event_transition[(event_id, curr_queue)] = next_queue
        # Trim arrival, wait, service, and destination to 7 decimals
        for q in self.log:
            self.queue_ids.append(q)
            self.service_rates[q] =  1
            self.service_loss[q] = {}
            for k in range(1, self.K + 1):
                self.service_loss[q][k] = 0
            if q == 'init':
                self.service_loss[q] = [0] * self.K
                self.service_rates[q] = 0
            for i in range(len(self.log[q])):
                q_times = [round(self.log[q][i][t], DECIMALS) for t in range(4)]
                q_log = q_times + list(self.log[q][i][4:])
                self.log[q][i] = tuple(q_log)
        # self.update_arrival_time('')
        #self.gibbs_sampling_update(initial=True)

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
            print('Event {} not found in queue {}'.format(event_id, queue_id))
            return
        event_log = self.log[queue_id][log_id]
        event_log_dict = {}
        event_log_dict['arrival_time'] = event_log[0]
        event_log_dict['service_time'] = event_log[1]
        event_log_dict['wait_time'] = event_log[2]
        event_log_dict['departure_time'] = event_log[3]
        event_log_dict['earliest_service_time'] = event_log[0] + event_log[2]
        return event_log_dict

    def update_departure_time(self, new_departure, event_id, queue_id, prev_departure_time, verbose=False):
        # print(event_id)
        # print(queue_id)
        # print(new_departure)
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
            print('Event {} not found in queue {}'.format(event_id, queue_id))
            return

        if queue_id == 'init':
            new_log = (
                0, 0, new_departure, new_departure, event_id, 0, {},0)
            self.log[queue_id][log_id]  = new_log
            return

        log_entry = old_log[log_id]
        # Update within Kth server only
        kth_server = 0
        for k in range(self.K):
            if log_entry[6][k] == event_id:
                kth_server = k
                break

        log_tuple = self.log[queue_id][log_id]

        servicing_state = log_tuple[6]  # Dict representing which subqueues are servicing which events
        # Chech new departure is valid

        arrival_time = log_tuple[0]
        earliest_service_time = max(arrival_time, prev_departure_time)
        waiting_time = earliest_service_time - arrival_time
        service_time = round(new_departure - earliest_service_time, DECIMALS)
        if service_time < 0:
            print('error')
        servicing_state = log_tuple[6]
        k_servers = log_tuple[7]
        new_log = (
            arrival_time, service_time, waiting_time, new_departure, event_id, kth_server, servicing_state, k_servers)
        if verbose:
            print('Old ' + str(old_log[i]))
            print('New ' + str(new_log))
        self.log[queue_id][log_id] = new_log


        # Create new log_entry with new departure

        earliest_service = log_tuple[0] + log_tuple[2]
        # self.log[queue_id][log_id] = (
        # log_tuple[0], new_departure - earliest_service , log_tuple[2], new_departure, log_tuple[4], log_tuple[5], servicing_state, log_tuple[7])
        # departure_times_subserver[log_tuple[4]] = new_departure
        # # print(self.log[queue_id][log_id])
        # # print('Dep ' + str(departure_times_subserver))
        # queue_events = []
        # servicing = [servicing_state[q] for q in servicing_state if servicing_state[q]]
        # if all(servicing):
        #     queue_departures = [departure_times_subserver[event] for event in servicing]
        #     for i in range(log_id + 1, len(old_log)):
        #         arrival_waiting = [old_log[i][0] < dep for dep in queue_departures]
        #         if all(arrival_waiting):
        #             queue_events.append(old_log[i][4])
        #         else:
        #             break
        #
        # # Rearrange log entries after the changed log
        # for i in range(log_id + 1, len(old_log)):
        #     event_id = old_log[i][4]
        #     arrival_time = old_log[i][0]
        #     departure_time = old_log[i][3]
        #     earliest_service_time = arrival_time
        #     servicing_events = [servicing_state[event] for event in servicing_state]
        #     if all(servicing_events):
        #         queue_available = [max(departure_times_subserver[event], arrival_time) for event in servicing_events]
        #         earliest_service_time = min(queue_available)
        #         subserver = 0
        #         for s in range(len(queue_available)):  # First argmin if multiple
        #             if queue_available[s] == earliest_service_time:
        #                 subserver = s
        #                 break
        #     else:
        #         earliest_service_time = arrival_time
        #         subserver = 0
        #         for s in servicing_state:
        #             sub_event = servicing_state[s]
        #             if not sub_event or departure_times_subserver[sub_event] < arrival_time:
        #                 subserver = s
        #                 break
        #

        #     servicing_state_new = {}
        #     servicing_state_new[subserver] = event_id
        #     for s in servicing_state:
        #         if s == subserver:
        #             continue
        #         event_id_old = servicing_state[s]
        #         if event_id_old and departure_times_subserver[event_id_old] > arrival_time:
        #             servicing_state_new[s] = event_id_old
        #         else:
        #             servicing_state_new[s] = None
        #
        #     new_log = (
        #     arrival_time, service_time, waiting_time, departure_time, event_id, subserver, servicing_state_new, log_tuple[7])
        #     if verbose:
        #         print('Old ' + str(old_log[i]))
        #         print('New ' + str(new_log))
        #
        #     compare = [new_log[t] == old_log[i][t] for t in range(len(new_log))]
        #
        #     # Compare new_log with old_log
        #     if all(compare) and i > self.K:
        #         if verbose:
        #             print('Stable')
        #         self.log[queue_id] = old_log
        #         return
        #     else:
        #         old_log[i] = new_log
        #         # Reconstruct relevant info from newest log
        #         log_tuple = old_log[i] #new_log
        #         new_departure = log_tuple[3]
        #         servicing_state = log_tuple[6]
        #         self.log[queue_id] = old_log
        #         departure_times_subserver[log_tuple[4]] = new_departure
        #         queue_events = []
        #         servicing = [servicing_state[q] for q in servicing_state if servicing_state[q]]
        #         if all(servicing):
        #             queue_departures = [departure_times_subserver[event] for event in servicing]
        #             for i in range(log_id + 1, len(old_log)):
        #                 arrival_waiting = [old_log[i][0] < dep for dep in queue_departures]
        #                 if all(arrival_waiting):
        #                     queue_events.append(old_log[i][4])
        #                 else:
        #                     break

    def update_arrival_time(self, new_arrival, event_id, queue_id, previous_departure, verbose=False):

        old_log = list(self.log[queue_id])
        # Proper insert point
        mod_point = 0
        if verbose:
            print('Updating arrival of event {} in queue {}'.format(event_id, queue_id))

        # Initial mod point
        while mod_point < len(old_log):
            if old_log[mod_point][4] == event_id:
                break
            else:
                mod_point += 1
        # Update within Kth server only
        kth_server = 0
        for k in range(self.K):
            if old_log[mod_point][6][k] == event_id:
                kth_server = k
                break

        while mod_point < len(old_log):
            # Delete old log
            if mod_point >= len(old_log):
                print('Event {} not found in queue {}'.format(event_id, queue_id))
                return
            delete_log = old_log[mod_point]
            old_departure_time = old_log[mod_point][3]
            #old_log = old_log[0:mod_point] + old_log[mod_point + 1:]  # Remove old log entry

            earliest_service = max(new_arrival, previous_departure)
            waiting_time = round(earliest_service - new_arrival, DECIMALS)
            if waiting_time < 0:
                raise Exception('Wait time cannot be negative')
            service_time = round(old_departure_time - earliest_service, DECIMALS)

            k_servers = delete_log[7]
            servicing_state = delete_log[6]
            new_log = (
                new_arrival, service_time, waiting_time, old_departure_time, event_id, kth_server, servicing_state,
                k_servers)

            #old_log = old_log[0:mod_point] + [new_log] + old_log[mod_point:]
            if verbose:
                print('Old ' + str(delete_log))
                print('New ' + str(new_log))
            # compare = [new_log[t] == delete_log[t] for t in range(len(new_log))]
            self.log[queue_id][mod_point] = new_log
            return

        #     # Compare new_log with old_log
        #     if all(compare):
        #         if verbose:
        #             print('Stable')
        #
        #         return
        #
        #     mod_point += 1
        #     if mod_point < len(old_log):
        #         event_id = old_log[mod_point][4]
        #         new_arrival = old_log[mod_point][0]
        # self.log[queue_id] = old_log

        # servicing_state = {}
        # departure_servicing = {}
        # #for k in range(self.K):
        # servicing_state[k] = None
        # departure_servicing[k] = None
        # if mod_point > 0:
        #     servicing_state = dict(old_log[mod_point - 1][6])
        # for log in old_log[0:mod_point]:
        #     # If previous event has already departed, remove from state
        #     ev_id = log[4]
        #     if log[3] < new_arrival:
        #         for k in range(self.K):
        #             if servicing_state[k] == ev_id:
        #                 servicing_state[k] = None
        #     else:
        #         for k in range(self.K):
        #             if servicing_state[k] == ev_id:
        #                 departure_servicing[k] = log[3] # state departure after new arrival
        # next_deps = [departure_servicing[k] for k in range(self.K)]
        # argmin_d = 0 # Earliest server available
        # if all(next_deps):
        #     earliest_service = next_deps[0]
        #     argmin_d = 0
        #     for d in range(len(next_deps)):
        #         if earliest_service > next_deps[d]:
        #             earliest_service = next_deps[d]
        #             argmin_d = d
        # else:
        #     earliest_service = new_arrival
        #     for k in range(self.K):
        #         if not servicing_state[k]:
        #             argmin_d = k
        #             break
        # servicing_state[argmin_d] = event_id
        # waiting_time = round(earliest_service - new_arrival, DECIMALS)
        # service_time = round(old_departure_time - earliest_service, DECIMALS)
        # # TODO Remove comments after you find bug.
        # if service_time < 0:
        #     raise Exception('Service time must be non-negative')

    # From a given log, search either forwards and backwards from a log point, and find one log per subqueue
    def surrounding_log_events(self, log_id, queue_id, forwards=True):
        queue_log = self.log[queue_id]
        server_k = 0
        event_id = queue_log[log_id][4]
        for k in range(self.K):
            if queue_log[log_id][6][k] == event_id:
                server_k = k
                break

        log_entry_arrival = {}
        log_entry_departure = {}
        log_entry_arrival[server_k] = None
        log_entry_departure[server_k] = None
        if log_id is not None:  # not none
            if forwards:
                log_id_next = log_id + 1
                while log_id_next < len(queue_log):
                    server_k_surrounding = queue_log[log_id_next][5]
                    if log_entry_arrival[server_k] is None and server_k == server_k_surrounding:
                        log_entry_arrival[server_k] = queue_log[log_id_next][0]
                        log_entry_departure[server_k] = queue_log[log_id_next][3]
                        return [log_entry_arrival, log_entry_departure]
                    else:
                        log_id_next += 1
                return [log_entry_arrival, log_entry_departure]
            else:
                log_id_prev = log_id - 1
                while log_id_prev >= 0:
                    server_k_surrounding = queue_log[log_id_prev][5]
                    if log_entry_arrival[server_k] is None and server_k == server_k_surrounding:
                        log_entry_arrival[server_k] = queue_log[log_id_prev][0]
                        log_entry_departure[server_k] = queue_log[log_id_prev][3]
                        return [log_entry_arrival, log_entry_departure]
                    else:
                        log_id_prev -= 1

        return [log_entry_arrival, log_entry_departure]

    def gibbs_sampling_update(self, initial=False, verbose=False):
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
        # sort 'init' log by departure
        init_log = sorted(self.log['init'], key=lambda x: x[3], reverse=False)
        self.log['init'] = init_log

        for dep_event in events_ordered_departure:
            current_queue_id = dep_event[8]
            if current_queue_id == 'init':
                continue
            event_id = dep_event[4]
            if event_id not in self.hidden_ids:
                continue
            next_queue_id = self.event_transition[(event_id, current_queue_id)]

            # Index in current queue log

            log_id_cq = None
            log_id_nq = None
            # if current_queue_id != 'init':

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
            current_event_current_queue_earliest_service = 0
            try:
                # Current event arrival, a_pi(e)
                current_event_current_queue_arrival = self.log[current_queue_id][log_id_cq][0]  # Earliest service time
                if current_queue_id != 'init':
                    current_event_current_queue_earliest_service = current_event_current_queue_arrival + self.log[current_queue_id][log_id_cq][2]
                current_event_current_queue_departure = self.log[current_queue_id][log_id_cq][3]  # Departure

                next_event_current_queue_departure = None
                next_event_current_queue_arrival = None
                previous_event_current_queue_departure = None
                previous_event_next_queue_arrival = None

                if current_queue_id != 'init':

                    # Previous event departure, d_rho(pi(e))
                    [previous_event_current_queue_arrival_dict,
                     previous_event_current_queue_departure_dict] = self.surrounding_log_events(log_id_cq,
                                                                                                current_queue_id,
                                                                                                forwards=False)

                    previous_event_current_queue_departure_nonempty = [previous_event_current_queue_departure_dict[k]
                                                                       for k in
                                                                       previous_event_current_queue_departure_dict if
                                                                       previous_event_current_queue_departure_dict[
                                                                           k] is not None]
                    # previous_event_current_queue_departure_empty = [previous_event_current_queue_departure_dict[k] for k
                    #                                                    in
                    #                                                    previous_event_current_queue_departure_dict if
                    #                                                    previous_event_current_queue_departure_dict[
                    #                                                        k] is None]
                    if len(previous_event_current_queue_departure_nonempty) != 0:
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
                    # next_event_current_queue_departure_nonempty = [next_event_current_queue_departure_dict[k] for k
                    #                                             in
                    #                                             next_event_current_queue_departure_dict if
                    #                                             next_event_current_queue_departure_dict[
                    #                                                 k] is  None]
                    if len(next_event_current_queue_departure_nonempty) != 0:
                        next_event_current_queue_departure = max(next_event_current_queue_departure_nonempty)

                    # Next event arrival, a_rho^{-1}(pi(e))
                    next_event_current_queue_arrival_nonempty = [next_event_current_queue_arrival_dict[k] for k
                                                                 in
                                                                 next_event_current_queue_arrival_dict if
                                                                 next_event_current_queue_arrival_dict[
                                                                     k] is not None]
                    # next_event_current_queue_arrival_empty = [next_event_current_queue_arrival_dict[k] for k
                    #                                              in
                    #                                              next_event_current_queue_arrival_dict if
                    #                                              next_event_current_queue_arrival_dict[
                    #                                                  k] is  None]
                    if len(next_event_current_queue_arrival_nonempty) != 0:
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
            current_event_next_queue_arrival = None
            current_event_next_queue_earliest = None
            previous_event_next_queue_departure = None
            if log_id_nq is not None and next_queue_id is not None:
                # Previous event arrival, a_rho(e)
                [previous_event_next_queue_arrival_dict,
                 previous_event_next_queue_departure_dict] = self.surrounding_log_events(log_id_nq, next_queue_id,
                                                                                         forwards=False)
                previous_event_next_queue_arrival = None
                previous_event_next_queue_arrival_nonempty = [previous_event_next_queue_arrival_dict[k] for k
                                                              in
                                                              previous_event_next_queue_arrival_dict if
                                                              previous_event_next_queue_arrival_dict[
                                                                  k] is not None]
                # previous_event_next_queue_arrival_empty = [previous_event_next_queue_arrival_dict[k] for k
                #                                               in
                #                                               previous_event_next_queue_arrival_dict if
                #                                               previous_event_next_queue_arrival_dict[
                #                                                   k] is None]
                if len(previous_event_next_queue_arrival_nonempty) != 0:
                    previous_event_next_queue_arrival = max(previous_event_next_queue_arrival_nonempty)

                # Previous event departure, d_rho(e)
                previous_event_next_queue_departure = None
                previous_event_next_queue_departure_nonempty = [previous_event_next_queue_departure_dict[k] for k
                                                                in
                                                                previous_event_next_queue_departure_dict if
                                                                previous_event_next_queue_departure_dict[
                                                                    k] is not None]
                # previous_event_next_queue_departure_empty = [previous_event_next_queue_departure_dict[k] for k
                #                                                 in
                #                                                 previous_event_next_queue_departure_dict if
                #                                                 previous_event_next_queue_departure_dict[
                #                                                     k] is None]
                if len(previous_event_next_queue_departure_nonempty) != 0:
                    previous_event_next_queue_departure = min(previous_event_next_queue_departure_nonempty)

                # Next event arrival, a_rho^{-1}(e)
                [next_event_next_queue_arrival_dict,
                 next_event_next_queue_departure_dict] = self.surrounding_log_events(log_id_nq, next_queue_id,
                                                                                     forwards=True)
                next_event_next_queue_arrival = None
                next_event_next_queue_arrival_nonempty = [next_event_next_queue_arrival_dict[k] for k
                                                          in
                                                          next_event_next_queue_arrival_dict if
                                                          next_event_next_queue_arrival_dict[
                                                              k] is not None]
                # next_event_next_queue_arrival_empty = [next_event_next_queue_arrival_dict[k] for k
                #                                           in
                #                                           next_event_next_queue_arrival_dict if
                #                                           next_event_next_queue_arrival_dict[
                #                                               k] is None]
                if len(next_event_next_queue_arrival_nonempty) != 0:
                    next_event_next_queue_arrival = min(next_event_next_queue_arrival_nonempty)

                # Current event arrival, d_e
                current_event_next_queue_departure = self.log[next_queue_id][log_id_nq][3]
                current_event_next_queue_arrival = self.log[next_queue_id][log_id_nq][0]

            # Lower bound
            lower_bound_choices = [0] + [x for x in
                                         [current_event_current_queue_arrival, previous_event_next_queue_arrival,
                                          previous_event_current_queue_departure] if x]
            upper_bound_choices = [np.infty] + [x for x in
                                                [next_event_next_queue_arrival, next_event_current_queue_departure,
                                                 current_event_next_queue_departure] if x]
            lower_bound_gibbs = max(lower_bound_choices)
            upper_bound_gibbs = min(upper_bound_choices)
            if verbose:
                print('Sample in d in [{}, {}]'.format(lower_bound_gibbs, upper_bound_gibbs))
            # Sample from region
            # Todo with probability, region Z
            # Sample

            if initial:
                # Sample from uniform across [L, U]
                if upper_bound_gibbs == np.infty:
                    continue
                d = lower_bound_gibbs + np.random.random() * (upper_bound_gibbs - lower_bound_gibbs)
                if verbose:
                    print('Sample d = {}'.format(d))
            else:
                #### Gibbs sampling
                ## Choose an interval
                cq_service_rate = self.service_rates[current_queue_id]
                if next_queue_id is not None:
                    nq_service_rate = self.service_rates[next_queue_id]
                else:
                    nq_service_rate = 0

                current_queue_current_event = [current_event_current_queue_arrival,
                                               current_event_current_queue_departure]
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

                d = sample_truncated_exponential_two_queues_open(z, lower_bound_gibbs, upper_bound_gibbs,
                                                                 cq_service_rate,
                                                                 nq_service_rate, current_queue_current_event,
                                                                 next_queue_current_event, next_queue_previous_event,
                                                                 current_queue_next_event)

                # self.event_transition[(event_id, queue_id)] this function gives the next queue for an event
                # print('Sampling from CQ {} *[ x - {}] , NQ {} * [{} - x] from x in [{}, {}]'.format(cq_service_rate,
                #                                                                                     current_event_current_queue_arrival,
                #                                                                                     nq_service_rate,
                #                                                                                     current_event_next_queue_departure,
                #                                                                                     lower_bound_gibbs,
                #                                                                                     upper_bound_gibbs))
                if verbose:
                    print('Sample d = {}'.format(d))
                if d > upper_bound_gibbs or d < lower_bound_gibbs:
                    d = np.random.random()*(upper_bound_gibbs - lower_bound_gibbs) + lower_bound_gibbs
                if np.isnan(d):
                    d = np.random.random() + lower_bound_gibbs
                    #raise Exception('Bound error')
            if previous_event_current_queue_departure is None:
                previous_event_current_queue_departure = 0
            if next_queue_id is not None :
                self.update_departure_time(d, event_id, current_queue_id, previous_event_current_queue_departure)
                if previous_event_next_queue_departure is None:
                    previous_event_next_queue_departure = 0
                self.update_arrival_time(d, event_id, next_queue_id, previous_event_next_queue_departure)


    def max_min_queue_grid(self, *argv, maximum=1):
        # print("call",maximum)
        bound = 0.0 if maximum == 1 else np.infty
        for arg in argv:
            # print("another arg through *argv:", arg)
            if arg is not None:
                bound = max(bound, arg) if maximum == 1 else min(bound, arg)
                # print("max:",maximum,"bound:", bound)
        return bound


K =4
events = 1000
p = 0.80
runs = 250
random.seed(events)
ns = network_structure.graph.nodes.get_nodes()
queues = {}

for node in ns:
    service_rate =  expon.rvs(scale=10)
    service_loss = {}
    for k in range(1, K + 1):
        if k == 1:
            service_loss[k] = 0
        else:
            service_loss[k] = 0#(k) * service_rate * np.random.random()
    queues[node] = Queue(node, service_rate, K, service_loss)

arrival_rate = 100
arrivals = np.zeros(events)
arrivals[0] = 0.0
for e in range(1, events):
    arrivals[e] = arrivals[e - 1] + np.random.exponential(1 / arrival_rate)
departures = np.zeros(events)

all_events = []
events_O = []
events_H = []

# Build events
for e in range(events):
    tasks = np.random.randint(2, 5)
    event_path = list(random_path(tasks))  # Make copy
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
S = Simulation(events_O_copy, events_H_copy, queues_copy, 'assistComplete')
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


true_service_loss = {}
queue_log = {}


for q in S.Queues:
    # if q == 'init':
    #     continue
    print('Queue {}'.format(q))
    print('Arrival, Service, Wait, Departure, ')
    queue = S.Queues[q]
    # true_service_loss[q] = {}
    # for k in range(1, K + 1):
    #     true_service_loss[q][k] = queue.service_loss[k]

    queue_log[q] = [qlog for qlog in queue.queue_log]
#    true_observed_sum = 0
    # for l in queue.queue_log:  # [arrival, service, wait, departure
    #     true_observed_sum += l[1]
    # true_service_rate[q] = len(queue.queue_log) / true_observed_sum
    # print('\n')

def service_rate_k(n, eta, sum_s, sum_sk):
    service_rate = n + eta * sum_s
    service_rate = service_rate / sum_sk
    return service_rate


queue_network = QueueNetwork(queue_log, hidden_ids, S.event_triggers, K)
true_service_rates = {}
true_service_rates_unflitered = {}
true_service_loss = {}
for queue_id, queue_log in queue_network.log.items():
    true_service_loss[queue_id] = {}
    for k in range(2, K+1):
        true_service_loss[queue_id] = 0

observation_sum = 0
for q in queue_network.log:
    if q == 'init':
        continue
    N_q = len(queue_network.log[q])
    observation_q = sum([entry[1]*entry[7] for entry in queue_network.log[q]])
    # true_service_rates_unflitered[q] = N_q/observation_q
    # observation_q_1 = sum([entry[1] * entry[7] for entry in queue_network.log[q] if entry[7] == 1])
    # observation_q_2 = sum([entry[1] * entry[7] for entry in queue_network.log[q] if entry[7] == 2])
    # true_service_loss[q] = observation_q_1 - observation_q_2
    true_service_rates[q] = N_q/observation_q


#true_service_rate = N_q/observation_sum

queue_network.gibbs_sampling_update(initial=True)



def log_likelihood(service_times, servers_k, service_rate):
    log_ll = 0
    for s, k in zip(service_times, servers_k):
        p_s = np.log(service_rate)  -service_rate*(s*k)
        #p_theta = np.log(10) - 10/service_rate

        log_ll +=  p_s #+ p_theta
    return log_ll


#runs = 50
# estimated_service_rate = {}
# for queue_id, queue_log in queue_network.log.items():
#     if queue_id == 'init':
#         continue

estimated_service_rates = {}
log_likelihood_runs = []
log_lh_full = 0
for queue_id, queue_log in queue_network.log.items():
    if queue_id == 'init':
        continue
    estimated_service_rates[queue_id] = []
    observed_estimation = queue_network.service_rates[queue_id]
    estimated_service_rates[queue_id].append(observed_estimation)


    service_times = [log[1] for log in queue_log]
    k_servers = [log[7] for log in queue_log]
    service_rate = queue_network.service_rates[queue_id]

    ll = log_likelihood(service_times, k_servers, service_rate)
    log_lh_full += ll
log_likelihood_runs.append(log_lh_full)


for i in range(runs):
    print("Run {}".format(i))

    # E - step
    print('E-step')
    queue_network.gibbs_sampling_update()

    # M - Step
    print("M-step")

    log_lh_full = 0
    for queue_id, queue_log in queue_network.log.items():
        if queue_id == 'init':
            continue
        observation_q = sum([entry[1]*entry[7] for entry in queue_network.log[queue_id]])

        N_q = len(queue_network.log[queue_id])
        observed_estimation = N_q / observation_q

        estimated_service_rates[queue_id].append(observed_estimation)
        queue_network.service_rates[queue_id] = observed_estimation

        print('True service rate: {}'.format(true_service_rates[queue_id]))
        print('Estimated service rate: {}'.format(observed_estimation))

        service_times = [log[1] for log in queue_log]
        k_servers = [log[7] for log in queue_log]
        ll = log_likelihood(service_times, k_servers, observed_estimation)
        log_lh_full += ll
    log_likelihood_runs.append(log_lh_full)

    # for k in range(1, K + 1):
    #     service_rate_observed += service_rate_k(obs[k], queue_network.service_loss[queue_id][k], s_sums[k],
    #                                             sk_sums[k])
    # estimated_service_rate[queue_id].append(service_rate_observed)


    print('Update service time estimation')

        # Update eta, service loss
        # print('Update service loss estimation')
        # for k in range(1, K + 1):
        #     service_loss_estimation = service_rate_observed * (k) - obs[k] / s_sums[k]
        #     queue_network.service_loss[queue_id][k] = service_loss_estimation


# Plot log likelihood of service rate estimation over runs
# for queue_id, queue_log in queue_network.log.items():
#     if queue_id == 'init':
#         continue
# estimated_service_rate_queue = estimated_service_rate[queue_id]
# true_service_rate_queue = true_service_rate[queue_id]

p_percent = int(100 * p)
csv_file = 'Results/server_k{}_events{}_p{}_queue_all_10queues.csv'.format(K, events, p_percent)
with open(csv_file, 'w') as f:
    f.write('Iteration,Squared_error,Estimate,Actual, Queue\n')
    iterations = len(log_likelihood_runs)
    for q in queue_network.log:
        if q == 'init':
            continue
        squared_error = [(e - true_service_rates[q]) ** 2 for e in estimated_service_rates[q]]
        #plt.plot(squared_error)
        #plt.show()
        for i in range(iterations):
            row = [str(i), str(squared_error[i]),  str(estimated_service_rates[q][i]), str(true_service_rates[q]), q]
            f.write(','.join(row) + '\n')

csv_file_all = 'Results/server_k{}_events{}_p{}_queue_all_loglikelihood_10queues.csv'.format(K, events, p_percent)
with open(csv_file_all, 'w') as f:
    f.write('Iteration,LogLikelihood\n')
    iterations = len(log_likelihood_runs)
    for i in range(iterations):
        row = [str(i), str(log_likelihood_runs[i])]
        f.write(','.join(row) + '\n')

plt.plot(log_likelihood_runs)
plt.title('Log Likelihood K = {} p = {}'.format(K, p))
plt.show()


def plot_service_time_histograms(events_O, events_H, queues):
    random.seed(50)
    events_O_copy = copy.deepcopy(events_O)
    events_H_copy = copy.deepcopy(events_H)
    queues_copy = copy.deepcopy(queues)
    S_w_assist = Simulation(events_O_copy, events_H_copy, queues_copy, 'assistComplete')
    for q in S_w_assist.Queues:
        q_log = S_w_assist.Queues[q].queue_log
        service_mean = 1 / S_w_assist.Queues[q].service_rate
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
            for log in queue.queue_log:  # [arrival, service, wait, departure
                k_servers = log[7]
                service_time = log[1]
                sum_service_times += service_time * k_servers
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
            for log in queue.queue_log:  # [arrival, service, wait, departure
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
        plt.hist(service_estimations_no_assist, bins=bin_edges[:-1], alpha=0.5, label='No collaboration',
                 edgecolor='black')
        ymax = max(hist) + 1
        # plt.vlines(true_service[key], ymin=0, ymax=ymax, color='red', label='True service rate')
        plt.legend()
        plt.yticks(range(0, ymax + 1, 5))
        plt.title('Service time estimation, standard processing; Queue {}, K = 3'.format(key))
        plt.xlabel('Service time estimation')
        # plt.show()

        service_estimations_w_assist = w_assist_service[key]
        hist, bin_edges = np.histogram(service_estimations_w_assist, bins=30)
        plt.hist(service_estimations_w_assist, bins=bin_edges[:-1], alpha=0.5, label='With collaboration',
                 edgecolor='black')
        ymax = max(ymax, max(hist) + 1)
        plt.vlines(true_service[key], ymin=0, ymax=ymax, color='red', label='True service rate')
        plt.legend()
        plt.yticks(range(0, ymax + 1, 5))
        plt.title('Service time estimation, collaborative processing; Queue {}, K = 3'.format(key))
        plt.xlabel('Service time estimation')
        plt.show()

# plot_service_time_histograms(events_O, events_H, queues)