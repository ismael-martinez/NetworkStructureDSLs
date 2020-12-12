# Generate Node_, NodeAttributes, Client_, and ClientAttributes classes

## Read parameters from .trs file

import json
from scipy.stats import expon
import numpy as np
from numpy.random import normal
#from networkStructure import *
from CodeGen.Python.networkStructure import * # TODO remove at the end
from textx import metamodel_from_file
from textx.export import metamodel_export
import os
import sys, getopt



### Utility functions to convert non-explicit schedules into explicit schedules ###

## Convert consistent schedule into explicit shedule
def convert_consistent_schedule(consistentMap):
    start = consistentMap['start']
    end = consistentMap['end']
    gap = consistentMap['gap']

    start_components = start.split(':')
    start_sec = int(start_components[0])*60*60 + int(start_components[1])*60
    if len(start_components) > 2:
        start_sec += int(start_components[3])

    end_components = end.split(':')
    end_sec = int(end_components[0]) * 60 * 60 + int(end_components[1]) * 60
    if len(end_components) > 2:
        end_sec += int(end_components[3])

    gap_components = gap.split(':')
    gap_sec = int(gap_components[0]) * 60 * 60 + int(gap_components[1]) * 60
    if len(gap_components) > 2:
        gap_sec += int(gap_components[3])

    schedule_sec = list(range(start_sec, end_sec, gap_sec))
    schedule_str = [str(timestamp(s)) for s in schedule_sec]
    return [schedule_sec, schedule_str]

## Convert probabilistic schedule into explicit shedule
def convert_probabilistic_schedule(probMap):
    start = probMap['start']
    end = probMap['end']

    start_components = start.split(':')
    start_sec = int(start_components[0])*60*60 + int(start_components[1])*60
    if len(start_components) > 2:
        start_sec += int(start_components[3])

    end_components = end.split(':')
    end_sec = int(end_components[0]) * 60 * 60 + int(end_components[1]) * 60
    if len(end_components) > 2:
        end_sec += int(end_components[3])

    distribution = probMap['interarrivalDistribution']
    if 'Exponential' in distribution:
        exp_lambda_str = probMap['lambda']
        exp_lambda = float(exp_lambda_str)

        schedule_sec = []
        curr_sec = start_sec
        while curr_sec < end_sec:
            schedule_sec.append(curr_sec)
            curr_sec += expon.rvs(scale=(1./exp_lambda))
        schedule_str = [str(timestamp(s)) for s in schedule_sec]
        return [schedule_sec, schedule_str]

    elif 'Gaussian' in distribution:
        mu_str = probMap['mu']
        var_str = probMap['var']
        mu = float(mu_str)
        var = float(var_str)
        schedule_sec = []
        curr_sec = start_sec
        while curr_sec < end_sec:
            schedule_sec.append(curr_sec)
            curr_sec += normal(mu, var)
        schedule_str = [str(timestamp(s)) for s in schedule_sec]
        return [schedule_sec, schedule_str]




### Utility functions for value assignment and verification of attribute by type ###

# For a given type, return the default parameter
# Input: string_type (string) - int, string, float, bool, timestamp
# Output: default_param (string) - form '<attr> = <default_val>'
def default_val_by_type(string_type):
    if 'int' in string_type:
        default_val = 0
    elif 'float' in string_type:
        default_val = 0.0
    elif 'str' in string_type:
        default_val = "''"
    elif 'bool' in string_type:
        default_val = False
    elif 'timestamp' in string_type:
        default_val = 'timestamp(0)'
    else:
        raise Exception('Type {} is not a valid simple type'.format(string_type))
    return default_val

# Generates list of attributes and default parameter instantiations for specified attrbutes of TRS or PNS model.
def attribute_parameters(attributes, attr_type_dict):
    # List of attribute names and types
    default_param_list = []
    for attr in attributes:
        # Register default value based on attribute type
        attr_type = attr_type_dict[attr]
        default_val = default_val_by_type(attr_type)
        default_param = '{} = {}'.format(attr, default_val)
        default_param_list.append(default_param)
    return default_param_list

