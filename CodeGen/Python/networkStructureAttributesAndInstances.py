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
# schedule_str = ['12:00:00', '12:04:50.365', '12:06:04.975', '12:19:13.677', '12:22:54.137', '12:24:05.172', '12:46:14.649', '12:48:11.212']
schedule = [timestamp(43200),timestamp(43490.36547595411),timestamp(43564.975791678786),timestamp(44353.67709348749),timestamp(44574.137840862706),timestamp(44645.17219144019),timestamp(45974.64934854122),timestamp(46091.21236370327)]
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
# schedule_str = ['10:00:00', '10:01:22.538', '10:02:52.930', '10:04:27.462', '10:06:06.867', '10:07:25.043', '10:08:50.791', '10:10:19.743', '10:11:54.923', '10:13:14.763', '10:14:48.927', '10:16:15.544', '10:17:53.045', '10:19:20.351', '10:20:47.085', '10:22:21.461', '10:23:51.590', '10:25:23.599', '10:26:48.375', '10:28:17.460', '10:29:47.811', '10:31:15.422', '10:32:46.178', '10:34:18.322', '10:35:44.632', '10:37:16.692', '10:38:47.058', '10:40:22.774', '10:42:04.977', '10:43:46.743', '10:45:09.412', '10:46:33.848', '10:48:07.091', '10:49:38.782', '10:51:14.990', '10:52:41.791', '10:54:08.248', '10:55:51.303', '10:57:19.579', '10:58:48.051', '11:00:15.178', '11:01:45.893', '11:03:14.301', '11:04:47.481', '11:06:14.244', '11:07:43.213', '11:09:14.399', '11:10:50.584', '11:12:23.925', '11:13:55.184', '11:15:14.127', '11:16:42.745', '11:18:13.775', '11:19:35.751', '11:21:03.533', '11:22:26.214', '11:23:59.038', '11:25:24.596', '11:26:52.290', '11:28:25.041', '11:29:56.912', '11:31:26.806', '11:33:00.423', '11:34:25.238', '11:35:52.524', '11:37:23.841', '11:38:49.636', '11:40:28.001', '11:41:58.436', '11:43:34.956', '11:44:59.442', '11:46:25.369', '11:47:57.279', '11:49:29.653', '11:51:07.981', '11:52:32.799', '11:54:04.558', '11:55:34.689', '11:57:11.057', '11:58:45.967', '12:00:17.558', '12:01:48.459', '12:03:06.554', '12:04:32.332', '12:06:02.589', '12:07:32.116', '12:09:05.134', '12:10:31.675', '12:12:01.912', '12:13:31.145', '12:15:01.730', '12:16:31.003', '12:17:55.461', '12:19:30.396', '12:21:01.857', '12:22:38.294', '12:24:02.516', '12:25:32.440', '12:27:00.521', '12:28:36.107', '12:30:03.757', '12:31:24.496', '12:32:55.588', '12:34:27.045', '12:36:03.383', '12:37:41.393', '12:39:12.576', '12:40:45.985', '12:42:13.243', '12:43:43.300', '12:45:06.801', '12:46:38.771', '12:48:15.072', '12:49:41.925', '12:51:18.724', '12:52:43.502', '12:54:12.034', '12:55:46.575', '12:57:20.501', '12:58:55.984', '13:00:34.453', '13:02:04.008', '13:03:34.558', '13:05:08.115', '13:06:42.198', '13:08:11.974', '13:09:46.799', '13:11:22.318', '13:13:00.889', '13:14:25.235', '13:15:57.702', '13:17:29.179', '13:19:00.721', '13:20:29.876', '13:22:00.497', '13:23:30.800', '13:25:00.517', '13:26:41.681', '13:28:05.916', '13:29:33.504', '13:31:02.958', '13:32:30.341', '13:33:57.725', '13:35:27.926', '13:36:50.728', '13:38:11.359', '13:39:35.558', '13:40:59.715', '13:42:40.080', '13:44:05.946', '13:45:35.175', '13:47:10.598', '13:48:36.970', '13:50:06.573', '13:51:30.782', '13:53:02.024', '13:54:33.568', '13:56:04.668', '13:57:33.775', '13:59:07.054', '14:00:35.777', '14:02:04.084', '14:03:33.326', '14:05:02.156', '14:06:23.466', '14:07:43.695', '14:09:13.573', '14:10:47.182', '14:12:14.793', '14:13:51.881', '14:15:26.811', '14:16:56.024', '14:18:27.723', '14:19:56.036', '14:21:19.807', '14:22:48.972', '14:24:18.271', '14:25:42.936', '14:27:11.527', '14:28:38.791', '14:30:09.741', '14:31:50.700', '14:33:15.802', '14:34:51.611', '14:36:23.674', '14:37:53.237', '14:39:27.730', '14:41:00.481', '14:42:30.461', '14:43:57.347', '14:45:24.346', '14:46:53.081', '14:48:24.822', '14:50:03.146', '14:51:30.359', '14:53:06.176', '14:54:38.248', '14:56:12.358', '14:57:42.427', '14:59:13.640']
schedule = [timestamp(36000),timestamp(36082.53886710574),timestamp(36172.930753337954),timestamp(36267.46204173813),timestamp(36366.86702810958),timestamp(36445.043097968635),timestamp(36530.791441417736),timestamp(36619.74368792686),timestamp(36714.92309298996),timestamp(36794.763421237396),timestamp(36888.92756449378),timestamp(36975.54438321326),timestamp(37073.04593152398),timestamp(37160.35171305961),timestamp(37247.08509078814),timestamp(37341.46150837737),timestamp(37431.5904157228),timestamp(37523.59982985207),timestamp(37608.37584173063),timestamp(37697.46047940548),timestamp(37787.811791412285),timestamp(37875.42208008344),timestamp(37966.17848367174),timestamp(38058.322213861786),timestamp(38144.63253742977),timestamp(38236.692889140875),timestamp(38327.05816913843),timestamp(38422.77490516916),timestamp(38524.977324006606),timestamp(38626.74328795555),timestamp(38709.4126295279),timestamp(38793.84893603508),timestamp(38887.09125404747),timestamp(38978.78293610898),timestamp(39074.99082219473),timestamp(39161.79197630447),timestamp(39248.248933575334),timestamp(39351.303107326756),timestamp(39439.57985113962),timestamp(39528.05158215823),timestamp(39615.17867929271),timestamp(39705.89336766391),timestamp(39794.30166815842),timestamp(39887.48198517601),timestamp(39974.24445041166),timestamp(40063.21305791093),timestamp(40154.39940522488),timestamp(40250.58422838324),timestamp(40343.92536032223),timestamp(40435.18473637793),timestamp(40514.12796465815),timestamp(40602.74558398406),timestamp(40693.775970203955),timestamp(40775.75101796692),timestamp(40863.53382413712),timestamp(40946.21400922753),timestamp(41039.03866567226),timestamp(41124.596586274245),timestamp(41212.29078517448),timestamp(41305.041151307545),timestamp(41396.91238891223),timestamp(41486.80640258498),timestamp(41580.42308106568),timestamp(41665.238041685734),timestamp(41752.52429688452),timestamp(41843.8410602284),timestamp(41929.63675863589),timestamp(42028.00129104648),timestamp(42118.43604154263),timestamp(42214.95605431477),timestamp(42299.44238180673),timestamp(42385.369889557725),timestamp(42477.27929150934),timestamp(42569.65381214648),timestamp(42667.98154868427),timestamp(42752.7992413384),timestamp(42844.55880069908),timestamp(42934.68967749718),timestamp(43031.05712799626),timestamp(43125.967971911465),timestamp(43217.558890942215),timestamp(43308.45978222138),timestamp(43386.55473484843),timestamp(43472.332049842036),timestamp(43562.58969528742),timestamp(43652.116991264906),timestamp(43745.1344311146),timestamp(43831.67546041964),timestamp(43921.91267595863),timestamp(44011.14504316875),timestamp(44101.73084052481),timestamp(44191.00395005059),timestamp(44275.46106713841),timestamp(44370.39627063712),timestamp(44461.857078404995),timestamp(44558.29401019134),timestamp(44642.51675467354),timestamp(44732.44065692642),timestamp(44820.52185078982),timestamp(44916.10780378244),timestamp(45003.75717484092),timestamp(45084.49618041177),timestamp(45175.5888421791),timestamp(45267.04530509702),timestamp(45363.383771705594),timestamp(45461.393180915125),timestamp(45552.57699630306),timestamp(45645.98569983094),timestamp(45733.243580553644),timestamp(45823.30080967087),timestamp(45906.8015323334),timestamp(45998.771582192145),timestamp(46095.072078293335),timestamp(46181.92530484736),timestamp(46278.724396111735),timestamp(46363.50249638288),timestamp(46452.03414910711),timestamp(46546.575970335994),timestamp(46640.50166413443),timestamp(46735.984154859216),timestamp(46834.453430103385),timestamp(46924.008602324364),timestamp(47014.55894408752),timestamp(47108.115893192895),timestamp(47202.19822380266),timestamp(47291.974329571145),timestamp(47386.799734039094),timestamp(47482.31831928648),timestamp(47580.88922730062),timestamp(47665.235548495206),timestamp(47757.70200790406),timestamp(47849.17913578514),timestamp(47940.721131116145),timestamp(48029.87674833096),timestamp(48120.497895023895),timestamp(48210.800187238485),timestamp(48300.517899044826),timestamp(48401.68198602736),timestamp(48485.91645161836),timestamp(48573.504971584734),timestamp(48662.95827439135),timestamp(48750.34180302802),timestamp(48837.72552333324),timestamp(48927.92689974062),timestamp(49010.728383384936),timestamp(49091.35994835476),timestamp(49175.55880712404),timestamp(49259.71501339453),timestamp(49360.08072341987),timestamp(49445.946411941266),timestamp(49535.17552069973),timestamp(49630.59887734583),timestamp(49716.97094027214),timestamp(49806.573196908896),timestamp(49890.782196765904),timestamp(49982.02413885809),timestamp(50073.56800571419),timestamp(50164.668731060636),timestamp(50253.77514689926),timestamp(50347.054758905484),timestamp(50435.77771923636),timestamp(50524.08489127311),timestamp(50613.32672930827),timestamp(50702.15644548578),timestamp(50783.46694464078),timestamp(50863.695664171806),timestamp(50953.57350936345),timestamp(51047.182214426044),timestamp(51134.79386145146),timestamp(51231.88171687874),timestamp(51326.81107303742),timestamp(51416.02498144937),timestamp(51507.723175844476),timestamp(51596.036057011246),timestamp(51679.807365585526),timestamp(51768.97219808258),timestamp(51858.27164156702),timestamp(51942.936156884425),timestamp(52031.52720261535),timestamp(52118.79105733173),timestamp(52209.741676999445),timestamp(52310.70096533382),timestamp(52395.80224279189),timestamp(52491.61135758443),timestamp(52583.67424076333),timestamp(52673.237500523144),timestamp(52767.73021603832),timestamp(52860.48197700376),timestamp(52950.46111763436),timestamp(53037.347060836),timestamp(53124.34604360027),timestamp(53213.08198760988),timestamp(53304.82224305362),timestamp(53403.146157009614),timestamp(53490.35914173254),timestamp(53586.17662983716),timestamp(53678.24843082941),timestamp(53772.35868956134),timestamp(53862.427538207514),timestamp(53953.640090402994)]
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
# schedule_str = ['12:00:00', '12:00:31.616', '12:02:11.927', '12:03:51.015', '12:06:40.668', '12:07:23.868', '12:08:29.391', '12:09:30.514', '12:11:17.186', '12:17:35.485', '12:21:24.613', '12:22:37.697', '12:25:19.422', '12:29:18.464', '12:37:38.947', '12:40:21.850', '12:40:38.126', '12:40:49.278', '12:45:30.027', '12:54:07.373', '12:54:13.751', '12:54:18.809', '12:54:31.889', '12:55:23.594', '12:56:42.755', '12:57:23.188', '12:57:46.348']
schedule = [timestamp(43200),timestamp(43231.61624989072),timestamp(43331.92701464454),timestamp(43431.0154171305),timestamp(43600.668677274596),timestamp(43643.86840966014),timestamp(43709.39116231832),timestamp(43770.51486341322),timestamp(43877.18615523791),timestamp(44255.48529021909),timestamp(44484.61336480647),timestamp(44557.697402693375),timestamp(44719.422975828405),timestamp(44958.46494958456),timestamp(45458.947235304084),timestamp(45621.8502206823),timestamp(45638.12621420347),timestamp(45649.27838778412),timestamp(45930.02722142371),timestamp(46447.37380909078),timestamp(46453.7511030721),timestamp(46458.80960240492),timestamp(46471.88934278966),timestamp(46523.594064945784),timestamp(46602.75504564848),timestamp(46643.18878680131),timestamp(46666.34861137903)]
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
# schedule_str = ['12:00:00', '12:01:51.488', '12:04:03.308', '12:06:42.134', '12:08:54.642', '12:10:46.006', '12:13:00.604', '12:14:57.999', '12:16:59.345', '12:19:23.426', '12:21:29.494', '12:23:52.334', '12:26:00.249', '12:27:48.335', '12:29:38.214', '12:31:42.873', '12:33:33.795', '12:35:14.135', '12:37:21.726', '12:39:08.790', '12:40:57.801', '12:42:50.068', '12:44:49.433', '12:46:59.554', '12:48:57.790', '12:50:48.238', '12:52:42.547', '12:54:44.711', '12:56:28.025', '12:58:36.045']
schedule = [timestamp(43200),timestamp(43311.488014821145),timestamp(43443.30851611432),timestamp(43602.13465310154),timestamp(43734.64266555299),timestamp(43846.006474561305),timestamp(43980.60416557582),timestamp(44097.99952418034),timestamp(44219.345134972595),timestamp(44363.42698490896),timestamp(44489.49412536532),timestamp(44632.334367320764),timestamp(44760.24999459732),timestamp(44868.335945924235),timestamp(44978.214823219045),timestamp(45102.87329108043),timestamp(45213.79547171545),timestamp(45314.135329295714),timestamp(45441.72614111257),timestamp(45548.79039490342),timestamp(45657.801781887014),timestamp(45770.06855948174),timestamp(45889.433196270635),timestamp(46019.55490830313),timestamp(46137.79049918148),timestamp(46248.23870915526),timestamp(46362.54787529246),timestamp(46484.71172877369),timestamp(46588.02550328427),timestamp(46716.04597621399)]
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

