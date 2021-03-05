let map;

let coordinateList = [];
let labelIndex = 1;

function initMap() {
    const myLatlng = { lat: 45.505613, lng: -73.613766 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: myLatlng,
    });
    coordinateMarkers(map);
}

function updateMap() {
    const inputVal = document.getElementById("pac-input").value;
    let newLatLng = inputVal.split(",");
    let newLat = parseFloat(newLatLng[0]);
    let newLng = parseFloat(newLatLng[1]);
    const myLatlng = {lat: newLat, lng: newLng};
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: myLatlng,
    });
    coordinateMarkers(map);
}

function coordinateMarkers(map){
    map.addListener("click", (e) => {
        let jsonCoordinates = e.latLng.toJSON();
        coordinateList.push(jsonCoordinates);

        //console.log(jsonCoordinates);
        placeMarkerAndPanTo(e.latLng, map);
    });
}

function placeMarkerAndPanTo(latLng, map) {
    new google.maps.Marker({
        position: latLng,
        map: map,
        label: labelIndex.toString()
    });
    labelIndex++;
    map.panTo(latLng);
}

function tableRow(tbody, rowTitle, placeholderText){
    let row = tbody.insertRow();
    let tdh = document.createElement("td");
    tdh.innerText = rowTitle;
    row.appendChild(tdh);
    let tdi = document.createElement("td");
    let tdBox = document.createElement("input");
    tdBox.type = "text";
    tdBox.placeholder = placeholderText;
    tdi.appendChild(tdBox);
    row.appendChild(tdi);
    tbody.appendChild(row);
}

function linkTableRow(tbody){
    let row = tbody.insertRow();
    let tdh = document.createElement("td");
    tdh.innerText = "New node pair:\t";
    row.appendChild(tdh);

    let tdi = document.createElement("td");
    let tdBox = document.createElement("input");
    tdBox.type = "text";
    tdBox.placeholder = "e.g. 1, 2";
    tdi.appendChild(tdBox);
    row.appendChild(tdi);

    let tds = document.createElement("td");
    tds.width = 25;
    row.appendChild(tds);
    let tdb = document.createElement("td");
    tdb.innerText = "\tBandwidth (MB/s):\t";
    row.appendChild(tdb);
    let tdbi = document.createElement("td");
    let tdBoxB = document.createElement("input");
    tdBoxB.type = "text";
    tdBoxB.placeholder = "e.g. 524.5";

    tdbi.appendChild(tdBoxB);
    row.appendChild(tdbi);

    tbody.appendChild(row);
}


function requestSchedTypeExplicit(markerNumber){
    let requestDistributionBody = document.getElementById("reqSchedBody" + markerNumber);
    requestDistributionBody.innerHTML = '';

    tableRow(requestDistributionBody, "Schedule:\t", "e.g. 13:00, 13:05, 13:32");
}

function requestSchedTypeConsistent(markerNumber){
    let requestDistributionBody = document.getElementById("reqSchedBody" + markerNumber);
    requestDistributionBody.innerHTML = '';

    tableRow(requestDistributionBody, "Start Time:\t", "e.g. 13:00");
    tableRow(requestDistributionBody, "End Time:\t", "e.g. 15:30");
    tableRow(requestDistributionBody, "Frequency:\t", "e.g. 00:15");
}

