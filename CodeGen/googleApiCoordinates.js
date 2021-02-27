let map;

var coordinateList = [];
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
    var newLatLng = inputVal.split(",");
    var newLat = parseFloat(newLatLng[0]);
    var newLng = parseFloat(newLatLng[1]);
    const myLatlng = {lat: newLat, lng: newLng};
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: myLatlng,
    });
    coordinateMarkers(map);
}

function coordinateMarkers(map){
    map.addListener("click", (e) => {
        var jsonCoordinates = e.latLng.toJSON();
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
    document.getElementById("form").appendChild(row);
}

function markerForm(markerNumber){
    var formHeader = document.createElement("h4");
    formHeader.innerText = "Resources " + markerNumber;
    document.getElementById("form").appendChild(formHeader);

    var tableResource = document.createElement("table");
    tableResource.style.borderSpacing = "15px";
    let tbody = tableResource.createTBody();
    tableRow(tbody, "CPU Resources:", "e.g. 3.42 GHz");
    tableRow(tbody, "STR Resources:", "e.g. 32.84 Gb");
    tableRow(tbody, "MEM Resources:", "e.g. 12.14 Gb");
}

function exportMarkerForm(){
    let labelIndex = 1;
    markedCandidates = {}
    for (const ll in coordinateList) {
        var id = labelIndex++;
        markerForm(id);
    }


}

function exportMarkers(){
    let labelIndex = 1;
    markedCandidates = {}
    for (const ll in coordinateList){
        var lat = coordinateList[ll]["lat"];
        var lng = coordinateList[ll]["lng"];
        //var coordinateJSON = '{"latitude":' + lat.toString() + ', "longitude":' + lng.toString() + ', "label":' + labelIndex.toString() + '}';
        var id = labelIndex++;
        var coordinateJSON = {
                "latitude": lat.toString(),
                "longitude": lng.toString(),
                "height" : 1.0
        };
        //var coordinate
        candidate = {};
        markedCandidates[id] = coordinateJSON;
        //markedCandidates.push(coordinateJSON);
    }
    //var jsonCandidatesString = markedCandidates.toString()
    //var jsonCandidates = '{"candidates":[' + jsonCandidatesString + ']}'
    var jsonCandidates = {"location": markedCandidates};
    var jsonCandidatesPretty = JSON.stringify(jsonCandidates, null, 2);
    console.log(jsonCandidatesPretty)
    var blob = new Blob([jsonCandidatesPretty],
        {type: "text/plain;charset=utf-8"});
    saveAs(blob, "location.json");
}