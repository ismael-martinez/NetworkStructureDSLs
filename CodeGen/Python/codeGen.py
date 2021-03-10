# Generate Node_, NodeAttributes, Client_, and ClientAttributes classes

## Read parameters from .nrs file

import json
from scipy.stats import expon, gamma, chi2, dirichlet, bernoulli, norm
from scipy.stats import beta as beta_dist
import numpy as np
from networkStructure import *
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
            curr_sec += norm.rvs(loc=mu, scale=np.sqrt(var))
        schedule_str = [str(timestamp(s)) for s in schedule_sec]
        return [schedule_sec, schedule_str]
    elif 'Gamma' in distribution:
        alpha_str = probMap['alpha']
        beta_str = probMap['beta']
        alpha = float(alpha_str)
        beta = float(beta_str)
        schedule_sec = []
        curr_sec = start_sec
        while curr_sec < end_sec:
            schedule_sec.append(curr_sec)
            curr_sec += gamma.rvs(alpha, scale=(1./beta))
        schedule_str = [str(timestamp(s)) for s in schedule_sec]
        return [schedule_sec, schedule_str]
    elif 'Chi-Square' in distribution:
        df_str = probMap['df']
        df = float(df_str)
        schedule_sec = []
        curr_sec = start_sec
        while curr_sec < end_sec:
            schedule_sec.append(curr_sec)
            curr_sec += chi2.rvs(df)
        schedule_str = [str(timestamp(s)) for s in schedule_sec]
        return [schedule_sec, schedule_str]
    elif 'Beta' in distribution:
        alpha_str = probMap['alpha']
        beta_str = probMap['beta']
        alpha = float(alpha_str)
        beta = float(beta_str)
        schedule_sec = []
        curr_sec = start_sec
        while curr_sec < end_sec:
            schedule_sec.append(curr_sec)
            curr_sec += beta_dist.rvs(alpha, beta)
        schedule_str = [str(timestamp(s)) for s in schedule_sec]
        return [schedule_sec, schedule_str]
    elif 'Dirichlet' in distribution:
        alpha_str = probMap['alpha']
        alpha = float(alpha_str)
        schedule_sec = []
        curr_sec = start_sec
        while curr_sec < end_sec:
            schedule_sec.append(curr_sec)
            curr_sec += dirichlet.rvs(alpha)
        schedule_str = [str(timestamp(s)) for s in schedule_sec]
        return [schedule_sec, schedule_str]
    elif 'Bernoulli' in distribution:
        p_str = probMap['p']
        p = float(p_str)
        schedule_sec = []
        curr_sec = start_sec
        while curr_sec < end_sec:
            schedule_sec.append(curr_sec)
            curr_sec += bernoulli.rvs(p)
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

# Generates list of attributes and default parameter instantiations for specified attrbutes of NRS or PNS model.
def attribute_parameters(attributes, attr_type_dict, radius_attr):
    # List of attribute names and types
    default_param_list = []
    for attr in attributes:
        if attr == radius_attr:
            default_val = 'np.infty'
        else:
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
            if not any([numerical not in str(type(attr_val)) for numerical in ['int', 'float']]):
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


### VERIFY NRS AND PNS FILES BEFORE PARSING
def verify_nrs_model(nrs_metamodel, nrs_file):
    try:
        nrs_model = nrs_metamodel.model_from_file(nrs_file)
        for client_set in nrs_model.clientSet:

            # All attributes are unique
            unique_set = list(set(client_set.attributes))
            if len(client_set.attributes) != len(unique_set):
                raise Exception("Clients attributes must be unique: ClientType {}.".format(client_set.name))
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
            print('Verification of file {} succeeded.'.format(nrs_file))
            # The radius attribute is a valid attribute
            radius = client_set.radius
            if radius and radius not in attr_type:
                raise Exception('Radius of ClientType {} is not a valid attributes'.format(client_set.name))
            # The radius attribute is non-negative for all clients
            for client in client_set.clients:
                for a in range(len(client.attributes)):
                    if client.attributes[a] == radius:
                        if client.val[a] < 0:
                            raise Exception('Radius of client {} must be non-negative'.format(client.name))
                        break

            return nrs_model
    except Exception as e:
        print('Verification Failed: Error in file {}'.format(nrs_file))
        print(e)
        exit()


