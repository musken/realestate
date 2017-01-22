import urllib.request
import re

prop = 			[	['div',	'class="sold-property-listing">'],\
					['span',	'class="item-result-meta-attribute-is-bold item-link">'],\
					['span',	'class="item-link">'],\
					['div',	'class="sold-property-listing__price-change">'],\
					['div',	'class="sold-property-listing__broker">'],\
					['div',	'class="sold-property-listing__subheading sold-property-listing--left">'],\
					['div',	'class="sold-property-listing__fee">'],\
					['span',	'class="sold-property-listing__subheading sold-property-listing--left">'],\
					['div',	'class="sold-property-listing__sold-date sold-property-listing--left">'],\
					['div',	'class="sold-property-listing__price-per-m2 sold-property-listing--left">']\
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
	
	def brackets(self, id):
		return ['<'+id+' ','</'+id+'>'] 
		
	def parse(self):
		html = open("hemnetDump.html", 'r')
		data = open("data.csv", 'w+')
		
		b = self.brackets(prop[0][0])
		objects = re.split(b[0]+prop[0][1], html.read())
		
		objects = objects[1:]
					
		i = 0
		for obj in objects:
			i += 1			
			
			for p in prop[1:]:
				content = self.htmlParser(obj, p)
				if(len(content)>1):
					data.write(content[0])
					data.write('\n')
			break
			
		html.close()
		data.close()
	
	def xtrctSubCat(self, list, s):
		res = []		
		for p in list:
			tmp = re.split(p[0]+' '+p[1], s, re.S)
			if(len(tmp)>1):
				tmp = self.htmlParser(p[0][1:], tmp[1])
				if(len(tmp) > 1):
					res.append(tmp(1))	
		return res
		

	def htmlParser(self, text, element):	
		occ = 0
		enc = self.brackets(element[0])
		s = re.split(element[1], text, re.S)
		s = s[1]
		for i in range(0, len(s)-1):
			if(s[i:(i+len(enc[0]))] == (enc[0])):
				occ += 1;
			elif(s[i:(i+len(enc[1]))] == (enc[1])):
				if(occ == 0):
					return [s[:(i-1)].strip(), s[(i):]]
				else:
					occ -= 1
		return [s]


d = hemnet("18042", "bostadsratt", 65, 3)

d.parse()

#d.fetchDumpContent("hemnetDump.html")