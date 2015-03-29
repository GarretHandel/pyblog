#!/usr/bin/env python

import os, sys

print "Content-Type: text/html\n\n"
print "TEST"

debug = True

html = "Debugging Output:<br><br>"

if debug:
    for e in os.environ:
        html += "{0} :: {1}<br>".format(e, os.environ[e])
print html
sys.exit(0)