def verify_pns_model(pns_metamodel, pns_file):
    try:
        pns_model = pns_metamodel.model_from_file(pns_file)
        # All attributes are unique
        ## Nodes
        for node_set in pns_model.nodeSet:
            unique_set_node = list(set(node_set.attributes))
            if len(node_set.attributes) != len(unique_set_node):
                raise Exception("NodeType attributes must be unique: Graph {}.".format(pns_model.name))
            # The attributes of each client is unique
            for node in node_set.nodes:
                node_unqiue_attr = list(set(node_set.attributes))
                if len(node_unqiue_attr) != len(node_set.attributes):
                    raise Exception("Node attribubte must be unqiue: Node {}".format(node.name))
            # The value of each node attribute conforms to the attribute type
            attr_type = {}
            for a in range(len(node_set.attributes)):
                attr_type[node_set.attributes[a]] = node_set.attributes[a].type
            for node in node_set.nodes:
                for a in range(len(node.attributes)):
                    # Verify attribute value matches defined attribute type
                    attribute_type_valid(node.attributes, node.val, attr_type)
            # The service_rate attribute is a valid attribute
            service_rate = node_set.serviceRate
            if service_rate and service_rate not in attr_type:
                raise Exception('Service rate of NodeType {} is not a valid attributes'.format(node_set.name))
            # The radius attribute is a valid attribute
            radius = node_set.radius
            if radius and radius not in attr_type:
                raise Exception('Radius of NodeType {} is not a valid attributes'.format(node_set.name))
            # The radius attribute is non-negative for all clients
            for node in node_set.nodes:
                for a in range(len(node.attributes)):
                    if node.attributes[a] == radius:
                        if node.val[a] < 0:
                            raise Exception('Radius of node {} must be non-negative'.format(node.name))
        ## Links
        for link_set in pns_model.linkSet:
            unique_set_link = list(set(link_set.attributes))
            if len(link_set.attributes) != len(unique_set_link):
                raise Exception("LinkType attributes must be unique: Graph {}.".format(pns_model.name))
            # The attributes of each client is unique
            for link in link_set.links:
                link_unqiue_attr = list(set(link_set.attributes))
                if len(link_unqiue_attr) != len(link_set.attributes):
                    raise Exception("Link attribute must be unique: Link {}".format(link.name))
            # The value of each link attribute conforms to the attribute type
            attr_type = {}
            for a in range(len(link_set.attributes)):
                attr_type[link_set.attributes[a]] = link_set.attributes[a].type
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


### GENERATE CLIENT INSTANCES FROM NRS PARSER ###
# Generate code for Client instances based on NRS file.
def generate_client_instances(nrs_model):
    client_type = nrs_model.name

    # Partition clients
    instance_code_gen_client = '###### All Client instances ######\n\n'
    for client_set in nrs_model.clientSet:
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
                    if attr == client_set.radius:
                        default_val = 'np.infty'
                    else:
                        attr_type = attr_type_dict[attr]
                        default_val = default_val_by_type(attr_type)
                    client_attributes[attr] = default_val

            for attr in client_attributes:
                instance_code_gen_client += '{} = {}\n'.format(attr, client_attributes[attr])

            # Build locations
            client_location = {"height": client.location.ht, "latitude": client.location.lat, "longitude": client.location.lng}

            instance_code_gen_client += 'locations = []\n'
            instance_code_gen_client += 'locations.append(Locations({}, {}, {}))\n'.format(client_location['latitude'], client_location['longitude'], client_location['height'])

            # Comment timestamp meaning
            instance_code_gen_client += '# schedule_str = {}\n'.format(schedule_str)
            instance_code_gen_client += 'schedule = ['
            for t in range(len(schedule_sec)-1):
                instance_code_gen_client += 'timestamp({}),'.format(schedule_sec[t])
            instance_code_gen_client += 'timestamp({})]\n'.format(schedule_sec[-1])

            parameters = ['schedule', 'locations'] + client_set.attributes
            instance_code_gen_client += 'client = Client_{}("{}", {})\n'.format(client_type, client_name, ', '.join(parameters))
            instance_code_gen_client += 'clients.append_client(client)\n\n'

    return instance_code_gen_client


