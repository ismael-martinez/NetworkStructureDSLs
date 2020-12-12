from networkStructure import *
import numpy as np
from networkUtil import * 

#from CodeGen.Python.networkStructure import *

# Client classes

## class Client_IoT
class Client_IoT(ClientAbstract):
	def __init__(self, id, schedule, locations, radius, fileSize_mb = 0, localCPU_ghz = 0.0, localProcessing_ms = 0, memoryReq_mb = 0, storageReq_mb = 0):
		self.client_type = "IoT"
		self.id = id
		self.schedule = schedule
		self.locations = locations
		self.radius = radius
		self.fileSize_mb = fileSize_mb
		self.localCPU_ghz = localCPU_ghz
		self.localProcessing_ms = localProcessing_ms
		self.memoryReq_mb = memoryReq_mb
		self.storageReq_mb = storageReq_mb
	def list_attributes(self):
		return ['fileSize_mb','localCPU_ghz','localProcessing_ms','memoryReq_mb','storageReq_mb']

class Graph_G(GraphAbstract):
	def __init__(self, id, nodes, links):
		self.id= id
		self.nodes = nodes
		self.links=links
		self.paths = depthFirstSearch(self.nodes.get_nodes())

# Link classes for specific attribute set
class Node_Edge(NodeAbstract):
	def __init__(self,id,locations,radius,storage_mb = 0,cpu_ghz = 0.0,memory_mb = 0):
		self.node_type = "Edge"
		self.id = id
		self.locations = locations
		self.radius = radius
		self.storage_mb = storage_mb
		self.cpu_ghz = cpu_ghz
		self.memory_mb = memory_mb
		self.neighbours = []
	def service_rate(self):
		return self.cpu_ghz
	def list_attributes(self):
		return ['storage_mb','cpu_ghz','memory_mb']

class Node_Dormant(NodeAbstract):
	def __init__(self,id,locations,radius,storage_mb = 0):
		self.node_type = "Dormant"
		self.id = id
		self.locations = locations
		self.radius = radius
		self.storage_mb = storage_mb
		self.neighbours = []
	def service_rate(self):
		return self.storage_mb
	def list_attributes(self):
		return ['storage_mb']


# Link classes for specific attribute set
class Link_Edge(LinkAbstract):
	def __init__(self,id,node_pair,bandwidth = 0.0):
		self.link_type = "Edge"
		self.id = id
		self.node_pair = node_pair
		self.bandwidth = bandwidth
	def list_attributes(self):
		return ['bandwidth']

###### All Client instances ######

#### Client_IoT instances ##### 

clients = Clients()

# Instance of Client t1
localCPU_ghz = 3.2
localProcessing_ms = 5
memoryReq_mb = 6
storageReq_mb = 0
fileSize_mb = 0
radius = np.infty
locations = []
locations.append(Locations(45.465660936499575, -73.74569047347666, 1))
# schedule_str = ['12:12:00', '12:27:00', '12:42:00', '12:57:00', '13:12:00', '13:27:00', '13:42:00']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
client = Client_IoT("t1", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)
clients.append_client(client)

# Instance of Client t2
fileSize_mb = 64
localCPU_ghz = 3.8
localProcessing_ms = 10
memoryReq_mb = 32
storageReq_mb = 0
radius = np.infty
locations = []
locations.append(Locations(45.465678336962135, -73.74567773298384, 1))
locations.append(Locations(45.46566399333796, -73.74567337439419, 1))
# schedule_str = ['12:00', '12:03', '13:21', '13:45', '14:29']
schedule = [timestamp(43200),timestamp(43380),timestamp(48060),timestamp(49500),timestamp(52140)]
client = Client_IoT("t2", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)
clients.append_client(client)

# Instance of Client t3
fileSize_mb = 85
localCPU_ghz = 4.6
localProcessing_ms = 32
memoryReq_mb = 24
storageReq_mb = 0
radius = 300.0
locations = []
locations.append(Locations(45.465660701358146, -73.74562408880354, 1))
# schedule_str = ['12:00:00', '12:15:45.601', '12:22:35.463', '12:23:07.009', '12:26:12.243', '12:28:40.560', '12:29:20.040', '12:39:32.800', '12:50:21.713', '12:57:54.016']
schedule = [timestamp(43200),timestamp(44145.601066377974),timestamp(44555.463808660155),timestamp(44587.009630071436),timestamp(44772.24349833289),timestamp(44920.5604273844),timestamp(44960.040082457956),timestamp(45572.80035898734),timestamp(46221.71375529934),timestamp(46674.016393910664)]
client = Client_IoT("t3", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)
clients.append_client(client)

