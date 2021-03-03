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

function markerForm(markerNumber){
    // Device header
    let rowHeader = document.createElement("h4");
    rowHeader.innerText = "Device " + markerNumber;
    document.getElementById("form").appendChild(rowHeader);
    // Selection
    let dropdown = document.createElement("select");
    dropdown.setAttribute('id', 'dropdown' + markerNumber);
    dropdown.onchange = function(){resourceAttributes(markerNumber)};

    dropdown.options[0] = new Option("IoT");
    dropdown.options[1] = new Option("Edge");
    document.getElementById("form").appendChild(dropdown);

    let deviceDiv = document.createElement('div');
    deviceDiv.setAttribute("id", "div" + markerNumber);
    document.getElementById("form").appendChild(deviceDiv);

    let tableResource = document.createElement("table");
    tableResource.setAttribute('id', 'dev' + markerNumber);
    tableResource.style.borderSpacing = "15px";

    // Default
    let tbody = tableResource.createTBody();
    // Resources
    tableRow(tbody, "File size (MB)", "e.g. 536");
    tableRow(tbody, "Local CPU (GHz):", "e.g. 3.42");
    tableRow(tbody, "Local processing (ms)", "e.g. 234");
    tableRow(tbody, "Storage memory required (MB):", "e.g. 59");
    tableRow(tbody, "RAM required: (MB)", "e.g. 242");
    tableRow(tbody, "Communication radius (meters)", "e.g. 279");
    // Location
    tableRow(tbody, "Height (metres)", "e.g. 1.2");
    tableResource.appendChild(tbody);

    deviceDiv.appendChild(tableResource);
}

function resourceAttributes(markerNumber){
    let dropdown = document.getElementById('dropdown' + markerNumber);
    dropdownValue = dropdown.options[dropdown.selectedIndex].text;
    tableResource = document.getElementById("dev" + markerNumber);
    tableResource.innerHTML = '';
    let tbody = tableResource.createTBody();
    let isIoT = dropdownValue.localeCompare("IoT");
    if(isIoT === 0){
        // Resources
        tableRow(tbody, "File size (MB)", "e.g. 536");
        tableRow(tbody, "Local CPU (GHz):", "e.g. 3.42");
        tableRow(tbody, "Local processing (ms)", "e.g. 234");
        tableRow(tbody, "Storage memory required (MB):", "e.g. 59");
        tableRow(tbody, "RAM required: (MB)", "e.g. 242");
        tableRow(tbody, "Communication radius (meters)", "e.g. 279");
        // Location
        tableRow(tbody, "Height (metres)", "e.g. 1.2");
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

function exportMarkerForm(){
    let deviceForm = document.getElementById("form");
    deviceForm.innerHTML = '';
    let formHeader = document.createElement("h3");
    formHeader.innerText = "Device Information";
    deviceForm.appendChild(formHeader);
    let labelIndex = 1;
    for (const ll in coordinateList) {
        let id = labelIndex++;
        markerForm(id);
    }
    // Hold for now -- May add functionality later
    let exportButton = document.createElement("button");
    exportButton.textContent = "Export device resources";
    exportButton.onclick = function(){exportMarkers()};
    document.getElementById("form").appendChild(exportButton);

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
    return `\tthing t${markerNumber} {\n` +
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
        let dropdownTag = 'dropdown' + markerNumber;
        let dropdown = document.getElementById(dropdownTag);
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