### GENERATE Graph INSTANCES FROM PNS PARSER ###
# Generate instances of Graph = (Nodes, Links) based on PNS file.
def generate_graph_instances(pns_model, graph_name):
    instance_code_gen_graph = 'nodes = Nodes()\nlinks=Links()\n'
    graph_name = pns_model.name
    ## Node instances
    instance_code_gen_graph += '###### All Node Instances ###### \n\n'
    for node_set in pns_model.nodeSet:
        instance_code_gen_graph += '### Node_{} Instances ### \n\n'.format(node_set.name)
        for node in node_set.nodes:
            node_name = node.name

            # Build Node attributes
            instance_code_gen_graph += '# Instance of Node {}\n'.format(node_name)
            node_type_dict = {}
            node_attributes = {}
            node_attr_keys = [a.name for a in node.attributes]
            for i in range(len(node.attributes)):
                attr = node.attributes[i].name
                attr_val = node.val[i]
                node_attributes[attr] = attr_val
            for i in range(len(node_set.attributes)):
                attr = node_set.attributes[i].name
                type = node_set.attributes[i].type
                node_type_dict[attr] = type
            for attr in node_attr_keys:
                if attr not in node_attributes:
                    if attr == node_set.radius.name:
                        default_val = 'np.infty'
                    else:
                        attr_type = node_type_dict[attr]
                        default_val = default_val_by_type(attr_type)
                    node_attributes[attr.name] = default_val

            for attr in node_attributes:
                instance_code_gen_graph += '{} = {}\n'.format(attr, node_attributes[attr])

            # Build locations
            node_location = {"height": node.location.ht, "latitude": node.location.lat,
                               "longitude": node.location.lng}

            instance_code_gen_graph += 'locations = []\n'
            instance_code_gen_graph += 'locations.append(Locations({}, {}, {}))\n'.format(node_location['latitude'],
                                                                                          node_location['longitude'],
                                                                                              node_location['height'])

            parameters = ['locations'] + node_attr_keys
            instance_code_gen_graph += 'node = Node_{}("{}", {})\n'.format(node_set.name, node_name, ', '.join(parameters))
            instance_code_gen_graph += 'nodes.append_node(node)\n\n'

    ## LINK instances

    instance_code_gen_graph += '###### All Link Instances ######\n\n'

    for link_set in pns_model.linkSet:
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
            link_attr_keys = [a.name for a in link_set.attributes]
            for i in range(len(link_attr_keys)):
                attr = link_set.attributes[i].name
                type = link_set.attributes[i].type
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
            instance_code_gen_graph += 'nodes.get_node("{}").neighbours.append(("{}", "{}"))\n'.format(node_pair[0], link_name, node_pair[1])
            # Generate instance of link class
            parameters = ['node_pair'] + link_attr_keys
            instance_code_gen_graph += 'link = Link_{}("{}", {})\n'.format(link_set.name, link_name, ', '.join(parameters))
            instance_code_gen_graph += 'links.append_link(link)\n\n'


    instance_code_gen_graph += 'graph = Graph_{}("{}", nodes, links)\n'.format(graph_name, graph_name)
    instance_code_gen_graph += 'network_structure = NetworkStructure(graph, clients)'

    return instance_code_gen_graph



