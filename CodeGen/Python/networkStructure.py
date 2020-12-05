from abc import ABC, abstractmethod
import math

def depthFirstSearch(nodes):
    all_paths = []
    node_visited_map = {}
    for node in nodes:
        node_visited_map[node] = False

    node_visited = [node_visited_map[key] for key in node_visited_map]
    for node in nodes:
        if all(node_visited):
            break
        [node_visited_map, _, all_paths] = depthFirstSearch_rec(nodes, node, node_visited_map, all_paths)
        node_visited = [node_visited_map[key] for key in node_visited_map]
    return all_paths

def depthFirstSearch_rec(nodes, root, node_visited_map, all_paths):
    root_paths = []
    if node_visited_map[root]:
        return [node_visited_map, []]
    node_visited_map[root] = True
    node = root
    root_paths.append([root])
    for nb in nodes[node].neighbours:
        [node_visited_map, paths, all_paths] = depthFirstSearch_rec(nodes, nb[1], node_visited_map, all_paths)
        for p in paths:
            root_paths.append([root] + p)
    for p in root_paths:
        all_paths.append(p)
    return [node_visited_map, root_paths, all_paths]


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

class NetworkStructure:
    def __init__(self, graph, things):
        self.graph = graph
        self.things = things


    def listNodeAttributes(self):
        for node in self.graph.nodes:
            attr = self.graph.nodes[node].attributes.listAttributes()
            break
        return attr

    def listLinkAttributes(self):
        for link in self.graph.links:
            attr = self.graph.links[link].attributes.listAttributes()
            break
        return attr

    def listThingAttributes(self):
        for thing in self.things:
            attr = self.things[thing].attributes.listAttributes()
            break
        return attr




class NodeAbstract(ABC):
    def __init__(self, id, locations, attributes):
        self.id = id
        self.locations = locations
        self.attributes = attributes
        self.neighbours = []

class LinkAbstract(ABC):
    def __init__(self, id, attributes, node_pair):
        self.id = id
        self.attributes = attributes
        self.node_pair = node_pair

class GraphAbstract(ABC):
    def __init__(self, id, nodes, links):
        self.id = id
        self.nodes = nodes
        self.links = links
        self.paths = depthFirstSearch(self.nodes)

class ThingAbstract(ABC):
    def __init__(self, id, schedule, locations, attributes):
        self.id = id
        self.schedule = schedule
        self.locations = locations
        self.attributes = attributes

class Locations:
    def __init__(self, latitude, longitude, height=1):
        self.latitude = latitude
        self.longitude = longitude
        self.height = height

