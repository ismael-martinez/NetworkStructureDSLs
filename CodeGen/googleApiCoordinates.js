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
    markedCandidates = {};
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
    let resources = {};
    for (let i = 0; i < tableResources.rows.length; i++) {
        let objCells = tableResources.rows.item(i).cells;
        let attr = objCells.item(0).innerHTML;
        let attrVal = objCells.item(1).firstChild.value;
        // Check attr type
        if(attr.includes("File size")){
            resources["fileSize"] = attrVal;
        }else if(attr.includes("Local CPU")){
            resources["localCPU"] = attrVal;
        }else if(attr.includes("Local processing")){
            resources["localProcessing"] = attrVal;
        }else if(attr.includes("Storage")){
            resources["storageReq"] = attrVal;
        }else if(attr.includes("RAM")){
            resources["memReq"] = attrVal;
        }else if(attr.includes("ComRad")){
            resources["comRad"] = attrVal;
        }else if(attr.includes("height")){
            resources["height"] = attrVal;
        }
    }
    return resources;
}

function readEdgeTable(markerNumber) {
    let tableResources = document.getElementById("dev" + markerNumber);
    for (let i = 0; i < tableResources.rows.length; i++) {
        let objCells = tableResources.rows.item(i).cells;
        let attr = objCells.item(0).innerHTML;
        let attrVal = objCells.item(1).firstChild.value;
        // Check attr type
        if(attr.includes("Local CPU")){
            resources["localCPU"] = attrVal;
        }else if(attr.includes("Local processing")){
            resources["localProcessing"] = attrVal;
        }else if(attr.includes("Storage")){
            resources["storageReq"] = attrVal;
        }else if(attr.includes("RAM")){
            resources["memReq"] = attrVal;
        }else if(attr.includes("ComRad")){
            resources["comRad"] = attrVal;
        }else if(attr.includes("serviceRate")){
            resources["serviceRate"] = attrVal;
        }else if(attr.includes("height")){
            resources["height"] = attrVal;
        }
    }
    return resources;
}

function exportMarkers(){
    let labelIndex = 1;
    markedCandidates = {};
    let coordinateJSON;
    for (const i in coordinateList){
        // Device i type
        let location = readLocation(i);
        markerNumber = +i + +1;
        let dropdownTag = 'dropdown' + markerNumber;
        let dropdown = document.getElementById(dropdownTag);
        dropdownValue = dropdown.options[dropdown.selectedIndex].text;
        let isIoT = dropdownValue.localeCompare("IoT");
        if(isIoT === 0){
            readIoTTable(markerNumber);
        } else{
            readEdgeTable(markerNumber);
        }

        let lat = coordinateList[i]["lat"];
        let lng = coordinateList[i]["lng"];
        //var coordinateJSON = '{"latitude":' + lat.toString() + ', "longitude":' + lng.toString() + ', "label":' + labelIndex.toString() + '}';
        let id = labelIndex++;
        coordinateJSON = {
                "latitude": lat.toString(),
                "longitude": lng.toString(),
                "height" : 1.0
        };
        markedCandidates[id] = coordinateJSON;
        //markedCandidates.push(coordinateJSON);
    }
    //var jsonCandidatesString = markedCandidates.toString()
    //var jsonCandidates = '{"candidates":[' + jsonCandidatesString + ']}'
    let jsonCandidates = {"location": markedCandidates};
    let jsonCandidatesPretty = JSON.stringify(jsonCandidates, null, 2);
    console.log(jsonCandidatesPretty);
    let blob = new Blob([jsonCandidatesPretty],
        {type: "text/plain;charset=utf-8"});
    saveAs(blob, "location.json");
}