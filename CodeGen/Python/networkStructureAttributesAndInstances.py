#from networkStructure import *
import numpy as np

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
	def __init__(self, id, schedule, locations, radius,attributes):
		self.id = id
		self.schedule = schedule
		self.locations = locations
		self.radius = radius
		self.attributes = attributes

class Graph_Edge(GraphAbstract):
	def __init__(self, id, nodes, links):
		self.id= id
		self.nodes = nodes
		self.links=links
		self.paths = depthFirstSearch(self.nodes)

class Node_Edge(NodeAbstract):
	def __init__(self, id, locations, attributes, radius = np.infty):
		self.id = id
		self.locations=locations
		self.attributes = attributes
		self.radius = radius
	def service_rate(self):
		return self.attributes.cpu_ghz

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

radius = np.infty
locations = []
locations.append(Locations(45.465660936499575, -73.74569047347666, 1))
attributes = ThingAttributes_IoT(16,3.2,5,6,0)
# schedule_str = ['12:12:00', '12:27:00', '12:42:00', '12:57:00', '13:12:00', '13:27:00', '13:42:00']
schedule = [timestamp(43920),timestamp(44820),timestamp(45720),timestamp(46620),timestamp(47520),timestamp(48420),timestamp(49320)]
things["t1"] = Thing_IoT("t1", schedule, locations, radius, attributes)

radius = np.infty
locations = []
locations.append(Locations(45.465678336962135, -73.74567773298384, 1))
locations.append(Locations(45.46566399333796, -73.74567337439419, 1))
attributes = ThingAttributes_IoT(64,3.8,10,32,0)
# schedule_str = ['12:00', '12:03', '13:21', '13:45', '14:29']
schedule = [timestamp(43200),timestamp(43380),timestamp(48060),timestamp(49500),timestamp(52140)]
things["t2"] = Thing_IoT("t2", schedule, locations, radius, attributes)

radius = 300.0
locations = []
locations.append(Locations(45.465660701358146, -73.74562408880354, 1))
attributes = ThingAttributes_IoT(85,4.6,32,24,0)
# schedule_str = ['12:00:00', '12:03:22.402', '12:16:11.442', '12:17:39.264', '12:19:42.755', '12:36:09.811', '12:48:20.554', '12:48:52.061', '12:49:39.067']
schedule = [timestamp(43200),timestamp(43402.40221738544),timestamp(44171.442249245796),timestamp(44259.26482304727),timestamp(44382.75587514436),timestamp(45369.81175797588),timestamp(46100.55493251213),timestamp(46132.06103446164),timestamp(46179.067983679815)]
things["t3"] = Thing_IoT("t3", schedule, locations, radius, attributes)