# Instance of Client t4
fileSize_mb = 64
localCPU_ghz = 1.3
localProcessing_ms = 52
memoryReq_mb = 73
storageReq_mb = 0
radius = 500.0
locations = []
locations.append(Locations(45.465690799452325, -73.745617383281, 1))
locations.append(Locations(45.465673398993594, -73.74559458450437, 1))
# schedule_str = ['10:00:00', '10:01:31.500', '10:03:01.696', '10:04:33.404', '10:06:12.096', '10:07:43.060', '10:09:16.658', '10:10:46.927', '10:12:08.682', '10:13:43.043', '10:15:05.765', '10:16:27.592', '10:17:52.170', '10:19:11.731', '10:20:43.208', '10:22:08.396', '10:23:35.342', '10:25:05.563', '10:26:31.974', '10:27:57.514', '10:29:31.367', '10:31:01.865', '10:32:34.541', '10:34:04.017', '10:35:26.545', '10:36:55.730', '10:38:24.238', '10:39:51.430', '10:41:16', '10:42:41.462', '10:44:09.831', '10:45:40.408', '10:47:17.204', '10:48:49.306', '10:50:21.152', '10:51:53.418', '10:53:25.784', '10:55:05.203', '10:56:27.070', '10:57:52.464', '10:59:25.031', '11:00:55.487', '11:02:26.138', '11:04:01.320', '11:05:32.477', '11:07:04.841', '11:08:33.109', '11:10:11.421', '11:11:42.286', '11:13:15.868', '11:14:50.286', '11:16:23.782', '11:17:46.011', '11:19:27.072', '11:20:53.793', '11:22:27.876', '11:23:58.957', '11:25:30.927', '11:26:57.182', '11:28:28.441', '11:29:59.631', '11:31:30.284', '11:32:47.943', '11:34:15.902', '11:35:44.609', '11:37:26.353', '11:38:49.821', '11:40:20.606', '11:41:50.657', '11:43:17.825', '11:44:40.145', '11:46:06.988', '11:47:24.213', '11:48:55.060', '11:50:28.801', '11:51:54.677', '11:53:24.690', '11:55:02.647', '11:56:34.808', '11:58:03.755', '11:59:29.645', '12:01:07.028', '12:02:38.431', '12:04:05.705', '12:05:31.818', '12:07:03.993', '12:08:35.917', '12:09:56.731', '12:11:22.458', '12:12:51.377', '12:14:19.502', '12:15:47.337', '12:17:13.083', '12:18:45.898', '12:20:13.032', '12:21:39.381', '12:23:02.165', '12:24:36.575', '12:26:13.403', '12:27:42.412', '12:29:20.612', '12:30:56.647', '12:32:23.628', '12:33:56.336', '12:35:31.940', '12:37:05.948', '12:38:40.281', '12:40:14.221', '12:41:40.513', '12:43:14.812', '12:44:44.341', '12:46:16.295', '12:47:45.539', '12:49:10.249', '12:50:40.917', '12:52:08.197', '12:53:41.611', '12:55:12.018', '12:56:46.472', '12:58:18.221', '12:59:52.044', '13:01:22.744', '13:02:55.381', '13:04:29.352', '13:06:02.274', '13:07:33.172', '13:09:07.701', '13:10:41.108', '13:12:16.714', '13:13:43.109', '13:15:17.579', '13:16:45.512', '13:18:14.322', '13:19:44.207', '13:21:12.944', '13:22:32.774', '13:23:55.812', '13:25:22.694', '13:26:42.632', '13:28:10.548', '13:29:38.273', '13:31:13.890', '13:32:40.093', '13:34:04.219', '13:35:30.963', '13:37:00.769', '13:38:32.831', '13:40:04.396', '13:41:35.275', '13:43:06.183', '13:44:34.387', '13:46:06.864', '13:47:38.641', '13:49:00.227', '13:50:23.993', '13:51:51.184', '13:53:33.413', '13:54:53.988', '13:56:19.743', '13:57:50.127', '13:59:21.326', '14:00:57.642', '14:02:27.146', '14:04:00.471', '14:05:28.480', '14:06:58.430', '14:08:24.686', '14:09:54.454', '14:11:26.634', '14:12:50.534', '14:14:26.308', '14:15:56.534', '14:17:22.477', '14:18:54.795', '14:20:08.926', '14:21:39.347', '14:23:02.115', '14:24:33.811', '14:26:07.534', '14:27:40.040', '14:29:08.591', '14:30:31.791', '14:32:00.238', '14:33:27.374', '14:34:52.975', '14:36:23.437', '14:37:51.228', '14:39:32.143', '14:41:01.279', '14:42:31.684', '14:43:56.611', '14:45:35.664', '14:47:11.126', '14:48:43.945', '14:50:10.521', '14:51:36.586', '14:53:06.963', '14:54:29.392', '14:56:02.275', '14:57:29.749', '14:58:57.063']
schedule = [timestamp(36000),timestamp(36091.50080032946),timestamp(36181.69648630683),timestamp(36273.40454727351),timestamp(36372.0969393949),timestamp(36463.060254122174),timestamp(36556.65816065683),timestamp(36646.927878368166),timestamp(36728.68260318382),timestamp(36823.043516741185),timestamp(36905.765904899206),timestamp(36987.59242831772),timestamp(37072.1700922776),timestamp(37151.73110906284),timestamp(37243.20840653612),timestamp(37328.396170648055),timestamp(37415.342028866275),timestamp(37505.56318090227),timestamp(37591.974465815314),timestamp(37677.51407645393),timestamp(37771.36782138462),timestamp(37861.86580365395),timestamp(37954.54136939944),timestamp(38044.01716013113),timestamp(38126.54512280323),timestamp(38215.73010492971),timestamp(38304.23831394887),timestamp(38391.43047015038),timestamp(38476.000269345976),timestamp(38561.46283771834),timestamp(38649.831837782025),timestamp(38740.40860148112),timestamp(38837.20435464053),timestamp(38929.306429824464),timestamp(39021.15233250853),timestamp(39113.418838130536),timestamp(39205.78489892871),timestamp(39305.203415965276),timestamp(39387.070402636324),timestamp(39472.46494672547),timestamp(39565.03143310925),timestamp(39655.487434458555),timestamp(39746.13869862543),timestamp(39841.320211584556),timestamp(39932.47758865917),timestamp(40024.841780868046),timestamp(40113.109556667965),timestamp(40211.42128388892),timestamp(40302.28633175427),timestamp(40395.86876329548),timestamp(40490.286839152606),timestamp(40583.78284278911),timestamp(40666.011576638055),timestamp(40767.07282963009),timestamp(40853.793227683265),timestamp(40947.87666387917),timestamp(41038.957768018845),timestamp(41130.92733113768),timestamp(41217.182265338575),timestamp(41308.44137396549),timestamp(41399.63149567003),timestamp(41490.28440443683),timestamp(41567.943614673444),timestamp(41655.90224487257),timestamp(41744.60961493644),timestamp(41846.353077300344),timestamp(41929.82109960244),timestamp(42020.6067976672),timestamp(42110.65782286445),timestamp(42197.82596853549),timestamp(42280.14544858726),timestamp(42366.9885263034),timestamp(42444.213562145276),timestamp(42535.06061512317),timestamp(42628.80182400189),timestamp(42714.67799921647),timestamp(42804.690808477615),timestamp(42902.6475405047),timestamp(42994.80870856519),timestamp(43083.755636066526),timestamp(43169.6452249394),timestamp(43267.02842384159),timestamp(43358.4310646524),timestamp(43445.705227606886),timestamp(43531.81803629143),timestamp(43623.993525440645),timestamp(43715.91757049136),timestamp(43796.73191355322),timestamp(43882.45893356581),timestamp(43971.3774391801),timestamp(44059.50246834774),timestamp(44147.33774348955),timestamp(44233.08336801572),timestamp(44325.89846551092),timestamp(44413.03201090235),timestamp(44499.38146365586),timestamp(44582.16560369714),timestamp(44676.57552077059),timestamp(44773.40389712843),timestamp(44862.41258289174),timestamp(44960.61212169282),timestamp(45056.64727354774),timestamp(45143.62877004404),timestamp(45236.33675009471),timestamp(45331.94012568272),timestamp(45425.94866011712),timestamp(45520.28183843137),timestamp(45614.221013121816),timestamp(45700.51331250552),timestamp(45794.8127344235),timestamp(45884.34159113055),timestamp(45976.29506614301),timestamp(46065.53976890949),timestamp(46150.24937016098),timestamp(46240.9175795508),timestamp(46328.197470385785),timestamp(46421.611084267446),timestamp(46512.01819548837),timestamp(46606.472295155465),timestamp(46698.22141153476),timestamp(46792.044550583356),timestamp(46882.74405632684),timestamp(46975.38194978496),timestamp(47069.352982148725),timestamp(47162.274915665),timestamp(47253.17265855757),timestamp(47347.70196221949),timestamp(47441.10813741723),timestamp(47536.71450271318),timestamp(47623.10991081746),timestamp(47717.57928595376),timestamp(47805.51248214291),timestamp(47894.32288938353),timestamp(47984.20781255),timestamp(48072.94423778272),timestamp(48152.77494580796),timestamp(48235.81236201567),timestamp(48322.69487326549),timestamp(48402.6323990491),timestamp(48490.54825954512),timestamp(48578.273435608404),timestamp(48673.89023431775),timestamp(48760.093805456265),timestamp(48844.219186853596),timestamp(48930.963151306074),timestamp(49020.769389909285),timestamp(49112.831791623765),timestamp(49204.39657783678),timestamp(49295.275817252375),timestamp(49386.18398707395),timestamp(49474.38772798316),timestamp(49566.864682654494),timestamp(49658.641421931665),timestamp(49740.2270570376),timestamp(49823.99333804306),timestamp(49911.18488712055),timestamp(50013.41331489036),timestamp(50093.98875009568),timestamp(50179.743496000425),timestamp(50270.12722156864),timestamp(50361.32664751323),timestamp(50457.64247836363),timestamp(50547.146628050774),timestamp(50640.471175282175),timestamp(50728.48015921641),timestamp(50818.430204138356),timestamp(50904.68699363435),timestamp(50994.454315283314),timestamp(51086.63448392603),timestamp(51170.53455649616),timestamp(51266.30828698151),timestamp(51356.534030133764),timestamp(51442.47720523609),timestamp(51534.79577142903),timestamp(51608.92699105071),timestamp(51699.34729761835),timestamp(51782.11564255944),timestamp(51873.81162058502),timestamp(51967.53415212716),timestamp(52060.04055283851),timestamp(52148.59197032381),timestamp(52231.79193193829),timestamp(52320.23899926709),timestamp(52407.37491185965),timestamp(52492.975398056384),timestamp(52583.43721875557),timestamp(52671.22820670214),timestamp(52772.14332762377),timestamp(52861.27946734595),timestamp(52951.68484430749),timestamp(53036.61140099355),timestamp(53135.66474821292),timestamp(53231.12632700463),timestamp(53323.94535347488),timestamp(53410.52153028352),timestamp(53496.586581606156),timestamp(53586.96389587757),timestamp(53669.39286083375),timestamp(53762.27552639991),timestamp(53849.74953346346),timestamp(53937.063840823874)]
client = Client_IoT("t4", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)
clients.append_client(client)

