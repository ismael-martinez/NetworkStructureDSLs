# Generate Node_, NodeAttributes, Thing_, and ThingAttributes classes

## Read parameters from .trs file

import json
from scipy.stats import expon
import numpy as np
from numpy.random import normal
from networkStructure import *

from textx import metamodel_from_file
from textx.export import metamodel_export
import os
import sys, getopt



# Schedules

def consistentSchedule(consistentMap):
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

def probabilisticSchedule(probMap):
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


# TRS Parser

def trs_parser(trs_model, location_json):
    thing_type = trs_model.name

    # Partition things

    instance_code_gen_thing = '## Thing instances ## \n\nthings = {}\n\n'
    for thing in trs_model.things:
        # Get thing ID
        thing_name = thing.name


        # Parse requestSchedule
        requestSchedule = thing.requestSchedule
        schedule_type =requestSchedule._tx_fqn
        if 'ConsistentRequestSchedule' in schedule_type:
            consistentMap = {}
            consistentMap['start'] = requestSchedule.start
            consistentMap['end'] = requestSchedule.end
            consistentMap['gap'] = requestSchedule.gap
            [schedule_sec, schedule_str] = consistentSchedule(consistentMap)

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
            [schedule_sec, schedule_str] = probabilisticSchedule(probMap)

        else:
            continue

        # Build Thing attributes
        thing_attributes = {}
        for i in range(len(thing.attributes)):
            attr = thing.attributes[i]
            attr_val = thing.val[i]
            thing_attributes[attr.name] = attr_val

        # Radius
        try:
            if thing.radius >= 0:
                instance_code_gen_thing += 'radius = {}\n'.format(thing.radius)
            else:
                instance_code_gen_thing += 'radius = np.infty\n'
        except:
            instance_code_gen_thing += 'radius = np.infty\n'

        # Build locations
        thing_location = {}
        loc_refs = thing.location.loc_ref
        for loc_ref in loc_refs:
            ref_str = str(loc_ref)
            location_data = location_json[ref_str]
            thing_location[loc_ref] = location_data

        instance_code_gen_thing += 'locations = []\n'
        for id in thing_location:
            instance_code_gen_thing += 'locations.append(Locations({}, {}, {}))\n'.format(thing_location[id]['latitude'], thing_location[id]['longitude'], thing_location[id]['height'])
        configurations_values = []
        for id in thing_attributes:
            configurations_values.append(str(thing_attributes[id]))
        instance_code_gen_thing += 'attributes = ThingAttributes_{}({})\n'.format(thing_type, ','.join(configurations_values))
        # Comment timestamp meaning
        instance_code_gen_thing += '# schedule_str = {}\n'.format(schedule_str)
        instance_code_gen_thing += 'schedule = ['
        for t in range(len(schedule_sec)-1):
            instance_code_gen_thing += 'timestamp({}),'.format(schedule_sec[t])
        instance_code_gen_thing += 'timestamp({})]\n'.format(schedule_sec[-1])
        instance_code_gen_thing += 'things["{}"] = Thing_{}("{}", schedule, locations, radius, attributes)\n\n'.format(thing_name, thing_type, thing_name)

    return instance_code_gen_thing


        #thing_elem = Thing(thing_idx, schedule, locations, configurations)
        #things_elems.append(thing_elem)

## Read parameters from .NSM file

