var map;
var infowindow;
var lat;
var lon;
var url;
window.onload = function() {
  var startPos;
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: { lat: 47.61, lng: -122.33},
    zoom: 15
  });
  var geoSuccess = function(position) {
    startPos = position;
    lat = startPos.coords.latitude;
    lon = startPos.coords.longitude;
    url = "/eventful?lat="+lat+"lon="+lon;
    console.log(url);
    $("a").attr('href',url);
    initialize();
  };
  navigator.geolocation.getCurrentPosition(geoSuccess);
};


function initialize() {
  var pyrmont = new google.maps.LatLng(lat, lon);

    map.panTo(pyrmont);

  var request = {
    location: pyrmont,
    radius: 500,
    types: ['store']
  };
  infowindow = new google.maps.InfoWindow();
  var service = new google.maps.places.PlacesService(map);
  service.nearbySearch(request, callback);
}

function callback(results, status) {
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      createMarker(results[i]);////
    }
  }
}

function createMarker(place) {
  var placeLoc = place.geometry.location;///
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location
  });

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent(place.name);////////
    infowindow.open(map, this);
  });
}