# Instance of Client t5
fileSize_mb = 543
localCPU_ghz = 4.7
localProcessing_ms = 542
memoryReq_mb = 13
storageReq_mb = 0
radius = np.infty
locations = []
locations.append(Locations(45.46570138080979, -73.74552954093576, 1))
# schedule_str = ['12:00:00', '12:05:38.406', '12:07:28.133', '12:08:47.283', '12:09:21.045', '12:10:10.954', '12:12:09.252', '12:18:24.615', '12:19:05.274', '12:21:36.734', '12:23:13.766', '12:26:33.411', '12:29:04.526', '12:30:09.362', '12:34:52.171', '12:36:36.442', '12:44:44.656', '12:47:30.853', '12:58:29.421', '12:59:57.598']
schedule = [timestamp(43200),timestamp(43538.4060906739),timestamp(43648.13326601374),timestamp(43727.28314328495),timestamp(43761.04518651285),timestamp(43810.95410319881),timestamp(43929.252063523854),timestamp(44304.61571001099),timestamp(44345.274075832036),timestamp(44496.7348766724),timestamp(44593.76673434996),timestamp(44793.411562201094),timestamp(44944.52615864378),timestamp(45009.362785840334),timestamp(45292.17175506001),timestamp(45396.44246803827),timestamp(45884.65659116279),timestamp(46050.85376747628),timestamp(46709.42129535153),timestamp(46797.59803071608)]
client = Client_IoT("t5", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)
clients.append_client(client)