function requestSchedTypeProbabilistic(markerNumber){
    console.log("reqSchedBody" + markerNumber);
    let requestDistributionBody = document.getElementById("reqSchedBody" + markerNumber);
    requestDistributionBody.innerHTML = '';


    let requestDistributionDropdown = document.createElement("select");
    requestDistributionDropdown.setAttribute("id", "reqDist" + markerNumber);
    requestDistributionDropdown.options[0] = new Option("Exponential");
    requestDistributionDropdown.options[1] = new Option("Gaussian");
    requestDistributionDropdown.options[2] = new Option("Gamma");
    requestDistributionDropdown.options[3] = new Option("Chi-Squared");
    requestDistributionDropdown.options[4] = new Option("Beta");
    requestDistributionDropdown.options[5] = new Option("Dirichlet");
    //requestDistributionDropdown.options[6] = new Option("Bernouilli");

    requestDistributionDropdown.onchange = function () {
        distributionParametersTable(markerNumber)
    };
    tableRow(requestDistributionBody, "Start Time:\t", "e.g. 13:00");
    tableRow(requestDistributionBody, "End Time:\t", "e.g. 15:30");

    let row = requestDistributionBody.insertRow();
    let tdh = document.createElement("td");
    tdh.innerText = "Interarrival distribution:";
    row.appendChild(tdh);
    let tdi = document.createElement("td");
    let reqDiv = document.createElement("div");
    reqDiv.appendChild(document.createElement("br"));
    let reqParamTable = document.createElement("table");
    let reqParamBody = document.createElement("tbody");
    distributionParameters("lambda", "1", reqParamBody, markerNumber); // Exponential Default
    reqParamBody.setAttribute("id", "param" + markerNumber);
    reqParamTable.appendChild(reqParamBody);

    reqDiv.appendChild(requestDistributionDropdown);
    reqDiv.appendChild(reqParamTable);
    reqDiv.setAttribute("id", "reqDiv" + markerNumber);

    tdi.appendChild(reqDiv);
    row.appendChild(tdi);
}

function requestScheduleTypeTable(markerNumber){
    let requestSchedTypeDropdown = document.getElementById("reqType" + markerNumber);
    let dropdownValue = requestSchedTypeDropdown.options[requestSchedTypeDropdown.selectedIndex].text;
    if(dropdownValue.includes("Explicit")){
        requestSchedTypeExplicit(markerNumber);
    } else if(dropdownValue.includes("Consistent")){
        requestSchedTypeConsistent(markerNumber);
    } else if(dropdownValue.includes("Probabilistic")){
        requestSchedTypeProbabilistic(markerNumber);
    }
}

function requestScheduleType(tbody, markerNumber){
    let row = tbody.insertRow();
    let tdh = document.createElement("td");
    tdh.innerText = "Request Schedule:\t";
    row.appendChild(tdh);
    // Request Schedule Type
    let tdr = document.createElement("td");
    let reqSchedTypeDiv = document.createElement("div");
    let reqSchedTypeTable = document.createElement("table");
    let reqSchedTypeBody = document.createElement("tbody");
    reqSchedTypeBody.setAttribute("id", "reqSchedBody" + markerNumber);
    let requestSchedType = document.createElement("select");
    requestSchedType.setAttribute("id", "reqType" + markerNumber);
    requestSchedType.options[0] = new Option("Explicit");
    requestSchedType.options[1] = new Option("Consistent");
    requestSchedType.options[2] = new Option("Probabilistic");
    requestSchedType.onchange = function(){requestScheduleTypeTable(markerNumber)};
    tableRow(reqSchedTypeBody, "Schedule:\t", "e.g. 13:00, 13:05, 13:32"); // Default


    reqSchedTypeTable.appendChild(reqSchedTypeBody);
    reqSchedTypeDiv.appendChild(requestSchedType);
    reqSchedTypeDiv.appendChild(reqSchedTypeTable);
    tdr.appendChild(reqSchedTypeDiv);
    row.appendChild(tdr);
    tbody.append(row);
}

function distributionParameters(parameter, placeholderValue, reqParamBody, markerNumber){
    let row = reqParamBody.insertRow();
    let tdh = document.createElement("td");
    tdh.innerText = parameter + ":\t";
    row.appendChild(tdh);
    let tdi = document.createElement("td");
    let tdBox = document.createElement("input");
    tdBox.setAttribute("id", parameter + markerNumber);
    tdBox.type = "text";
    tdBox.placeholder = "e.g. " + placeholderValue;
    tdi.appendChild(tdBox);
    row.appendChild(tdi);
}