def pns_parser(pns_model, location_json, graph_name):
    instance_code_gen_graph = 'nodes = {}\nlinks={}\n'

    ## Node instances
    instance_code_gen_graph += '## Node Instances \n\n'
    node_set = pns_model.nodeSet.nodes
    for node in node_set:
        node_name = node.name
        # Build Node attributes
        node_attributes = {}
        for i in range(len(node.attributes)):
            attr = node.attributes[i]
            attr_val = node.val[i]
            node_attributes[attr.name] = attr_val

        # Build locations
        node_locations = {}
        loc_refs = node.location.loc_ref
        for loc_ref in loc_refs:
            ref_str = str(loc_ref)
            location_data = location_json[ref_str]
            node_locations[loc_ref] = location_data

        instance_code_gen_graph += 'locations = []\n'
        for id in node_locations:
            instance_code_gen_graph += 'locations.append(Locations({}, {}, {}))\n'.format(node_locations[id]['latitude'],
                                                                                             node_locations[id]['longitude'],
                                                                                             node_locations[id]['height'])
        # Radius
        try:
            if node.radius >= 0:
                instance_code_gen_graph += 'radius = {}\n'.format(node.radius)
            else:
                instance_code_gen_graph += 'radius = np.infty\n'
        except:
            instance_code_gen_graph += 'radius = np.infty\n'

        attributes_values = []
        for id in node_attributes:
            attributes_values.append(str(node_attributes[id]))
        instance_code_gen_graph += 'attributes = NodeAttributes_{}({})\n'.format(graph_name,','.join(attributes_values))
        instance_code_gen_graph += 'nodes["{}"] = Node_{}("{}", locations, attributes, radius)\n\n'.format(node_name, graph_name, node_name)

    ## LINK instances

    instance_code_gen_graph += '## Link Instances\n\n'
    link_set = pns_model.linkSet.links
    for link in link_set:
        link_name = link.name
        # Build Link attributes
        link_attributes = {}
        for i in range(len(link.attributes)):
            attr = link.attributes[i]
            attr_val = link.val[i]
            link_attributes[attr.name] = attr_val

        # NodePair
        node_pair = [link.nodePair.nodeSource.name, link.nodePair.nodeTarget.name]


        attributes_values = []
        for id in link_attributes:
            attributes_values.append(str(link_attributes[id]))
        instance_code_gen_graph += 'node_pair = {}\n'.format(node_pair)
        instance_code_gen_graph += 'nodes["{}"].neighbours.append(("{}", "{}"))\n'.format(node_pair[0], link_name, node_pair[1])
        instance_code_gen_graph += 'attributes = LinkAttributes_{}({})\n'.format(graph_name,','.join(attributes_values))
        instance_code_gen_graph += 'links["{}"] = Link_{}("{}", node_pair, attributes)\n\n'.format(link_name, graph_name, link_name)


    instance_code_gen_graph += 'graph = Graph_{}("{}", nodes, links)\n'.format(graph_name, graph_name)
    instance_code_gen_graph += 'network_structure = NetworkStructure(graph, things)'

    return instance_code_gen_graph


## Generate Things

def generateThingClass(name, attributes):
    class_gen = 'class Thing_{}(ThingAbstract):\n\tdef __init__(self, id, schedule, locations, radius'.format(name)
    if len(attributes) > 0:
        class_gen += ',attributes):\n'
    else:
        class_gen += '):\n'
    class_gen += '\t\tself.id = id\n'
    class_gen += '\t\tself.schedule = schedule\n'
    class_gen += '\t\tself.locations = locations\n'
    class_gen += '\t\tself.radius = radius\n'
    if len(attributes) > 0:
        class_gen += '\t\tself.attributes = attributes\n'
    return class_gen

def generateThingAttributes(name, attributes):
    param_list = ', '.join(attributes)
    thing_attributes_class = 'class ThingAttributes_{}:\n\tdef __init__(self'.format(name)
    if len(param_list) > 0:
        thing_attributes_class += ', ' + param_list + '):\n'
    else:
        thing_attributes_class += '):\n'
    for attr in attributes:
        thing_attributes_class += '\t\tself.{} = {}\n'.format(attr, attr)

    attribute_list = ['"' + attr + '"' for attr in attributes]
    thing_attributes_class += '\tdef listAttributes(self):\n\t\treturn [{}]\n'.format(','.join(attribute_list))
    return thing_attributes_class

