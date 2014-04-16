$(document).ready(function() {
  var map;

  map = new GMaps({
    div: '#map',
    lat: -12.043333,
    lng: -77.028333,
  });

  GMaps.geolocate({
    success: function(position) {
      window.lat = position.coords.latitude;
      window.lng = position.coords.longitude;
      map.setCenter(position.coords.latitude, position.coords.longitude);
    },
    error: function(error) {
      alert('Geolocation failed: '+error.message);
    },
    not_supported: function() {
      alert("Your browser does not support geolocation");
    },
  });

  function geocode(address){
    GMaps.geocode({
      address: address,
      callback: function(results, status) {
        if (status == 'OK') {
          var latlng = results[0].geometry.location;
          map.setCenter(latlng.lat(), latlng.lng());
          map.addMarker({
            lat: latlng.lat(),
            lng: latlng.lng()
          });
        window.lat = latlng.lat();
        window.lng = latlng.lng();
        }
      }
    });
  }

  function inject_latlng() {
    var form, input;
    form = $("form#geo_lookup");

    input = $("<input></input>");
    input.attr("value", window.lat);
    input.attr("type", "hidden");
    input.attr("name", "lat");
    form.append(input);

    input = $("<input></input>");
    input.attr("value", window.lng);
    input.attr("type", "hidden");
    input.attr("name", "lng");
    form.append(input);
  }

  $("button[type='submit']").click(function(e){
    geocode($('#address').val());
    inject_latlng();
    $('form').submit();
  });

  $("#use_current_location").click(function(){
    inject_latlng();
    $('form').submit();
  });

// End ready
});