def attribute_type_valid(attributes, values, types_dict):
    for a in range(len(attributes)):
        attr_name = attributes[a]
        try:
            attr_type = types_dict[attr_name]
        except:
            raise Exception('{} is not a member of available attributes'.format(attr_name))
        attr_val = values[a]
        if attr_type == 'int':
            if 'int' not in str(type(attr_val)):
                raise Exception("Attribute {} must receive a value of type int.".format(attr_name))
        if attr_type == 'float':
            if 'float' not in str(type(attr_val)):
                raise Exception("Attribute {} must receive a value of type float.".format(attr_name))
        elif attr_type == 'string':
            if 'str' not in str(type(attr_val)):
                raise Exception("Attribute {} must receive a value of type str.".format(attr_name))
        elif attr_type == 'bool':
            if 'bool' not in str(type(attr_val)):
                raise Exception("Attribute {} must receive a value of type bool.".format(attr_name))
        elif attr_type == 'timestamp':
            try:
                timestamp.convert_to_seconds(attr_val)
            except:
                raise Exception("Attribute {} must receive a value of type float.".format(attr_name))
    return True


### VERIFY TRS AND PNS FILES BEFORE PARSING
def verify_trs_model(trs_metamodel, trs_file):
    try:
        trs_model = trs_metamodel.model_from_file(trs_file)
        for client_set in trs_model.clientSet:

            # All attributes are unique
            unique_set = list(set(client_set.attributes))
            if len(client_set.attributes) != len(unique_set):
                raise Exception("Clients attributes must be unique: ClientSet {}.".format(client_set.name))
            # The attributes of each client is unique
            for client in client_set.clients:
                client_unqiue_attr = list(set(client.attributes))
                if len(client_unqiue_attr) != len(client.attributes):
                    raise Exception("Client attribubte must be unqiue: Client {}".format(client.name))
            # The value of each client attribute conforms to the attribute type
            attr_type = {}
            for a in range(len(client_set.attributes)):
                attr_type[client_set.attributes[a]] = client_set.type[a]

            for client in client_set.clients:
                # Verify attribute value matches defined attribute type
                attribute_type_valid(client.attributes, client.val, attr_type)
            print('Verification of file {} succeeded.'.format(trs_file))
            return trs_model
    except Exception as e:
        print('Verification Failed: Error in file {}'.format(trs_file))
        print(e)
        exit()


def verify_pns_model(pns_metamodel, pns_file):
    try:
        pns_model = pns_metamodel.model_from_file(pns_file)
        # All attributes are unique
        ## Nodes
        for node_set in pns_model.nodeSets:
            unique_set_node = list(set(node_set.attributes))
            if len(node_set.attributes) != len(unique_set_node):
                raise Exception("NodeSet attributes must be unique: Graph {}.".format(pns_model.name))
            # The attributes of each client is unique
            for node in node_set.nodes:
                node_unqiue_attr = list(set(node_set.attributes))
                if len(node_unqiue_attr) != len(node_set.attributes):
                    raise Exception("Node attribubte must be unqiue: Node {}".format(node.name))
            # The value of each node attribute conforms to the attribute type
            attr_type = {}
            for a in range(len(node_set.attributes)):
                attr_type[node_set.attributes[a]] = node_set.type[a]
            for node in node_set.nodes:
                for a in range(len(node.attributes)):
                    # Verify attribute value matches defined attribute type
                    attribute_type_valid(node.attributes, node.val, attr_type)
            # The service_rate attribute is a valid attribute
            service_rate = node_set.serviceRate
            if service_rate not in attr_type:
                raise Exception('Service rate of NodeSet {} is not a valid attributes'.format(nose_set.name))

        ## Links
        for link_set in pns_model.linkSets:
            unique_set_link = list(set(link_set.attributes))
            if len(link_set.attributes) != len(unique_set_link):
                raise Exception("LinkSet attributes must be unique: Graph {}.".format(pns_model.name))
            # The attributes of each client is unique
            for link in link_set.links:
                link_unqiue_attr = list(set(link_set.attributes))
                if len(link_unqiue_attr) != len(link_set.attributes):
                    raise Exception("Link attribute must be unqiue: Link {}".format(link.name))
            # The value of each link attribute conforms to the attribute type
            attr_type = {}
            for a in range(len(link_set.attributes)):
                attr_type[link_set.attributes[a]] = link_set.type[a]
            for link in link_set.links:
                for a in range(len(link.attributes)):
                    # Verify attribute value matches defined attribute type
                    attribute_type_valid(link.attributes, link.val, attr_type)
            print('Verification of file {} succeeded.'.format(pns_file))
            return pns_model
    except Exception as e:
        print('Verification Failed: Error in file {}'.format(pns_file))
        print(e)
        exit()


