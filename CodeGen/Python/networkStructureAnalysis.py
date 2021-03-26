from networkStructureAttributesAndInstances import *
import networkStructure as NS
import networkUtil as NU
from Simulation import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import random
import networkx as nx
import os
import cv2
import math
import sys, getopt


def handshake():
    # Handshake -- create a distance matrix between every 'thing' and 'node'
    T = len(network_structure.clients.get_clients())
    N = len(network_structure.graph.nodes.get_nodes())
    distance_matrix = np.zeros((T, N))
    nearest_node = [0] * T
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
                    distance_matrix[t][n] = NU.distance_location(client_location, node_location)
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
        node_radius = network_structure.graph.nodes.get_node(node_id).get_radius()
        client_radius = network_structure.clients.get_client(client_id).get_radius()
        within_node_radius = (distance_matrix[t][n]) * 1000 <= node_radius # kilometers to meters
        within_thing_radius = (distance_matrix[t][n]) * 1000 <= client_radius # kilometers to meters
        if (within_node_radius and within_thing_radius):  # distance matrix in kilometeres. Radius in meters.
            client = network_structure.clients.get_client(client_id)
            client_attributes = [client.schedule, client.fileSize_mb, client.local_CPU_ghz, client.storageReq_mb, client.ramReq_mb]
            old_attributes = node_arrival_schedules[node_name]
            new_attributes = NU.merge_timestamps_attr(client_attributes, old_attributes) # Merge via first index = schedule
            node_arrival_schedules[node_name] = new_attributes

    node_arrival_keys = [a for a in node_arrival_schedules.keys()]
    for node in node_arrival_keys:
        if node_arrival_schedules[node] == []:
            node_arrival_schedules.pop(node, None)

    return node_arrival_schedules

def timestamp_floor(timestamp_var, parts_per_hour = 1):
    partition_minutes = 60/parts_per_hour
    timestamp_hour = timestamp_var.hour
    timestamp_floor_minutes = 0
    for p in range(parts_per_hour):
        if timestamp_var.minutes >= p*partition_minutes:
            timestamp_floor_minutes = p
        else:
            break
    # Build timestamp_floor
    timestamp_seconds = timestamp_floor_minutes*partition_minutes*60
    timestamp_seconds += timestamp_hour*3600
    timestamp_floor = NS.timestamp(timestamp_seconds)
    return timestamp_floor

# def timestamp_ceil(timestamp_var, parts_per_hour = 1):
#     partition_minutes = 60/parts_per_hour
#     timestamp_hour = timestamp_var.hour
#     timestamp_ceil_minutes = 60
#     for p in range(parts_per_hour, -1, -1):
#         if timestamp_var.minutes <= p*partition_minutes:
#             timestamp_ceil_minutes = p
#         else:
#             break
#     # Build timestamp_floor
#     timestamp_seconds = timestamp_ceil_minutes*60
#     timestamp_seconds += timestamp_hour*3600
#     timestamp_ceil = NS.timestamp(timestamp_seconds)
#     return timestamp_ceil

def minute_str(integer):
    int_str = str(integer)
    if int_str == '0':
        int_str = '00'
    return int_str