# Instance of Client t6
fileSize_mb = 5
localCPU_ghz = 5.2
localProcessing_ms = 5
memoryReq_mb = 6
storageReq_mb = 0
radius = np.infty
locations = []
locations.append(Locations(45.465699734820994, -73.7455637391007, 1))
# schedule_str = ['12:00:00', '12:01:58.262', '12:03:49.685', '12:06:02.228', '12:08:15.084', '12:10:30.298', '12:12:56.897', '12:14:32.346', '12:16:43.045', '12:18:27.215', '12:20:14.267', '12:22:22.971', '12:24:42.886', '12:26:39.595', '12:28:59.845', '12:30:42.510', '12:32:43.194', '12:34:50.396', '12:36:48.519', '12:38:40.787', '12:40:57.270', '12:42:44.878', '12:44:29.234', '12:46:17.894', '12:48:33.498', '12:50:29.333', '12:52:40.684', '12:54:41.903', '12:56:59.862', '12:58:42.860']
schedule = [timestamp(43200),timestamp(43318.262425452944),timestamp(43429.685430293954),timestamp(43562.22858169921),timestamp(43695.08462599575),timestamp(43830.298704993664),timestamp(43976.89729488285),timestamp(44072.34613208988),timestamp(44203.04536046253),timestamp(44307.21562426573),timestamp(44414.26731274997),timestamp(44542.97120535374),timestamp(44682.88696771354),timestamp(44799.59515004746),timestamp(44939.84504633896),timestamp(45042.510638389074),timestamp(45163.194816044306),timestamp(45290.39675652414),timestamp(45408.51973652265),timestamp(45520.78757421759),timestamp(45657.270650957165),timestamp(45764.87884345888),timestamp(45869.234993978134),timestamp(45977.89406668655),timestamp(46113.49834119763),timestamp(46229.333744431155),timestamp(46360.68499516425),timestamp(46481.90385459863),timestamp(46619.862217655915),timestamp(46722.860367631554)]
client = Client_IoT("t6", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)
clients.append_client(client)