function distributionParametersTable(markerNumber){
    let requestDropdown = document.getElementById("reqDist" + markerNumber);
    let dropdownValueDistribution = requestDropdown.options[requestDropdown.selectedIndex].text;
    let reqParamBody = document.getElementById("param" + markerNumber);
    reqParamBody.innerHTML = '';
    // Parameters
    if(dropdownValueDistribution.includes("Gaussian")){
        distributionParameters("mu", "0", reqParamBody, markerNumber);
        distributionParameters("var", "1", reqParamBody, markerNumber);
    } else if(dropdownValueDistribution.includes("Exponential")){
        distributionParameters("lambda", "1", reqParamBody, markerNumber);
    } else if(dropdownValueDistribution.includes("Gamma")){
        distributionParameters("alpha", "1", reqParamBody, markerNumber);
        distributionParameters("beta", "1", reqParamBody, markerNumber);
    } else if(dropdownValueDistribution.includes("Chi-Squared")){
        distributionParameters("k", "1", reqParamBody, markerNumber);
    } else if(dropdownValueDistribution.includes("Beta")){
        distributionParameters("alpha", "1", reqParamBody, markerNumber);
        distributionParameters("beta", "1", reqParamBody, markerNumber);
    } else if(dropdownValueDistribution.includes("Dirichlet")){
        distributionParameters("alpha", "1", reqParamBody, markerNumber);
    } else if(dropdownValueDistribution.includes("Bernouilli")){
        distributionParameters("p", "0.5", reqParamBody, markerNumber);
    }
}

function markerFormIoT(markerNumber){
    // Device header
    let rowHeader = document.createElement("h4");
    rowHeader.innerText = "Device " + markerNumber;
    document.getElementById("form").appendChild(rowHeader);

    let deviceDiv = document.createElement('div');
    deviceDiv.setAttribute("id", "div" + markerNumber);
    document.getElementById("form").appendChild(deviceDiv);

    let tableResource = document.createElement("table");
    tableResource.setAttribute('id', 'dev' + markerNumber);
    tableResource.style.borderSpacing = "15px";

    // Default
    let tbody = tableResource.createTBody();
    // Resources
    tableRow(tbody, "File size (MB):\t", "e.g. 536");
    tableRow(tbody, "Local CPU (GHz):\t", "e.g. 3.42");
    tableRow(tbody, "Local processing (ms):\t", "e.g. 234");
    tableRow(tbody, "Storage memory required (MB):\t", "e.g. 59");
    tableRow(tbody, "RAM required: (MB):\t", "e.g. 242");
    tableRow(tbody, "Communication radius (meters):\t", "e.g. 279");
    // Location
    tableRow(tbody, "Height (metres):\t", "e.g. 1.2");
    // Request distribution
    requestScheduleType(tbody, markerNumber);
    //requestDistributionRow(tbody, markerNumber);


    tableResource.appendChild(tbody);

    deviceDiv.appendChild(tableResource);
}

function markerFormEdge(markerNumber){
    // Device header
    let rowHeader = document.createElement("h4");
    rowHeader.innerText = "Device " + markerNumber;
    document.getElementById("form").appendChild(rowHeader);

    let deviceDiv = document.createElement('div');
    deviceDiv.setAttribute("id", "div" + markerNumber);
    document.getElementById("form").appendChild(deviceDiv);

    let tableResource = document.createElement("table");
    tableResource.setAttribute('id', 'dev' + markerNumber);
    tableResource.style.borderSpacing = "15px";

    // Default
    let tbody = tableResource.createTBody();
    // Resources
    tableRow(tbody, "Local CPU (GHz):", "e.g. 3.42");
    tableRow(tbody, "Local processing (ms)", "e.g. 234");
    tableRow(tbody, "Storage memory required (MB):", "e.g. 59");
    tableRow(tbody, "RAM required: (MB)", "e.g. 242");
    tableRow(tbody, "Communication radius (meters)", "e.g. 279");
    tableRow(tbody, "Service rate", "e.g. 2.71");
    // Location
    tableRow(tbody, "Height (metres)", "e.g. 1.2");


    tableResource.appendChild(tbody);

    deviceDiv.appendChild(tableResource);
}