### GENERATE CLIENT INSTANCES FROM TRS PARSER ###
# Generate code for Client instances based on TRS file.
def generate_client_instances(trs_model, location_json):
    client_type = trs_model.name

    # Partition clients
    instance_code_gen_client = '###### All Client instances ######\n\n'
    for client_set in trs_model.clientSet:
        instance_code_gen_client += '#### Client_{} instances ##### \n\n'.format(client_set.name)
        instance_code_gen_client += 'clients = Clients()\n\n'
        for client in client_set.clients:
            # Get client ID
            client_name = client.name

            # Parse and convert requestSchedule
            requestSchedule = client.requestSchedule
            schedule_type =requestSchedule._tx_fqn
            if 'ConsistentRequestSchedule' in schedule_type:
                consistentMap = {}
                consistentMap['start'] = requestSchedule.start
                consistentMap['end'] = requestSchedule.end
                consistentMap['gap'] = requestSchedule.gap
                [schedule_sec, schedule_str] = convert_consistent_schedule(consistentMap)

            elif 'ExplicitRequestSchedule' in schedule_type:
                explicitMap = {}
                explicitMap['schedule'] = requestSchedule.schedule
                schedule_str = requestSchedule.schedule[1:-1].split(',')
                schedule_sec = [timestamp.convert_to_seconds(s) for s in schedule_str]
            elif 'ProbabilisticRequestSchedule' in schedule_type:
                distribution = str(requestSchedule.interarrivalDistribution)
                probMap = {}
                probMap['start'] = requestSchedule.start
                probMap['end'] = requestSchedule.end
                probMap['interarrivalDistribution'] = distribution
                if 'Exponential' in distribution:
                    probMap['lambda'] = requestSchedule.interarrivalDistribution.lambda_mean
                elif 'Gaussian' in distribution:
                    probMap['mu'] = requestSchedule.interarrivalDistribution.mu
                    probMap['var'] = requestSchedule.interarrivalDistribution.var
                [schedule_sec, schedule_str] = convert_probabilistic_schedule(probMap)

            else:
                continue

            instance_code_gen_client += '# Instance of Client {}\n'.format(client_name)
            # Build Client attributes
            client_attributes = {}
            for i in range(len(client.attributes)):
                attr = client.attributes[i]
                attr_val = client.val[i]
                client_attributes[attr] = attr_val
            attr_type_dict = {}
            for a in range(len(client_set.attributes)):
                attr= client_set.attributes[a]
                type = client_set.type[a]
                attr_type_dict[attr] = type
            for attr in client_set.attributes:
                if attr not in client_attributes:
                    attr_type = attr_type_dict[attr]
                    default_val = default_val_by_type(attr_type)
                    client_attributes[attr] = default_val

            for attr in client_attributes:
                instance_code_gen_client += '{} = {}\n'.format(attr, client_attributes[attr])

            # Radius
            try:
                if client.radius >= 0:
                    instance_code_gen_client += 'radius = {}\n'.format(client.radius)
                else:
                    instance_code_gen_client += 'radius = np.infty\n'
            except:
                instance_code_gen_client += 'radius = np.infty\n'

            # Build locations
            client_location = {}
            loc_refs = client.location.loc_ref
            for loc_ref in loc_refs:
                ref_str = str(loc_ref)
                location_data = location_json[ref_str]
                client_location[loc_ref] = location_data

            instance_code_gen_client += 'locations = []\n'
            for id in client_location:
                instance_code_gen_client += 'locations.append(Locations({}, {}, {}))\n'.format(client_location[id]['latitude'], client_location[id]['longitude'], client_location[id]['height'])

            # Comment timestamp meaning
            instance_code_gen_client += '# schedule_str = {}\n'.format(schedule_str)
            instance_code_gen_client += 'schedule = ['
            for t in range(len(schedule_sec)-1):
                instance_code_gen_client += 'timestamp({}),'.format(schedule_sec[t])
            instance_code_gen_client += 'timestamp({})]\n'.format(schedule_sec[-1])

            parameters = ['schedule', 'locations', 'radius'] + client_set.attributes
            instance_code_gen_client += 'client = Client_{}("{}", {})\n'.format(client_type, client_name, ', '.join(parameters))
            instance_code_gen_client += 'clients.append_client(client)\n\n'

    return instance_code_gen_client


