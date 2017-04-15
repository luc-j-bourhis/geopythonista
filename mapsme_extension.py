import appex
import console
import geocoordinates

def main():
	if not appex.is_running_extension():
		print('Running in Pythonista app, using test data...\n')
		text = 'https://maps.google.co.uk/maps?oe=UTF-8&hl=en-gb&client=safari&um=1&ie=UTF-8&fb=1&gl=uk&entry=s&sa=X&ll=48.390394,-4.486076&z=12&ftid=0x4816bbe1d9925b93:0xc6488358179c30ab&q=Brest,+France&gmm=CgIgAQ%3D%3D&ved=0ahUKEwiSvZfG6JfTAhUCPBoKHWRJAc4Q8gEILjAB'
	else:
		text = appex.get_text()
	try:
		x = geocoordinates.Geocoordinates.from_google_map_url(text)
		x.open_in('maps.me')
	except geocoordinates.NotAGoogleMapUrl as err:
		msg = ('\n'.join(err.url.split('\n')[:5]) if err.url.find('\n') >= 0 else
					 err.url)
		console.alert(str(err), msg, 'OK', hide_cancel_button=True)
	finally:
		appex.finish()

if __name__ == '__main__':
	main()
