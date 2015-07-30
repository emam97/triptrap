var directionsDisplay;
var directionsService = new google.maps.DirectionsService();
var map;
var lat;
var lon;
var end_lat;
var end_lon;
var start;
var end;
var infowindow;
var url;
var url1;
var startPos;
var geocoder;
// function destination()
// {
// end_lat = document.getElementById("locationlat").value;
// end_lon = document.getElementById("locationlon").value;
// console.log(end_lat, end_lon);
// }
window.onload = function() {
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: { lat: 47.61, lng: -122.33},
    zoom: 14
  });
  var geoSuccess = function(position) {
    startPos = position;
    lat = startPos.coords.latitude;
    lon = startPos.coords.longitude;
    start = new google.maps.LatLng(lat, lon);
    end = new google.maps.LatLng(end_lat, end_lon);
    url = "/eventful?lat="+lat+"lon="+lon;
    console.log(url);
    $("#eventful").attr('href',url);
    url1 = "/yelp?lat="+lat+","+lon;
    console.log(url1);
    $("#yelp").attr('href',url1);
    $("#hidden_lat").attr('value', (lat + "," + lon));
    initialize(start, end);
  };
  navigator.geolocation.getCurrentPosition(geoSuccess);
};

function initialize(start, end) {
  geocoder = new google.maps.Geocoder();
  directionsDisplay = new google.maps.DirectionsRenderer();
  var mapOptions = {
    zoom: 14,
    center: start
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  directionsDisplay.setMap(map);
  var marker = new google.maps.Marker({
      position: start,
      map: map
  });
}

function calcRoute(name) {
  // end_lat = document.getElementById(name+"lat").value;
  // end_lon = document.getElementById(name+"lon").value;
  // console.log(end_lat, end_lon);
  var address = document.getElementById(name).value;
  console.log(address);
  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map,
          position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
  var selectedMode = document.getElementById('mode').value;
  start = new google.maps.LatLng(lat, lon);
  end = address;
  console.log(end);
  var request = {
      origin: start,
      destination: end,
      // Note that Javascript allows us to access the constant
      // using square brackets and a string value as its
      // "property."
      travelMode: google.maps.TravelMode[selectedMode]
  };
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
    }
  });
}