def generateThingClasses(trs_model):
    thing_name = trs_model.name
    attributes = []
    for attr in trs_model.attributes:
        attributes.append(attr.name)

    thing_class_gen = generateThingClass(thing_name, attributes)
    thing_attributes_class = generateThingAttributes(thing_name, attributes)
    thing_classes = thing_attributes_class + '\n' + thing_class_gen
    return thing_classes

## Generate Graph

def generateGraphClass(name):
    graph_class = 'class Graph_{}(GraphAbstract):\n'.format(name)
    graph_class += '\tdef __init__(self, id, nodes, links):\n'
    graph_class += '\t\tself.id= id\n'
    graph_class += '\t\tself.nodes = nodes\n\t\tself.links=links\n'
    graph_class += '\t\tself.paths = depthFirstSearch(self.nodes)\n'
    return graph_class

def generateNodeClass(name, service_attr):
    node_class = 'class Node_{}(NodeAbstract):\n'.format(name)
    node_class += '\tdef __init__(self, id, locations, attributes, radius):\n'
    node_class += '\t\tself.id = id\n'
    node_class += '\t\tself.locations=locations\n'
    node_class += '\t\tself.attributes = attributes\n'
    node_class += '\t\tself.radius = radius\n'
    node_class += '\t\tself.neighbours = []\n\n'
    node_class += '\tdef service_rate(self):\n'
    if service_attr is not None:
        node_class += '\t\treturn self.attributes.{}\n'.format(service_attr.name)
    else:
        node_class += '\t\treturn 0'
    return node_class

def generateLinkClass(name):
    link_class = 'class Link_{}(LinkAbstract):\n'.format(name)
    link_class += '\tdef __init__(self, id, node_pair, attributes):\n'
    link_class += '\t\tself.id = id\n'
    link_class += '\t\tself.node_pair=node_pair\n'
    link_class += '\t\tself.attributes=attributes\n'
    return link_class

def generateNodeAttributes(name, node_set):
    attributes = []
    for attr in node_set.attributes:
        attributes.append(attr.name)

    param_list = ', '.join(attributes)
    nodeAttributesClass = 'class NodeAttributes_{}:\n\tdef __init__(self'.format(name)
    if len(param_list) > 0:
        nodeAttributesClass += ', ' + param_list + '):\n'
    else:
        nodeAttributesClass += '):\n'
    for attr in attributes:
        nodeAttributesClass += '\t\tself.{} = {}\n'.format(attr, attr)
    attribute_list = ['"' + attr + '"' for attr in attributes]
    nodeAttributesClass += '\tdef listAttributes(self):\n\t\treturn [{}]\n'.format(','.join(attribute_list))
    return nodeAttributesClass

def generateLinkAttributes(name, link_set):
    attributes = []
    for attr in link_set.attributes:
        attributes.append(attr.name)

    param_list = ', '.join(attributes)
    linkAttributesClass = 'class LinkAttributes_{}:\n\tdef __init__(self'.format(name)
    if len(param_list) > 0:
        linkAttributesClass += ', ' + param_list + '):\n'
    else:
        linkAttributesClass += '):\n'
    for attr in attributes:
        linkAttributesClass += '\t\tself.{} = {}\n'.format(attr, attr)
    attribute_list = ['"' + attr + '"' for attr in attributes]
    linkAttributesClass += '\tdef listAttributes(self):\n\t\treturn [{}]\n'.format(','.join(attribute_list))
    return linkAttributesClass

def generateGraphClasses(pns_model):
    graph_name = pns_model.name
    node_set = pns_model.nodeSet
    link_set = pns_model.linkSet

    graph_class_gen = []
    graph_class_gen.append(generateGraphClass(graph_name))
    graph_class_gen.append(generateNodeClass(graph_name, pns_model.nodeSet.serviceRate))
    graph_class_gen.append(generateLinkClass(graph_name))
    graph_class_gen.append(generateNodeAttributes(graph_name, node_set))
    graph_class_gen.append(generateLinkAttributes(graph_name, link_set))
    return ['\n'.join(graph_class_gen), graph_name]

