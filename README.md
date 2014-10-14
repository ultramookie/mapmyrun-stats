mapmyrun-stats
==============

pull run stats from mapmyrun (mapmyfitness) to create a simple text file with some
basic aggregations.

for authentication...

sign up at https://www.mapmyapi.com and get your client key and client secret by
registering an app with mapmyapi. the easiest way to get an access token is to
use the api explorer: https://www.mapmyapi.com/io-docs which has lets you play
with the api using your client key/secret, there is an authorization process at
the top that will spit out an access token when you use it for the first time.

in the script the vars at the top...
apikey: client key
authorization: access token in this format... "Bearer ACCESS_TOKEN"
user: your userid. hover over your avatar and it's your profile id number
mytz: your local timezone (eg.'America/Los_Angeles')

the activites var defines what activity types to pull in. i have it set by default
to run/jog (16) and treadmill (146 & 208).

activities='&activity_type=146&activity_type=208&activity_type=16'

