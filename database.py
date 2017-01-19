import urllib.request

def createURL(location, type, rooms, area):

	baseURL = "http://www.hemnet.se/salda/bostader?"
	
	return (baseURL + "location_ids%5B%5D=" + str(location) \
		+ "&item_types%5B%5D=" + str(type) + "&rooms_min=" + \
		str(rooms) + "&living_area_min=" + str(area))
		
		

url = "http://www.hemnet.se/salda/bostader?location_ids%5B%5D=18042&item_types%5B%5D=bostadsratt&rooms_min=1.5&living_area_min=35"

url2 = createURL("18042", "bostadsratt", 3, 65)

print(url2)

#file = "urlretrieve.html"

#site = urllib.request.urlopen(url)

#urllib.request.urlretrieve(url, file)