radius = 500.0
locations = []
locations.append(Locations(45.465690799452325, -73.745617383281, 1))
locations.append(Locations(45.465673398993594, -73.74559458450437, 1))
attributes = ThingAttributes_IoT(64,1.3,52,73,0)
# schedule_str = ['10:00:00', '10:01:24.454', '10:02:51.080', '10:04:14.431', '10:05:42.413', '10:07:15.705', '10:08:42.601', '10:10:04.022', '10:11:41.732', '10:13:17.256', '10:14:45.353', '10:16:23.133', '10:17:53.009', '10:19:26.309', '10:21:00.496', '10:22:31.951', '10:24:01.553', '10:25:32.813', '10:27:05.611', '10:28:29.150', '10:30:02.826', '10:31:35.610', '10:33:05.082', '10:34:28.380', '10:36:04.407', '10:37:33.057', '10:39:00.100', '10:40:23.959', '10:41:50.084', '10:43:22.965', '10:44:48.911', '10:46:15.611', '10:47:48.999', '10:49:14.558', '10:50:48.181', '10:52:19.663', '10:53:51.954', '10:55:37.569', '10:57:05.673', '10:58:35.202', '11:00:01.260', '11:01:32.190', '11:02:58.543', '11:04:19.479', '11:05:49.614', '11:07:20.101', '11:08:53.381', '11:10:20.086', '11:11:49.013', '11:13:14.132', '11:14:38.513', '11:15:59.680', '11:17:33.226', '11:18:59.696', '11:20:28.877', '11:21:54.777', '11:23:17.222', '11:24:47.750', '11:26:18.483', '11:27:46.682', '11:29:19.707', '11:30:53.650', '11:32:22.544', '11:33:40.547', '11:35:20.309', '11:36:52.885', '11:38:29.536', '11:40:01.953', '11:41:23.206', '11:42:51.177', '11:44:18.788', '11:45:44.878', '11:47:09.853', '11:48:43.048', '11:50:17.464', '11:51:52.855', '11:53:22.028', '11:54:53.698', '11:56:17.443', '11:57:38.674', '11:59:07.462', '12:00:38.535', '12:02:06.910', '12:03:32.158', '12:05:02.765', '12:06:40.741', '12:08:09.943', '12:09:29.395', '12:10:55.703', '12:12:26.975', '12:14:00.039', '12:15:29.290', '12:16:52.988', '12:18:16.752', '12:19:47.810', '12:21:17.493', '12:22:39.675', '12:24:04.383', '12:25:27.332', '12:26:58.549', '12:28:31.085', '12:29:48.279', '12:31:13.350', '12:32:40.685', '12:34:12.519', '12:35:52.017', '12:37:18.850', '12:38:56.658', '12:40:29.387', '12:41:56.302', '12:43:30.308', '12:44:56.190', '12:46:30.331', '12:47:53.391', '12:49:19.332', '12:50:45.380', '12:52:16.217', '12:53:39.841', '12:55:13.852', '12:56:38.911', '12:58:15.993', '12:59:44.669', '13:01:06.038', '13:02:30.500', '13:03:59.477', '13:05:21.085', '13:06:52.436', '13:08:24.060', '13:09:48.034', '13:11:16.280', '13:12:42.575', '13:14:08.685', '13:15:43.267', '13:17:12.170', '13:18:46.276', '13:20:20.397', '13:21:56.942', '13:23:29.015', '13:24:56.378', '13:26:23.177', '13:27:59.613', '13:29:28.486', '13:30:58.275', '13:32:28.848', '13:33:53.720', '13:35:19.027', '13:36:44.106', '13:38:14.548', '13:39:41.150', '13:41:17.830', '13:42:55.700', '13:44:26.134', '13:45:55.519', '13:47:31.856', '13:48:58.058', '13:50:28.559', '13:52:06.261', '13:53:35.252', '13:55:03.779', '13:56:33.883', '13:58:06.803', '13:59:38.193', '14:01:01.420', '14:02:34.213', '14:03:59.500', '14:05:31.077', '14:07:05.008', '14:08:39.619', '14:10:08.078', '14:11:35.069', '14:13:08.232', '14:14:34.350', '14:16:00.832', '14:17:31.186', '14:19:02.624', '14:20:24.519', '14:21:52.572', '14:23:20.364', '14:24:49.693', '14:26:23.578', '14:27:46.640', '14:29:21.530', '14:30:55.724', '14:32:31.621', '14:34:01.826', '14:35:25.604', '14:36:52.956', '14:38:33.118', '14:40:04.888', '14:41:31.529', '14:42:50.961', '14:44:12.187', '14:45:42.685', '14:47:09.133', '14:48:42.190', '14:50:11.765', '14:51:38.857', '14:53:15.475', '14:54:49.730', '14:56:25.814', '14:57:45.312', '14:59:18.967']
schedule = [timestamp(36000),timestamp(36084.454862746694),timestamp(36171.08076009011),timestamp(36254.43196787191),timestamp(36342.41334292951),timestamp(36435.70543470147),timestamp(36522.60184389356),timestamp(36604.02253311599),timestamp(36701.73231842966),timestamp(36797.256200587144),timestamp(36885.35350427218),timestamp(36983.13350151251),timestamp(37073.00944601407),timestamp(37166.30931571426),timestamp(37260.49648347123),timestamp(37351.95193623535),timestamp(37441.55362080116),timestamp(37532.81342973068),timestamp(37625.61117790899),timestamp(37709.15025907443),timestamp(37802.82659254925),timestamp(37895.61024876608),timestamp(37985.08296243402),timestamp(38068.38020296227),timestamp(38164.40791378668),timestamp(38253.05712928639),timestamp(38340.10009597302),timestamp(38423.95926047738),timestamp(38510.084967880706),timestamp(38602.96584587172),timestamp(38688.91108561544),timestamp(38775.61100155224),timestamp(38868.99950562403),timestamp(38954.55886867169),timestamp(39048.18108715507),timestamp(39139.66386801818),timestamp(39231.9546981519),timestamp(39337.56996606718),timestamp(39425.67317679923),timestamp(39515.202281904305),timestamp(39601.26043652431),timestamp(39692.19005378882),timestamp(39778.5431377876),timestamp(39859.47926475991),timestamp(39949.61431673023),timestamp(40040.10191879741),timestamp(40133.38133230621),timestamp(40220.08692982205),timestamp(40309.01306497541),timestamp(40394.13260846817),timestamp(40478.51347251752),timestamp(40559.68085511835),timestamp(40653.22615667504),timestamp(40739.69610940795),timestamp(40828.877681354264),timestamp(40914.77737975581),timestamp(40997.222217426),timestamp(41087.75026803924),timestamp(41178.48387281525),timestamp(41266.68233552041),timestamp(41359.70799849172),timestamp(41453.65073451905),timestamp(41542.54492269399),timestamp(41620.5475104836),timestamp(41720.309559740155),timestamp(41812.88562342261),timestamp(41909.536304279325),timestamp(42001.95393718671),timestamp(42083.20646270928),timestamp(42171.177976327475),timestamp(42258.788266665884),timestamp(42344.87875856098),timestamp(42429.853179076),timestamp(42523.04820499045),timestamp(42617.46480391187),timestamp(42712.85535235898),timestamp(42802.02860410396),timestamp(42893.69803888816),timestamp(42977.443651870235),timestamp(43058.67429446543),timestamp(43147.46276467176),timestamp(43238.53513492705),timestamp(43326.910260334655),timestamp(43412.15823542853),timestamp(43502.76547906699),timestamp(43600.741906647185),timestamp(43689.94331502136),timestamp(43769.39519239553),timestamp(43855.7030174431),timestamp(43946.97548389714),timestamp(44040.03977709027),timestamp(44129.2900854934),timestamp(44212.98885683446),timestamp(44296.752238977555),timestamp(44387.81000675647),timestamp(44477.493062473855),timestamp(44559.675190913295),timestamp(44644.38337370662),timestamp(44727.33206137803),timestamp(44818.54957371501),timestamp(44911.08542248993),timestamp(44988.27979040716),timestamp(45073.35031519759),timestamp(45160.68583553962),timestamp(45252.51936168802),timestamp(45352.01758118152),timestamp(45438.85013418415),timestamp(45536.65845699071),timestamp(45629.38764801391),timestamp(45716.3025578543),timestamp(45810.30844258072),timestamp(45896.19026540579),timestamp(45990.331472412465),timestamp(46073.39141104246),timestamp(46159.332468968416),timestamp(46245.38052027141),timestamp(46336.21758546361),timestamp(46419.841647003355),timestamp(46513.8528209923),timestamp(46598.91122057486),timestamp(46695.99395457597),timestamp(46784.66901956514),timestamp(46866.0382066399),timestamp(46950.50060443488),timestamp(47039.47785131568),timestamp(47121.08503612003),timestamp(47212.43652791756),timestamp(47304.060384168275),timestamp(47388.034009078736),timestamp(47476.28083670988),timestamp(47562.575527809044),timestamp(47648.68550665353),timestamp(47743.26783278716),timestamp(47832.17069887181),timestamp(47926.27632111947),timestamp(48020.39727192369),timestamp(48116.942796336945),timestamp(48209.01565410231),timestamp(48296.37888974237),timestamp(48383.17712722025),timestamp(48479.6130023738),timestamp(48568.48635672716),timestamp(48658.27574776426),timestamp(48748.848205971546),timestamp(48833.72041435671),timestamp(48919.02744716104),timestamp(49004.10656128057),timestamp(49094.548913420265),timestamp(49181.150873021135),timestamp(49277.83095898432),timestamp(49375.70021264998),timestamp(49466.13406462506),timestamp(49555.51944031358),timestamp(49651.8565513188),timestamp(49738.05839232891),timestamp(49828.55937973022),timestamp(49926.26101943198),timestamp(50015.252602367094),timestamp(50103.77980806471),timestamp(50193.88326165421),timestamp(50286.80365251773),timestamp(50378.19315432072),timestamp(50461.420833084645),timestamp(50554.21333657423),timestamp(50639.50060485686),timestamp(50731.0778584401),timestamp(50825.00844516837),timestamp(50919.6193557591),timestamp(51008.078169840686),timestamp(51095.06978572075),timestamp(51188.232047878126),timestamp(51274.35072879452),timestamp(51360.832324088646),timestamp(51451.18682851324),timestamp(51542.62482538809),timestamp(51624.51924798635),timestamp(51712.57287660547),timestamp(51800.36453028502),timestamp(51889.69369931115),timestamp(51983.57876773632),timestamp(52066.640131981134),timestamp(52161.530821271816),timestamp(52255.72455984844),timestamp(52351.62105420758),timestamp(52441.826889782584),timestamp(52525.60431989436),timestamp(52612.956314958305),timestamp(52713.11843454022),timestamp(52804.88839275341),timestamp(52891.529941844834),timestamp(52970.961124461974),timestamp(53052.187253714284),timestamp(53142.68517749496),timestamp(53229.13379043522),timestamp(53322.19095164021),timestamp(53411.765698174),timestamp(53498.85743269756),timestamp(53595.47536817224),timestamp(53689.73049035839),timestamp(53785.81496225709),timestamp(53865.31255721641),timestamp(53958.967420533576)]
things["t4"] = Thing_IoT("t4", schedule, locations, radius, attributes)

