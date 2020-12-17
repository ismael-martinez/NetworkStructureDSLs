from networkStructure import *
import numpy as np
from networkUtil import * 

# Client classes

## class Client_IoT
class Client_IoT(ClientAbstract):
	def __init__(self, id, schedule, locations, fileSize_mb = 0, localCPU_ghz = 0.0, localProcessing_ms = 0, memoryReq_mb = 0, storageReq_mb = 0, comm_rad = np.infty):
		self.client_type = "IoT"
		self.id = id
		self.schedule = schedule
		self.locations = locations
		self.fileSize_mb = fileSize_mb
		self.localCPU_ghz = localCPU_ghz
		self.localProcessing_ms = localProcessing_ms
		self.memoryReq_mb = memoryReq_mb
		self.storageReq_mb = storageReq_mb
		self.comm_rad = comm_rad
# Defines the attribute that represents the radius (in metres), if any.
	def get_radius(self):

# The comm_rad attribute represents the radius.
		return self.comm_rad

# List the available attributes
	def list_attributes(self):
		return ['fileSize_mb','localCPU_ghz','localProcessing_ms','memoryReq_mb','storageReq_mb','comm_rad']

class Graph_G(GraphAbstract):
	def __init__(self, id, nodes, links):
		self.id= id
		self.nodes = nodes
		self.links=links
		self.paths = depthFirstSearch(self.nodes.get_nodes())

# Link classes for specific attribute set
class Node_Edge(NodeAbstract):
	def __init__(self,id,locations,storage_mb = 0,cpu_ghz = 0.0,memory_mb = 0,com_rad = np.infty):
		self.node_type = "Edge"
		self.id = id
		self.locations = locations
		self.storage_mb = storage_mb
		self.cpu_ghz = cpu_ghz
		self.memory_mb = memory_mb
		self.com_rad = com_rad
		self.neighbours = []

# Defines the attribute that represents the service rate, if any.
	def get_service_rate(self):
# The cpu_ghz attribute represents the service rate.
		return self.cpu_ghz
# Defines the attribute that represents the radius (in metres), if any.
	def get_radius(self):
# The com_rad attribute represents the radius.
		return self.com_rad

# List the available attributes
	def list_attributes(self):
		return ['storage_mb','cpu_ghz','memory_mb','com_rad']

class Node_Dormant(NodeAbstract):
	def __init__(self,id,locations,storage_mb = 0):
		self.node_type = "Dormant"
		self.id = id
		self.locations = locations
		self.storage_mb = storage_mb
		self.neighbours = []

# Defines the attribute that represents the service rate, if any.
	def get_service_rate(self):
# The storage_mb attribute represents the service rate.
		return self.storage_mb
# Defines the attribute that represents the radius (in metres), if any.
	def get_radius(self):

# No attribute defines the radius.
		return np.infty

# List the available attributes
	def list_attributes(self):
		return ['storage_mb']


# Link classes for specific attribute set
class Link_Edge(LinkAbstract):
	def __init__(self,id,node_pair,bandwidth = 0.0):
		self.link_type = "Edge"
		self.id = id
		self.node_pair = node_pair
		self.bandwidth = bandwidth

# List the available attributes
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
comm_rad = 500.0
fileSize_mb = 0
locations = []
locations.append(Locations(45.465660936499575, -73.74569047347666, 1))
# schedule_str = ['12:12:00', '12:27:00', '12:42:00', '12:57:00', '13:12:00', '13:27:00', '13:42:00']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
client = Client_IoT("t1", schedule, locations, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb, comm_rad)
clients.append_client(client)

# Instance of Client t2
fileSize_mb = 64
localCPU_ghz = 3.8
localProcessing_ms = 10
memoryReq_mb = 32
storageReq_mb = 0
comm_rad = 500.0
locations = []
locations.append(Locations(45.465678336962135, -73.74567773298384, 1))
locations.append(Locations(45.46566399333796, -73.74567337439419, 1))
# schedule_str = ['12:00', '12:03', '13:21', '13:45', '14:29']
schedule = [timestamp(43200),timestamp(43380),timestamp(48060),timestamp(49500),timestamp(52140)]
client = Client_IoT("t2", schedule, locations, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb, comm_rad)
clients.append_client(client)

