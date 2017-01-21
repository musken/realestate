import urllib.request
import re

prop = 			[	['<div',	'class="sold-property-listing">',											'</div>'],\
					['<span',	'class="item-result-meta-attribute-is-bold item-link">',					'</span>'],\
					['<span',	'class="item-link">',														'</span>'],\
					['<div',	'class="sold-property-listing__size">', 									'</div>'],\
					['<div',	'class="sold-property-listing__price">',									'</div>'],\
					['<div',	'class="sold-property-listing__price-change">',								'</div>'],\
					['<div',	'class="sold-property-listing__broker">'									'</div>']\
				]
				
pSize = 		[	['<div',	'class="sold-property-listing__subheading sold-property-listing--left">',	'</div>'],\
					['<div',	'class="sold-property-listing__fee">', 										'</div>']\
				]
				
pPrice =		[	['<span',	'class="sold-property-listing__subheading sold-property-listing--left">',	'</span>'],\
					['<div',	'class="sold-property-listing__sold-date sold-property-listing--left">',	'</div>'],\
					['<div',	'class="sold-property-listing__price-per-m2 sold-property-listing--left">',	'</div>']\
				]

class hemnet:
	
	def __init__(self, location, type, area, rooms):
		self.baseURL = "http://www.hemnet.se/salda/bostader?"
		self.location = location
		self.type = type
		self.area = area
		self.rooms = rooms
		self.url = self.createURL()
		
		
		
	def createURL(self):		
		return (self.baseURL + "location_ids%5B%5D=" + str(self.location) \
			+ "&item_types%5B%5D=" + str(self.type) + "&rooms_min=" + \
			str(self.rooms) + "&living_area_min=" + str(self.area))
			
	def fetchContent(self):
		return urllib.request.urlopen(self.url)
		
	def fetchDumpContent(self, file):
		f = open(file, 'w+')
		urllib.request.urlretrieve(self.url, file)
		f.close()
		
	# def parse(self, page = 1):
		# html = open("hemnetDump.html")
		# data = open("data.csv")
		# next = re.find("href=.+>Nästa", html.read())
		
		# for 
	def parse(self):
		html = open("hemnetDump.html", 'r')
		data = open("data.csv", 'w+')
		
		objects = re.split((prop[0][0]+' '+prop[0][1]), html.read())
		
		objects = objects[1:]
					
		i = 0
		for obj in objects:
			i += 1
			data.write('############ NEW OBJECT ('+str(i)+')##################')
			data.write(obj)
			data.write('\n\n\n\n\n')
			data.write('EXTRACTED DATA')
			
			for p in range(1, len(prop)-1):
				s = re.split(prop[p][0]+' '+prop[p][1], obj, re.S)
				if(len(s) >1):
					s = self.htmlParser(prop[p][0][1:], s[1])
					if(len(s) > 1):
						data.write('\n' + s[0])
			
			data.write('\n\n\n\n\n')
			break
			
		html.close()
		data.close()
	
		
	def htmlParser(self, enc, text):	
		occ = 0
		
		for i in range(0, len(text)-1):
			if(text[i:(i+len(enc)+1)] == ('<'+enc)):
				occ += 1;
			elif(text[i:(i+len(enc)+2)] == ('</' + enc)):
				if(occ == 0):
					return [text[:(i-1)], text[(i):]]
				else:
					occ -= 1
		return [text]


d = hemnet("18042", "bostadsratt", 65, 3)

d.parse()

#d.fetchDumpContent("hemnetDump.html")