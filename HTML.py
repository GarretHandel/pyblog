#!/usr/bin/env python

import os, sys, db, cgi, cgitb, re, json, operator

class HTML(object):
    """used to generate the HTML code to be outputted"""
    def __init__(self, debug, tStr, page, area, **dbInfo):
        docRoot = os.environ["DOCUMENT_ROOT"]
        self.incPath = os.path.join(docRoot, 'layout')
        layout = open(os.path.join(self.incPath, 'all', 'layout.json'))
        self.layout = json.load(layout)
        layout.close()
        tags = open(os.path.join(self.incPath, 'all', 'tags.json'))
        self.tags = json.load(tags)
        tags.close()
        self.page = page
        pages = {"home": "Home", "365": "Project 365", "projlife": "Project Life", "about": "About", "contact": "Contact"}
        pName = pages[page]
        self.layout['head']['title'] = "{0} | {1}".format(tStr, pName)
        self.area = area
        self.db = db.connect(**dbInfo)
        self.debug = debug
        self.debugOut = ''
        self.debugBody = ''

    def generateBody(self):
        areaPath = os.path.join(self.incPath, self.area)
        # load layout paths
        layoutPath = os.path.join(areaPath, 'layout.json')
        menuPath = os.path.join(areaPath, 'menu.json')
        pagePath = os.path.join(areaPath, '{0}.json'.format(self.page))
        self.debugOut += '<p>Loading packages: <br>{0}</p>'
        self.debugOut = self.debugOut.format('<br> '.join([layoutPath, menuPath, pagePath]))
        # read file for area layout and add to main layout
        if os.path.exists(layoutPath):
            f = open(layoutPath, 'r')
            self.layout['body']['html'] = json.load(f)
            f.close()
            # read file for menu layout and add to main layout
            for x in self.layout['body']['html']:
                for y in self.layout['body']['html'][x]:
                    if self.debug:
                        self.debugOut += "<br>Checking layout for: {0}<br>".format(y)
                    if y == "menu":
                        if os.path.exists(menuPath):
                            self.debugOut += "Loaded menu layout<br>"
                            self.layout['body']['html'][x][y]['html'] = json.load(open(menuPath, 'r'))
                        else:
                            self.layout['body']['html'][x][y]['html'] = "err404"
                    elif y == "main":
                        if os.path.exists(pagePath):
                            self.debugOut += "Loaded page layout<br>"
                            self.layout['body']['html'][x][y]['html'] = json.load(open(pagePath, 'r'))
                        else:
                            self.layout['body']['html'][x][y]['html'] = "err404"
                    else:
                        # retain original contents
                        pass
        self.debugOut += "<br>Body contents: <br>{0}<br>".format(self.layout['body'])

    def recurse(self, d):
        d = sorted(d.items(), key=operator.itemgetter(0))
        html = ''
        for k, v in d:
            try:
                if k in self.tags:
                    tag = self.tags[k]
                    attrs = ''
                    for ak in v['attrs']:
                        attrs += ' {0}="{1}"'.format(ak, v['attrs'][ak])
                    if isinstance(v['html'], dict):
                        html += tag.format(attrs, self.recurse(v['html']))
                    else:
                        html += tag.format(attrs, v['html'])
                else:
                    if isinstance(v, dict):
                        html += self.recurse(v)
            except KeyError:
                if isinstance(v, dict):
                    html += self.recurse(v)
        return html

    """Add JavaScript script to HTML head section"""
    def addJS(self, sPath="", sBody=""):
        index = 0 if len(self.layout['head']['js']) < 1 else len(self.layout['head']['js']) + 1
        self.layout['head']['js'][index] = {'src': sPath, 'body': sBody}

    """Add a new link to the HTML head section"""
    def addLink(self, lRel, lType, lPath, lMedia):
        index = 0 if len(self.layout['head']['links']) < 1 else len(self.layout['head']['links']) + 1
        self.layout['head']['links'][index] = {'rel': lRel, 'type': lType, 'href': lPath, 'media': lMedia}

    def addMeta(self, name, content):
        index = 0 if len(self.layout['head']['meta']) < 1 else len(self.layout['head']['meta']) + 1
        self.layout['head']['meta'][index] = {'name': name, 'content': content}

    def addTagToBody(self, tagName, body, **attrs):
        index = 0 if len(self.layout['body']) < 1 else len(self.layout['body']) + 1
        self.layout['body'][index] = {'tag': tagName, 'body': body, 'attrs': attrs}

    """Output generated HTML code"""
    def render(self):
        html = self.tags['html']
        head = self.tags['head']
        title = self.tags['title'].format(self.layout['head']['title'])
        body = self.tags['body']
        metaItems = ''
        metaTag = self.tags['meta']
        for x in self.layout['head']['meta']:
            metaItems = '\n'.join([metaItems, metaTag.format(self.layout['head']['meta'][x]['name'], self.layout['head']['meta'][x]['content'])])
        linkItems = ''
        linkTag = self.tags['link']
        for x in self.layout['head']['links']:
            linkItems = '\n'.join([linkItems, linkTag.format(self.layout['head']['links'][x]['rel'], self.layout['head']['links'][x]['type'], \
                self.layout['head']['links'][x]['href'], self.layout['head']['links'][x]['media'])])
        jsItems = ''
        jsTag = self.tags['script']
        for x in self.layout['head']['js']:
            jsItems = '\n'.join([jsItems, jsTag.format(self.layout['head']['js'][x]['src'], self.layout['head']['js'][x]['body'])])
        head = head.format(title, metaItems, linkItems, jsItems)
        children = self.recurse(self.layout['body']['html'])
        children += '<a href="?debug={0}">Turn Debugging {1}</a>'.format(int(not self.debug), "On" if self.debug is False else "Off")
        if self.debug:
            children = self.debugOut + self.debugBody + children
        body = body.format(children)
        html = html.format(head, body)
        html = self.tags['doctype'].format(html)
        return html
        