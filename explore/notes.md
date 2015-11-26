
# Notes on neighborhood clustering

## Data


###Have

* crime
	* [sf opendata](https://data.sfgov.org/Public-Safety/SFPD-Incidents-from-1-January-2003/tmnf-yvry) (lat, lon)
		* 107 MB

* business
	* (registered businesses sf)[https://data.sfgov.org/Economy-and-Community/Registered-Business-Locations-San-Francisco/g8m3-pdis]
		* by address
		* 38 MB

* address to lat lon
	* (http://geocoder.us/)
		* url request -> scrape
	* [US TIGER/line](http://www.census.gov/geo/maps-data/data/tiger.html)(tlgdb)
		* CA
		* address lookup database
		* 219 MB (zipped)

* demographics
	* population density
		* [Gridded population of the world](http://sedac.ciesin.columbia.edu/data/set/gpw-v3-population-density) (usa_gpwv)
			* 2.5 arc-minute bins
		* us census
			* http://factfinder.census.gov/
			* ~500 block group in SF
			* DEC_10_SF1_P1.zip (deleted for block-level)
			* http://tigerweb.geo.census.gov/tigerweb/ - display blocks map
		* us census, by block
			* count
			* 7388 blocks in sf
			* DEC_10_SF1_P1.zip
	* income
		* us census, by block group (~500 in SF)
			* ACS_13_5YR_B19001.zip
			* 16 income bins, count, margin of error
	* household size
		* us census, block level, 7388 in SF
			* DEC_10_SF1_H13.zip
	* sex by age
		* us census, block level, 7388 in SF
			* DEC_10_SF1_P12.zip
			* 23 age bins per gender


* property values
	* SF property assessment q4 2013
		* https://data.sfgov.org/City-Management-and-Ethics/Secured-Property-Assessment-Roll-FY13-Q4/e6sm-rank
		* 'secured property assessment'
		* ~ 200,000 addresses
		* 26.7 MB csv


* [yelp dataset](https://www.yelp.com/dataset_challenge/dataset)
	* business lat/lon, reviews, users
	* only select cities
	* 575 MB (zipped)

###Getting


###Potential

* yelp api
	* (https://www.yelp.com/developers/documentation/v2/overview)
	* 25,000 calls/day, up to 40 results/call -> 1M per day?
* [US Census](http://factfinder.census.gov/faces/nav/jsf/pages/download_center.xhtml)
* [sfdata](data.sfgov.org)
* walkscore
	* requested academic data
	* api: 5,000 requests per day
	* data snaps to lat/long on 500ft. grid
	* San Francisco: 7mi x 7mi -> 70 pts x 70 pts -> **4,900** pts

* property values
	* [sf assessor](http://propertymap.sfplanning.org/ )(okay scrape, from address)
* business $$$, ratings, density(grocery, gas, shop...)
* schools
* demographic
	* income
	* age
	* employment
* crime
	* [spotcrime](http://www.spotcrime.com/ca/san+francisco) (scrapable, single table on page, ~3 days) crime type by address
	* [crimereports](https://www.crimereports.com/)
		* scrapable; tables
		* 6 months, crime name, address, date; 1 month at a time
* address to lat lon
	* [census geocoder](https://www.census.gov/geo/maps-data/data/geocoder.html)
		* 1000 requests at a time
* schools
	* [greatschools](www.greatschools.org)
		* scrape/api: address, rating



###SF Open Data, checked
* all tabular data


###Ref

* [spatial cluster analysis](https://books.google.com/books?hl=en&lr=&id=4iqX4926x40C&oi=fnd&pg=PA395&dq=geographic+cluster+boundaries&ots=XHZIU6vDXB&sig=r-e74fc7v0jVtuNcz_gb5_xfB7k#v=onepage&q=geographic%20cluster%20boundaries&f=false) - google books
* [hood theory](https://hood.theory.org/) - sf neighborhoods based on housing posts from craigslist
* [wikipedia](https://en.wikipedia.org/wiki/Neighborhoods_in_San_Francisco) - sf neighborhoods - 36 official
* [Anson Whitmer](http://ansonwhitmer.tumblr.com/post/76570597222/sf-hoods-project) - Zipfian alum SF neighborhood project

## Database

* export postgres: `pg_dump DBNAME > dbexport.pgsql`

## Graph

* igraph - lots of c dependencies
* [**graph-tool**](https://graph-tool.skewed.de) - use this asap; 20x-170x faster than networkx

## Maps
* [gmpas.js](https://hpneo.github.io/gmaps/)
* [gmaps api](https://developers.google.com/maps/) - documentation
* [mapshaper](http://www.mapshaper.org/) - simplify shapefiles to reduce size
* [snazzymaps](https://snazzymaps.com/) - google maps color schemes
* [arcgis](http://crupley.maps.arcgis.com/) - utility for working with map data; dissolve boundaries
* shapely - python package - work with shapes, polygons, etc
* ogr2ogr - convert among file formats: shapefile, kml, geojson, csv, postgresql
	* [ogr file formats](http://www.gdal.org/ogr_formats.html)
* Tutorials
	* [macwrithe](http://www.macwright.org/2012/10/31/gis-with-python-shapely-fiona.html) - tutorial on python gis
	*[humangeo](http://blog.thehumangeo.com/2014/05/12/drawing-boundaries-in-python/) - drawing  boundaries in python
* [fastkml](https://fastkml.readthedocs.org/en/latest/usage_guide.html) - convert shapely elements to kml
* voronoi map tesselation: http://stackoverflow.com/questions/20515554/colorize-voronoi-diagram

## docstring
    """
    Reconstruct infinite voronoi regions in a 2D diagram to finite
    regions.

    Parameters
    ----------
    vor : Voronoi
        Input diagram
    radius : float, optional
        Distance to 'points at infinity'.

    Returns
    -------
    regions : list of tuples
        Indices of vertices in each revised Voronoi regions.
    vertices : list of tuples
        Coordinates for revised Voronoi vertices. Same as coordinates
        of input vertices, with 'points at infinity' appended to the
        end.

    """
