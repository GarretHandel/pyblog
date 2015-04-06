#!/usr/bin/env python

import os, sys, cgi, cgitb, HTML, re, json

cgitb.enable()

print "Content-Type: text/html\n\n"

form = cgi.FieldStorage()

page = form.getvalue("p", "home")
area = form.getvalue("a", "main")

dbFile = open('db.json', 'r')
dbInfo = json.load(dbFile)

debug = True

template = HTML.HTML(debug, 'Blog', page, area, **dbInfo)

for root, dirs, files in os.walk("js"):
    for f in files:
        template.addJS(os.path.join(root, f))

for root, dirs, files in os.walk("css"):
    for f in files:
        css = re.split(".", f)
        media = "" if css[0] == "main" else css[0]
        template.addLink("stylesheet", "text/css", os.path.join(root, f), media)

template.generateBody()

print template.render()
sys.exit(0)