/*
function resourceAttributes(markerNumber){
    let dropdown = document.getElementById('deviceType');
    dropdownValue = dropdown.options[dropdown.selectedIndex].text;
    tableResource = document.getElementById("dev" + markerNumber);
    tableResource.innerHTML = '';
    let tbody = tableResource.createTBody();
    let isIoT = dropdownValue.localeCompare("IoT");
    if(isIoT === 0){
        // Resources
        tableRow(tbody, "File size (MB):\t", "e.g. 536");
        tableRow(tbody, "Local CPU (GHz):\t", "e.g. 3.42");
        tableRow(tbody, "Local processing (ms):\t", "e.g. 234");
        tableRow(tbody, "Storage memory required (MB):\t", "e.g. 59");
        tableRow(tbody, "RAM required: (MB):\t", "e.g. 242");
        tableRow(tbody, "Communication radius (meters):\t", "e.g. 279");
        // Location
        tableRow(tbody, "Height (metres):\t", "e.g. 1.2");
        // Request distribution
        requestDistributionRow(tbody, markerNumber);
    } else {
        // Resources
        tableRow(tbody, "Local CPU (GHz):", "e.g. 3.42");
        tableRow(tbody, "Local processing (ms)", "e.g. 234");
        tableRow(tbody, "Storage memory required (MB):", "e.g. 59");
        tableRow(tbody, "RAM required: (MB)", "e.g. 242");
        tableRow(tbody, "Communication radius (meters)", "e.g. 279");
        tableRow(tbody, "Service rate", "e.g. 2.71");
        // Location
        tableRow(tbody, "Height (metres)", "e.g. 1.2");
    }

    tableResource.appendChild(tbody);
}
*/


function exportMarkerForm(){
    let deviceForm = document.getElementById("form");
    deviceForm.innerHTML = '';
    let formHeader = document.createElement("h3");
    formHeader.innerText = "Device Information";
    deviceForm.appendChild(formHeader);

    let dropdown = document.getElementById('deviceType');
    dropdownValue = dropdown.options[dropdown.selectedIndex].text;
    let isIoT = dropdownValue.localeCompare("IoT");

    let labelIndex = 1;
    if(isIoT === 0){
        for (const ll in coordinateList) {
            let id = labelIndex++;
            markerFormIoT(id);
        }
    } else{

        for (const ll in coordinateList) {
            let id = labelIndex++;
            markerFormEdge(id);
        }
    }

    // Link connections
    let linkHeader = document.createElement("h3");
    linkHeader.innerText = "Link Connections";
    document.getElementById("form").appendChild(linkHeader);
    let linkTable = document.createElement("table");
    let linkBody = document.createElement("tbody");
    linkBody.setAttribute("id", "linkBody");
    linkTable.appendChild(linkBody);
    document.getElementById("form").appendChild(linkTable);

    let addLinkButton = document.createElement("button");
    addLinkButton.innerText = "Add Link";
    addLinkButton.onclick = function(){addLinkField()};
    document.getElementById("form").appendChild(addLinkButton);
    document.getElementById("form").appendChild(document.createElement("br"));


    let exportButton = document.createElement("button");
    exportButton.textContent = "Export device resources";
    exportButton.onclick = function(){exportMarkers()};
    document.getElementById("form").appendChild(exportButton);

}

function addLinkField(){
    let linkBody = document.getElementById("linkBody");
    linkTableRow(linkBody, "Node pair:\t", "e.g. 1, 2");
}

function readLocation(markerNumber){
    let location = {};
    location["lat"] = coordinateList[markerNumber]["lat"];
    location["lng"] = coordinateList[markerNumber]["lng"];
    return location;
}

