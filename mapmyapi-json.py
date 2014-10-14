#!/usr/bin/python

import json
import urllib
import urllib2
import os.path
import pprint

#authorization stuff 
apikey=''
authorization=''
contenttype='application/json'
user=''
mytz='America/Los_Angeles'
jsondir = 'mapmyrun-json/'

headers = { 'Api-Key' : apikey,
            'Authorization' : authorization,
            'Content-Type' : contenttype }
limit=40
offset=0
activities='&activity_type=146&activity_type=208&activity_type=16'

base_url = 'https://oauth2-api.mapmyapi.com'

url = "/v7.0/workout/?user=" + user + "&offset=" + str(offset) + "&limit=" + str(limit) + activities
req = urllib2.Request('%s%s' % (base_url, url), None, headers)
r = urllib2.urlopen(req)
resp = json.loads(r.read())
r.close()

#get total number of items
total_count = resp.get('total_count')

while offset <= total_count:
	url = "/v7.0/workout/?user=" + user + "&offset=" + str(offset) + "&limit=" + str(limit) + activities
	req = urllib2.Request('%s%s' % (base_url, url), None, headers)
	r = urllib2.urlopen(req)
	resp = json.loads(r.read())
	r.close()
	workouts = resp.get('_embedded')
	for key,value in workouts.iteritems():
		for workout in value:
			links = workout.get('_links')
			self = links.get('self')
			id = self[0].get('id')
			jsonfile = jsondir + id + ".json"
			if not os.path.isfile(jsonfile):
				file = open(jsonfile,'w+')
				json.dump(workout,file)
				file.close()	
	offset = offset + limit
