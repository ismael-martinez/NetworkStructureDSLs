from networkStructure import *
import numpy as np
from networkUtil import * 

#from CodeGen.Python.networkStructure import *

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
		return self.cpu_ghz

# Defines the attribute that represents the radius (in metres), if any.
	def get_radius(self):
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
		return self.storage_mb

# Defines the attribute that represents the radius (in metres), if any.
	def get_radius(self):
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
# schedule_str = ['12:00:00', '12:08:57.310', '12:14:29.466', '12:26:24.385', '12:28:07.965', '12:38:47.870', '12:53:25.101', '12:54:03.063']
schedule = [timestamp(43200),timestamp(43737.3107876411),timestamp(44069.466384297906),timestamp(44784.385689635805),timestamp(44887.96522185529),timestamp(45527.87069624907),timestamp(46405.10157241229),timestamp(46443.06370302304)]
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
# schedule_str = ['10:00:00', '10:01:27.556', '10:02:59.476', '10:04:17.369', '10:05:37.731', '10:07:01.514', '10:08:30.493', '10:09:53.602', '10:11:23.601', '10:12:49.121', '10:14:19.809', '10:15:43.911', '10:17:14.240', '10:18:39.910', '10:20:13.096', '10:21:45.201', '10:23:09.996', '10:24:43.013', '10:26:13.711', '10:27:35.450', '10:29:12.100', '10:30:42.991', '10:32:12.168', '10:33:33.748', '10:35:07.214', '10:36:38.555', '10:38:11.503', '10:39:40.822', '10:41:04.635', '10:42:29.905', '10:44:13.125', '10:45:44.613', '10:47:19.313', '10:48:47.334', '10:50:20.538', '10:51:52.283', '10:53:13.125', '10:54:44.766', '10:56:14.377', '10:57:55.234', '10:59:25.036', '11:00:57.216', '11:02:31.807', '11:03:57.297', '11:05:33.329', '11:06:58.734', '11:08:18.420', '11:09:49.056', '11:11:09.835', '11:12:34.394', '11:14:13.565', '11:15:47.976', '11:17:13.862', '11:18:47.398', '11:20:16.168', '11:21:55.263', '11:23:34.366', '11:25:04.841', '11:26:35.979', '11:28:05.776', '11:29:31.177', '11:30:57.504', '11:32:32.698', '11:34:06.205', '11:35:31.619', '11:37:06.588', '11:38:38.698', '11:40:08.140', '11:41:38.513', '11:43:02.639', '11:44:39.596', '11:46:07.813', '11:47:31.527', '11:49:00.469', '11:50:36.596', '11:52:10.706', '11:53:34.328', '11:55:03.730', '11:56:33.031', '11:57:57.126', '11:59:26.446', '12:00:50.094', '12:02:11.683', '12:03:31.039', '12:04:59.888', '12:06:38.056', '12:08:07.783', '12:09:35.010', '12:11:03.366', '12:12:34.516', '12:14:01.147', '12:15:35.500', '12:17:07.607', '12:18:40.519', '12:20:22.678', '12:21:58.707', '12:23:28.153', '12:24:49.038', '12:26:14.187', '12:27:50.152', '12:29:19.020', '12:30:53.296', '12:32:24.020', '12:33:57.025', '12:35:23.153', '12:36:50.721', '12:38:16.883', '12:39:53.862', '12:41:27.577', '12:43:06.747', '12:44:41.365', '12:46:17.878', '12:47:51.889', '12:49:16.861', '12:50:39.259', '12:52:12.551', '12:53:37.229', '12:55:04.113', '12:56:36.685', '12:58:01.359', '12:59:29.589', '13:00:56.037', '13:02:28.945', '13:03:56.889', '13:05:28.582', '13:06:57.604', '13:08:31.992', '13:10:04.294', '13:11:39.833', '13:13:08.493', '13:14:32.671', '13:16:04.996', '13:17:24.517', '13:18:49.993', '13:20:17.736', '13:21:35.683', '13:22:57.795', '13:24:22.456', '13:25:54.370', '13:27:21.662', '13:28:48.028', '13:30:27.295', '13:31:48.413', '13:33:13.107', '13:34:50.547', '13:36:22.103', '13:37:53.071', '13:39:20.492', '13:40:56.156', '13:42:24.348', '13:43:58.012', '13:45:37.686', '13:47:01.829', '13:48:29.719', '13:50:03.057', '13:51:41.672', '13:53:14.963', '13:54:51.710', '13:56:26.416', '13:57:44.811', '13:59:11.447', '14:00:58.644', '14:02:34.492', '14:04:06.235', '14:05:34.247', '14:07:07.278', '14:08:37.908', '14:10:09.469', '14:11:38.899', '14:13:10.287', '14:14:43.397', '14:16:15.686', '14:17:48.214', '14:19:15.266', '14:20:45.662', '14:22:17.690', '14:23:46.816', '14:25:13.934', '14:26:48.719', '14:28:22.981', '14:30:00.057', '14:31:25.515', '14:32:54.792', '14:34:18.953', '14:35:52.414', '14:37:12.232', '14:38:44.294', '14:40:10.474', '14:41:52.596', '14:43:22.234', '14:44:54.886', '14:46:26.308', '14:48:00.399', '14:49:27.302', '14:50:49.535', '14:52:20.658', '14:53:48.638', '14:55:25.292', '14:56:54.260', '14:58:18.931', '14:59:42.345']
schedule = [timestamp(36000),timestamp(36087.556997637075),timestamp(36179.47658628837),timestamp(36257.36987415755),timestamp(36337.73195026491),timestamp(36421.51442784864),timestamp(36510.493136851386),timestamp(36593.60266164888),timestamp(36683.6019383647),timestamp(36769.12160655743),timestamp(36859.809419804056),timestamp(36943.91128981337),timestamp(37034.24068821062),timestamp(37119.91021515216),timestamp(37213.09624761402),timestamp(37305.20126288947),timestamp(37389.996214802064),timestamp(37483.01331826783),timestamp(37573.711168660804),timestamp(37655.450537425735),timestamp(37752.10079402825),timestamp(37842.991349957636),timestamp(37932.168477768115),timestamp(38013.74826759812),timestamp(38107.21470233342),timestamp(38198.55592263912),timestamp(38291.50347081603),timestamp(38380.82246380982),timestamp(38464.635766026855),timestamp(38549.90507052338),timestamp(38653.12540193395),timestamp(38744.61382710994),timestamp(38839.31305495075),timestamp(38927.33450965769),timestamp(39020.53872544129),timestamp(39112.28368137918),timestamp(39193.12570399659),timestamp(39284.7668816031),timestamp(39374.37753720828),timestamp(39475.23489684303),timestamp(39565.03627293986),timestamp(39657.2165721525),timestamp(39751.80721547864),timestamp(39837.29778320592),timestamp(39933.32917370166),timestamp(40018.73467710916),timestamp(40098.42091929524),timestamp(40189.05661377054),timestamp(40269.83599150689),timestamp(40354.39486770461),timestamp(40453.56534243975),timestamp(40547.97603681983),timestamp(40633.862940431405),timestamp(40727.39889275407),timestamp(40816.16822833774),timestamp(40915.26341432705),timestamp(41014.366081580105),timestamp(41104.84134793705),timestamp(41195.97987945278),timestamp(41285.77690114091),timestamp(41371.17775271357),timestamp(41457.504685406144),timestamp(41552.69847087925),timestamp(41646.20511560876),timestamp(41731.61962166),timestamp(41826.588790820715),timestamp(41918.69849095223),timestamp(42008.1402917004),timestamp(42098.51312173696),timestamp(42182.63966211944),timestamp(42279.59664535898),timestamp(42367.813156006785),timestamp(42451.527692431584),timestamp(42540.46934963459),timestamp(42636.59673414056),timestamp(42730.706785615665),timestamp(42814.328404320455),timestamp(42903.73035365327),timestamp(42993.03121574101),timestamp(43077.12676525556),timestamp(43166.44646739585),timestamp(43250.09401988961),timestamp(43331.68396477908),timestamp(43411.039104978394),timestamp(43499.8880240825),timestamp(43598.05604853759),timestamp(43687.78317741445),timestamp(43775.010305648444),timestamp(43863.366614039645),timestamp(43954.51670407596),timestamp(44041.147503742955),timestamp(44135.50040451968),timestamp(44227.607953771265),timestamp(44320.51900716994),timestamp(44422.67866618775),timestamp(44518.70702616866),timestamp(44608.15399344591),timestamp(44689.03879607727),timestamp(44774.187084168196),timestamp(44870.15248369597),timestamp(44959.02093789759),timestamp(45053.29657705309),timestamp(45144.020615400266),timestamp(45237.02576004075),timestamp(45323.15377598588),timestamp(45410.7212356591),timestamp(45496.88364543072),timestamp(45593.86262778448),timestamp(45687.57707687969),timestamp(45786.747152110314),timestamp(45881.36559616659),timestamp(45977.878558768745),timestamp(46071.889225220555),timestamp(46156.861818722246),timestamp(46239.259455838466),timestamp(46332.55166487274),timestamp(46417.22934391741),timestamp(46504.11372739864),timestamp(46596.68500376227),timestamp(46681.35988706058),timestamp(46769.58949683836),timestamp(46856.03710983576),timestamp(46948.94569410377),timestamp(47036.88922171942),timestamp(47128.58254859919),timestamp(47217.60484943791),timestamp(47311.99282325041),timestamp(47404.294189016444),timestamp(47499.83326970118),timestamp(47588.49386416012),timestamp(47672.67118048709),timestamp(47764.99622675564),timestamp(47844.517789779995),timestamp(47929.99372142963),timestamp(48017.73663213956),timestamp(48095.68312917984),timestamp(48177.79591370059),timestamp(48262.45643068362),timestamp(48354.37030440032),timestamp(48441.662362843526),timestamp(48528.028879566715),timestamp(48627.29571561089),timestamp(48708.413592656536),timestamp(48793.1070900546),timestamp(48890.54799589103),timestamp(48982.1030447047),timestamp(49073.07149754862),timestamp(49160.492125633675),timestamp(49256.15606636924),timestamp(49344.3486251948),timestamp(49438.01272196872),timestamp(49537.68690207089),timestamp(49621.82915932415),timestamp(49709.71927474986),timestamp(49803.05765213227),timestamp(49901.672992520296),timestamp(49994.963909368445),timestamp(50091.71053735337),timestamp(50186.41614603355),timestamp(50264.81192355259),timestamp(50351.44780319337),timestamp(50458.644833634666),timestamp(50554.492256734105),timestamp(50646.23511984673),timestamp(50734.247271515145),timestamp(50827.27842357199),timestamp(50917.90824449873),timestamp(51009.46936794256),timestamp(51098.89976653796),timestamp(51190.28708659619),timestamp(51283.39765538613),timestamp(51375.68628277761),timestamp(51468.214655787284),timestamp(51555.266649444966),timestamp(51645.662591799424),timestamp(51737.69083323651),timestamp(51826.816471675134),timestamp(51913.93424149773),timestamp(52008.71954761567),timestamp(52102.98155677426),timestamp(52200.057341178726),timestamp(52285.515988677995),timestamp(52374.79241307388),timestamp(52458.95396899368),timestamp(52552.414600965596),timestamp(52632.23270400407),timestamp(52724.29457076884),timestamp(52810.47472207853),timestamp(52912.59629469349),timestamp(53002.23407667607),timestamp(53094.886590002105),timestamp(53186.30815391672),timestamp(53280.399025051476),timestamp(53367.30219249776),timestamp(53449.535565725055),timestamp(53540.65897236583),timestamp(53628.63873449708),timestamp(53725.292532644264),timestamp(53814.260490972185),timestamp(53898.931249796064),timestamp(53982.34572834076)]
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
# schedule_str = ['12:00:00', '12:01:53.023', '12:02:42.161', '12:02:51.099', '12:03:19.410', '12:03:48.110', '12:04:01.495', '12:05:03.505', '12:11:24.236', '12:14:07.935', '12:15:09.454', '12:17:39.993', '12:23:05.295', '12:25:48.561', '12:28:37.866', '12:37:30.266', '12:40:53.115', '12:42:30.992', '12:42:59.046', '12:44:12.597', '12:46:11.622', '12:49:04.961', '12:50:02.468', '12:51:23.768', '12:54:06.640', '12:56:04.890', '12:58:57.233']
schedule = [timestamp(43200),timestamp(43313.023271944745),timestamp(43362.1614704279),timestamp(43371.099966805974),timestamp(43399.41003125702),timestamp(43428.11014851624),timestamp(43441.49596028357),timestamp(43503.50579608204),timestamp(43884.236004625556),timestamp(44047.93526979792),timestamp(44109.45413990226),timestamp(44259.99327575486),timestamp(44585.2951492729),timestamp(44748.56115947512),timestamp(44917.86694359651),timestamp(45450.26648319654),timestamp(45653.11589981488),timestamp(45750.992932888155),timestamp(45779.04659263644),timestamp(45852.59744462017),timestamp(45971.6221025867),timestamp(46144.96147844304),timestamp(46202.46806124465),timestamp(46283.76856340159),timestamp(46446.64083236825),timestamp(46564.89023391758),timestamp(46737.23366735587)]
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
# schedule_str = ['12:00:00', '12:01:53.391', '12:03:56.979', '12:06:15.250', '12:08:24.951', '12:10:09.595', '12:12:23.450', '12:14:27.922', '12:16:25.353', '12:18:19.213', '12:20:26.333', '12:22:36.431', '12:25:01.769', '12:27:09.498', '12:29:06.461', '12:31:11.125', '12:33:13.666', '12:35:25.118', '12:37:16.807', '12:39:15.907', '12:41:13.273', '12:43:30.316', '12:45:33.750', '12:47:11.736', '12:49:00.748', '12:50:23.557', '12:52:14.417', '12:54:28.509', '12:55:45.474', '12:57:30.731', '12:59:19.927']
schedule = [timestamp(43200),timestamp(43313.39194010937),timestamp(43436.97951396854),timestamp(43575.250675366406),timestamp(43704.95130569715),timestamp(43809.59521338833),timestamp(43943.45057993863),timestamp(44067.92241947617),timestamp(44185.35322053916),timestamp(44299.2137017953),timestamp(44426.33346305593),timestamp(44556.43155110609),timestamp(44701.769908976006),timestamp(44829.49811829683),timestamp(44946.46168443384),timestamp(45071.125261051275),timestamp(45193.66609842344),timestamp(45325.11831524287),timestamp(45436.80714959735),timestamp(45555.90788682549),timestamp(45673.273411362396),timestamp(45810.316892587805),timestamp(45933.75042752851),timestamp(46031.73693405927),timestamp(46140.74817735098),timestamp(46223.55730994212),timestamp(46334.41720159481),timestamp(46468.50943825214),timestamp(46545.47491632215),timestamp(46650.73141530675),timestamp(46759.92771432378)]
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