### GENERATE Graph INSTANCES FROM PNS PARSER ###
# Generate instances of Graph = (Nodes, Links) based on PNS file.
def generate_graph_instances(pns_model, location_json, graph_name):
    instance_code_gen_graph = 'nodes = Nodes()\nlinks=Links()\n'
    graph_name = pns_model.name
    ## Node instances
    instance_code_gen_graph += '###### All Node Instances ###### \n\n'
    for node_set in pns_model.nodeSets:
        instance_code_gen_graph += '### Node_{} Instances ### \n\n'.format(node_set.name)
        for node in node_set.nodes:
            node_name = node.name

            # Build Node attributes
            instance_code_gen_graph += '# Instance of Node {}\n'.format(node_name)
            node_type_dict = {}
            node_attributes = {}
            for i in range(len(node.attributes)):
                attr = node.attributes[i]
                attr_val = node.val[i]
                node_attributes[attr] = attr_val
            for i in range(len(node_set.attributes)):
                attr = node_set.attributes[i]
                type = node_set.type[i]
                node_type_dict[attr] = type
            for attr in node_set.attributes:
                if attr not in node_attributes:
                    attr_type = node_type_dict[attr]
                    default_val = default_val_by_type(attr_type)
                    node_attributes[attr.name] = default_val

            for attr in node_attributes:
                instance_code_gen_graph += '{} = {}\n'.format(attr, node_attributes[attr])

            # Build locations
            node_locations = {}
            loc_refs = node.location.loc_ref
            for loc_ref in loc_refs:
                ref_str = str(loc_ref)
                location_data = location_json[ref_str]
                node_locations[loc_ref] = location_data

            instance_code_gen_graph += 'locations = []\n'
            for attr in node_locations:
                instance_code_gen_graph += 'locations.append(Locations({}, {}, {}))\n'.format(node_locations[attr]['latitude'],
                                                                                                 node_locations[attr]['longitude'],
                                                                                                 node_locations[attr]['height'])
            # Radius
            try:
                if node.radius >= 0:
                    instance_code_gen_graph += 'radius = {}\n'.format(node.radius)
                else:
                    instance_code_gen_graph += 'radius = np.infty\n'
            except:
                instance_code_gen_graph += 'radius = np.infty\n'

            parameters = ['locations', 'radius'] + node_set.attributes
            instance_code_gen_graph += 'node = Node_{}("{}", {})\n'.format(node_set.name, node_name, ', '.join(parameters))
            instance_code_gen_graph += 'nodes.append_node(node)\n\n'

    ## LINK instances

    instance_code_gen_graph += '###### All Link Instances ######\n\n'

    for link_set in pns_model.linkSets:
        instance_code_gen_graph += '### Link_{} Instance ###\n\n'.format(link_set.name)
        for link in link_set.links:
            link_name = link.name

            # Build Link attributes
            instance_code_gen_graph += '# Instance of Link {}\n'.format(link_name)
            link_attributes = {}
            for i in range(len(link.attributes)):
                attr = link.attributes[i]
                attr_val = link.val[i]
                link_attributes[attr] = attr_val
            link_type_dict = {}
            for i in range(len(link_set.attributes)):
                attr = link_set.attributes[i]
                type = link_set.type[i]
                link_type_dict[attr] = type
            for attr in link_set.attributes:
                if attr not in link_attributes:
                    attr_type = link_type_dict[attr]
                    default_val = default_val_by_type(attr_type)
                    link_attributes[attr] = default_val

            for attr in link_attributes:
                instance_code_gen_graph += '{} = {}\n'.format(attr, link_attributes[attr])

            # NodePair
            node_pair = [link.nodePair.nodeSource.name, link.nodePair.nodeTarget.name]
            instance_code_gen_graph += 'node_pair = {}\n'.format(node_pair)
            # Set neighbours of nodes based on link definitions
            instance_code_gen_graph += 'nodes["{}"].neighbours.append(("{}", "{}"))\n'.format(node_pair[0], link_name, node_pair[1])
            # Generate instance of link class
            parameters = ['node_pair'] + link_set.attributes
            instance_code_gen_graph += 'link = Link_{}("{}", {})\n'.format(link_name, link_set.name, link_name, ', '.join(parameters))
            instance_code_gen_graph += 'links.append_link(link)\n\n'


    instance_code_gen_graph += 'graph = Graph_{}("{}", nodes, links)\n'.format(graph_name, graph_name)
    instance_code_gen_graph += 'network_structure = NetworkStructure(graph, clients)'

    return instance_code_gen_graph