# Instance of Client t3
fileSize_mb = 85
localCPU_ghz = 4.6
localProcessing_ms = 32
memoryReq_mb = 24
storageReq_mb = 0
comm_rad = 500.0
locations = []
locations.append(Locations(45.465660701358146, -73.74562408880354, 1))
# schedule_str = ['12:00:00', '12:01:59.097', '12:04:35.880', '12:20:04.257', '12:20:48.694', '12:21:50.987', '12:28:22.302', '12:45:43.710', '12:52:04.566', '12:55:35.401', '12:55:44.266']
schedule = [timestamp(43200),timestamp(43319.097460788085),timestamp(43475.88072974265),timestamp(44404.25723668737),timestamp(44448.69493952668),timestamp(44510.98775128017),timestamp(44902.30263159327),timestamp(45943.71020559959),timestamp(46324.566615614676),timestamp(46535.401229881434),timestamp(46544.26691719283)]
client = Client_IoT("t3", schedule, locations, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb, comm_rad)
clients.append_client(client)

# Instance of Client t4
fileSize_mb = 64
localCPU_ghz = 1.3
localProcessing_ms = 52
memoryReq_mb = 73
storageReq_mb = 0
comm_rad = 500.0
locations = []
locations.append(Locations(45.465690799452325, -73.745617383281, 1))
locations.append(Locations(45.465673398993594, -73.74559458450437, 1))
# schedule_str = ['10:00:00', '10:01:30.616', '10:03:06.015', '10:04:38.299', '10:06:05.023', '10:07:29.777', '10:09:09.868', '10:10:51.467', '10:12:28.010', '10:13:57.350', '10:15:32.723', '10:17:08.713', '10:18:44.372', '10:20:01.067', '10:21:28.571', '10:23:04.518', '10:24:30.795', '10:26:05.186', '10:27:37.811', '10:29:04.660', '10:30:40.818', '10:32:09.153', '10:33:44.454', '10:35:11.334', '10:36:41.219', '10:38:09.046', '10:39:36.240', '10:41:02.375', '10:42:29.557', '10:44:01.782', '10:45:32.067', '10:47:06.543', '10:48:43.618', '10:50:17.148', '10:51:49.492', '10:53:22.445', '10:54:54.555', '10:56:23.866', '10:57:55.692', '10:59:35.160', '11:01:07.903', '11:02:40.900', '11:04:05.681', '11:05:32.604', '11:06:56.952', '11:08:25.196', '11:09:57.706', '11:11:27.101', '11:12:53.774', '11:14:25.985', '11:15:48.629', '11:17:16.856', '11:18:52.678', '11:20:25.284', '11:22:00.875', '11:23:28.896', '11:24:58.954', '11:26:35.095', '11:28:07.113', '11:29:33.447', '11:30:59.557', '11:32:31.917', '11:33:59.876', '11:35:32.443', '11:37:01.478', '11:38:30.714', '11:40:05.354', '11:41:32.211', '11:43:08.758', '11:44:39.847', '11:46:11.812', '11:47:47.769', '11:49:14.821', '11:50:41.190', '11:52:11.173', '11:53:37.197', '11:55:01.435', '11:56:21.027', '11:57:46.606', '11:59:17.346', '12:00:47.260', '12:02:11.710', '12:03:35.430', '12:05:07.965', '12:06:44.273', '12:08:10.744', '12:09:37.780', '12:11:15.784', '12:12:42.921', '12:14:13.789', '12:15:54.954', '12:17:24.999', '12:18:55.721', '12:20:25.166', '12:21:58.177', '12:23:31.755', '12:24:56.457', '12:26:28.704', '12:27:51.837', '12:29:15.492', '12:30:43.753', '12:32:14.265', '12:33:42.595', '12:35:06.430', '12:36:43.410', '12:38:09.413', '12:39:39.593', '12:41:16.512', '12:42:46.720', '12:44:11.703', '12:45:41.495', '12:47:15.098', '12:48:45.310', '12:50:20.957', '12:51:42.023', '12:53:12.427', '12:54:41.491', '12:56:12.039', '12:57:50.247', '12:59:11.618', '13:00:40.474', '13:02:05.426', '13:03:27.113', '13:05:04.427', '13:06:36.143', '13:08:07.956', '13:09:39.602', '13:11:07.251', '13:12:31.016', '13:13:59.559', '13:15:30.989', '13:17:12.990', '13:18:43.053', '13:20:17.306', '13:21:49.436', '13:23:13.320', '13:24:46.842', '13:26:12.848', '13:27:37.623', '13:29:11.364', '13:30:44.857', '13:32:09.949', '13:33:39.201', '13:35:05.015', '13:36:29.568', '13:37:54.833', '13:39:36.703', '13:40:56.678', '13:42:28.156', '13:43:56.788', '13:45:21.817', '13:46:46.166', '13:48:17.905', '13:49:35.708', '13:51:09.381', '13:52:36.465', '13:54:12.567', '13:55:42.072', '13:57:13.594', '13:58:48.887', '14:00:11.425', '14:01:42.043', '14:03:12.027', '14:04:38.303', '14:06:01.393', '14:07:41.457', '14:09:07.217', '14:10:44.693', '14:12:08.430', '14:13:47.680', '14:15:18.860', '14:16:45.049', '14:18:12.262', '14:19:48.559', '14:21:20.062', '14:22:48.538', '14:24:15.178', '14:25:49.954', '14:27:16.219', '14:28:55.846', '14:30:31.031', '14:32:05.856', '14:33:29.772', '14:34:58.652', '14:36:35.207', '14:38:08.967', '14:39:39.037', '14:41:16.683', '14:42:47.046', '14:44:21.593', '14:45:41.904', '14:47:16.956', '14:48:47.352', '14:50:17.239', '14:51:41.027', '14:53:15.795', '14:54:46.135', '14:56:11.850', '14:57:39.811', '14:59:07.598']
schedule = [timestamp(36000),timestamp(36090.61601954143),timestamp(36186.01550444751),timestamp(36278.29992359056),timestamp(36365.023349426534),timestamp(36449.777226512124),timestamp(36549.86881444862),timestamp(36651.467576111856),timestamp(36748.01082258202),timestamp(36837.35022662932),timestamp(36932.72323732014),timestamp(37028.71324887213),timestamp(37124.37219958824),timestamp(37201.06759880091),timestamp(37288.57143438449),timestamp(37384.518596523165),timestamp(37470.79512147107),timestamp(37565.18614586426),timestamp(37657.81199837937),timestamp(37744.66085074741),timestamp(37840.81870123108),timestamp(37929.15334936441),timestamp(38024.45404608033),timestamp(38111.33484373773),timestamp(38201.21966330382),timestamp(38289.04683552697),timestamp(38376.24052014126),timestamp(38462.375856496496),timestamp(38549.55766596032),timestamp(38641.782571983116),timestamp(38732.067075122744),timestamp(38826.54339149579),timestamp(38923.618915982755),timestamp(39017.148087624126),timestamp(39109.49293698069),timestamp(39202.44588864496),timestamp(39294.55577779652),timestamp(39383.86602800695),timestamp(39475.69288514607),timestamp(39575.160102824935),timestamp(39667.90329117654),timestamp(39760.90025828004),timestamp(39845.681865161125),timestamp(39932.60423009509),timestamp(40016.95258776242),timestamp(40105.19609783671),timestamp(40197.70607850712),timestamp(40287.10178710692),timestamp(40373.774957271395),timestamp(40465.98530974003),timestamp(40548.62935788736),timestamp(40636.85636253653),timestamp(40732.67814347789),timestamp(40825.28414139083),timestamp(40920.87541143783),timestamp(41008.896067978174),timestamp(41098.95480100935),timestamp(41195.095769607426),timestamp(41287.11347175193),timestamp(41373.44708161803),timestamp(41459.557736243456),timestamp(41551.917209744555),timestamp(41639.87671448232),timestamp(41732.44304742607),timestamp(41821.47885609059),timestamp(41910.71444870558),timestamp(42005.354524842995),timestamp(42092.211333161016),timestamp(42188.758638612664),timestamp(42279.847058875646),timestamp(42371.812975773944),timestamp(42467.76914066146),timestamp(42554.821844783844),timestamp(42641.19094712435),timestamp(42731.17322995953),timestamp(42817.19765410038),timestamp(42901.43594761638),timestamp(42981.027879245165),timestamp(43066.60653798721),timestamp(43157.34669812716),timestamp(43247.26085211271),timestamp(43331.71083197423),timestamp(43415.430689019675),timestamp(43507.965431573764),timestamp(43604.273408358),timestamp(43690.744403290395),timestamp(43777.78015027548),timestamp(43875.784944098334),timestamp(43962.92178226324),timestamp(44053.789351707914),timestamp(44154.954313799295),timestamp(44244.999679688495),timestamp(44335.72171879171),timestamp(44425.16689222075),timestamp(44518.17776385335),timestamp(44611.7558101645),timestamp(44696.45715623421),timestamp(44788.70428128319),timestamp(44871.837007539136),timestamp(44955.49217348201),timestamp(45043.75345103406),timestamp(45134.26527174265),timestamp(45222.59523017793),timestamp(45306.430905833884),timestamp(45403.41043025032),timestamp(45489.41354548129),timestamp(45579.59353903366),timestamp(45676.51203686522),timestamp(45766.720057125545),timestamp(45851.703945463065),timestamp(45941.49561831656),timestamp(46035.09895906115),timestamp(46125.310154337014),timestamp(46220.95727479418),timestamp(46302.02329957649),timestamp(46392.427550599954),timestamp(46481.491693389435),timestamp(46572.039049698564),timestamp(46670.24723802123),timestamp(46751.61872374052),timestamp(46840.47499307306),timestamp(46925.42601740296),timestamp(47007.11361555255),timestamp(47104.42719686934),timestamp(47196.14317029532),timestamp(47287.956628981614),timestamp(47379.60210534639),timestamp(47467.25106869007),timestamp(47551.01606426043),timestamp(47639.5598288504),timestamp(47730.9898996651),timestamp(47832.990238635975),timestamp(47923.0537752233),timestamp(48017.30604275889),timestamp(48109.43675902287),timestamp(48193.32092802426),timestamp(48286.842583369886),timestamp(48372.84884240972),timestamp(48457.62382029452),timestamp(48551.36412454739),timestamp(48644.85702404562),timestamp(48729.949717150266),timestamp(48819.20175115929),timestamp(48905.01530065257),timestamp(48989.56833252241),timestamp(49074.83323077289),timestamp(49176.70396431073),timestamp(49256.67893119337),timestamp(49348.15646456108),timestamp(49436.78864124074),timestamp(49521.81759435621),timestamp(49606.166864953724),timestamp(49697.90537820786),timestamp(49775.708689580715),timestamp(49869.381406535795),timestamp(49956.46553951612),timestamp(50052.567643725735),timestamp(50142.07212061836),timestamp(50233.59460966485),timestamp(50328.887054049046),timestamp(50411.425380891786),timestamp(50502.04309739149),timestamp(50592.02712565548),timestamp(50678.30363349091),timestamp(50761.39338704807),timestamp(50861.45763003709),timestamp(50947.217194561985),timestamp(51044.693770532525),timestamp(51128.43090480214),timestamp(51227.68009467732),timestamp(51318.86015282668),timestamp(51405.04929784094),timestamp(51492.26283426638),timestamp(51588.55900585286),timestamp(51680.06218708039),timestamp(51768.53853251948),timestamp(51855.1788398113),timestamp(51949.95416673466),timestamp(52036.219061649856),timestamp(52135.846514852914),timestamp(52231.03119184168),timestamp(52325.85602855308),timestamp(52409.77227810721),timestamp(52498.65233502062),timestamp(52595.20770341884),timestamp(52688.96745341958),timestamp(52779.037591815635),timestamp(52876.683529413785),timestamp(52967.0464388178),timestamp(53061.59329258126),timestamp(53141.90417993705),timestamp(53236.956161449205),timestamp(53327.352377426025),timestamp(53417.239585856034),timestamp(53501.02703242915),timestamp(53595.795454910316),timestamp(53686.13511673441),timestamp(53771.8503301627),timestamp(53859.811870692734),timestamp(53947.59893871522)]
client = Client_IoT("t4", schedule, locations, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb, comm_rad)
clients.append_client(client)

