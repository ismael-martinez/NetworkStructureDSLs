#from networkStructure import *
import numpy as np

from CodeGen.Python.networkStructure import *

class Client_IoT(ClientAbstract):
	def __init__(self, id, schedule, locations, radius, fileSize_mb = 0, localCPU_ghz = 0.0, localProcessing_ms = 0, memoryReq_mb = 0, storageReq_mb = 0)
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
		self.paths = depthFirstSearch(self.nodes)

# Link classes for specific attribute set
class Node_Edge(NodeAbstract):
	def __init__(self,id,locations,radius,storage_mb = 0,cpu_ghz = 0.0,memory_mb = 0):
		self.id = id
		self.locations = locations
		self.radius = radius
		self.storage_mb = storage_mb
		self.cpu_ghz = cpu_ghz
		self.memory_mb = memory_mb
		self.neighbours = []
	def service_rate(self):
		return self.attributes.cpu_ghz
	def list_attributes(self):
		return ['storage_mb','cpu_ghz','memory_mb']

class Node_Dormant(NodeAbstract):
	def __init__(self,id,locations,radius,storage_mb = 0):
		self.id = id
		self.locations = locations
		self.radius = radius
		self.storage_mb = storage_mb
		self.neighbours = []
	def service_rate(self):
		return self.attributes.storage_mb
	def list_attributes(self):
		return ['storage_mb']


# Link classes for specific attribute set
class Link_Edge(LinkAbstract):
	def __init__(self,id,node_pair,bandwidth = 0.0):
		self.id = id
		self.node_pair = node_pair
		self.bandwidth = bandwidth
	def list_attributes(self):
		return ['bandwidth']

## Client_IoT instances ## 

clients = {}

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
clients["t1"] = Client_IoT("t1", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)

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
clients["t2"] = Client_IoT("t2", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)