def hour_partition(node_arrival_schedules, arrival_pdf, parts_per_hour=1, histo_type='quantity'):


    if (60 % parts_per_hour != 0):
        raise ValueError("Partitions must equally divide an hour by minutes")

    for node in node_arrival_schedules:
        minutes_per_partition = int(60/parts_per_hour)
        first_partition = timestamp_floor(node_arrival_schedules[node][0][0], parts_per_hour)
        last_partition = timestamp_floor(node_arrival_schedules[node][-1][0], parts_per_hour)


        partitions_qty = int((last_partition.timestamp_to_seconds() - first_partition.timestamp_to_seconds())/(60*minutes_per_partition)) + 1
        partition_timestamps = [NS.timestamp(first_partition.timestamp_to_seconds() + p*minutes_per_partition*60) for p in range(partitions_qty)]


        arrivals = [0] * (partitions_qty)
        partition_indices = list(range((partitions_qty)))
        for row in node_arrival_schedules[node]:
            ts = row[0]
            ts_partition = timestamp_floor(ts, parts_per_hour)
            ts_partition_idx = int((ts_partition.timestamp_to_seconds() - first_partition.timestamp_to_seconds())/(60*minutes_per_partition))
            if histo_type == 'quantity':
                # For quantity of arrivals
                arrivals[ts_partition_idx] += 1
            elif histo_type == 'storage':
                # For storage of arrivals
                arrivals[ts_partition_idx] += row[4]
            elif histo_type == 'ram':
                # For storage of arrivals
                arrivals[ts_partition_idx] += row[5]

        # Plot in PDF
        # Plot arrivals by partition
        fig, ax = plt.subplots(figsize=(10,10))
        ax.bar(partition_indices, arrivals)
        partition_str = [str(ts.hour) + 'h' + minute_str(ts.minutes) for ts in partition_timestamps]
        ax.set_xticks(partition_indices)
        ax.set_xticklabels(partition_str)
        ax.set_xticklabels(partition_str, rotation=45)
        # ax.set_ylim(0, max_y)
        # ax.set_yticks(list(range(0, max_y+1)))
        ax.set_xlabel('Time')
        if histo_type == 'quantity':
            ax.set_ylabel('# of Arrivals')
        elif histo_type == 'storage':
            ax.set_ylabel('Storage Required (GB)')
        elif histo_type == 'ram':
            ax.set_ylabel('RAM Required (GB)')
        ax.set_title('Arrivals per 1/{} Hour — Node {}'.format(parts_per_hour, node))

        rects = ax.patches
        ax_labels = [str(a) for a in arrivals]
        for rect, ax_label in zip(rects, ax_labels):
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2, height + 5, ax_label, ha='center', va='bottom')

        # plt.show()
        arrival_pdf.savefig(fig)


def main(argv):
    # Arguments
    queue_analysis = False
    arrival_analysis = False
    network_structure_analysis = False
    partitions = 1
    histo_type = "quantity" #Default

    try:
        opts, args = getopt.getopt(argv, "hqanp:t:", ["queueAnalysis=", "arrivalAnalysis=", "networkAnalysis=", "numberPartitions=", "histogramType="])
    except getopt.GetoptError:
        print('networkStructureAnalysis.py -q (optional) -a (optional) -n (optional) -p <number of partitions per hour> (optional) -t <type of histogram> (optional)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('networkStructureAnalysis.py -q (optional) -a (optional) -n (optional) -p <number of partitions per hour> (optional) -t <type of histogram> (optional)')
            sys.exit()
        elif opt in ("-q", "--queueAnalysis"):
            queue_analysis = True
        elif opt in ("-a", "--arrivalAnalysis"):
            arrival_analysis = True
        elif opt in ("-n", "--networkAnalysis"):
            network_structure_analysis = True
        elif opt in ('-p', '--numberPartitions'):
            partitions = int(arg)
        elif opt in ('-t', '--histogramType'):
            histo_type = str(arg)

    print('*** ATTRIBUTES ***')
    for client_set in network_structure.clients.attributes:
        print('Client type {} : {}'.format(client_set, network_structure.clients.attributes[client_set]))
    for node_set in network_structure.graph.nodes.attributes:
        print('Node type {} : {}'.format(node_set, network_structure.graph.nodes.attributes[node_set]))
    for link_set in network_structure.graph.links.attributes:
        print('Link type {} : {}'.format(link_set, network_structure.graph.links.attributes[link_set]))



    # Request arrival graphs ####################
    node_arrival_schedules = handshake()


    if arrival_analysis:
        print('Arrival Request graphs printing in .pdf files')

        arrival_pdf = PdfPages('request_arrival_{}partitions_{}.pdf'.format(partitions, histo_type))
        hour_partition(node_arrival_schedules, arrival_pdf, partitions, histo_type)
        arrival_pdf.close()
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