def code_gen(trs_model, pns_model, trs_location, nsm_location):

    attribute_class_gen = []
    attribute_class_gen.append('from networkStructure import *\nimport numpy as np\n')
    attribute_class_gen.append('#from CodeGen.Python.networkStructure import *\n')

    attribute_class_gen.append(generateThingClasses(trs_model=trs_model))
    [graph_code_gen, graph_name] = generateGraphClasses(pns_model)
    attribute_class_gen.append(graph_code_gen)

    # Instances
    attribute_class_gen.append(trs_parser(trs_model, trs_location))
    attribute_class_gen.append(pns_parser(pns_model, nsm_location, graph_name))

    a = open('networkStructureAttributesAndInstances.py', 'w')
    a.write('\n'.join(attribute_class_gen))


def main(argv):
    # Arguments
    trs_file = ''
    pns_file = ''
    trs_location_file = ''
    pns_location_file = ''
    try:
        opts, args = getopt.getopt(argv, "ht:T:p:P:", ["trsfile=", "pnsfile=", "thinglocation=", "nodelocation="])
    except getopt.GetoptError:
        print('codeGen.py -t <trsfilepath> -T <thinglocationJSON> -p <pnsfilepath> -P <nodelocationJSON>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('codeGen.py -t <trsfilepath> -T <thinglocationJSON> -p <pnsfilepath> -P <nodelocationJSON>')
            sys.exit()
        elif opt in ("-t", "--trsfile"):
            trs_file = arg
        elif opt in ("-p", "--pnsfile"):
            pns_file = arg
        elif opt in ("-T", "--thinglocation"):
            trs_location_file = arg
        elif opt in ("-P", "--nodelocation"):
            pns_location_file = arg

    print("TRS file:" + trs_file)
    #trs_file = 'TRS/iotRequestSchedule.trs'
    trs_grammar = 'TRS/trs.tx'
    #trs_location_file = 'TRS/location.json'

    ## Verify TRS file
    mm_trs = metamodel_from_file(trs_grammar)
    metamodel_export(mm_trs, 'TRS/trs.dot')
    os.system('dot -Tpng -O  TRS/trs.dot')
    #os.system('dot -Tpng -O  TRS/trs_grammar.dot') # Creates PNG of metamodel from Grammar
    try:
        trs_model = mm_trs.model_from_file(trs_file)
        # All attributes are unique
        unique_set = list(set(trs_model.attributes))
        if len(trs_model.attributes) != len(unique_set):
            raise Exception("Things attributes must be unique: ThingSet {}.".format(trs_model.name))
        # The attributes of each thing is unique
        for thing in trs_model.things:
            thing_unqiue_attr = list(set(thing.attributes))
            if len(thing_unqiue_attr) != len(thing.attributes):
                raise Exception("Thing attribubte must be unqiue: Thing {}".format(thing.name))
        # The value of each thing attribute conforms to the attribute type
        for thing in trs_model.things:
            for a in range(len(thing.attributes)):
                attr_name = thing.attributes[a].name
                attr_type = thing.attributes[a].type
                attr_val = thing.val[a]
                if attr_type == 'int':
                    if 'int' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type int.".format(attr_name))
                if attr_type == 'float':
                    if 'float' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type float.".format(attr_name))
                if attr_type == 'string':
                    if 'str' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type str.".format(attr_name))
                if attr_type == 'bool':
                    if 'bool' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type bool.".format(attr_name))
                if attr_type == 'timestamp':
                    try:
                        timestamp.convert_to_seconds(attr_val)
                    except:
                        raise Exception("Attribute {} must receive a value of type float.".format(attr_name))
    except Exception as e:
        print('Verification Failed: Error in file {}'.format(trs_file))
        print(e)
        exit()
    print('Verification of file {} succeeded.'.format(trs_file))
    with open(trs_location_file) as loc:
        loc_data_trs = json.load(loc)

    trs_parser(trs_model, loc_data_trs['location']) #

    #pns_file = 'PNS/edgeNetwork.pns'
    #pns_location_file = 'PNS/location.json'
    pns_grammar = 'PNS/pns.tx'
    ## Verify PNM file
    mm_pns = metamodel_from_file(pns_grammar)
    metamodel_export(mm_pns, 'PNS/pns.dot')
    os.system('dot -Tpng -O  PNS/pns.dot')
    #os.system('dot -Tpng -O  TRS/trs_grammar.dot') # Creates PNG of metamodel from Grammar
    try:
        pns_model = mm_pns.model_from_file(pns_file)
        # All attributes are unique
        ## Nodes
        nodeSet = pns_model.nodeSet
        unique_set_node = list(set(nodeSet.attributes))
        if len(nodeSet.attributes) != len(unique_set_node):
            raise Exception("NodeSet attributes must be unique: Graph {}.".format(pns_model.name))
        # The attributes of each thing is unique
        for node in nodeSet.nodes:
            node_unqiue_attr = list(set(nodeSet.attributes))
            if len(node_unqiue_attr) != len(nodeSet.attributes):
                raise Exception("Node attribubte must be unqiue: Node {}".format(node.name))
        # The value of each node attribute conforms to the attribute type
        for node in nodeSet.nodes:
            for a in range(len(node.attributes)):
                attr_name = node.attributes[a].name
                attr_type = node.attributes[a].type
                attr_val = node.val[a]
                if attr_type == 'int':
                    if 'int' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type int.".format(attr_name))
                if attr_type == 'float':
                    if 'float' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type float.".format(attr_name))
                if attr_type == 'string':
                    if 'str' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type str.".format(attr_name))
                if attr_type == 'bool':
                    if 'bool' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type bool.".format(attr_name))
                if attr_type == 'timestamp':
                    try:
                        timestamp.convert_to_seconds(attr_val)
                    except:
                        raise Exception("Attribute {} must receive a value of type float.".format(attr_name))
        ## Links
        linkSet = pns_model.linkSet
        unique_set_link = list(set(linkSet.attributes))
        if len(linkSet.attributes) != len(unique_set_link):
            raise Exception("LinkSet attributes must be unique: Graph {}.".format(pns_model.name))
        # The attributes of each thing is unique
        for link in linkSet.links:
            link_unqiue_attr = list(set(linkSet.attributes))
            if len(link_unqiue_attr) != len(linkSet.attributes):
                raise Exception("Link attribubte must be unqiue: Link {}".format(link.name))
        # The value of each link attribute conforms to the attribute type
        for link in linkSet.links:
            for a in range(len(link.attributes)):
                attr_name = link.attributes[a].name
                attr_type = link.attributes[a].type
                attr_val = link.val[a]
                if attr_type == 'int':
                    if 'int' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type int.".format(attr_name))
                if attr_type == 'float':
                    if 'float' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type float.".format(attr_name))
                if attr_type == 'string':
                    if 'str' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type str.".format(attr_name))
                if attr_type == 'bool':
                    if 'bool' not in str(type(attr_val)):
                        raise Exception("Attribute {} must receive a value of type bool.".format(attr_name))
                if attr_type == 'timestamp':
                    try:
                        timestamp.convert_to_seconds(attr_val)
                    except:
                        raise Exception("Attribute {} must receive a value of type float.".format(attr_name))

    except Exception as e:
        print('Verification Failed: Error in file {}'.format(pns_file))
        print(e)
        exit()
    print('Verification of file {} succeeded.'.format(pns_file))


    with open(pns_location_file) as loc:
        loc_data_nsm = json.load(loc)

    code_gen(trs_model, pns_model, loc_data_trs['location'], loc_data_nsm['location'])


if __name__=="__main__":
    main(sys.argv[1:])