# Instance of Client t3
fileSize_mb = 85
localCPU_ghz = 4.6
localProcessing_ms = 32
memoryReq_mb = 24
storageReq_mb = 0
radius = 300.0
locations = []
locations.append(Locations(45.465660701358146, -73.74562408880354, 1))
# schedule_str = ['12:00:00', '12:02:18.365', '12:02:45.461', '12:04:32.461', '12:15:17.155', '12:23:00.340', '12:28:20.234', '12:32:33.276', '12:56:20.782']
schedule = [timestamp(43200),timestamp(43338.36525495193),timestamp(43365.46180825798),timestamp(43472.461250336164),timestamp(44117.15542552115),timestamp(44580.3407564042),timestamp(44900.234896958595),timestamp(45153.27610028016),timestamp(46580.78299155652)]
clients["t3"] = Client_IoT("t3", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)

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
# schedule_str = ['10:00:00', '10:01:37.352', '10:03:02.266', '10:04:33.281', '10:06:08.010', '10:07:33.505', '10:09:09.945', '10:10:37.934', '10:11:59.909', '10:13:36.407', '10:15:05.867', '10:16:29.453', '10:18:05.160', '10:19:38.513', '10:21:05.623', '10:22:32.739', '10:24:07.441', '10:25:36.898', '10:27:08.395', '10:28:30.070', '10:30:00.911', '10:31:27.925', '10:32:57.641', '10:34:28.828', '10:36:05.233', '10:37:36.077', '10:39:07.289', '10:40:38.774', '10:42:04.158', '10:43:30.065', '10:45:01.565', '10:46:26.053', '10:48:00.055', '10:49:32.068', '10:51:02.844', '10:52:26.317', '10:53:52.433', '10:55:19.661', '10:56:53.928', '10:58:28.420', '10:59:53.198', '11:01:28.976', '11:02:57.247', '11:04:24.860', '11:05:54.905', '11:07:27.196', '11:09:04.645', '11:10:35.066', '11:12:02.250', '11:13:30.569', '11:14:56.492', '11:16:27.560', '11:17:54.802', '11:19:23.330', '11:20:51.330', '11:22:16.912', '11:23:51.992', '11:25:25.967', '11:26:51.554', '11:28:20.745', '11:29:49.706', '11:31:14.442', '11:32:45.818', '11:34:21.743', '11:35:47.595', '11:37:22.144', '11:39:00.649', '11:40:29.518', '11:41:58.605', '11:43:27.750', '11:44:56.926', '11:46:25.620', '11:47:56.388', '11:49:32.848', '11:50:54.529', '11:52:19.434', '11:53:48.905', '11:55:21.492', '11:56:49.299', '11:58:23.331', '11:59:49.652', '12:01:25.844', '12:02:58.360', '12:04:18.659', '12:06:03.079', '12:07:39.928', '12:09:08.213', '12:10:43.697', '12:12:17.258', '12:13:45.799', '12:15:12.740', '12:16:45.351', '12:18:20.594', '12:19:51.033', '12:21:25.052', '12:22:53.799', '12:24:24.719', '12:25:48.729', '12:27:15.807', '12:28:43.968', '12:30:19.063', '12:31:53.035', '12:33:22.813', '12:34:58.813', '12:36:32.848', '12:37:57.977', '12:39:17.391', '12:40:53.030', '12:42:18.904', '12:43:47.543', '12:45:23.867', '12:46:41.759', '12:48:10.090', '12:49:45.725', '12:51:11.990', '12:52:48.062', '12:54:26.217', '12:55:53.561', '12:57:32.564', '12:59:04.795', '13:00:42.220', '13:02:05.800', '13:03:37.605', '13:05:17.908', '13:06:50.276', '13:08:21.722', '13:09:50.855', '13:11:19.626', '13:12:45.621', '13:14:11.455', '13:15:42.870', '13:17:21.222', '13:18:52.580', '13:20:30.345', '13:22:04.448', '13:23:31.088', '13:25:00.893', '13:26:31.120', '13:27:53.475', '13:29:21.815', '13:30:58.296', '13:32:31.879', '13:34:01.625', '13:35:35.313', '13:37:14.245', '13:38:59.630', '13:40:34.599', '13:41:56.755', '13:43:29.800', '13:45:04.453', '13:46:30.244', '13:47:50.833', '13:49:22.623', '13:50:55.558', '13:52:28.246', '13:53:59.179', '13:55:24.327', '13:56:42.525', '13:58:09.534', '13:59:26.008', '14:01:01.739', '14:02:32.657', '14:04:00.307', '14:05:27.102', '14:06:55.410', '14:08:20.775', '14:09:43.453', '14:11:20.515', '14:12:46.030', '14:14:12.205', '14:15:34.867', '14:17:04.159', '14:18:31.432', '14:20:08.174', '14:21:40.729', '14:23:12.904', '14:24:47.340', '14:26:24.296', '14:27:57.761', '14:29:23.187', '14:30:47.179', '14:32:14.999', '14:33:43.344', '14:35:09.314', '14:36:34.967', '14:38:04.608', '14:39:30.163', '14:40:55.791', '14:42:29.357', '14:44:00.599', '14:45:32.959', '14:47:03.795', '14:48:39.051', '14:50:16.892', '14:51:51.360', '14:53:20.722', '14:54:45.236', '14:56:16.401', '14:57:38.983', '14:59:09.980']
schedule = [timestamp(36000),timestamp(36097.352189420824),timestamp(36182.26699582102),timestamp(36273.28167159032),timestamp(36368.01032294342),timestamp(36453.50560636343),timestamp(36549.945836271116),timestamp(36637.93490834782),timestamp(36719.9090063654),timestamp(36816.40777216527),timestamp(36905.867241340544),timestamp(36989.45339425768),timestamp(37085.16050426803),timestamp(37178.513935252144),timestamp(37265.62378298343),timestamp(37352.739349891504),timestamp(37447.441741034156),timestamp(37536.89869411099),timestamp(37628.39524345305),timestamp(37710.07098733878),timestamp(37800.91132635998),timestamp(37887.92517931784),timestamp(37977.64162842594),timestamp(38068.828361240965),timestamp(38165.23316198008),timestamp(38256.077308890155),timestamp(38347.28910410654),timestamp(38438.77422168217),timestamp(38524.158969003314),timestamp(38610.06562830512),timestamp(38701.565504055514),timestamp(38786.05376097645),timestamp(38880.05556275135),timestamp(38972.0685861986),timestamp(39062.84402430253),timestamp(39146.317753625306),timestamp(39232.433914019966),timestamp(39319.6617595815),timestamp(39413.92805360646),timestamp(39508.42076217224),timestamp(39593.19803791533),timestamp(39688.976899714864),timestamp(39777.247423320834),timestamp(39864.86073637845),timestamp(39954.905491806036),timestamp(40047.19620498793),timestamp(40144.64566011219),timestamp(40235.06668775187),timestamp(40322.25075967414),timestamp(40410.56989974341),timestamp(40496.49214264561),timestamp(40587.56092072193),timestamp(40674.80203122771),timestamp(40763.33018380264),timestamp(40851.3305629668),timestamp(40936.91251281876),timestamp(41031.99255705473),timestamp(41125.967283726946),timestamp(41211.55484314508),timestamp(41300.745134301076),timestamp(41389.70653769521),timestamp(41474.44242994563),timestamp(41565.818339912636),timestamp(41661.7431743044),timestamp(41747.595744650076),timestamp(41842.14468791976),timestamp(41940.64951485754),timestamp(42029.51842562314),timestamp(42118.6056246973),timestamp(42207.75074503298),timestamp(42296.92668570457),timestamp(42385.62025012842),timestamp(42476.388225372386),timestamp(42572.84805882788),timestamp(42654.52964847737),timestamp(42739.43498476064),timestamp(42828.90516798711),timestamp(42921.49257138074),timestamp(43009.29901756862),timestamp(43103.3319193089),timestamp(43189.65213620587),timestamp(43285.844292153),timestamp(43378.36081875529),timestamp(43458.65991742463),timestamp(43563.079353493675),timestamp(43659.92891249817),timestamp(43748.2139527446),timestamp(43843.697949181435),timestamp(43937.25826005459),timestamp(44025.79952231846),timestamp(44112.74069041761),timestamp(44205.35197142094),timestamp(44300.59479348317),timestamp(44391.03327976757),timestamp(44485.05209339065),timestamp(44573.799485340525),timestamp(44664.71904841447),timestamp(44748.729770040474),timestamp(44835.80797797846),timestamp(44923.96856663926),timestamp(45019.063564221586),timestamp(45113.035401952635),timestamp(45202.813787334635),timestamp(45298.81345074863),timestamp(45392.84815790389),timestamp(45477.97701068591),timestamp(45557.3919449692),timestamp(45653.03066879669),timestamp(45738.90458927438),timestamp(45827.5434873061),timestamp(45923.867319630925),timestamp(46001.75934670243),timestamp(46090.09088033356),timestamp(46185.725565902576),timestamp(46271.99096026074),timestamp(46368.06215454129),timestamp(46466.217260587575),timestamp(46553.56160089943),timestamp(46652.56473485637),timestamp(46744.7957920062),timestamp(46842.220700800026),timestamp(46925.80072327142),timestamp(47017.60565849534),timestamp(47117.90897826258),timestamp(47210.27685005468),timestamp(47301.72296805771),timestamp(47390.85564257576),timestamp(47479.62698890365),timestamp(47565.621381495184),timestamp(47651.45537225816),timestamp(47742.870175302676),timestamp(47841.22216354631),timestamp(47932.580119700775),timestamp(48030.34563485882),timestamp(48124.44894703864),timestamp(48211.088579593066),timestamp(48300.893657794746),timestamp(48391.1205387782),timestamp(48473.47521727488),timestamp(48561.81565553687),timestamp(48658.296109313276),timestamp(48751.8795189776),timestamp(48841.62592118501),timestamp(48935.31334001481),timestamp(49034.24530703702),timestamp(49139.6300535938),timestamp(49234.599704720655),timestamp(49316.75558588276),timestamp(49409.80087324988),timestamp(49504.4534710635),timestamp(49590.244041726524),timestamp(49670.83350778238),timestamp(49762.62391132333),timestamp(49855.558305594495),timestamp(49948.2468865367),timestamp(50039.1799959523),timestamp(50124.32731033985),timestamp(50202.5250523108),timestamp(50289.53437163681),timestamp(50366.0086815492),timestamp(50461.739467392355),timestamp(50552.65717171964),timestamp(50640.3071558097),timestamp(50727.10256387195),timestamp(50815.41016023311),timestamp(50900.775687812595),timestamp(50983.45357327403),timestamp(51080.515167434896),timestamp(51166.03065650633),timestamp(51252.205209648244),timestamp(51334.86793239455),timestamp(51424.15963992118),timestamp(51511.43278193237),timestamp(51608.17476955401),timestamp(51700.729641198544),timestamp(51792.904198035125),timestamp(51887.34001728337),timestamp(51984.29653813537),timestamp(52077.761033474395),timestamp(52163.187139353606),timestamp(52247.179481660496),timestamp(52334.999085983145),timestamp(52423.34489808949),timestamp(52509.31485887366),timestamp(52594.967470629286),timestamp(52684.60896003227),timestamp(52770.16302492355),timestamp(52855.79110035378),timestamp(52949.357963606235),timestamp(53040.599415304496),timestamp(53132.95997574556),timestamp(53223.79543011398),timestamp(53319.05106010942),timestamp(53416.89206223536),timestamp(53511.36013790543),timestamp(53600.72271341067),timestamp(53685.23692571303),timestamp(53776.401926831095),timestamp(53858.98311988179),timestamp(53949.980441662425)]
clients["t4"] = Client_IoT("t4", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)

