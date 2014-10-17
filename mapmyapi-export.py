#!/usr/bin/python

import json
import urllib
import urllib2
import time
import datetime
from time import mktime
from datetime import datetime
import pytz

#authorization stuff 
apikey=''
authorization=''
contenttype='application/json'
user=''
mytz='America/Los_Angeles'

headers = { 'Api-Key' : apikey,
            'Authorization' : authorization,
            'Content-Type' : contenttype }
limit=40
offset=0
activities='&activity_type=146&activity_type=208&activity_type=16'
current_month = None
current_month_mileage = 0
all_time_mileage = 0
all_time_seconds = 0
all_time_runs = 0

base_url = 'https://oauth2-api.mapmyapi.com'

file = open('mapmyrun.txt','w+')

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
			all_time_runs = all_time_runs + 1
			notes = workout.get('notes')
			source = workout.get('source').split()
			agg = workout.get('aggregates')
			start_time = time.strptime(workout.get('start_datetime'), '%Y-%m-%dT%H:%M:%S+00:00')
			dt = datetime.fromtimestamp(mktime(start_time)).replace(tzinfo=pytz.utc)
			local = dt.astimezone(pytz.timezone(mytz))
			date = local.strftime('%a %m/%d/%y')
			month = local.strftime('%B')
			if month != current_month:
				current_month = month
				file.write('\n')
				if current_month_mileage > 0:
					file.write('Total Distance: ' + current_month_distance + ' miles\n')
					file.write('\n')
					current_month_mileage = 0
				file.write('--' + current_month + '--\n')
				file.write("Date : Distance : Pace : Duration : Avg HR : Min HR : Avg Speed : Max Speed : Cadence (Avg/Max) :: Source :: Notes \n")

			avgheartrate = agg.get('heartrate_avg')
			minheartrate = agg.get('heartrate_min')
			avgspeed = '%.2f' % round(float(agg.get('speed_avg') * 2.2369362920544),2)
			if agg.get('speed_max'):
				maxspeed = '%.2f' % round(float(agg.get('speed_max') * 2.2369362920544),2)
			else:
				maxspeed = '--'
			# convert from km to mi and round
			if agg.get('cadence_avg'):
				avgcad = int(agg.get('cadence_avg'))
			else:
				avgcad = '--'
			if agg.get('cadence_max'):
				maxcad = agg.get('cadence_max')
			else:
				maxcad = '--'

			cadence = str(avgcad) + '/' + str(maxcad)

			miles = float(agg.get('distance_total')) * 0.000621371
			current_month_mileage = current_month_mileage + miles
			all_time_mileage = all_time_mileage + miles
			all_time_distance = '%.2f' % round(all_time_mileage, 2)
			current_month_distance = '%.2f' % round(current_month_mileage, 2)
			distance = '%.2f' % round(miles, 2)

			duration_seconds = int(agg.get('active_time_total'))
			all_time_seconds = all_time_seconds + duration_seconds

			pace = ''
			if miles > 0:
				seconds_per_mile = duration_seconds / miles
			else:
				seconds_per_mile = 0
			hours, remainder = divmod(seconds_per_mile, 3600)
			minutes, seconds = divmod(remainder, 60)
			pace = '(%.0f\'%02.0f/mi)' % (minutes, seconds)
			durhours, durrem = divmod(duration_seconds, 3600)
			durmins, dursecs = divmod(durrem,60)

			file.write(str(date) + " : " + distance.ljust(5) + "mi " + pace.ljust(11) + "" + str(durhours).rjust(2, '0') + ":" + str(durmins).rjust(2,'0') + ":" + str(dursecs).rjust(2, '0') + " " + str(avgheartrate).ljust(5) + " " + str(minheartrate).ljust(5) + " " + avgspeed.ljust(5) + " " + maxspeed.ljust(5) + " : " + cadence.ljust(9) + " :: " + str(source[0]).ljust(12) + " :: " + str(notes) + "\n")
	
	offset = offset + limit

pace = ''
if miles > 0:
	seconds_per_mile = all_time_seconds / all_time_mileage
else:
	seconds_per_mile = 0
hours, remainder = divmod(seconds_per_mile, 3600)
minutes, seconds = divmod(remainder, 60)
pace = '(%.0f\'%02.0f/mi)' % (minutes, seconds)
durhours, durrem = divmod(all_time_seconds, 3600)
durmins, dursecs = divmod(durrem,60)

file.write('\n')
file.write('Total Distance: ' + current_month_distance + ' miles\n')
file.write('\n')
file.write('----------------\n')
file.write('All Time Metrics\n')
file.write('----------------\n')
file.write('Distance: ' + all_time_distance + ' miles\n')
file.write('Pace: ' + pace + '\n')
file.write('Duration: ' + str(durhours) + ":" + str(durmins) + ":" + str(dursecs) + '\n')
file.write('Runs: ' + str(all_time_runs) + '\n')
file.write('----------------\n')
file.close()
