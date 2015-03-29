#!/usr/bin/env python

import cgi, cgitb, re, sys, os, db

cgitb.enable(display=0, logdir="/logs")

filePath = os.path.join(os.environ["DOCUMENT_ROOT"], "files")


userAgent = os.environ["HTTP_USER_AGENT"]
if re.match("Mozilla", userAgent):
	pass
else:
	print "Content-Type: text/html\n\n"

html = ""



form = cgi.FieldStorage()
message = form.getvalue("message", "(no message)")

fname = os.path.join(filePath, os.environ["REMOTE_ADDR"])

if os.path.exists(fname):
    f = open(fname, 'r+')
    html += "Previous message:<br>"
    for line in f:
        html += "{0}<br>".format(line)
    html += "<br>New message:<br>"
    lines = re.split('\n', message)
    if lines is not None:
        for line in lines:
            html += "{0}<br>".format(cgi.escape(line))
    f.truncate(0)
    f.write(message)
    f.close()
else:
    html += "Previous message:<br>(no message)<br>"
    html += "<br>New message:<br>"
    lines = re.split('\n', message)
    if lines is not None:
        for line in lines:
            html += "{0}<br>".format(cgi.escape(line))
    f = open(fname, 'w')
    f.write(message)
    f.close()

html += "<br><br>Message stored at: http://{0}/files/{1}".format(os.environ["SERVER_NAME"], os.environ["REMOTE_ADDR"])

print html
sys.exit(0)