# Instance of Client t5
fileSize_mb = 543
localCPU_ghz = 4.7
localProcessing_ms = 542
memoryReq_mb = 13
storageReq_mb = 0
radius = np.infty
locations = []
locations.append(Locations(45.46570138080979, -73.74552954093576, 1))
# schedule_str = ['12:00:00', '12:01:22.948', '12:06:14.418', '12:07:56.847', '12:09:16.483', '12:10:59.247', '12:12:01.362', '12:19:31.589', '12:19:59.631', '12:24:03.039', '12:24:10.228', '12:26:29.537', '12:28:11.389', '12:29:05.934', '12:32:33.284', '12:33:19.082', '12:34:33.822', '12:34:38.794', '12:38:16.190', '12:43:58.572', '12:44:42.554', '12:45:31.825', '12:46:31.884', '12:46:37.109', '12:51:43.981', '12:51:47.647', '12:55:27.842', '12:55:46.486', '12:58:17.855', '12:58:37.216', '12:58:40.409']
schedule = [timestamp(43200),timestamp(43282.94831775457),timestamp(43574.41804031737),timestamp(43676.84725705157),timestamp(43756.48301146178),timestamp(43859.24731713969),timestamp(43921.36275496965),timestamp(44371.5898461825),timestamp(44399.63144669681),timestamp(44643.03939689084),timestamp(44650.22884408248),timestamp(44789.53714062267),timestamp(44891.38948845254),timestamp(44945.93494936443),timestamp(45153.284516692715),timestamp(45199.08290417717),timestamp(45273.82282539886),timestamp(45278.79407235116),timestamp(45496.19065547889),timestamp(45838.57278027507),timestamp(45882.55461920875),timestamp(45931.825184881745),timestamp(45991.88497142817),timestamp(45997.10954055435),timestamp(46303.981801283844),timestamp(46307.64754410242),timestamp(46527.84214369415),timestamp(46546.48624867541),timestamp(46697.85566539626),timestamp(46717.21648783507),timestamp(46720.40930249928)]
clients["t5"] = Client_IoT("t5", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)