## Generate class Client - includes name, and specified attributes (with default parameters)
# Input: nrs_model (TextX model, conforms to NRS.tx grammar)
# Output: client_class_gen (string) - Generated code for 'class Client'
def generate_client_class(nrs_model):
    # List of attribute names and types
    client_class_gen = '# Client classes\n\n'
    for client_set in nrs_model.clientSet:
        attr_name_list = client_set.attributes
        attr_type = {}
        for a in range(len(client_set.attributes)):
            attr_type[client_set.attributes[a]] = client_set.type[a]
        default_param_list = attribute_parameters(attr_name_list, attr_type, client_set.radius)

        mandatory_param_list = ['self', 'id', 'schedule', 'locations']
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

        ## Generate radius() method. Defines which attribute corresponds to the service rate.
        radius_attr = client_set.radius
        client_class_gen += '# Defines the attribute that represents the radius (in metres), if any.\n'
        client_class_gen += '\tdef get_radius(self):\n'
        if radius_attr is not None:
            client_class_gen += '\n# The {} attribute represents the radius.\n'.format(radius_attr)
            client_class_gen += '\t\treturn self.{}\n'.format(radius_attr)
        else:
            client_class_gen += '# No attribute defines the radius.\n'
            client_class_gen += '\t\treturn np.infty\n'  # If service_rate not specified, default to 0

        ## Generate list_attributes() method which returns a string of attribute names
        atnrs_string = ','.join(["'{}'".format(attr) for attr in attr_name_list])
        client_class_gen += '\n# List the available attributes\n'
        client_class_gen += '\tdef list_attributes(self):\n\t\treturn [{}]\n'.format(atnrs_string)
    return client_class_gen


## Generate class Node - includes name, and specified attributes (with default parameters)
# Input: pns_model (TextX model, conforms to PNS.tx grammar), service_atnrs (str)
# Output: pns_class_gen (string) - Generated code for 'class Node'
def generate_node_class(pns_model):
    node_class_gen = '# Link classes for specific attribute set\n'
    for node_set in pns_model.nodeSet:
        node_class_gen += 'class Node_{}(NodeAbstract):\n'.format(node_set.name)
        # List of attribute names and types
        attr_name_list = node_set.attributes
        attr_type = {}
        for a in range(len(node_set.attributes)):
            attr_type[node_set.attributes[a]] = node_set.attributes[a].type
        default_param_list = attribute_parameters(attr_name_list, attr_type, node_set.radius)
        mandatory_param_list = ['self', 'id', 'locations']
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
        node_class_gen += '\n# Defines the attribute that represents the service rate, if any.\n'
        node_class_gen += '\tdef get_service_rate(self):\n'
        if service_attr is not None:
            node_class_gen += '# The {} attribute represents the service rate.\n'.format(service_attr)
            node_class_gen += '\t\treturn self.{}\n'.format(service_attr)
        else:
            node_class_gen += '# No attribute defines the service rate.\n'
            node_class_gen += '\t\treturn 0\n' # If service_rate not specified, default to 0

        ## Generate radius() method. Defines which attribute corresponds to the service rate.
        radius_attr = node_set.radius
        node_class_gen += '# Defines the attribute that represents the radius (in metres), if any.\n'
        node_class_gen += '\tdef get_radius(self):\n'
        if radius_attr:
            node_class_gen += '# The {} attribute represents the radius.\n'.format(radius_attr)
            node_class_gen += '\t\treturn self.{}\n'.format(radius_attr)
        else:
            node_class_gen += '\n# No attribute defines the radius.\n'
            node_class_gen += '\t\treturn np.infty\n'  # If service_rate not specified, default to 0

        ## Generate list_attributes() method which returns a string of attribute names
        atnrs_string = ','.join(["'{}'".format(attr) for attr in attr_name_list])
        node_class_gen += '\n# List the available attributes\n'
        node_class_gen += '\tdef list_attributes(self):\n\t\treturn [{}]\n\n'.format(atnrs_string)
    return node_class_gen



