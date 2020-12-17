from networkStructureAttributesAndInstances import *
import networkStructure as NS
from networkUtil import *
from Simulation import *
import numpy as np
import matplotlib.pyplot as plt
import random
import networkx as nx
import os
import cv2
import math
import sys, getopt


def main(argv):
    # Arguments
    queue_analysis = False
    arrival_analysis = False
    network_structure_analysis = False

    try:
        opts, args = getopt.getopt(argv, "hqan", ["queueAnalysis=", "arrivalAnalysis=", "networkAnalysis="])
    except getopt.GetoptError:
        print('networkStructureAnalysis.py -q (optional) -a (optional) -n (optional)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('networkStructureAnalysis.py -q (optional) -a (optional) -n (optional)')
            sys.exit()
        elif opt in ("-q", "--queueAnalysis"):
            queue_analysis = True
        elif opt in ("-a", "--arrivalAnalysis"):
            arrival_analysis = True
        elif opt in ("-n", "--networkAnalysis"):
            network_structure_analysis = True

    print('*** ATTRIBUTES ***')
    for client_set in network_structure.clients.attributes:
        print('Client type {} : {}'.format(client_set, network_structure.clients.attributes[client_set]))
    for node_set in network_structure.graph.nodes.attributes:
        print('Node type {} : {}'.format(node_set, network_structure.graph.nodes.attributes[node_set]))
    for link_set in network_structure.graph.links.attributes:
        print('Link type {} : {}'.format(link_set, network_structure.graph.links.attributes[link_set]))



    # Request arrival graphs ####################

    # Handshake -- create a distance matrix between every 'thing' and 'node'
    T = len(network_structure.clients.get_clients())
    N = len(network_structure.graph.nodes.get_nodes())
    distance_matrix = np.zeros((T, N))
    nearest_node = [0]*T
    client_key_index = []
    for client in network_structure.clients.get_clients():
        client_key_index.append(client)
    node_key_index = []
    node_key_dict = {}
    n = 0
    for node in network_structure.graph.nodes.get_nodes():
        node_key_index.append(node)
        node_key_dict[node] = n
        n += 1

    t = 0
    for client in network_structure.clients.get_clients():
        for client_location in network_structure.clients.get_client(client).locations:
            n = 0
            for node in network_structure.graph.nodes.get_nodes():
                for node_location in network_structure.graph.nodes.get_node(node).locations:
                    distance_matrix[t][n] = distance_location(client_location, node_location)
                    if distance_matrix[t][n] < distance_matrix[t][nearest_node[t]]:
                        nearest_node[t] = n
                n += 1
        t += 1

    node_arrival_schedules = {}

    for t in range(T):
        node_id = node_key_index[nearest_node[t]]
        node_name = network_structure.graph.nodes.get_node(node_id).id
        if node_name not in node_arrival_schedules.keys():
            node_arrival_schedules[node_name] = []
        client_id = client_key_index[t]
        n = node_key_dict[node_id]
        within_node_radius = (distance_matrix[t][n])*1000 <= network_structure.graph.nodes.get_node(node_id).get_radius()
        within_thing_radius = (distance_matrix[t][n])*1000 <= network_structure.clients.get_client(client_id).get_radius()
        if (within_node_radius and within_thing_radius): # distance matrix in kilometeres. Radius in meters.
            sched = network_structure.clients.get_client(client_id).schedule
            old_sched = node_arrival_schedules[node_name]
            new_sched = merge_timestamps(sched, old_sched)
            node_arrival_schedules[node_name] = new_sched

    if arrival_analysis:
        print('Arrival Request graphs printing in .pdf files')

    # Arrivals per hour
    first_hour_all = 24
    last_hour_all = 0
    for node in node_arrival_schedules:
        first_hour = node_arrival_schedules[node][0].hour
        last_hour = node_arrival_schedules[node][-1].hour
        if first_hour < first_hour_all:
            first_hour_all = first_hour
        if last_hour > last_hour_all:
            last_hour_all = last_hour

    hours = list(range(first_hour_all, last_hour_all+1))
    arrivals_node = {}
    for h in hours:
        arrivals_node[h] = 0
    #max_y = 0 # Max y-axis value for plot
    for node in node_arrival_schedules:
        arrivals = [0]*(last_hour_all - first_hour_all + 1)
        for timestamp in node_arrival_schedules[node]:
            hour = timestamp.hour
            idx = hour - first_hour_all
            arrivals[idx] += 1
        arrivals_node[node] = arrivals
        # for a in arrivals:
        #     if a > max_y:
        #         max_y = a

    for node in node_arrival_schedules:
        # Plot hourly arrival
        arrivals = arrivals_node[node]
        fig, ax = plt.subplots()
        ax.bar(hours, arrivals)
        hour_str = [str(h) + 'h00' for h in hours]
        ax.set_xticks(hours)
        ax.set_xticklabels(hour_str)
        ax.set_xticklabels(hour_str, rotation=45)
        #ax.set_ylim(0, max_y)
        #ax.set_yticks(list(range(0, max_y+1)))
        ax.set_xlabel('Hours')
        ax.set_ylabel('Arrivals')
        ax.set_title('Arrivals per hour - Node {}'.format(node))
        #plt.show()


        if arrival_analysis:

            plot_pdf = 'request_arrivals_perHour_{}.pdf'.format(node)
            fig.savefig(plot_pdf, bbox_inches='tight')

    # Arrivals per quarter hour (15)
    quarters = []
    for h in hours:
        for i in range(4):
            quarter_time = h + i*0.25
            quarters.append(quarter_time)
    arrivals_node = {}
    for h in hours:
        arrivals_node[h] = 0
    #max_y = 0
    for node in node_arrival_schedules:
        arrivals = [0]*(last_hour_all - first_hour_all + 1)*4
        for timestamp in node_arrival_schedules[node]:
            hour = timestamp.hour
            minutes = timestamp.minutes
            idx = 4*(hour - first_hour_all)
            if minutes >= 15 and minutes < 30:
                idx += 1
            elif minutes >= 30 and minutes < 45:
                idx += 2
            elif minutes >= 45:
                idx += 3
            arrivals[idx] += 1
        arrivals_node[node] = arrivals
        # for a in arrivals:
        #     if a > max_y:
        #         max_y = a

    for node in node_arrival_schedules:
        # Plot quarterly arrival
        arrivals = arrivals_node[node]
        fig, ax = plt.subplots()
        ax.bar(quarters, arrivals, 0.2, color='g')
        quarter_str = []
        for q in quarters:
            h = math.floor(q)
            m = q % 1
            if m < 0.25:
                quarter_str.append(str(h) + 'h00')
            elif m < 0.5:
                quarter_str.append(str(h) + 'h15')
            elif m < 0.75:
                quarter_str.append(str(h) + 'h30')
            else:
                quarter_str.append(str(h) + 'h45')
        ax.set_xticks(quarters)
        ax.set_xticklabels(quarter_str, rotation=45)
        #ax.set_ylim(0, max_y)
        #ax.set_yticks(list(range(0, max_y+1)))
        ax.set_xlabel('Quarter Hours')
        ax.set_ylabel('Arrivals')
        ax.set_title('Arrivals per 15 minutes - Node {}'.format(node))
        #plt.show()

        if arrival_analysis:
            plot_pdf = 'request_arrivals_perQuarter_{}.pdf'.format(node)
            fig.savefig(plot_pdf, bbox_inches='tight')

    if arrival_analysis:
        print('Complete')
    ############################################

    if queue_analysis:

        # Queue Simulation
        random.seed(100)
        ns = network_structure.graph.nodes.get_nodes()
        queues = {}
        K = 1


        arrivals = []
        zero_timestamp = NS.timestamp(0)
        arrivals.append(zero_timestamp)



        for n in ns:
            if n not in node_arrival_schedules:
                continue
            arrivals = [s.timestamp_to_seconds() for s in  node_arrival_schedules[n]]
            events = []
            node = ns[n]
            service_rate = node.get_service_rate()
            queues = {n:Queue(n, service_rate, K)}
            for a in range(len(arrivals)):
                id = 't{}'.format(a)
                events.append(Event(id, [arrivals[a]], [0.0], [n]))
            # Init calls execution_initial() internally
            S = Simulation(events, [], queues)

            queue_simulation_file = 'queue_simulation_{}.txt'.format(n)
            with open(queue_simulation_file, 'w') as g:
                print('Simulation log, queue {}'.format(n))
                for log in S.simulation_log:
                    g.write(log)
                    g.write('\n')

            queue_log_file = 'queue_log_{}.csv'.format(n)
            f = open(queue_log_file, 'w')


            queue_log = {}
            for q in S.Queues:
                if q == 'init':
                    continue
                f.write('Queue {}'.format(q) + '\n')
                f.write('Arrival, Service, Wait, Departure\n ')
                queue = queues[q]
                queue_log[q] = queue.queue_log
                for l in queue.queue_log:  # [arrival, service, wait, departure
                    arrival = NS.timestamp.convertTime(l[0])
                    departure = NS.timestamp.convertTime(l[3])
                    log = [arrival, str(l[1]), str(l[2]), departure]
                    f.write(','.join(log) + '\n')
            f.close()
            print('Queue simulation log available in {}'.format(queue_simulation_file))
            print('Queue event log available in {}'.format(queue_log_file))
    ##############################
    # Show Network Structure
    if network_structure_analysis:
        print('Network Structure graph')
        G = nx.DiGraph()
        ns_graph = network_structure.graph
        for node_id in ns_graph.nodes.get_nodes():
            G.add_node(node_id)
        for link_id in ns_graph.links.get_links():
            [n_source, n_target] = ns_graph.links.get_link(link_id).node_pair
            G.add_edge(n_source, n_target)

        ## Network structure
        A = nx.nx_pydot.write_dot(G, 'graph.dot')
        os.system('dot -Tpng -O  graph.dot')
        graph_img = cv2.imread('graph.dot.png')
        cv2.imshow('Graph Structure', graph_img)
        cv2.waitKey(0)


if __name__=="__main__":
    main(sys.argv[1:])