# Instance of Client t5
fileSize_mb = 543
localCPU_ghz = 4.7
localProcessing_ms = 542
memoryReq_mb = 13
storageReq_mb = 0
comm_rad = 500.0
locations = []
locations.append(Locations(45.46570138080979, -73.74552954093576, 1))
# schedule_str = ['12:00:00', '12:04:19.013', '12:06:09.579', '12:08:52.814', '12:09:04.891', '12:09:11.294', '12:17:44.920', '12:20:52.535', '12:26:24.092', '12:28:32.215', '12:29:10.648', '12:29:22.970', '12:30:19.707', '12:31:52.970', '12:35:13.838', '12:40:00.898', '12:42:02.831', '12:46:26.019', '12:47:53.097', '12:49:11.994', '12:49:26.256', '12:53:07.212', '12:55:18.222']
schedule = [timestamp(43200),timestamp(43459.01376249505),timestamp(43569.579892578986),timestamp(43732.814464005605),timestamp(43744.89116442585),timestamp(43751.29465536393),timestamp(44264.92020637198),timestamp(44452.535827134205),timestamp(44784.092775529665),timestamp(44912.21513759686),timestamp(44950.64802360201),timestamp(44962.97083705745),timestamp(45019.70786024012),timestamp(45112.97049138475),timestamp(45313.83890142575),timestamp(45600.89805980508),timestamp(45722.83180552083),timestamp(45986.019347906404),timestamp(46073.09735236759),timestamp(46151.99491645558),timestamp(46166.25627077756),timestamp(46387.2120212901),timestamp(46518.222618867505)]
client = Client_IoT("t5", schedule, locations, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb, comm_rad)
clients.append_client(client)