## Generate class Client - includes name, and specified attributes (with default parameters)
# Input: trs_model (TextX model, conforms to TRS.tx grammar)
# Output: client_class_gen (string) - Generated code for 'class Client'
def generate_client_class(trs_model):
    # List of attribute names and types
    client_class_gen = '# Client classes\n\n'
    for client_set in trs_model.clientSet:
        attr_name_list = client_set.attributes
        attr_type = {}
        for a in range(len(client_set.attributes)):
            attr_type[client_set.attributes[a]] = client_set.type[a]
        default_param_list = attribute_parameters(attr_name_list, attr_type)

        mandatory_param_list = ['self', 'id', 'schedule', 'locations', 'radius']
        param_list = mandatory_param_list + default_param_list
        # Generate Client class __init__() function with all mandatory and optional parameters.
        # Optional parameters have default value
        client_class_gen += '## class Client_{}\n'.format(client_set.name)
        client_class_gen += 'class Client_{}(ClientAbstract):\n\tdef __init__({}):\n'.format(client_set.name, ', '.join(param_list))

        # Generate body of __init__() function
        param_list = mandatory_param_list + attr_name_list
        for p in param_list:
            if 'self' == p:
                client_class_gen += '\t\tself.client_type = "{}"\n'.format(client_set.name)
                continue
            client_class_gen += '\t\tself.{} = {}\n'.format(p, p)

        ## Generate list_attributes() method which returns a string of attribute names
        attrs_string = ','.join(["'{}'".format(attr) for attr in attr_name_list])
        client_class_gen += '\tdef list_attributes(self):\n\t\treturn [{}]\n'.format(attrs_string)
    return client_class_gen


## Generate class Node - includes name, and specified attributes (with default parameters)
# Input: pns_model (TextX model, conforms to PNS.tx grammar), service_attrs (str)
# Output: pns_class_gen (string) - Generated code for 'class Node'
def generate_node_class(pns_model):
    node_class_gen = '# Link classes for specific attribute set\n'
    for node_set in pns_model.nodeSets:
        node_class_gen += 'class Node_{}(NodeAbstract):\n'.format(node_set.name)
        # List of attribute names and types
        attr_name_list = node_set.attributes
        attr_type = {}
        for a in range(len(node_set.attributes)):
            attr_type[node_set.attributes[a]] = node_set.type[a]
        default_param_list = attribute_parameters(attr_name_list, attr_type)
        mandatory_param_list = ['self', 'id', 'locations', 'radius']
        param_list = mandatory_param_list + default_param_list

        # Generate Node class __init__() function with all mandatory and optional parameters.
        # Optional parameters have default value
        node_class_gen += '\tdef __init__({}):\n'.format(','.join(param_list))
        ## Generate body of __init__() function
        param_list = mandatory_param_list + attr_name_list
        for p in param_list:
            if 'self' == p:
                node_class_gen += '\t\tself.node_type = "{}"\n'.format(node_set.name)
                continue
            node_class_gen += '\t\tself.{} = {}\n'.format(p, p)
        node_class_gen += '\t\tself.neighbours = []\n' # Neighbours are a pair (link, neighbour_node)

        ## Generate service_rate() method. Defines which attribute corresponds to the service rate.
        service_attr = node_set.serviceRate
        node_class_gen += '\tdef service_rate(self):\n'
        if service_attr is not None:
            node_class_gen += '\t\treturn self.attributes.{}\n'.format(service_attr)
        else:
            node_class_gen += '\t\treturn 0\n' # If service_rate not specified, default to 0

        ## Generate list_attributes() method which returns a string of attribute names
        attrs_string = ','.join(["'{}'".format(attr) for attr in attr_name_list])
        node_class_gen += '\tdef list_attributes(self):\n\t\treturn [{}]\n\n'.format(attrs_string)
    return node_class_gen



