''' Utilities to manage longitude and latitude '''

from __future__ import division

import appex
from objc_util import UIApplication, nsurl
import re


class Error(RuntimeError):
	''' Any error raised in this module '''
		
		
class NotAGoogleMapUrl(Error):
	''' Erroneous attempt to extract coordinates fron a Google map URL
			that is not one actually.
	'''
	def __init__(self, url):
		Error.__init__(self, 'Not a Google map URL')
		self.url = url
			
			
class Geocoordinates:
	''' Coordinates of a point on the surface of the Earth 
	
			Properties and attributes:
				
				* longitude, latitude: in decimal degrees
	'''
	
	def __init__(self, longitude, latitude):
		'''
		Construct the location with the given longitude and latitude,
		in decimal degrees
		
		Synopsis:
			
		>>> x = Geocoordinates(1.5, -2.5)
		>>> x.longitude
		1.5
		>>> x.latitude
		-2.5
		'''
		self.longitude = longitude
		self.latitude = latitude
		
	coord_ = r'-?\d+\.\d+'
	google_map_url_pat_ = (re.compile(r'^ http s? : // .* ll = ({}) , ({})'
																	  .format(coord_, coord_),
																 	  re.X))	
			
	@classmethod
	def from_google_map_url(cls, url):
		'''
		Construct an instance of this class from a Google map URL
		
		Synopsis:
			
		>>> x = Geocoordinates.from_google_map_url('https://maps.google.com/maps?ll=1.5,-2.5')
		>>> x.longitude
		1.5
		>>> x.latitude
		-2.5
		>>> x = Geocoordinates.from_google_map_url(None)
		Traceback (most recent call last):
		...
		TypeError: expected string or buffer
		>>> x = Geocoordinates.from_google_map_url('zeus')
		Traceback (most recent call last):
		...
		NotAGoogleMapUrl: Not a Google map URL
		>>> 
		'''
		m = cls.google_map_url_pat_.search(url)
		if not m:
			raise NotAGoogleMapUrl(url)
		return cls(longitude=float(m.group(1)), latitude=float(m.group(2)))
		
	def as_text(self, separator):
		'''
		The longitude, then the latitude separated by the specified string
		
		Synopsis:
			
		>>> x = Geocoordinates(1.5, -2.5)
		>>> x.as_text(separator='  ')
		'1.5  -2.5'
		'''
		return '{.longitude}{}{.latitude}'.format(self, separator, self)
		
	xurl_format = {
		'maps.me': 'mapswithme://map?ll={.longitude},{.latitude}',
	}
		
	def as_xurl(self, app):
		'''
		The iOS URL callback to display self's location in the app 
		with the given moniker
		
		Synopsis:
			
		>>> x = Geocoordinates(1.5, -2.5)
		>>> x.as_xurl('maps.me')
		'mapswithme://map?ll=1.5,-2.5'
		'''
		return self.xurl_format[app].format(self, self)
		
	def open_in(self, app):
		''' Display self's location in the app with the given moniker '''
		from objc_util import UIApplication, nsurl
		app_ = UIApplication.sharedApplication()
		xurl = nsurl(self.as_xurl(app))
		app_.openURL_(xurl)

if __name__ == '__main__':
	import doctest
	doctest.testmod()
	
