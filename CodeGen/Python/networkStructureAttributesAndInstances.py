from CodeGen.Python.networkStructure import *

class ThingAttributes_IoT:
	def __init__(self, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb):
		self.fileSize_mb = fileSize_mb
		self.localCPU_ghz = localCPU_ghz
		self.localProcessing_ms = localProcessing_ms
		self.memoryReq_mb = memoryReq_mb
		self.storageReq_mb = storageReq_mb
	def listAttributes(self):
		return ["fileSize_mb","localCPU_ghz","localProcessing_ms","memoryReq_mb","storageReq_mb"]

class Thing_IoT(ThingAbstract):
	def __init__(self,id, schedule, locations,attributes):
		self.id = id
		self.schedule = schedule
		self.locations = locations
		self.attributes = attributes

class Graph_Edge(GraphAbstract):
	def __init__(self, id, nodes, links):
		self.id= id
		self.nodes = nodes
		self.links=links
		self.paths = depthFirstSearch(self.nodes)

class Node_Edge(NodeAbstract):
	def __init__(self, id, locations, attributes):
		self.id = id
		self.locations=locations
		self.attributes = attributes
		self.neighbours = []

class Link_Edge(LinkAbstract):
	def __init__(self, id, node_pair, attributes):
		self.id = id
		self.node_pair=node_pair
		self.attributes=attributes

class NodeAttributes_Edge:
	def __init__(self, storage_mb, cpu_ghz, memory_mb):
		self.storage_mb = storage_mb
		self.cpu_ghz = cpu_ghz
		self.memory_mb = memory_mb
	def listAttributes(self):
		return ["storage_mb","cpu_ghz","memory_mb"]

class LinkAttributes_Edge:
	def __init__(self, bandwidth):
		self.bandwidth = bandwidth
	def listAttributes(self):
		return ["bandwidth"]

## Thing instances ## 

things = {}

locations = []
locations.append(Locations(45.465660936499575, -73.74569047347666, 1))
attributes = ThingAttributes_IoT(16,3.2,5,6,0)
# schedule_str = ['12:12:00', '12:27:00', '12:42:00', '12:57:00', '13:12:00', '13:27:00', '13:42:00']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
things["t1"] = Thing_IoT("t1", schedule, locations, attributes)

locations = []
locations.append(Locations(45.465678336962135, -73.74567773298384, 1))
locations.append(Locations(45.46566399333796, -73.74567337439419, 1))
attributes = ThingAttributes_IoT(64,3.8,10,32,0)
# schedule_str = ['12:00', '12:03', '14:29']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
things["t2"] = Thing_IoT("t2", schedule, locations, attributes)

locations = []
locations.append(Locations(45.465660701358146, -73.74562408880354, 1))
attributes = ThingAttributes_IoT(85,4.6,32,24,0)
# schedule_str = ['12:00', '12:03', '14:29']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
things["t3"] = Thing_IoT("t3", schedule, locations, attributes)

locations = []
locations.append(Locations(45.465690799452325, -73.745617383281, 1))
locations.append(Locations(45.465673398993594, -73.74559458450437, 1))
attributes = ThingAttributes_IoT(64,1.3,52,73,0)
# schedule_str = ['12:00', '12:03', '14:29']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
things["t4"] = Thing_IoT("t4", schedule, locations, attributes)

locations = []
locations.append(Locations(45.46570138080979, -73.74552954093576, 1))
attributes = ThingAttributes_IoT(543,4.7,542,13,0)
# schedule_str = ['12:00', '12:03', '14:29']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
things["t5"] = Thing_IoT("t5", schedule, locations, attributes)

locations = []
locations.append(Locations(45.465699734820994, -73.7455637391007, 1))
attributes = ThingAttributes_IoT(5,5.2,5,6,0)
# schedule_str = ['12:00', '12:03', '14:29']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
things["t6"] = Thing_IoT("t6", schedule, locations, attributes)

locations = []
locations.append(Locations(45.46563554122027, -73.74553524062992, 1))
locations.append(Locations(45.4656552931052, -73.74553758756281, 1))
attributes = ThingAttributes_IoT(79,3.2,13,798,0)
# schedule_str = ['12:00:00']
schedule = [timestamp(43200)]
things["t7"] = Thing_IoT("t7", schedule, locations, attributes)


nodes = {}
links={}
## Node Instances 

locations = []
locations.append(Locations(45.465664933903625, -73.7456826990701, 1))
attributes = NodeAttributes_Edge(3.2,1024,512)
nodes["n1"] = Node_Edge("n1", locations, attributes)

locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
attributes = NodeAttributes_Edge(2.8,32,128)
nodes["n2"] = Node_Edge("n2", locations, attributes)

locations = []
locations.append(Locations(45.46569244544138, -73.74554328725696, 1))
attributes = NodeAttributes_Edge(1.6,64,32)
nodes["n3"] = Node_Edge("n3", locations, attributes)

locations = []
locations.append(Locations(45.46563906834305, -73.74555032805563, 1))
attributes = NodeAttributes_Edge(2.9,2048,4096)
nodes["n4"] = Node_Edge("n4", locations, attributes)

## Link Instances

node_pair = ['n1', 'n2']
nodes["n1"].neighbours.append(("l1", "n2"))
attributes = LinkAttributes_Edge(3.5)
links["l1"] = Link_Edge("l1", node_pair, attributes)

node_pair = ['n2', 'n3']
nodes["n2"].neighbours.append(("l2", "n3"))
attributes = LinkAttributes_Edge(8.1)
links["l2"] = Link_Edge("l2", node_pair, attributes)

node_pair = ['n2', 'n4']
nodes["n2"].neighbours.append(("l3", "n4"))
attributes = LinkAttributes_Edge(7.3)
links["l3"] = Link_Edge("l3", node_pair, attributes)

graph = Graph_Edge("Edge", nodes, links)
network_structure = NetworkStructure(graph, things)