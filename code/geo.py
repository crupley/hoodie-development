# Helper functions for working with geographic data

import numpy as np

REARTH = 3959 * 5280 # miles to feet

def make_geo_grid(start, nsrange, ewrange, in_feet=True):
	'''
	Makes a grid of latitude, longitude tuples stepped according to 
	north-south and east-west ranges.
	INPUT
		start: (latitude, longitude) tuple of starting point; tuple of float
		nsrange: locations of grid lines relative to start, in feet; list
		ewrange: locations of grid lines relative to start, in feet; list
		in_feet: are the steps in feet (True) or degrees (False); Boolean
	RETURNS
		array of lat,lon tuples spaced according to grid
	'''

	startlat, startlon = start
	nsgrid, ewgrid = np.meshgrid(nsrange, ewrange)
	if in_feet:
		latgrid, longrid = distance_to_angle(start, nsgrid, ewgrid)
		latgrid += startlat
		longrid += startlon
	else:
		latgrid, longrid = nsgrid, ewgrid

	return np.vstack((latgrid.ravel(),
					  longrid.ravel())).T



def distance_to_angle(start, ns, ew):
	'''
	INPUT
		start: starting coordinate as a lat, lon tuple; tuple
		ns: distance moved in the north-south direction in feet; float
		ew: distance move in the east-west direction in feet; float
	OUTPUT
		dlat, dlon: change in latitude, longitude; floats
	
	Convert distance along surface of earth to lat/lon change
	'''

	lat, lon = start
	lat = deg_to_rad(lat)
	lon = deg_to_rad(lon)

	dlat = ns / float(REARTH)
	dlon = ew / float(REARTH) / np.cos(lat)

	return (rad_to_deg(dlat), rad_to_deg(dlon))


def deg_to_rad(a):
	return a * np.pi / 180

def rad_to_deg(a):
	return a * 180 / np.pi


if __name__ == '__main__':
	# city limits: -122.5185:-122.35454, 37.70784:37.8195
	citycenter = (37.77, -122.454)
	stepsize = 500 #feet
	nsrange = np.arange(-3.5*5280, 3.5*5280, stepsize)
	ewrange = nsrange[:]
	g = make_geo_grid(citycenter, nsrange, ewrange)