radius = np.infty
locations = []
locations.append(Locations(45.46570138080979, -73.74552954093576, 1))
attributes = ThingAttributes_IoT(543,4.7,542,13,0)
# schedule_str = ['12:00:00', '12:04:08.647', '12:04:43.748', '12:06:02.159', '12:06:25.227', '12:07:10.838', '12:11:23.166', '12:11:31.759', '12:11:53.840', '12:16:19.418', '12:18:26.805', '12:19:12.059', '12:22:19.582', '12:25:31.375', '12:26:39.301', '12:28:59.665', '12:29:35.877', '12:33:54.238', '12:36:05.632', '12:39:48.533', '12:42:54.751', '12:43:04.557', '12:45:07.932', '12:45:38.653', '12:46:41.462', '12:48:19.251', '12:48:43.207', '12:49:10.646', '12:51:34.706', '12:52:29.908', '12:53:38.647', '12:55:30.006', '12:55:46.881', '12:58:28.823', '12:59:02.960', '12:59:56.770']
schedule = [timestamp(43200),timestamp(43448.64707314732),timestamp(43483.748369095105),timestamp(43562.15970011594),timestamp(43585.22734329869),timestamp(43630.838271223445),timestamp(43883.16654169257),timestamp(43891.759774621445),timestamp(43913.84084269083),timestamp(44179.41829634256),timestamp(44306.80512685356),timestamp(44352.059191041786),timestamp(44539.58288631626),timestamp(44731.375650493625),timestamp(44799.30106312756),timestamp(44939.665177563154),timestamp(44975.87759459),timestamp(45234.23817580443),timestamp(45365.63296436366),timestamp(45588.533274582995),timestamp(45774.75102898967),timestamp(45784.55726811235),timestamp(45907.93226239771),timestamp(45938.653651992885),timestamp(46001.46263713781),timestamp(46099.251363347386),timestamp(46123.20702965689),timestamp(46150.64694797633),timestamp(46294.706062490644),timestamp(46349.90894359193),timestamp(46418.64729876885),timestamp(46530.006455421666),timestamp(46546.881397096295),timestamp(46708.82371793969),timestamp(46742.96013917304),timestamp(46796.77016770371)]
things["t5"] = Thing_IoT("t5", schedule, locations, radius, attributes)

