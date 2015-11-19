# notes on google maps javascript api

##Potentially useful [samples](https://developers.google.com/maps/documentation/javascript/examples/)

* simple map:

```html
    <div id="map"></div>
    <script>

var map;
function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: -34.397, lng: 150.644},
    zoom: 8
  });
}

    </script>
    <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"
        async defer></script>
```

* do things when things happen; [reference](https://developers.google.com/maps/documentation/javascript/3.exp/reference)

	```js
	map.addListener(event, function() {
	    infowindow.setContent('Zoom: ' + map.getZoom());
	  });
	```
	* useful events
		* mouseover - when mouse enters container
		* mouseout - mouse exits container
		* click

* KmlLayer class
	* setMap(map:Map) - renders kml on specified Map

* `myMap.data.addGeoJson(...);`



## Other resources

[mapbuildr](https://mapbuildr.com/buildr) - interactive google map property creation