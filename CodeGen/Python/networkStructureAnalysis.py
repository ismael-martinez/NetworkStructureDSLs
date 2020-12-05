from networkStructureAttributesAndInstances import *
from networkUtil import *
#from CodeGen.Python.networkStructureAttributesAndInstances import *
#from CodeGen.Python.networkUtil import *
import numpy as np
import matplotlib.pyplot as plt
import nxviz as nv
import networkx as nx
import os
import cv2
import math


def main():
    print('*** ATTRIBUTES ***')
    print('Node Attributes: ' + str(network_structure.listNodeAttributes()))
    print('Thing Attributes: ' + str(network_structure.listThingAttributes()))
    print('Link Attributes: ' + str(network_structure.listLinkAttributes()) + '\n')

    # Show Network Structure
    G = nx.DiGraph()
    ns_graph = network_structure.graph
    for node_id in ns_graph.nodes:
        G.add_node(node_id)
    for link_id in ns_graph.links:
        [n_source, n_target] = ns_graph.links[link_id].node_pair
        G.add_edge(n_source, n_target)

    A = nx.nx_pydot.write_dot(G, 'graph.dot')
    os.system('dot -Tpng -O  graph.dot')


    # Handshake -- create a distance matrix between every 'thing' and 'node'
    T = len(network_structure.things)
    N = len(network_structure.graph.nodes)
    distance_matrix = np.zeros((T, N))
    nearest_node = [0]*T
    thing_key_index = []
    for thing in network_structure.things:
        thing_key_index.append(thing)
    node_key_index = []
    for node in network_structure.graph.nodes:
        node_key_index.append(node)

    t = 0
    for thing in network_structure.things:
        n = 0
        for node in network_structure.graph.nodes:
            thing_location = network_structure.things[thing].locations[0]
            node_location = network_structure.graph.nodes[node].locations[0]
            distance_matrix[t][n] = distance_location(thing_location, node_location)
            if distance_matrix[t][n] < distance_matrix[t][nearest_node[t]]:
                nearest_node[t] = n
            n += 1
        t += 1

    node_arrival_schedules = {}

    for t in range(T):
        node_id = node_key_index[nearest_node[t]]
        node_name = network_structure.graph.nodes[node_id].id
        if node_name not in node_arrival_schedules.keys():
            node_arrival_schedules[node_name] = []
        thing_id = thing_key_index[t]
        sched = network_structure.things[thing_id].schedule
        # Merge
        i, j = 0, 0
        new_sched = []
        old_sched = node_arrival_schedules[node_name]
        while i < len(old_sched) and j < len(sched):
            if compare_time(old_sched[i], sched[j]) < 0:
                new_sched.append(old_sched[i])
                i += 1
            else:
                new_sched.append(sched[j])
                j += 1
        while i < len(old_sched):
            new_sched.append(old_sched[i])
            i += 1
        while j < len(sched):
            new_sched.append(sched[j])
            j += 1
        node_arrival_schedules[node_name] = new_sched

    # Arrivals per hour
    min_hour = 0
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
    max_y = 0
    for node in node_arrival_schedules:
        arrivals = [0]*(last_hour_all - first_hour + 1)
        for timestamp in node_arrival_schedules[node]:
            hour = timestamp.hour
            idx = hour - first_hour_all
            arrivals[idx] += 1
        arrivals_node[node] = arrivals
        for a in arrivals:
            if a > max_y:
                max_y = a

    for node in node_arrival_schedules:
        # Plot hourly arrival
        arrivals = arrivals_node[node]
        fig, ax = plt.subplots()
        ax.bar(hours, arrivals)
        hour_str = [str(h) + 'h00' for h in hours]
        ax.set_xticks(hours)
        ax.set_xticklabels(hour_str)
        ax.set_ylim(0, max_y)
        ax.set_yticks(list(range(0, max_y+1)))
        ax.set_xlabel('Hours')
        ax.set_ylabel('Arrivals')
        ax.set_title('Arrivals per hour - Node {}'.format(node))
        #plt.show()

    # Arrivals per quarter hour (15)
    quarters = []
    for h in hours:
        for i in range(4):
            quarter_time = h + i*0.25
            quarters.append(quarter_time)
    arrivals_node = {}
    max_y = 0
    for node in node_arrival_schedules:
        arrivals = [0]*(last_hour_all - first_hour + 1)*4
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
        for a in arrivals:
            if a > max_y:
                max_y = a

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
        ax.set_xticklabels(quarter_str)
        ax.set_ylim(0, max_y)
        ax.set_yticks(list(range(0, max_y+1)))
        ax.set_xlabel('Quarter Hours')
        ax.set_ylabel('Arrivals')
        ax.set_title('Arrivals per 15 minutes - Node {}'.format(node))
        #plt.show()

    graph_img = cv2.imread('graph.dot.png')
    cv2.imshow('Graph Structure', graph_img)
    cv2.waitKey(0)

if __name__=="__main__":
    main()