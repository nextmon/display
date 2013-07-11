#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
import re
import time
import sys
from lxml.etree import ElementTree, parse
from StringIO import StringIO

import cgi
import cgitb
form = cgi.FieldStorage()

all_stops = (
    ('mit', "", (
        # tech shuttle tracking is broken: tech|wcamp|mass84
        ("Boston Daytime", "boston|boston|mass84_d", ),
        ("Northwest Shuttle", "northwest|nwcamp|mass77", ),
        ("Boston East", "saferidebostone|boston|mass84_d", ),
        ("Boston West", "saferidebostonw|boston|mass84_d", ),
        ("Boston All (West)", "saferidebostonall|boston|mass84", ),
        ("Cambridge East", "saferidecambeast|frcamp|mass84_d", ),
        ("Cambridge West", "saferidecambwest|frcamp|mass84_d", ),
        ("Cambridge All (West)", "saferidecamball|frcamp|mass84_d", ),
    ), ),
    ('mbta', "MBTA ", (
        ("MBTA 1 (→ Cambridge)", "1|1_0_var0|97", ),
    ), ),
)

hubway_stations = (
    (67, "MIT (Bexley)", ), #MIT at Mass Ave / Amherst St
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
    return '<table class="weather" align="center" cellspacing="20"><tr><td>' + \
        "<h2>"+time.strftime("%l:%M %p<br />%b %e")+"</h2>" + \
        "</td><td>" + \
        '<img src="%s" /><h2>%s&deg;F</h2>' % (img, cond.get("temp")) + \
        "</td></tr></table>"

def minutes(n):
    n = int(n)
    if n == 1:
        return "1 min"
    else:
        return "%s mins" % n

def build_url(agency, stops):
    url = "http://webservices.nextbus.com/service/publicXMLFeed?command=predictionsForMultiStops&a=" + agency
    url += "".join("&stops="+s for t,s in stops)
    return url

def print_predictions(agency, stops, label=""):
    url = build_url(agency, stops)
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
        print "<h2>"+title+"</h2>"
        #print "<h1>"+stops[n][0]+"</h1>"
        times = p.findall(".//prediction")
        print "<ol class='predictions'>"
        print '<li>%s</li>' % minutes(times.pop(0).get("minutes"))
        for t in times[0:2]:
            print '<li>%s</li>' % minutes(t.get("minutes"))
        print "</ol>"

def print_hubway(locationID, label=None):
    url = "http://thehubway.com/data/stations/bikeStations.xml"
    print >>sys.stderr, "Hubway", url
    f = urllib.urlopen(url)

    e = ElementTree(file=f)

    stations = e.findall("//station")
    stations = filter(lambda x: int(x.find("id").text) == locationID, stations)
    assert len(stations) == 1
    station = stations[0]

    name = label or station.find("name").text
    bikes = int(station.find("nbBikes").text)
    empty = int(station.find("nbEmptyDocks").text)
    total = bikes + empty
    tmpl = "<h2>%s</h2><img src=\"http://chart.apis.google.com/chart?chf=bg,s,65432100&amp;chs=175x87&amp;cht=p&amp;chdl=bikes%%3a%%20%d|docks%%3a%%20%d&amp;chco=6BC533|6A747C&amp;chd=t:%d,%d\">"
    print tmpl % (name, bikes, empty, bikes, empty)

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

print "<div class='routes'>"
for agency, label, stops in all_stops:
    print_predictions(agency, stops, label, )

for lid, label in hubway_stations:
    print_hubway(lid, label)

if 'urls' in form:
    print "<ul>"
    for agency, label, stops in all_stops:
        print "<li><a href='%s'>%s</a></li>" % (build_url(agency, stops), agency)
    print "</ul>"

print "</div>"

print """</body>
</html>"""
