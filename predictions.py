#!/usr/bin/env python

import urllib
import re
import time
import sys
from lxml.etree import ElementTree

stops = """boston|boston|mass84_d
northwest|nwcamp|mass77
tech|wcamp|mass84
saferidebostone|boston|mass84_d
saferidebostonw|boston|mass84_d
saferidecambeast|frcamp|mass84_d
saferidecambwest|frcamp|mass84_d""".split()

def timeandweather():
    f = urllib.urlopen("http://www.google.com/ig/api?weather=02139")
    e = ElementTree(file=f)
    
    cond = e.find(".//current_conditions")

    return '<table align="center" cellspacing="20"><tr><td>' + \
        "<h1>"+time.strftime("%l:%M %p<br />%b %e")+"</h1>" + \
        "</td><td>" + \
        '<img src="http://www.google.com%s" /><h1>%s&deg;F</h1>' % (cond.find("icon").get("data"), cond.find("temp_f").get("data")) + \
        "</td></tr></table>"

url="http://www.nextbus.com/service/publicXMLFeed?command=predictionsForMultiStops&a=mit&stops="+"&stops=".join(stops)
print >>sys.stderr, url
f = urllib.urlopen(url)

e = ElementTree(file=f)

predictions = e.findall("//predictions")
predictions = filter(lambda el: el.find(".//prediction") is not None, predictions)
predictions.sort(key=lambda el: el.find(".//prediction").get("epochTime"))

print "Content-type: text/html"
print

print """<html>
<head>
<title>Current Predictions</title>
<style type="text/css">
body { background: black; color: white }
</style>
</head>
<body>"""
print timeandweather()

def minutes(n):
    n = int(n)
    if n == 1:
        return "1 minute"
    else:
        return "%s minutes" % n

for p in predictions:
    title = p.get("routeTitle")
    title = re.sub(r'^Saferide ', '', title)
    print "<h1>"+title+"</h1>"
    times = p.findall(".//prediction")
    print '<div class="big">%s</div>' % minutes(times.pop(0).get("minutes"))
    for t in times[0:2]:
        print '<div class="small">%s</div>' % minutes(t.get("minutes"))

print """</body>
</html>"""
