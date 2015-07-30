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

window.onload = function() {
  var startPos;
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    center: { lat: 47.61, lng: -122.33},
    zoom: 14
  });
  var geoSuccess = function(position) {
    startPos = position;
    lat = startPos.coords.latitude;
    lon = startPos.coords.longitude;
    function destination()
    {
    end_lat = document.getElementById("locationlat");
    end_lon = document.getElementById("locationlon");
    console.log(end_lat, end_lon);
    start = new google.maps.LatLng(lat, lon);
    end = new google.maps.LatLng(end_lat, end_lon);
    }
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
  directionsDisplay = new google.maps.DirectionsRenderer();
  var mapOptions = {
    zoom: 14,
    center: start
  }
  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  directionsDisplay.setMap(map);
}

function calcRoute() {
  var selectedMode = document.getElementById('mode').value;
  var request = {
      origin: start,
      destination: end,
      // Note that Javascript allows us to access the constant
      // using square brackets and a string value as its
      // "property."
      travelMode: google.maps.TravelMode[selectedMode]
  };
  var marker = new google.maps.Marker({
      position: start,
      map: map,
      title: 'You are here!'
  });
  directionsService.route(request, function(response, status) {
    if (status == google.maps.DirectionsStatus.OK) {
      directionsDisplay.setDirections(response);
    }
  });
}