function readIoTTable(markerNumber){
    let tableResources = document.getElementById("dev" + markerNumber);
    let resourceDict = {};
    for (let i = 0; i < tableResources.rows.length; i++) {
        let objCells = tableResources.rows.item(i).cells;
        let attr = objCells.item(0).innerHTML;
        let attrVal = objCells.item(1).firstChild.value;
        // Check attr type
        if(attr.includes("File size")){
            resourceDict["fileSize"] = attrVal;
        }else if(attr.includes("Local CPU")){
            resourceDict["localCPU"] = attrVal;
        }else if(attr.includes("Local processing")){
            resourceDict["localProcessing"] = attrVal;
        }else if(attr.includes("Storage")){
            resourceDict["storageReq"] = attrVal;
        }else if(attr.includes("RAM")){
            resourceDict["memReq"] = attrVal;
        }else if(attr.includes("Comm")){
            resourceDict["comRad"] = attrVal;
        }else if(attr.includes("Height")){
            resourceDict["height"] = attrVal;
        }
    }
    return resourceDict;
}

function iotAttributes(){
    return "attributes: {\n" +
        "\t key: filseSize_mb, type: int \n" +
        "\t key: local_CPU_ghz, type: float \n" +
        "\t key: localProcessing_ms, type: int \n" +
        "\t key: storageReq_mb, type: int \n" +
        "\t key: ramReq_mb, type: int \n" +
        "\t key: communicationRadius_m, type:float \n" +
        "}";
}