# Instance of Client t6
fileSize_mb = 5
localCPU_ghz = 5.2
localProcessing_ms = 5
memoryReq_mb = 6
storageReq_mb = 0
comm_rad = 500.0
locations = []
locations.append(Locations(45.465699734820994, -73.7455637391007, 1))
# schedule_str = ['12:00:00', '12:01:42.838', '12:03:46.943', '12:06:03.879', '12:08:18.377', '12:10:09.923', '12:12:01.144', '12:13:56.950', '12:15:55.949', '12:17:26.687', '12:19:22.691', '12:21:41.685', '12:23:25.664', '12:25:07.082', '12:26:49.835', '12:28:56.943', '12:31:18.517', '12:33:04.631', '12:34:50.878', '12:37:22.793', '12:38:43.585', '12:40:49.740', '12:42:56.338', '12:44:39.356', '12:46:38.926', '12:48:20.586', '12:50:02.971', '12:51:34.364', '12:53:50.522', '12:55:30.316', '12:57:15.672', '12:59:06.469']
schedule = [timestamp(43200),timestamp(43302.838321843315),timestamp(43426.94353371798),timestamp(43563.879024026355),timestamp(43698.37726067731),timestamp(43809.923374050304),timestamp(43921.14420581497),timestamp(44036.95016600593),timestamp(44155.949208859536),timestamp(44246.687080525684),timestamp(44362.69177007427),timestamp(44501.68548688902),timestamp(44605.66467301287),timestamp(44707.08276728755),timestamp(44809.83530133108),timestamp(44936.943307300615),timestamp(45078.51797952329),timestamp(45184.63182522104),timestamp(45290.878774734105),timestamp(45442.79310201297),timestamp(45523.58502724248),timestamp(45649.74072116643),timestamp(45776.338480499886),timestamp(45879.35619360091),timestamp(45998.92654497978),timestamp(46100.58607531019),timestamp(46202.97164842233),timestamp(46294.36439947874),timestamp(46430.52224199135),timestamp(46530.316612944414),timestamp(46635.67248578861),timestamp(46746.469993911815)]
client = Client_IoT("t6", schedule, locations, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb, comm_rad)
clients.append_client(client)

