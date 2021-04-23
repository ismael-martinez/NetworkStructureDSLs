# NetworkStructureDSLs

TRS and ENS DSLs, with Python Code Generation and Analysis
-----------------------------------------

## Physical Request Schedule (PNS) DSL

The grammar is available in `EdgeNetwork\Python\TRS\trs.tx`


### TRS Metamodel
![alt text](https://github.com/ismael-martinez/NetworkStructureDSLs/blob/main/metamodel-diagrams/trs-metamodel.JPG "TRS Metamodel")


### TRS Sample
```
Thing IoT 
	clientSet IoTSet { 
	attributes {
	 key: fileSize_mb, type: int 
	 key: local_CPU_ghz, type: float 
	 key: localProcessing_ms, type: int 
	 key: storageReq_mb, type: int 
	 key: ramReq_mb, type: int 
	 key: communicationRadius_m, type:float 
}
radius: communicationRadius_m
		thing t1 {
			explicitRequestSchedule {
			[13:00, 13:01, 13:06, 14:14, 15:16]
	}
			location {
				latitude: 45.464733061090094 
				longitude: -73.75060543257906 
				height: 1 
	}
			attributes {
				fileSize_mb: 537
				local_CPU_ghz: 3.42
				localProcessing_ms: 234
				storageReq_mb: 86
				ramReq_mb: 354
				communicationRadius_m: 50000
			}
		}
		thing t2 {
		consistentRequestSchedule {
		start:	13:00
		end:	14:00
		gap:	00:05
		}
		location {
			latitude: 45.46262611989521 
			longitude: -73.74725803572848 
			height: 1 
			}
		attributes {
			fileSize_mb: 538
			local_CPU_ghz: 3.45
			localProcessing_ms: 785
			storageReq_mb: 465
			ramReq_mb: 345
			communicationRadius_m: 70000
		}
	}


```


-----------------------------------------
## Physical Request Schedule (PNS) DSL

The grammar is available in `EdgeNetwork\Python\PNS\pns.tx`

### PNS Metamodel
![alt text](https://github.com/ismael-martinez/NetworkStructureDSLs/blob/main/metamodel-diagrams/pns-metamodel.JPG "PNS Metamodel")



### PNS Sample
```
Graph Edge 
	nodeSet EdgeSet {
		attributes {
		key: local_CPU_ghz, type: float 
		key: localProcessing_ms, type: int 
		key: storageAvail_mb, type: int 
		key: ramAvail_mb, type: int 
		key: communicationRadius_m, type: float 
}
serviceRate: local_CPU_ghz
radius: communicationRadius_m
	node n1 {
	location {
		latitude: 45.464289282566135 
		longitude: -73.74175835693006 
		height: 5 
}
	attributes {
		local_CPU_ghz: 5.78
		localProcessing_ms: 789
		storageAvail_mb: 465
		ramAvail_mb: 9789
		communicationRadius_m: 80000
	}
}
	node n2 {
	location {
		latitude: 45.46555341943783 
		longitude: -73.7503414257777 
		height: 2 
}
	attributes {
		local_CPU_ghz: 7.89
		localProcessing_ms: 87
		storageAvail_mb: 687
		ramAvail_mb: 6547
		communicationRadius_m: 95000
	}
}
	node n3 {
	location {
		latitude: 45.468382575431434 
		longitude: -73.74544907653454 
		height: 3 
}
	attributes {
		local_CPU_ghz: 8.54
		localProcessing_ms: 465
		storageAvail_mb: 3158
		ramAvail_mb: 6785
		communicationRadius_m: 95000
	}
}
}linkSet EdgeLinks { 
	attributes { 
		key: bandwidth, type: float
	}
	link l0 {
	attributes { 
		bandwidth: 456
}		nodePair: (n1, n2)
}
	link l1 {
	attributes { 
		bandwidth: 4658
}		nodePair: (n2, n3)
}
	link l2 {
	attributes { 
		bandwidth: 536
}		nodePair: (n1, n3)
}
}

```
