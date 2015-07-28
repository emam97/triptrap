import urllib2
import json
 r=urllib2.urlopen("http://api.eventful.com/json/events/search?app_key=TpFKjZjQc76tZrpF&where=32.746682,-117.162741&within=25")
s= r.read()
import json
  d= json.loads(s)