# Instance of Client t7
fileSize_mb = 79
localCPU_ghz = 3.2
localProcessing_ms = 13
memoryReq_mb = 798
storageReq_mb = 0
radius = np.infty
locations = []
locations.append(Locations(45.46563554122027, -73.74553524062992, 1))
locations.append(Locations(45.4656552931052, -73.74553758756281, 1))
# schedule_str = ['12:00:00']
schedule = [timestamp(43200)]
client = Client_IoT("t7", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)
clients.append_client(client)


nodes = Nodes()
links=Links()
###### All Node Instances ###### 

### Node_Edge Instances ### 

# Instance of Node n1
cpu_ghz = 3.2
memory_mb = 1024
storage_mb = 512
locations = []
locations.append(Locations(45.465664933903625, -73.7456826990701, 1))
radius = np.infty
node = Node_Edge("n1", locations, radius, storage_mb, cpu_ghz, memory_mb)
nodes.append_node(node)

# Instance of Node n2
cpu_ghz = 2.8
memory_mb = 32
storage_mb = 128
locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
radius = np.infty
node = Node_Edge("n2", locations, radius, storage_mb, cpu_ghz, memory_mb)
nodes.append_node(node)

# Instance of Node n3
cpu_ghz = 1.6
memory_mb = 64
storage_mb = 32
locations = []
locations.append(Locations(45.46569244544138, -73.74554328725696, 1))
radius = np.infty
node = Node_Edge("n3", locations, radius, storage_mb, cpu_ghz, memory_mb)
nodes.append_node(node)

# Instance of Node n4
cpu_ghz = 2.9
memory_mb = 2048
storage_mb = 4096
locations = []
locations.append(Locations(45.46563906834305, -73.74555032805563, 1))
radius = np.infty
node = Node_Edge("n4", locations, radius, storage_mb, cpu_ghz, memory_mb)
nodes.append_node(node)

### Node_Dormant Instances ### 

# Instance of Node n5
storage_mb = 512
locations = []
locations.append(Locations(45.465664933903625, -73.7456826990701, 1))
radius = np.infty
node = Node_Dormant("n5", locations, radius, storage_mb)
nodes.append_node(node)

###### All Link Instances ######

### Link_Edge Instance ###

# Instance of Link l1
bandwidth = 3.5
node_pair = ['n1', 'n2']
nodes.get_node("n1").neighbours.append(("l1", "n2"))
link = Link_Edge("l1", node_pair, bandwidth)
links.append_link(link)

# Instance of Link l2
bandwidth = 8.1
node_pair = ['n2', 'n3']
nodes.get_node("n2").neighbours.append(("l2", "n3"))
link = Link_Edge("l2", node_pair, bandwidth)
links.append_link(link)

# Instance of Link l3
bandwidth = 7.3
node_pair = ['n2', 'n4']
nodes.get_node("n2").neighbours.append(("l3", "n4"))
link = Link_Edge("l3", node_pair, bandwidth)
links.append_link(link)

# Instance of Link l4
bandwidth = 3.3
node_pair = ['n2', 'n5']
nodes.get_node("n2").neighbours.append(("l4", "n5"))
link = Link_Edge("l4", node_pair, bandwidth)
links.append_link(link)

graph = Graph_G("G", nodes, links)
network_structure = NetworkStructure(graph, clients)