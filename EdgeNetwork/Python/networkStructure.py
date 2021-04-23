from abc import ABC, abstractmethod
from networkUtil import *
import math


class NetworkStructure:
    def __init__(self, graph, clients):
        self.graph = graph
        self.clients = clients


class Clients:
    def __init__(self):
        self.attributes = {}
        self.client_set = {}
    def append_client(self, client):
        client_type = client.client_type
        if client_type not in self.client_set:
            self.client_set[client_type] = {}
        self.client_set[client_type][client.id] = client
        if client_type not in self.attributes:
            self.attributes[client_type] = client.list_attributes()
    def get_client(self, client_id):
        for client_type in self.client_set:
            if client_id in self.client_set[client_type]:
                return self.client_set[client_type][client_id]
    def get_clients(self):
        clients = {}
        for client_type in self.client_set:
            client_set = self.client_set[client_type]
            for client_id in client_set:
                client = client_set[client_id]
                clients[client_id] = client
        return clients
    def list_attributes(self, client_type):
        return self.attributes[client_type]


class Nodes:
    def __init__(self):
        self.attributes = {}
        self.node_set = {}
    def append_node(self, node):
        node_type = node.node_type
        if node_type not in self.node_set:
            self.node_set[node_type] = {}
        self.node_set[node_type][node.id] = node
        if node_type not in self.attributes:
            self.attributes[node_type] = node.list_attributes()
    def get_node(self, node_id):
        for node_type in self.node_set:
            if node_id in self.node_set[node_type]:
                return self.node_set[node_type][node_id]
    def get_nodes(self):
        nodes = {}
        for node_type in self.node_set:
            node_set = self.node_set[node_type]
            for node_id in node_set:
                node = node_set[node_id]
                nodes[node_id] = node
        return nodes
    def list_attributes(self, node_type):
        return self.attributes[node_type]

class Links:
    def __init__(self):
        self.attributes = {}
        self.link_set = {}
    def append_link(self, link):
        link_type = link.link_type
        if link_type not in self.link_set:
            self.link_set[link_type] = {}
        self.link_set[link_type][link.id] = link
        if link_type not in self.attributes:
            self.attributes[link_type] = link.list_attributes()
    def get_link(self, link_id):
        for link_type in self.link_set:
            if link_id in self.link_set[link_type]:
                return self.link_set[link_type][link_id]
    def get_links(self):
        links = {}
        for link_type in self.link_set:
            link_set = self.link_set[link_type]
            for link_id in link_set:
                link = link_set[link_id]
                links[link_id] = link
        return links
    def list_attributes(self, link_type):
        return self.attributes[link_type]


class NodeAbstract(ABC):
    def __init__(self, id, locations):
        self.id = id
        self.locations = locations
        self.neighbours = []

class LinkAbstract(ABC):
    def __init__(self, id, node_pair):
        self.id = id
        self.node_pair = node_pair

class GraphAbstract(ABC):
    def __init__(self, id, nodes, links):
        self.id = id
        self.nodes = nodes
        self.links = links
        self.paths = depthFirstSearch(self.nodes)

class ClientAbstract(ABC):
    def __init__(self, id, schedule, locations):
        self.id = id
        self.schedule = schedule
        self.locations = locations


class Locations:
    def __init__(self, latitude, longitude, height=1):
        self.latitude = latitude
        self.longitude = longitude
        self.height = height


## Timestamp class and functions ##
class timestamp:
    def __init__(self, time_seconds):
        time_remaining = time_seconds
        self.hour = math.floor(time_remaining/ 3600)
        time_remaining -= 3600 * self.hour
        self.minutes = math.floor(time_remaining / 60)
        time_remaining -= 60 * self.minutes
        self.seconds = math.floor(time_remaining)
        self.milliseconds = int((time_remaining % 1)*1000)


    def __str__(self):
        hour_str = str(self.hour)
        if len(hour_str) < 2:
            hour_str = '0' + hour_str

        min_str = str(self.minutes)
        if len(min_str) < 2:
            min_str = '0' + min_str

        sec_str = str(self.seconds)
        if len(sec_str) < 2:
            sec_str = '0' + sec_str
        if self.milliseconds > 0:
            ms_str = str(self.milliseconds)
            if len(ms_str) < 2:
                ms_str = '00' + ms_str
            if len(ms_str) < 3:
                ms_str = '0' + ms_str
            sec_str += '.' + ms_str

        time = hour_str + ':' + min_str + ':' + sec_str
        return time

    @staticmethod
    def time_format(time):
        components = time.split(':')
        hour = int(components[0])
        min = int(components[1])
        if len(components[0]) != 2 or (hour < 0 or hour > 23):
            raise Exception("Not a valid Hour.")
        if len(components[1]) != 2 or (min < 0 or min > 59):
            raise Exception("Not a valid Minute.")
        if len(components) > 2:
            sec = float(components[3])
            if len(components[3].split('.')[0]) != 2 or (sec < 0 or sec >= 60):
                raise Exception('Not a valid Second.')
        return True

    @staticmethod
    def convertTime(seconds):
        hour = math.floor(seconds / 3600)
        hour_str = str(hour)
        if len(hour_str) < 2:
            hour_str = '0' + hour_str
        seconds -= 3600 * hour

        min = math.floor(seconds / 60)
        min_str = str(min)
        seconds -= 60 * min
        if len(min_str) < 2:
            min_str = '0' + min_str

        sec_str = str(seconds)
        if len(sec_str.split('.')[0]) < 2:
            sec_str = '0' + sec_str
        if len(sec_str) > 6:
            sec_str = sec_str[0:6]

        time = hour_str + ':' + min_str + ':' + sec_str
        return time

    @staticmethod
    def convert_to_seconds(timestamp_str):
        seconds = 0
        componenets = timestamp_str.split(':')
        seconds += int(componenets[0])*3600
        if len(componenets) > 1:
            seconds += int(componenets[1])*60
            if len(componenets) > 2:
                seconds += float(componenets[2])
        return seconds

    def timestamp_to_seconds(self):
        time_seconds = self.hour *3600
        time_seconds += self.minutes*60
        time_seconds += self.seconds
        time_seconds += (self.milliseconds)*0.001
        return  time_seconds