## Generate class Link - includes name, and specified attributes (with default parameters)
# Input: pns_model (TextX model, conforms to PNS.tx grammar)
# Output: pns_class_gen (string) - Generated code for 'class Link'
def generate_link_class(pns_model):
    link_class_gen = '# Link classes for specific attribute set\n'
    for link_set in pns_model.linkSets:
        link_class_gen += 'class Link_{}(LinkAbstract):\n'.format(link_set.name)
        # List of attribute names and types
        attr_name_list = link_set.attributes
        attr_type = {}
        for a in range(len(link_set.attributes)):
            attr_type[link_set.attributes[a]] = link_set.type[a]
        default_param_list = attribute_parameters(attr_name_list, attr_type)
        mandatory_param_list = ['self', 'id', 'node_pair']
        param_list = mandatory_param_list + default_param_list

        # Generate Link class __init__() function with all mandatory and optional parameters.
        # Optional parameters have default value
        link_class_gen += '\tdef __init__({}):\n'.format(','.join(param_list))
        ## Generate body of __init__() function
        param_list = mandatory_param_list + attr_name_list
        for p in param_list:
            if 'self' == p:
                link_class_gen += '\t\tself.link_type = "{}"\n'.format(link_set.name)
                continue
            link_class_gen += '\t\tself.{} = {}\n'.format(p, p)

        ## Generate list_attributes() method which returns a string of attribute names
        attrs_string = ','.join(["'{}'".format(attr) for attr in attr_name_list])
        link_class_gen += '\tdef list_attributes(self):\n\t\treturn [{}]\n'.format(attrs_string)
    return link_class_gen


def generate_graph_classes(pns_model):
    # Generate Graph class and __init__() method
    graph_class_gen = 'class Graph_{}(GraphAbstract):\n'.format(pns_model.name)
    graph_class_gen += '\tdef __init__(self, id, nodes, links):\n'
    graph_class_gen += '\t\tself.id= id\n'
    graph_class_gen += '\t\tself.nodes = nodes\n\t\tself.links=links\n'
    graph_class_gen += '\t\tself.paths = depthFirstSearch(self.nodes)\n'
    pns_classes = [graph_class_gen]

    # Generate Node class
    pns_classes.append(generate_node_class(pns_model))
    # Generate Link class
    pns_classes.append(generate_link_class(pns_model))
    return '\n'.join(pns_classes)

def code_generation(trs_model, pns_model, trs_location, pns_location):
    attribute_class_gen = []
    # File headers and imports
    attribute_class_gen.append('from networkStructure import *\nimport numpy as np\nfrom networkUtil import * \n')
    attribute_class_gen.append('#from CodeGen.Python.networkStructure import *\n')

    # Generate Client classes
    attribute_class_gen.append(generate_client_class(trs_model=trs_model))
    # Generate Graph, Node and Link classes
    attribute_class_gen.append(generate_graph_classes(pns_model))

    # Generate client instances
    attribute_class_gen.append(generate_client_instances(trs_model, trs_location))
    # Generate node and link instances
    attribute_class_gen.append(generate_graph_instances(pns_model, pns_location, pns_model.name))

    a = open('networkStructureAttributesAndInstances.py', 'w')
    a.write('\n'.join(attribute_class_gen))


def main(argv):
    # Arguments
    trs_file = ''
    pns_file = ''
    trs_location_file = ''
    pns_location_file = ''
    try:
        opts, args = getopt.getopt(argv, "ht:T:p:P:", ["trsfile=", "pnsfile=", "clientlocation=", "nodelocation="])
    except getopt.GetoptError:
        print('codeGen.py -t <trsfilepath> -T <clientlocationJSON> -p <pnsfilepath> -P <nodelocationJSON>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('codeGen.py -t <trsfilepath> -T <clientlocationJSON> -p <pnsfilepath> -P <nodelocationJSON>')
            sys.exit()
        elif opt in ("-t", "--trsfile"):
            trs_file = arg
        elif opt in ("-p", "--pnsfile"):
            pns_file = arg
        elif opt in ("-T", "--clientlocation"):
            trs_location_file = arg
        elif opt in ("-P", "--nodelocation"):
            pns_location_file = arg


    ### Verify TRS File
    print("TRS file:" + trs_file)
    trs_grammar = 'TRS/trs.tx'
    mm_trs = metamodel_from_file(trs_grammar) # TextX Metamodel
    metamodel_export(mm_trs, 'TRS/trs.dot')
    os.system('dot -Tpng -O  TRS/trs.dot')
    trs_model = verify_trs_model(mm_trs, trs_file)
    with open(trs_location_file) as loc:
        loc_data_trs = json.load(loc)


    ### Verify PNS file
    pns_grammar = 'PNS/pns.tx'
    mm_pns = metamodel_from_file(pns_grammar) # TextX Metamodel
    metamodel_export(mm_pns, 'PNS/pns.dot')
    os.system('dot -Tpng -O  PNS/pns.dot')
    pns_model = verify_pns_model(mm_pns, pns_file)
    with open(pns_location_file) as loc:
        loc_data_pns = json.load(loc)

    code_generation(trs_model, pns_model, loc_data_trs['location'], loc_data_pns['location'])


if __name__=="__main__":
    main(sys.argv[1:])