function iotEntry(markerNumber, locationDict, resourceDict){
    let reqTypeDropdown = document.getElementById("reqType" + markerNumber);
    let reqTypeValue = reqTypeDropdown.options[reqTypeDropdown.selectedIndex].text;
    let reqScheduleString = '';
    if(reqTypeValue.includes("Probabilistic")) {
        reqScheduleString += 'probabilisticRequestSchedule {\n';
        let reqSchedBody = document.getElementById("reqSchedBody" + markerNumber);
        let probSched = {};
        for (let i = 0; i < reqSchedBody.rows.length; i++) {
            let objCells = reqSchedBody.rows.item(i).cells;
            let attr = objCells.item(0).innerHTML;
            let attrVal = objCells.item(1).firstChild.value;
            // Check attr type
            if(attr.includes("Start")){
                probSched["start"] = attrVal;
            }else if(attr.includes("End")){
                probSched["end"] = attrVal;
            }else if(attr.includes("Interarrival")){
                let distribtuionDropdown = document.getElementById("reqDist" + markerNumber);
                probSched["interarrivalDist"] = distribtuionDropdown.options[distribtuionDropdown.selectedIndex].text;
                let paramTable = document.getElementById("param" + markerNumber);
                for (let i = 0; i < paramTable.rows.length; i++) {
                    let objCells = paramTable.rows.item(i).cells;
                    let attrParam = objCells.item(0).innerHTML;
                    if(attrParam.includes("lambda"))
                        probSched["lambda"] = objCells.item(1).firstChild.value;
                    else if(attrParam.includes("mu"))
                        probSched["mu"] = objCells.item(1).firstChild.value;
                    else if(attrParam.includes("var"))
                        probSched["var"] = objCells.item(1).firstChild.value;
                    else if(attrParam.includes("alpha"))
                        probSched["alpha"] = objCells.item(1).firstChild.value;
                    else if(attrParam.includes("beta"))
                        probSched["beta"] = objCells.item(1).firstChild.value;
                    else if(attrParam.includes("k"))
                        probSched["k"] = objCells.item(1).firstChild.value;
                }

            }
        }
        reqScheduleString += `\t\tstart:\t${probSched["start"]}\n`;
        reqScheduleString += `\t\tend:\t${probSched["end"]}\n`;
        reqScheduleString += `\t\tinterarrivalDistribution:\t${probSched["interarrivalDist"]}(`;
        if(probSched["interarrivalDist"].includes("Exponential")){
            reqScheduleString += `lambda=${probSched["lambda"]})\n}`
        }else if(probSched["interarrivalDist"].includes("Gaussian")){
            reqScheduleString += `mu=${probSched["mu"]}, var=${probSched["var"]})\n}`
        }else if(probSched["interarrivalDist"].includes("Gamma")){
            reqScheduleString += `alpha=${probSched["alpha"]}, beta=${probSched["beta"]})\n}`
        }else if(probSched["interarrivalDist"].includes("Beta")){
            reqScheduleString += `alpha=${probSched["alpha"]}, beta=${probSched["beta"]})\n}`
        }else if(probSched["interarrivalDist"].includes("Chi")){
            reqScheduleString += `k=${probSched["k"]})\n}`
        }else if(probSched["interarrivalDist"].includes("Dirichlet")){
            reqScheduleString += `alpha=${probSched["alpha"]})\n}`
        }
    } else if(reqTypeValue.includes("Consistent")) {
        reqScheduleString += 'consistentRequestSchedule {\n';
        let reqSchedBody = document.getElementById("reqSchedBody" + markerNumber);
        let probSched = {};
        for (let i = 0; i < reqSchedBody.rows.length; i++) {
            let objCells = reqSchedBody.rows.item(i).cells;
            let attr = objCells.item(0).innerHTML;
            let attrVal = objCells.item(1).firstChild.value;
            // Check attr type
            if (attr.includes("Start")) {
                probSched["start"] = attrVal;
            } else if (attr.includes("End")) {
                probSched["end"] = attrVal;
            } else if (attr.includes("Frequency")) {
                probSched["frequency"] = attrVal;
            }
        }
        reqScheduleString += `\t\tstart:\t${probSched["start"]}\n`;
        reqScheduleString += `\t\tend:\t${probSched["end"]}\n`;
        reqScheduleString += `\t\tgap:\t${probSched["frequency"]}\n}`;

    }
    else if(reqTypeValue.includes("Explicit")) {
        reqScheduleString += 'explicitRequestSchedule {\n';
        let reqSchedBody = document.getElementById("reqSchedBody" + markerNumber);
        let probSched = {};
        for (let i = 0; i < reqSchedBody.rows.length; i++) {
            let objCells = reqSchedBody.rows.item(i).cells;
            let attr = objCells.item(0).innerHTML;
            let attrVal = objCells.item(1).firstChild.value;
            // Check attr type
            if (attr.includes("Schedule")) {
                probSched["schedule"] = attrVal;
            }
        }
        reqScheduleString += `\t\t[${probSched["schedule"]}]\n}`;

    }
    console.log(reqScheduleString);

    return `\tthing t${markerNumber} {\n` +
        `\t\t${reqScheduleString}\n` +
        `\t\tlocation {\n` + // Location
        `\t\t\tlatitude: ${locationDict["lat"]} \n` +
        `\t\t\tlongitude: ${locationDict["lng"]} \n` +
        `\t\t\theight: ${resourceDict["height"]} \n` +
        `}\n\t\tattributes {\n` + // Resource attributes
        `\t\t\tfileSize_mb: ${resourceDict["fileSize"]}\n` +
        `\t\t\tlocal_CPU_ghz: ${resourceDict["localCPU"]}\n` +
        `\t\t\tlocalProcessing_ms: ${resourceDict["localProcessing"]}\n` +
        `\t\t\tstorageAvail_mb: ${resourceDict["storageAvail"]}\n` +
        `\t\t\tramAvail_mb: ${resourceDict["memAvail"]}\n` +
        `\t\t\tcommunicationRadius_m: ${resourceDict["comRad"]}\n` +
        `\t\t\tserviceRate: ${resourceDict["serviceRate"]}\n` +
        `\t\t}\n}`;
}

function readEdgeTable(markerNumber) {
    let tableResources = document.getElementById("dev" + markerNumber);
    let resourceDict = {};
    for (let i = 0; i < tableResources.rows.length; i++) {
        let objCells = tableResources.rows.item(i).cells;
        let attr = objCells.item(0).innerHTML;
        let attrVal = objCells.item(1).firstChild.value;
        // Check attr type
        if(attr.includes("Local CPU")){
            resourceDict["localCPU"] = attrVal;
        }else if(attr.includes("Local processing")){
            resourceDict["localProcessing"] = attrVal;
        }else if(attr.includes("Storage")){
            resourceDict["storageAvail"] = attrVal;
        }else if(attr.includes("RAM")){
            resourceDict["memAvail"] = attrVal;
        }else if(attr.includes("Comm")){
            resourceDict["comRad"] = attrVal;
        }else if(attr.includes("Service")){
            resourceDict["serviceRate"] = attrVal;
        }else if(attr.includes("Height")){
            resourceDict["height"] = attrVal;
        }
    }
    return resourceDict;
}