# Instance of Client t6
fileSize_mb = 5
localCPU_ghz = 5.2
localProcessing_ms = 5
memoryReq_mb = 6
storageReq_mb = 0
radius = np.infty
locations = []
locations.append(Locations(45.465699734820994, -73.7455637391007, 1))
# schedule_str = ['12:00:00', '12:02:05.127', '12:04:10.876', '12:06:12.277', '12:07:44.898', '12:09:40.540', '12:11:37.037', '12:13:26.260', '12:15:37.287', '12:17:35.526', '12:19:22.182', '12:20:56.680', '12:22:33.894', '12:24:40.916', '12:26:07.563', '12:27:56.668', '12:30:19.806', '12:32:24.727', '12:34:49.485', '12:36:59.025', '12:39:19.313', '12:41:09.561', '12:43:02.068', '12:44:55.054', '12:46:59.570', '12:48:59.505', '12:50:57.437', '12:52:34.807', '12:54:47.881', '12:56:56.588', '12:59:08.417']
schedule = [timestamp(43200),timestamp(43325.127068043104),timestamp(43450.87603221221),timestamp(43572.27767164931),timestamp(43664.89817485018),timestamp(43780.54001848875),timestamp(43897.03750841419),timestamp(44006.26041989362),timestamp(44137.287098001216),timestamp(44255.52610479244),timestamp(44362.18265210639),timestamp(44456.68033869297),timestamp(44553.894752829845),timestamp(44680.916967117155),timestamp(44767.563769271714),timestamp(44876.668492665565),timestamp(45019.806237624594),timestamp(45144.72746527769),timestamp(45289.48544329688),timestamp(45419.02500009678),timestamp(45559.3135566065),timestamp(45669.56131189897),timestamp(45782.0683690115),timestamp(45895.05455696045),timestamp(46019.57003119776),timestamp(46139.5051455767),timestamp(46257.43752796193),timestamp(46354.807661258244),timestamp(46487.881563858195),timestamp(46616.58807525592),timestamp(46748.417085999085)]
clients["t6"] = Client_IoT("t6", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)

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
clients["t7"] = Client_IoT("t7", schedule, locations, radius, fileSize_mb, localCPU_ghz, localProcessing_ms, memoryReq_mb, storageReq_mb)