## Generate class Link - includes name, and specified attributes (with default parameters)
# Input: pns_model (TextX model, conforms to PNS.tx grammar)
# Output: pns_class_gen (string) - Generated code for 'class Link'
def generate_link_class(pns_model):
    link_class_gen = '# Link classes for specific attribute set\n'
    for link_set in pns_model.linkSet:
        link_class_gen += 'class Link_{}(LinkAbstract):\n'.format(link_set.name)
        # List of attribute names and types
        attr_name_list = link_set.attributes
        attr_type = {}
        for a in range(len(link_set.attributes)):
            attr_type[link_set.attributes[a]] = link_set.attributes[a].type
        default_param_list = attribute_parameters(attr_name_list, attr_type, '')
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
        atnrs_string = ','.join(["'{}'".format(attr) for attr in attr_name_list])
        link_class_gen += '\n# List the available attributes\n'
        link_class_gen += '\tdef list_attributes(self):\n\t\treturn [{}]\n'.format(atnrs_string)
    return link_class_gen


def generate_graph_classes(pns_model):
    # Generate Graph class and __init__() method
    graph_class_gen = 'class Graph_{}(GraphAbstract):\n'.format(pns_model.name)
    graph_class_gen += '\tdef __init__(self, id, nodes, links):\n'
    graph_class_gen += '\t\tself.id= id\n'
    graph_class_gen += '\t\tself.nodes = nodes\n\t\tself.links=links\n'
    graph_class_gen += '\t\tself.paths = depthFirstSearch(self.nodes.get_nodes())\n'
    pns_classes = [graph_class_gen]

    # Generate Node class
    pns_classes.append(generate_node_class(pns_model))
    # Generate Link class
    pns_classes.append(generate_link_class(pns_model))
    return '\n'.join(pns_classes)

def code_generation(nrs_model, pns_model):
    attribute_class_gen = []
    # File headers and imports
    attribute_class_gen.append('from networkStructure import *\nimport numpy as np\nfrom networkUtil import * \n')
    #attribute_class_gen.append('#from CodeGen.Python.networkStructure import *\n')

    # Generate Client classes
    attribute_class_gen.append(generate_client_class(nrs_model=nrs_model))
    # Generate Graph, Node and Link classes
    attribute_class_gen.append(generate_graph_classes(pns_model))

    # Generate client instances
    attribute_class_gen.append(generate_client_instances(nrs_model))
    # Generate node and link instances
    attribute_class_gen.append(generate_graph_instances(pns_model, pns_model.name))

    code_gen_output = 'networkStructureAttributesAndInstances.py'
    a = open(code_gen_output, 'w')
    a.write('\n'.join(attribute_class_gen))
    print('\nCode generate in {}'.format(code_gen_output))

def main(argv):
    # Arguments
    nrs_file = ''
    pns_file = ''
    try:
        opts, args = getopt.getopt(argv, "hr:p:", ["nrsfile=", "pnsfile="])
    except getopt.GetoptError:
        print('codeGen.py -r <nrsfilepath> -p <pnsfilepath>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('codeGen.py -r <nrsfilepath> -p <pnsfilepath>')
            sys.exit()
        elif opt in ("-r", "--nrsfile"):
            nrs_file = arg
        elif opt in ("-p", "--pnsfile"):
            pns_file = arg


    ### Verify NRS File
    print("NRS file:" + nrs_file)
    nrs_grammar = 'TRS/trs.tx'
    mm_nrs = metamodel_from_file(nrs_grammar) # TextX Metamodel
    metamodel_export(mm_nrs, 'TRS/trs.dot')
    os.system('dot -Tpng -O  TRS/trs.dot')
    nrs_model = verify_nrs_model(mm_nrs, nrs_file)

    ### Verify PNS file
    pns_grammar = 'ENS/ens.tx'
    mm_pns = metamodel_from_file(pns_grammar) # TextX Metamodel
    metamodel_export(mm_pns, 'ENS/pns.dot')
    os.system('dot -Tpng -O  ENS/pns.dot')
    pns_model = verify_pns_model(mm_pns, pns_file)

    code_generation(nrs_model, pns_model)


if __name__=="__main__":
    main(sys.argv[1:])
