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
# schedule_str = ['12:00:00', '12:02:54.581', '12:18:14.443', '12:32:29.199', '12:39:35.535', '12:48:09.412', '12:52:21.523', '12:59:14.122']
schedule = [timestamp(43200),timestamp(43374.58100778712),timestamp(44294.44379780122),timestamp(45149.199003197406),timestamp(45575.53570180399),timestamp(46089.41241020302),timestamp(46341.52383990456),timestamp(46754.122362940325)]
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
# schedule_str = ['10:00:00', '10:01:29.310', '10:03:01.290', '10:04:21.600', '10:05:55.928', '10:07:32.842', '10:09:02.869', '10:10:38.874', '10:12:21.670', '10:13:59.450', '10:15:26.037', '10:16:50.424', '10:18:18.583', '10:19:44.691', '10:21:22.694', '10:22:49.238', '10:24:25.375', '10:25:59.694', '10:27:31.723', '10:29:04.883', '10:30:32.200', '10:32:10.372', '10:33:50.240', '10:35:22.491', '10:36:48.951', '10:38:24.287', '10:39:50.552', '10:41:12.940', '10:42:53.460', '10:44:31.212', '10:45:55.472', '10:47:19.706', '10:48:38.772', '10:50:13.002', '10:51:52.222', '10:53:25.850', '10:54:54.566', '10:56:29.377', '10:58:00.472', '10:59:42.460', '11:01:22.532', '11:02:54.091', '11:04:27.367', '11:05:53.788', '11:07:25.866', '11:09:03.134', '11:10:34.038', '11:12:09.105', '11:13:37.034', '11:15:01.449', '11:16:39.757', '11:18:20.804', '11:19:48.530', '11:21:19.893', '11:22:51.418', '11:24:19.908', '11:25:54.090', '11:27:20.318', '11:28:46.450', '11:30:25.194', '11:32:02.797', '11:33:37.871', '11:35:03.957', '11:36:28.341', '11:37:58.422', '11:39:31.652', '11:41:07.198', '11:42:39.599', '11:44:17.490', '11:45:47.763', '11:47:13.066', '11:48:42.421', '11:50:09.818', '11:51:41.727', '11:53:06.817', '11:54:42.720', '11:56:13.829', '11:57:46.878', '11:59:18.852', '12:00:49.659', '12:02:18.770', '12:03:41.681', '12:05:04.773', '12:06:36.778', '12:08:04.995', '12:09:39.071', '12:11:11.531', '12:12:41.545', '12:14:10.866', '12:15:37.165', '12:17:11.803', '12:18:43.557', '12:20:07.828', '12:21:34.518', '12:23:01.904', '12:24:31.535', '12:26:03.320', '12:27:37.198', '12:29:06.451', '12:30:29.968', '12:32:11.237', '12:33:33.782', '12:35:04.369', '12:36:37.940', '12:38:13.303', '12:39:43.472', '12:41:16.668', '12:42:45.152', '12:44:13.710', '12:45:45.830', '12:47:08.751', '12:48:31.656', '12:50:10.045', '12:51:41.391', '12:53:16.723', '12:54:41.658', '12:56:11.303', '12:57:37.048', '12:58:59.226', '13:00:31.320', '13:02:00.807', '13:03:36.817', '13:05:17.058', '13:06:46.164', '13:08:15.335', '13:09:48.732', '13:11:18.020', '13:12:54.475', '13:14:18.816', '13:15:46.240', '13:17:14.456', '13:18:41.269', '13:20:10.440', '13:21:31.921', '13:22:51.884', '13:24:27.285', '13:26:04.352', '13:27:29.552', '13:28:51.730', '13:30:19.963', '13:31:40.038', '13:33:08.822', '13:34:44.192', '13:36:22.378', '13:37:54.644', '13:39:30.385', '13:40:57.717', '13:42:28.479', '13:44:02.209', '13:45:33.103', '13:47:05.076', '13:48:36.067', '13:50:01.868', '13:51:28.606', '13:53:02.359', '13:54:37.519', '13:56:13.320', '13:57:39.897', '13:59:13.421', '14:00:46.206', '14:02:17.957', '14:03:46.151', '14:05:15.887', '14:06:51.288', '14:08:26.659', '14:10:01.376', '14:11:25.861', '14:12:50.948', '14:14:22.719', '14:15:49.869', '14:17:23.094', '14:18:51.446', '14:20:26.810', '14:21:55.561', '14:23:14.775', '14:24:49.113', '14:26:15.283', '14:27:36.387', '14:29:05.556', '14:30:43.068', '14:32:14.152', '14:33:38.423', '14:35:11.050', '14:36:34.179', '14:38:06.356', '14:39:37.235', '14:41:01.276', '14:42:31.126', '14:44:01.195', '14:45:39.909', '14:47:13.900', '14:48:49.147', '14:50:23.018', '14:51:46.531', '14:53:21.968', '14:54:56.322', '14:56:29.629', '14:57:54.381', '14:59:28.432']
schedule = [timestamp(36000),timestamp(36089.31054819652),timestamp(36181.29083868267),timestamp(36261.60027417418),timestamp(36355.92824134544),timestamp(36452.84210700714),timestamp(36542.86979076792),timestamp(36638.87462771184),timestamp(36741.6705591554),timestamp(36839.450923113196),timestamp(36926.037775996425),timestamp(37010.42479406172),timestamp(37098.583324242725),timestamp(37184.69111751104),timestamp(37282.6941955186),timestamp(37369.23894012703),timestamp(37465.3753183665),timestamp(37559.69472355306),timestamp(37651.72310112164),timestamp(37744.88319272105),timestamp(37832.200842191356),timestamp(37930.37266661947),timestamp(38030.24024662863),timestamp(38122.49134995182),timestamp(38208.9517520427),timestamp(38304.28770517356),timestamp(38390.55243293917),timestamp(38472.940304175354),timestamp(38573.460911135924),timestamp(38671.212352042974),timestamp(38755.47278633464),timestamp(38839.70689661091),timestamp(38918.772323982055),timestamp(39013.002190885505),timestamp(39112.22221287513),timestamp(39205.85049878918),timestamp(39294.56699232984),timestamp(39389.377479916504),timestamp(39480.4725123835),timestamp(39582.460678551564),timestamp(39682.53249688),timestamp(39774.091426342704),timestamp(39867.367298519246),timestamp(39953.78817962242),timestamp(40045.866221678596),timestamp(40143.13400800544),timestamp(40234.03817280249),timestamp(40329.10530416039),timestamp(40417.034448130595),timestamp(40501.44955277157),timestamp(40599.757946781334),timestamp(40700.80456838237),timestamp(40788.530505906994),timestamp(40879.89382873905),timestamp(40971.41888021813),timestamp(41059.908503337494),timestamp(41154.090595404276),timestamp(41240.318572962315),timestamp(41326.45091822037),timestamp(41425.19434833433),timestamp(41522.79773290726),timestamp(41617.87187935675),timestamp(41703.957494837225),timestamp(41788.341669002606),timestamp(41878.422081370154),timestamp(41971.65257635527),timestamp(42067.19869770681),timestamp(42159.599571507824),timestamp(42257.49033448406),timestamp(42347.76379874232),timestamp(42433.06657572648),timestamp(42522.42133901635),timestamp(42609.81888100703),timestamp(42701.72774599169),timestamp(42786.81788492545),timestamp(42882.720080963285),timestamp(42973.82975171301),timestamp(43066.87885920697),timestamp(43158.85246560322),timestamp(43249.65925236142),timestamp(43338.77084022713),timestamp(43421.681134782586),timestamp(43504.773261561844),timestamp(43596.77832799393),timestamp(43684.99544890819),timestamp(43779.071303727855),timestamp(43871.53192642956),timestamp(43961.54540259615),timestamp(44050.86699615828),timestamp(44137.16502511673),timestamp(44231.803149367996),timestamp(44323.55718606344),timestamp(44407.82822603897),timestamp(44494.51849889985),timestamp(44581.904364994276),timestamp(44671.535144858004),timestamp(44763.32011334664),timestamp(44857.19899774522),timestamp(44946.45150898075),timestamp(45029.968830017024),timestamp(45131.237764189624),timestamp(45213.7829392905),timestamp(45304.36908449057),timestamp(45397.94085282204),timestamp(45493.30310724177),timestamp(45583.47222262771),timestamp(45676.66880380192),timestamp(45765.152148758185),timestamp(45853.710237022984),timestamp(45945.83078196617),timestamp(46028.75122798518),timestamp(46111.656365822964),timestamp(46210.04576640782),timestamp(46301.39169563744),timestamp(46396.72337316566),timestamp(46481.658413238816),timestamp(46571.303730415006),timestamp(46657.048086510076),timestamp(46739.22618033688),timestamp(46831.320482051226),timestamp(46920.80703877709),timestamp(47016.81701297103),timestamp(47117.0583349686),timestamp(47206.1645801778),timestamp(47295.335829014475),timestamp(47388.73222165605),timestamp(47478.020861574),timestamp(47574.47541231427),timestamp(47658.81622574708),timestamp(47746.24073207521),timestamp(47834.4567497309),timestamp(47921.26982478943),timestamp(48010.44038161175),timestamp(48091.92178480549),timestamp(48171.88445899518),timestamp(48267.285757824575),timestamp(48364.3529017066),timestamp(48449.55206192453),timestamp(48531.73089543489),timestamp(48619.96339532636),timestamp(48700.03876811673),timestamp(48788.822135809416),timestamp(48884.19238482336),timestamp(48982.37819939108),timestamp(49074.644734491456),timestamp(49170.38543078063),timestamp(49257.71748580165),timestamp(49348.47965244624),timestamp(49442.209797276504),timestamp(49533.10348305735),timestamp(49625.076327214825),timestamp(49716.0677866155),timestamp(49801.86872447879),timestamp(49888.60689019302),timestamp(49982.35950216893),timestamp(50077.51923966075),timestamp(50173.32043497905),timestamp(50259.897923470715),timestamp(50353.421966790316),timestamp(50446.20607528684),timestamp(50537.95718326648),timestamp(50626.15197114023),timestamp(50715.887294063585),timestamp(50811.28877479267),timestamp(50906.65997826357),timestamp(51001.37672846373),timestamp(51085.86145591052),timestamp(51170.948048655664),timestamp(51262.71981412695),timestamp(51349.86975240553),timestamp(51443.0941390351),timestamp(51531.44633117909),timestamp(51626.810926457416),timestamp(51715.56124763395),timestamp(51794.775783624),timestamp(51889.11317142683),timestamp(51975.2836915973),timestamp(52056.387208294065),timestamp(52145.55626537681),timestamp(52243.06898899297),timestamp(52334.15235643251),timestamp(52418.42342100402),timestamp(52511.05037320727),timestamp(52594.17962787748),timestamp(52686.35610650807),timestamp(52777.23598790804),timestamp(52861.27625600219),timestamp(52951.12624045408),timestamp(53041.19558075978),timestamp(53139.90903749784),timestamp(53233.90056499857),timestamp(53329.147196187885),timestamp(53423.01881791611),timestamp(53506.5314180032),timestamp(53601.96858365948),timestamp(53696.322865288224),timestamp(53789.62998619536),timestamp(53874.381327562136),timestamp(53968.43257381154)]
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
# schedule_str = ['12:00:00', '12:00:55.530', '12:01:01.616', '12:01:30.597', '12:04:29.191', '12:05:29.082', '12:10:11.490', '12:15:27.231', '12:27:00.891', '12:27:51.169', '12:28:46.547', '12:34:57.736', '12:37:00.610', '12:38:57.083', '12:40:16.828', '12:45:46.658', '12:46:29.429', '12:47:57.200', '12:54:25.466', '12:54:34.859']
schedule = [timestamp(43200),timestamp(43255.53029898591),timestamp(43261.61661427115),timestamp(43290.597398116864),timestamp(43469.191421264986),timestamp(43529.08286853382),timestamp(43811.49052465124),timestamp(44127.23155698656),timestamp(44820.89167786055),timestamp(44871.16902423958),timestamp(44926.547032057264),timestamp(45297.73621806521),timestamp(45420.610009821976),timestamp(45537.083701369964),timestamp(45616.82854651216),timestamp(45946.65803512324),timestamp(45989.429686736716),timestamp(46077.20094513641),timestamp(46465.46649026241),timestamp(46474.85932091051)]
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
# schedule_str = ['12:00:00', '12:02:03.006', '12:04:17.426', '12:06:20.302', '12:08:07.507', '12:10:18.020', '12:12:05.935', '12:14:11.613', '12:16:20.942', '12:18:04.439', '12:20:01.276', '12:21:46.681', '12:23:42.705', '12:25:33.740', '12:27:31.996', '12:29:23.442', '12:31:31.055', '12:32:57.407', '12:34:35.285', '12:36:30.453', '12:38:17.530', '12:40:34.077', '12:42:31.865', '12:44:29.678', '12:46:40.400', '12:48:36.209', '12:50:40.619', '12:52:42.970', '12:54:42.957', '12:56:54.432', '12:58:35.856']
schedule = [timestamp(43200),timestamp(43323.0066156295),timestamp(43457.426903771),timestamp(43580.302490640664),timestamp(43687.50783908833),timestamp(43818.02025581284),timestamp(43925.935378478374),timestamp(44051.61304170029),timestamp(44180.94252623998),timestamp(44284.43992146909),timestamp(44401.276782078174),timestamp(44506.681157955536),timestamp(44622.705051674784),timestamp(44733.74097490376),timestamp(44851.99612209173),timestamp(44963.442769816036),timestamp(45091.05507672878),timestamp(45177.407386020066),timestamp(45275.28586722763),timestamp(45390.45355340813),timestamp(45497.53047662053),timestamp(45634.077235629695),timestamp(45751.86549411587),timestamp(45869.678074838),timestamp(46000.400766558916),timestamp(46116.20947520327),timestamp(46240.619817862),timestamp(46362.97031613013),timestamp(46482.957317292414),timestamp(46614.43235306858),timestamp(46715.85616498222)]
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