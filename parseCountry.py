import csv
import pycountry
from unidecode import unidecode
import re
from geopy.geocoders import Nominatim
import time

rows = []
with open("users_cleaned.csv", "r") as f:
	csvreader = csv.reader(f)
	header = next(csvreader)
	for row in csvreader:
		loc = unidecode(row[9])
		loc = re.sub('[,;:&]', ' ', loc)
		loc = re.sub('[^A-Za-z ]+', '', loc)
		loc = loc.strip()
		if loc :
			loc = " ".join([x[0].upper() + x[1:].lower() for x in loc.split()])
			rows.append([row[1], loc])

N = len(rows)

us_states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
	"Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
	"Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
	"Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
	"Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
	"North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
	"Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
	"Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming", 
	'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
	'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
	'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
	'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
	'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY', "Carolina"]
us_states = [i.lower() for i in us_states]

geolocator = Nominatim(user_agent="python")

with open("countries.txt", "r") as f:
	t = f.read().splitlines()
	done = [i.split(",")[0] for i in t]


S = 0

matches = {
	"uk": "United Kingdom",
	"russia": "Russia"
}

with open("countries2.txt", "a") as f:
	for uid, loc in rows:
		if uid in done :
			continue

		found = False
		for country in pycountry.countries:
			if country.name in loc:
				country = country.name
				found = True
				break

		if not(found):
			t = [i.lower() for i in loc.split()]
			for i in t:
				if i in us_states:
					country = "United States"
					found = True
				if i in matches:
					country = matches[i]
					found = True				
		
		if not(found):
			try:
				place = geolocator.geocode(loc, exactly_one=True, language="en", addressdetails=True)
				if place:
					country = place.raw['address']['country']
					found = True
			except:
				pass

		if found:
			f.write(f'{uid}, {country}\n')
			S+=1
		else:
			print(loc)

print(S, N, S/N)