nodes = {}
links={}
## Node Instances 

# Instance of Node n1
cpu_ghz = 3.2
memory_mb = 1024
storage_mb = 512
locations = []
locations.append(Locations(45.465664933903625, -73.7456826990701, 1))
radius = np.infty
nodes["n1"] = Node_Edge("n1", locations, radius, storage_mb, cpu_ghz, memory_mb)

# Instance of Node n2
cpu_ghz = 2.8
memory_mb = 32
storage_mb = 128
locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
radius = np.infty
nodes["n2"] = Node_Edge("n2", locations, radius, storage_mb, cpu_ghz, memory_mb)

# Instance of Node n3
cpu_ghz = 1.6
memory_mb = 64
storage_mb = 32
locations = []
locations.append(Locations(45.46569244544138, -73.74554328725696, 1))
radius = np.infty
nodes["n3"] = Node_Edge("n3", locations, radius, storage_mb, cpu_ghz, memory_mb)

# Instance of Node n4
cpu_ghz = 2.9
memory_mb = 2048
storage_mb = 4096
locations = []
locations.append(Locations(45.46563906834305, -73.74555032805563, 1))
radius = np.infty
nodes["n4"] = Node_Edge("n4", locations, radius, storage_mb, cpu_ghz, memory_mb)

# Instance of Node n5
storage_mb = 512
locations = []
locations.append(Locations(45.465664933903625, -73.7456826990701, 1))
radius = np.infty
nodes["n5"] = Node_Dormant("n5", locations, radius, storage_mb)

## Link Instances

# Instance of Link l1
bandwidth = 3.5
node_pair = ['n1', 'n2']
nodes["n1"].neighbours.append(("l1", "n2"))
links["l1"] = Link_Edge("l1", node_pair, bandwidth)

# Instance of Link l2
bandwidth = 8.1
node_pair = ['n2', 'n3']
nodes["n2"].neighbours.append(("l2", "n3"))
links["l2"] = Link_Edge("l2", node_pair, bandwidth)

# Instance of Link l3
bandwidth = 7.3
node_pair = ['n2', 'n4']
nodes["n2"].neighbours.append(("l3", "n4"))
links["l3"] = Link_Edge("l3", node_pair, bandwidth)

graph = Graph_G("G", nodes, links)
network_structure = NetworkStructure(graph, clients)