#!/usr/bin/env python

import os, sys, cgi, cgitb, HTML, re, json

cgitb.enable()

print "Content-Type: text/html\n\n"

form = cgi.FieldStorage()

page = form.getvalue("p", "home")
area = form.getvalue("a", "main")
debug = bool(int(form.getvalue("debug", 0)))

dbFile = open('db.json', 'r')
dbInfo = json.load(dbFile)

template = HTML.HTML(debug, 'Blog', page, area, **dbInfo)

for root, dirs, files in os.walk("js"):
    for f in files:
        template.addJS(os.path.join(root, f))

for root, dirs, files in os.walk("css"):
    for f in files:
        css = re.split("\.", f)[0]
        media = "screen"
        if css == area:
            template.addLink("stylesheet", "text/css", os.path.join('http://'+os.environ['SERVER_NAME'], root, f), media)

template.generateBody()

print template.render()
sys.exit(0)