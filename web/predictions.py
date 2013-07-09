#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re
import time
import sys
from lxml.etree import ElementTree, parse
from StringIO import StringIO

# tech shuttle tracking is broken: tech|wcamp|mass84
saferide_stops = (
    ("Boston Daytime", "boston|boston|mass84_d", ),
    ("Northwest Shuttle", "northwest|nwcamp|mass77", ),
    ("Boston East", "saferidebostone|boston|mass84_d", ),
    ("Boston West", "saferidebostonw|boston|mass84_d", ),
    ("Boston All (West)", "saferidebostonall|boston|mass84", ),
    ("Cambridge East", "saferidecambeast|frcamp|mass84_d", ),
    ("Cambridge West", "saferidecambwest|frcamp|mass84_d", ),
)

mbta_stops = (
    ("MBTA 1 (→ Cambridge)", "1|1_0_var0|97", ),
)

def timeandweather():
    # If this ever dies, there's always Microsoft:
    # http://weather.service.msn.com/find.aspx?outputview=search&src=Windows7&weasearchstr=02139&weadegreetype=F&culture=en-US

    f = urllib.urlopen("http://weather.yahooapis.com/forecastrss?w=12758738&u=f")
    e = ElementTree(file=f)
    
    cond = e.find(".//{http://xml.weather.yahoo.com/ns/rss/1.0}condition")

    img = e.findtext(".//item/description")
    img = parse(StringIO("<doc>%s</doc>" % img)).find(".//img").get("src")

    # cond.get("text") is nice too
    return '<table align="center" cellspacing="20"><tr><td>' + \
        "<h1>"+time.strftime("%l:%M %p<br />%b %e")+"</h1>" + \
        "</td><td>" + \
        '<img src="%s" /><h1>%s&deg;F</h1>' % (img, cond.get("temp")) + \
        "</td></tr></table>"

def minutes(n):
    n = int(n)
    if n == 1:
        return "1 min"
    else:
        return "%s mins" % n

def print_predictions(agency, stops, label=""):
    url = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictionsForMultiStops&a=" + agency
    url += "".join("&stops="+s for t,s in stops)
    print >>sys.stderr, url
    f = urllib.urlopen(url)

    e = ElementTree(file=f)

    predictions = e.findall("//predictions")
    predictions = filter(lambda el: el.find(".//prediction") is not None, predictions)
    predictions.sort(key=lambda el: el.find(".//prediction").get("epochTime"))

    for n, p in enumerate(predictions):
        title = p.get("routeTitle")
        title = re.sub(r'^Saferide ', '', title)
        title = label + title
        print "<h1>"+title+"</h1>"
        #print "<h1>"+stops[n][0]+"</h1>"
        times = p.findall(".//prediction")
        print '<div class="big">%s</div>' % minutes(times.pop(0).get("minutes"))
        for t in times[0:2]:
            print '<div class="small">%s</div>' % minutes(t.get("minutes"))

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

print_predictions('mit', saferide_stops)
print_predictions('mbta', mbta_stops, label="MBTA ")

print """</body>
</html>"""