# Instance of Client t7
fileSize_mb = 79
localCPU_ghz = 3.2
localProcessing_ms = 13
memoryReq_mb = 798
storageReq_mb = 0
comm_rad = 500.0
locations = []
locations.append(Locations(45.46563554122027, -73.74553524062992, 1))
locations.append(Locations(45.4656552931052, -73.74553758756281, 1))
# schedule_str = ['12:00:00']
schedule = [timestamp(43200)]
client = Client_IoT("t7", schedule, locations, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb, comm_rad)
clients.append_client(client)


nodes = Nodes()
links=Links()
###### All Node Instances ###### 

### Node_Edge Instances ### 

# Instance of Node n1
cpu_ghz = 3.2
memory_mb = 1024
storage_mb = 512
com_rad = 500.0
locations = []
locations.append(Locations(45.465664933903625, -73.7456826990701, 1))
node = Node_Edge("n1", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
nodes.append_node(node)

# Instance of Node n2
cpu_ghz = 2.8
memory_mb = 32
storage_mb = 128
com_rad = 500.0
locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
node = Node_Edge("n2", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
nodes.append_node(node)

# Instance of Node n3
cpu_ghz = 1.6
memory_mb = 64
storage_mb = 32
com_rad = 500.0
locations = []
locations.append(Locations(45.46569244544138, -73.74554328725696, 1))
node = Node_Edge("n3", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
nodes.append_node(node)

# Instance of Node n4
cpu_ghz = 2.9
memory_mb = 2048
storage_mb = 4096
com_rad = 500.0
locations = []
locations.append(Locations(45.46563906834305, -73.74555032805563, 1))
node = Node_Edge("n4", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
nodes.append_node(node)

### Node_Dormant Instances ### 

# Instance of Node n5
storage_mb = 512
locations = []
locations.append(Locations(45.465678336962135, -73.74567773298384, 1))
node = Node_Dormant("n5", locations, storage_mb)
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