radius = np.infty
locations = []
locations.append(Locations(45.465699734820994, -73.7455637391007, 1))
attributes = ThingAttributes_IoT(5,5.2,5,6,0)
# schedule_str = ['12:00:00', '12:02:16.683', '12:04:33.246', '12:06:46.340', '12:08:29.449', '12:09:52.372', '12:12:01.133', '12:13:46.958', '12:15:44.271', '12:17:44.206', '12:20:01.246', '12:22:14.895', '12:24:42.094', '12:26:49.727', '12:28:23.832', '12:30:30.864', '12:32:11.060', '12:34:19.653', '12:36:17.114', '12:38:16.091', '12:40:26.423', '12:42:17.807', '12:44:01.885', '12:46:27.079', '12:48:40.622', '12:50:46.309', '12:52:33.001', '12:54:48.863', '12:56:34.192', '12:58:36.958']
schedule = [timestamp(43200),timestamp(43336.683395726206),timestamp(43473.24690964147),timestamp(43606.340834069335),timestamp(43709.449901346445),timestamp(43792.37258313607),timestamp(43921.13313440674),timestamp(44026.958152175444),timestamp(44144.27127622535),timestamp(44264.20641333773),timestamp(44401.2461811274),timestamp(44534.895448509895),timestamp(44682.09405768776),timestamp(44809.727856646125),timestamp(44903.83231305979),timestamp(45030.864181256526),timestamp(45131.06085484173),timestamp(45259.65318448705),timestamp(45377.11431768406),timestamp(45496.09126169409),timestamp(45626.423035021595),timestamp(45737.80744803013),timestamp(45841.885743756386),timestamp(45987.07951137505),timestamp(46120.62208169607),timestamp(46246.309211758526),timestamp(46353.00109481847),timestamp(46488.86392381314),timestamp(46594.192371436184),timestamp(46716.95819576292)]
things["t6"] = Thing_IoT("t6", schedule, locations, radius, attributes)

