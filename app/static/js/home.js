function updatedListingsDisplay() {
  console.log(listings);
  var list = document.getElementById('listingList').children;
  var sortedList = [];
  //sortedList.className = "list";
  //console.log(list);
  var listingCounter = 0;
  var listCounter = 0;
  for (listingCounter = 0; listingCounter < Object.keys(listings).length; listingCounter++) {
    for (listCounter = 0; listCounter < list.length; listCounter++) {
      // console.log(listings[listingCounter]['listingID']);
      //  console.log(list[listCounter].id);
      if (listings[listingCounter]['listingID'] == list[listCounter].id) {
        sortedList[listingCounter] = list[listCounter];
        //  console.log("ran");
        //  console.log(listCounter);
      }
    }
  }
  console.log(sortedList);
  var realList = document.getElementById('listingList')
  realList.innerHTML = '';
  for (listCounter = 0; listCounter < sortedList.length; listCounter++) {
    //    console.log(sortedList[listCounter]);
    realList.appendChild(sortedList[listCounter]);
  }
  //  console.log(realList);
}


function findCurrentLocationGoog() {
  return new Promise(function(resolve, reject) {
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        infoWindow.setPosition(pos);
        infoWindow.setContent('Location found.');
        infoWindow.open(map);
        map.setCenter(pos);
        resolve(pos);
      }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
        resolve({
          lat: 0,
          lng: 0
        });
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
      resolve({
        lat: 0,
        lng: 0
      });
    }
  });
}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
    'Error: The Geolocation service failed.' :
    'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}


function sortDistances(locations, currentLocation) {
  return new Promise(function(resolve, reject) {
    var service = new google.maps.DistanceMatrixService();
    //console.log(locations[1]);
    service.getDistanceMatrix({
      origins: [currentLocation],
      destinations: locations,
      travelMode: 'DRIVING'
    }, function(response, status) {
      // See Parsing the Results for
      // the basics of a callback function.
      var dests = response.destinationAddresses;
      var data = response.rows[0]['elements'];
      //  console.log(realMarkerPositions);
      //console.log(response);
      var distances = [];
      var counter = 0;
      for (counter; counter < data.length; counter++) {
        if (data[counter].status != "ZERO_RESULTS") {
          var distance = data[counter].distance.text;
          //console.log(distance);
          if (distance[distance.length - 2] == "k") {
            distances.push(parseFloat(distance.slice(0, distance.length - 3)));
          } else {
            distances.push(parseFloat(distance.slice(0, distance.length - 2)));
          }
        }
      }
      //   console.log(distances);
      var distancesToSort = distances.slice();
      distancesToSort.sort(function(a, b) {
        return a - b
      });
      //console.log(distances);
      // console.log(distancesToSort);
      //var sortedData = [];
      var sortedMarkerPositions = [];
      var distanceCounter = 0;
      for (counter = 0; counter < distances.length; counter++) {
        for (distanceCounter = 0; distanceCounter < distancesToSort.length; distanceCounter++) {
          if (distances[counter] == distancesToSort[distanceCounter]) {
              sortedMarkerPositions[distanceCounter] = realMarkerPositions[counter];
              distancesToSort[distanceCounter] = {};
              distances[counter] = {};
          }
        }
      }
      //  console.log(sortedMarkerPositions);
      var sortedMarkerPositionsCopy = sortedMarkerPositions.slice();
      var sortedListings = {};
      for (counter = 0; counter < realMarkerPositions.length; counter++) {
        for (distanceCounter = 0; distanceCounter < sortedMarkerPositions.length; distanceCounter++) {
          if (realMarkerPositions[counter] == sortedMarkerPositionsCopy[distanceCounter]) {
            sortedListings[distanceCounter] = listings[counter];
            sortedMarkerPositionsCopy[distanceCounter] = {};
            realMarkerPositions[counter] = {};
          }
        }
      }
      resolve([sortedListings, sortedMarkerPositions]);
    });
  });
}


function countOccurences(a, obj) {
  var stupidCounter = 0;
  //console.log(a);
  for (var newindex = 0; newindex < obj.length; newindex++) {
    if ((typeof(obj[newindex]) != "undefined") && (Math.abs(obj[newindex]['lat'] - a['lat']) < .00000001) && (Math.abs(obj[newindex]['lng'] - a['lng']) < .00000001)) {
      stupidCounter++;
      //console.log(obj[newindex]);
      //console.log(a);
    }
  }
  //  console.log(a);
  //  console.log(obj);
  //  console.log(stupidCounter);
  return stupidCounter;
}


function findLatLang(address, i, geocoder) {
  return new Promise(function(resolve, reject) {
    geocoder.geocode({
      'address': address
    }, function(results, status) {
      //  console.log(results);
      //console.log(status);
      if (status === 'OK') {
        //console.log(results);
        resolve([results[0].geometry.location.lat(), results[0].geometry.location.lng()]);
      } else {
        realMarkerPositions[i] = {
          lat: 0,
          lng: 0
        };
        //console.log("ran");
        reject(new Error('Couldnt\'t find the location ' + address));
      }
    })
  })
}


