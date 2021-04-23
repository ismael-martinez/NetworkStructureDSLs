# NetworkStructureDSLs

TRS and PNS DSLs, with Python Code Generation and Analysis
-----------------------------------------

## Setup
Ensure the proper softwares are downloaded.

### Python
Python3 - https://www.python.org/downloads/

### Python libraries
Ensure the following python libraries are installed. You can use `pip install <module>` to install the appropriate modules.
* numpy
* scipy
* textx
* matplotlob
* opencv-python
* networkx

### Graphviz
This is used to display the network structures and metamodels as images.
In particular, you will need dot.exe that is in the downloaded Graphviz/bin/ folder.
https://graphviz.org/download/

-----------------------------------------
## Execute Code Generation 
The create a `location.json` file, execute the `map.html` file in `CodeGen\` directory. Follow the steps at the bottom of the html file, and export the location file.

The appropriate Code Generation files are in the `CodeGen\Python` directory. To execute in the command line, you run
`python codeGen.py -t "<path_to_trs_model>.trs" -T "<path_to_trs_locations>.json" -p "<path_to_pns_file>.pns" -P "<path_to_pnss_locations>.json"`. 
This will generate the `networkStructureAttributesAndInstances.py` script.

## Execute Network Analysis

Execute `python networkStructureAnalysis.py` with any of the following parameters. Ensure the generated file is in the same directory as the analysis script.

- `-n` : Network structure graph.
- `-q` : Queue simulation logs.
- `-a` : Arrival request per node, one graph per node.

-----------------------------------------
## Primitives
### Timestamp
Defines a timestamp with hours, minutes, seconds (optional), and milliseconds (optional with seconds).

e.g.
* 23:05
* 18:35:04
* 05:43:24.357

### SimpleType
One of the following types --  `int | float | string | bool | timestamp`


## Traffic Request Schedule (TRS) DSL
The grammar is available in `CodeGen\Python\TRS\trs.tx`

### TRS Metamodel
![alt text](https://github.com/ismael-martinez/NetworkStructureDSLs/blob/main/metamodel-diagrams/trs-metamodel.JPG "TRS Metamodel")

### TRS DSL 
* *name* -- Name of TRS configurations.
* *attribute* -- A name and type of an attribute common to all Things in ThingSet.
	* key: string
	* type: (string | float | int | bool | timestamp)
* *requestSchedule* -- Defines the timestamps of requests from a Thing. Abstract type.
	* *explicitRequestShedule* -- Array of timestamps.
	* *consistentRequestSchedule* -- Defines an interval (start and end), and a frequency gap. A schedule is constructued by by executing one request in even gaps between the interval.
	* *probabilisticRequestSchedule* -- Defines an interval (start, end), and a interarrival distribution. A schedule is constructed by sampling the next request timestamp from the distribution, between the interval.
		* Gaussian (mu, var)
		* Exponential (lambda)
* *location* -- Reference to index of location element (latitiude, longitude, height) of separate `<path_to_trs_locations>.json`.
* *radius* (optional) -- The maximum distance between a `node` and a `thing` for which a request can be sent. 

### TRS Sample
```
Things IoT

attributes {
			key: fileSize_mb, type: int
			key: localCPU_ghz, type: float
			key: localProcessing_ms, type: int
			key: memoryReq_mb, type: int
			key: storageReq_mb, type: int
		}

thing t1 {
	consistentRequestSchedule {
		start: 12:12
		end: 13:54
		gap:00:15
	}
	location { 
		["5"]
	}
	attributes {
		fileSize_mb : 16
		localCPU_ghz:3.2
		localProcessing_ms: 5
		memoryReq_mb:6
		storageReq_mb:0
	}
}

thing t2 {
	explicitRequestSchedule{
		[12:00, 12:03, 13:21, 13:45, 14:29]
	}
	location { 
		["6", "7"]
	}
	attributes {
		fileSize_mb:64
		localCPU_ghz:3.8
		localProcessing_ms: 10
		memoryReq_mb:32
		storageReq_mb:0
	}
}

thing t3 {
	probabilisticRequestSchedule {
		start:12:00
		end: 13:00
		interarrivalDistribution: Exponential(lambda=0.002)
	}
	
	location { 
		["8"]
	}
	radius: 300.0
	attributes {
		fileSize_mb:85
		localCPU_ghz:4.6
		localProcessing_ms: 32
		memoryReq_mb:24
		storageReq_mb:0
	}
}

```


-----------------------------------------
## Physical Request Schedule (PNS) DSL

The grammar is available in `CodeGen\Python\PNS\pns.tx`

### PNS Metamodel
![alt text](https://github.com/ismael-martinez/NetworkStructureDSLs/blob/main/metamodel-diagrams/pns-metamodel.JPG "PNS Metamodel")

### PNS DSL 
* *name* -- Name of PNS configurations.
* *attribute* -- A name and type of an attribute common to all Nodes in NodeSet, or Links in LinkSet.
	* key: string
	* type: (string | float | int | bool | timestamp)
* *location* -- Reference to index of location element (latitiude, longitude, height) of separate `<path_to_trs_locations>.json`.
* *serviceRate* (optional) -- Attribute that defines the service rate for a `NodeSet`.
* *radius* (optional) -- The maximum distance between a `node` and a `thing` for which a request can be received.
* *nodePair* -- Reference two two `node`.


### PNS Sample
```
Graph Edge
	nodeSet {
		attributes {
			key: storage_mb, type: int
			key: cpu_ghz, type: float
			key: memory_mb, type: int
		}
        serviceRate: cpu_ghz
		node n1 {
				attributes {
					cpu_ghz: 3.2
					memory_mb: 1024
					storage_mb: 512
				} 
				location {
	            	["1"]
	            }
		}
		node n2 {
				attributes {
					cpu_ghz: 2.8
					memory_mb: 32
					storage_mb: 128
				}
				location {
	            	["2"]
	            }
				radius : 525.0
		}

	} 
	linkSet {
		attributes {
		    key: bandwidth, type:float
		}
		link l1 {
				attributes {
				    bandwidth: 3.5
				}
				nodePair: (n1, n2)
		}
	}

```