radius = np.infty
locations = []
locations.append(Locations(45.46563554122027, -73.74553524062992, 1))
locations.append(Locations(45.4656552931052, -73.74553758756281, 1))
attributes = ThingAttributes_IoT(79,3.2,13,798,0)
# schedule_str = ['12:00:00']
schedule = [timestamp(43200)]
things["t7"] = Thing_IoT("t7", schedule, locations, radius, attributes)


nodes = {}
links={}
## Node Instances 

locations = []
locations.append(Locations(45.465664933903625, -73.7456826990701, 1))
radius = np.infty
attributes = NodeAttributes_Edge(3.2,1024,512)
nodes["n1"] = Node_Edge("n1", locations, attributes, radius)

locations = []
locations.append(Locations(45.46566563932783, -73.74562006549, 1))
radius = np.infty
attributes = NodeAttributes_Edge(2.8,32,128)
nodes["n2"] = Node_Edge("n2", locations, attributes, radius)

locations = []
locations.append(Locations(45.46569244544138, -73.74554328725696, 1))
radius = np.infty
attributes = NodeAttributes_Edge(1.6,64,32)
nodes["n3"] = Node_Edge("n3", locations, attributes, radius)

locations = []
locations.append(Locations(45.46563906834305, -73.74555032805563, 1))
radius = np.infty
attributes = NodeAttributes_Edge(2.9,2048,4096)
nodes["n4"] = Node_Edge("n4", locations, attributes, radius)

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