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

* kml event

	```
  kmlLayer.addListener('click', function(kmlEvent) {
    var text = kmlEvent.featureData.description;
    showInContentWindow(text);
  });

  function showInContentWindow(text) {
    var sidediv = document.getElementById('content-window');
    sidediv.innerHTML = text;
  }
	```
	
	```
	<?xml version="1.0" encoding="utf-8"?>
	<kml xmlns="http://www.opengis.net/kml/2.2">
	  <Placemark>
	    <name>My office</name>
	    <description>This is the location of my office.</description>
	    <Point>
	      <coordinates>-122.087461,37.422069</coordinates>
	    </Point>
	  </Placemark>
	</kml>
	```
	On click, displays the text in the kml file under 'description'

* `document.getElementById("Name")` - get/set things in html area by id
	* `<p id="Name">text</p>`

## Other resources

* [mapbuildr](https://mapbuildr.com/buildr) - interactive google map property creation
* [kml reference](https://developers.google.com/kml/documentation/kmlreference)

## Charts

* [google charts](https://developers.google.com/chart/interactive/docs/)