function getMarkerPositions(geocoder) {
  var markerPositions = [];
  var i;
  for (i = 0; i < Object.keys(listings).length; i++) {
    //console.log(i);
    if (listings[i]['location'] == "None") {
      markerPositions[i] = {
        lat: 0,
        lng: 0
      };
    } else if (listings[i]['location'][0] != "{") {
      // console.log(codeAddress(listings[i]['location']));
      // markerPositions[i] = codeAddress(listings[i]['location']);
      var newPromise = findLatLang(listings[i]['location'], i, geocoder);
      markerPositions[i] = {
        lat: newPromise[0],
        lng: newPromise[1]
      };
      promised.push(newPromise);

      //  console.log(markerPositions[i]);
    } else {
      var j;
      var markerPosition = {
        lat: "",
        lng: ""
      };
      var past = 0;
      for (j = 1; j < listings[i]['location'].length - 1; j++) {
        if ((listings[i]['location'][j] == ":") || (listings[i]['location'][j] == ",")) {
          past++;
        } else if (past == 1) {
          markerPosition['lat'] += listings[i]['location'][j];
        } else if (past == 3) {
          markerPosition['lng'] += listings[i]['location'][j];
        }
      }
      markerPosition['lat'] = parseFloat(markerPosition['lat']);
      markerPosition['lng'] = parseFloat(markerPosition['lng']);
      //console.log(markerPosition);
      markerPositions[i] = markerPosition;
      // var marker = new google.maps.Marker({
      //   map: map,
      //   position: markerPosition
      // });
    }
  }
  return markerPositions;
}
var allGoogMarkers = [];
var searchedMarker;

function setUpSearchBox(newMarkers) {
  //console.log(realMarkerPositions);
  // Create the search box and link it to the UI element.
  var input = document.getElementById('pac-input');
  var searchBox = new google.maps.places.SearchBox(input);


  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  var markerCounter = 0;
  for (markerCounter; markerCounter < newMarkers.length; markerCounter++) {
    var newMarker = new google.maps.Marker({
      map: map,
      position: newMarkers[markerCounter]
    });
    newMarker.id = "M" + listings[markerCounter]['listingID'];
    //console.log(newMarker);
    newMarker.addListener('click', function() {
      map.setCenter(this.position);
      var correspondingListing = document.getElementById(this.id.slice(1));
      correspondingListing.scrollIntoView();
      select(this.id.slice(1));
    });

    allGoogMarkers[markerCounter] = newMarker;
    //console.log(document.getElementById("M" + listings[markerCounter]['listingID']));
    // newMarker.then(function(result){
    //   console.log(result);
    // });
    var correspondingListing = document.getElementById(newMarker.id.slice(1));
    correspondingListing.addEventListener('click', function(){
      console.log(allGoogMarkers);
      var corMarker;
      for (var ss=0; ss<allGoogMarkers.length; ss++){
        if (allGoogMarkers[ss].id == "M" + this.id){
          corMarker = allGoogMarkers[ss];
        }
      }
      console.log(corMarker);
      map.setCenter(corMarker.position);
      select(this.id);
    });
  }

  var markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // // Clear out the old markers.
    // markers.forEach(function(marker) {
    //   marker.setMap(null);
    // });
    // markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      if (!place.geometry) {
        console.log("Returned place contains no geometry");
        return;
      }
      // var icon = {
      //   url: place.icon,
      //   size: new google.maps.Size(71, 71),
      //   origin: new google.maps.Point(0, 0),
      //   anchor: new google.maps.Point(17, 34),
      //   scaledSize: new google.maps.Size(25, 25)
      // };
      if (document.getElementById('searched') == null) {
        // Create a marker for each place.
        if (typeof(searchedMarker) == "undefined"){
          searchedMarker = new google.maps.Marker({map: map, title:place.name, position: place.geometry.location});
        } else {
          searchedMarker.setPosition(place.geometry.location);
          searchedMarker.setTitle(place.name);
        }
        // markers.push(new google.maps.Marker({
        //   map: map,
        //   title: place.name,
        //   position: place.geometry.location,
        //   id: "searched"
        // }));
      } else {
        document.getElementById('searched').position = place.geometry.location;
      }

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }

      var newPromise = sortDistances(realMarkerPositions, place.geometry.location);
      newPromise.then(function(superReturnVals) {
        listings = superReturnVals[0];
        realMarkerPositions = superReturnVals[1];
        //  console.log(superReturnVals);
        updatedListingsDisplay();
      });

    });
    map.fitBounds(bounds);
  });
}

var currentHover = "";

function hover(id) {
  //  console.log(id);
  var newHover = document.getElementById(id);
  newHover.children[0].className = newHover.children[0].className + " shadow-lg";
}

function unhover(id) {
  var oldHover = document.getElementById(id);
  oldHover.children[0].className = oldHover.children[0].className.slice(0, oldHover.children[0].className.length - 10);
}

var alreadySelected = "";

function select(id){
  var newlySelected = document.getElementById(id);
  if (alreadySelected == ""){
    alreadySelected = newlySelected;
    newlySelected.children[0].style['border-width'] = 'medium';
    newlySelected.children[0].style['border-color'] = 'blue';
} else if (newlySelected != alreadySelected){
  //  alreadySelected.children[0].style = alreadySelected.children[0].style.slice(0, alreadySelected.children[0].style.length - 38)
    alreadySelected.children[0].style['border-width'] = '';
    alreadySelected.children[0].style['border-color'] = '';
    //console.log(alreadySelected.children[0].style);
    newlySelected.children[0].style['border-width'] = 'medium';
    newlySelected.children[0].style['border-color'] = 'blue';
    alreadySelected = newlySelected;
  } else if (newlySelected == alreadySelected){
    alreadySelected.children[0].style['border-width'] = '';
    alreadySelected.children[0].style['border-color'] = '';
    alreadySelected = "";
  }
}