# Instance of Node n6
cpu_ghz = 2.8
memory_mb = 32
storage_mb = 128
com_rad = 500.0
locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
node = Node_Edge("n6", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
nodes.append_node(node)

# Instance of Node n7
cpu_ghz = 2.8
memory_mb = 32
storage_mb = 128
com_rad = 500.0
locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
node = Node_Edge("n7", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
nodes.append_node(node)

# Instance of Node n8
cpu_ghz = 2.8
memory_mb = 32
storage_mb = 128
com_rad = 500.0
locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
node = Node_Edge("n8", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
nodes.append_node(node)

# Instance of Node n9
cpu_ghz = 2.8
memory_mb = 32
storage_mb = 128
com_rad = 500.0
locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
node = Node_Edge("n9", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
nodes.append_node(node)

# Instance of Node n10
cpu_ghz = 2.8
memory_mb = 32
storage_mb = 128
com_rad = 500.0
locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
node = Node_Edge("n10", locations, storage_mb, cpu_ghz, memory_mb, com_rad)
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

# Instance of Link l5
bandwidth = 3.3
node_pair = ['n5', 'n6']
nodes.get_node("n5").neighbours.append(("l5", "n6"))
link = Link_Edge("l5", node_pair, bandwidth)
links.append_link(link)

# Instance of Link l6
bandwidth = 3.3
node_pair = ['n5', 'n7']
nodes.get_node("n5").neighbours.append(("l6", "n7"))
link = Link_Edge("l6", node_pair, bandwidth)
links.append_link(link)

# Instance of Link l7
bandwidth = 3.3
node_pair = ['n6', 'n8']
nodes.get_node("n6").neighbours.append(("l7", "n8"))
link = Link_Edge("l7", node_pair, bandwidth)
links.append_link(link)

# Instance of Link l8
bandwidth = 3.3
node_pair = ['n6', 'n9']
nodes.get_node("n6").neighbours.append(("l8", "n9"))
link = Link_Edge("l8", node_pair, bandwidth)
links.append_link(link)

# Instance of Link l9
bandwidth = 3.3
node_pair = ['n8', 'n10']
nodes.get_node("n8").neighbours.append(("l9", "n10"))
link = Link_Edge("l9", node_pair, bandwidth)
links.append_link(link)

graph = Graph_G("G", nodes, links)
network_structure = NetworkStructure(graph, clients)