function edgeAttributes(){
    return "\tattributes: {\n" +
        "\t\tkey: local_CPU_ghz, type: float \n" +
        "\t\tkey: localProcessing_ms, type: int \n" +
        "\t\tkey: storageAvail_mb, type: int \n" +
        "\t\tkey: ramAvail_mb, type: int \n" +
        "\t\tkey: communicationRadius_m, type:float \n" +
        "\t\tkey: serviceRate, type: float \n" +
        "}";
}

function edgeEntry(markerNumber, locationDict, resourceDict){
    return `node n${markerNumber} {\n` +
        `\tlocation {\n` + // Location
        `\t\tlatitude: ${locationDict["lat"]} \n` +
        `\t\tlongitude: ${locationDict["lng"]} \n` +
        `\t\theight: ${resourceDict["height"]} \n` +
        `}\n\tattributes {\n` + // Resource attributes
        `\t\tlocal_CPU_ghz: ${resourceDict["localCPU"]}\n` +
        `\t\tlocalProcessing_ms: ${resourceDict["localProcessing"]}\n` +
        `\t\tstorageAvail_mb: ${resourceDict["storageAvail"]}\n` +
        `\t\tramAvail_mb: ${resourceDict["memAvail"]}\n` +
        `\t\tcommunicationRadius_m: ${resourceDict["comRad"]}\n` +
        `\t\tserviceRate: ${resourceDict["serviceRate"]}\n` +
        `\t}\n}`;
}

function exportMarkers(){
    let trs_candidates = {}; let trs_id = 0;
    let ens_candidates = {}; let ens_id = 0;
    let coordinateJSON;
    for (const i in coordinateList){
        // Device i type
        let locationDict = readLocation(i);
        markerNumber = +i + +1;
        let dropdown = document.getElementById('deviceType');
        dropdownValue = dropdown.options[dropdown.selectedIndex].text;
        let isIoT = dropdownValue.localeCompare("IoT");
        if(isIoT === 0){ // is IoT
            let resourceDict = readIoTTable(markerNumber);
            // Build TRS entry
            trs_candidates[trs_id++] = iotEntry(markerNumber, locationDict, resourceDict);
        } else{ // is Edge
            let resourceDict = readEdgeTable(markerNumber);
            // Build ENS entry
            ens_candidates[ens_id++] = edgeEntry(markerNumber, locationDict, resourceDict);
        }
    }

    let trsFile;
    if(trs_id > 0){
        trsFile  = "Thing IoT \n\t " + iotAttributes();
        for(let i_id = 0; i_id < trs_id; i_id++){
            trsFile = trsFile + '\n\t' + trs_candidates[i_id];
        }
        trsFile = trsFile + '\n}';
        console.log(trsFile);
    }

    let ensFile;
    if(ens_id > 0){
        ensFile = "Graph Edge \n\tnodeset {\n\t" + edgeAttributes();
        for(let e_id = 0; e_id < ens_id; e_id++){
            ensFile = ensFile + '\n\t' + ens_candidates[e_id];
        }
        ensFile = ensFile + '\n}\n}';
        console.log(ensFile);
    }



    //var jsonCandidatesString = markedCandidates.toString()
    //var jsonCandidates = '{"candidates":[' + jsonCandidatesString + ']}'
    //let jsonCandidates = {"location": markedCandidates};
    //let jsonCandidatesPretty = JSON.stringify(jsonCandidates, null, 2);
    //console.log(jsonCandidatesPretty);
    //let blob = new Blob([jsonCandidatesPretty],
    //    {type: "text/plain;charset=utf-8"});
   // saveAs(blob, "location.json");
}