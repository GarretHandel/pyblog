#!/usr/bin/env python

import os, sys, db, cgi, cgitb, re, json

class HTML(object):
    """used to generate the HTML code to be outputted"""
    def __init__(self, tStr, page, area, **dbInfo):
        self.incPath = os.path.join(os.environ["DOCUMENT_ROOT"], 'include')
        layout = open(os.path.join(self.incPath, 'all', 'layout.json'))
        self.layout = json.load(layout)
        layout.close()
        tags = open(os.path.join(self.incPath, 'all', 'tags.json'))
        self.tags = json.load(tags)
        tags.close()
        self.page = page
        pName = "Project 365" if page == "365" else "Project Life" if page == "projlife" else \
            "About" if page == "about" else "Contact" if page == "contact" else "Home"
        self.layout['head']['title'] = "{0} | {1}".format(tStr, pName)
        self.area = area
        self.db = db.connect(**dbInfo)

    def generateBody(self):
        areareaPath = os.path.join('include', self.area)
        incPath = os.path.join(os.environ["DOCUMENT_ROOT"], areaPath)
        # read file for area layout and add to main layout
        fPath = os.path.join(incPath, 'layout.json')
        mPath = os.path.join(incPath, 'menu.json')
        pPath = os.path.join(incPath, '{0}.json'.format(self.page))
        if os.path.exists(fPath):
            f = open(fPath, 'r')
            self.layout['body']['children'] = json.load(f)
            f.close()
            # read file for menu layout and add to main layout
            for x in self.layout['body']['children']:
                for y in self.layout['body']['childred'][x]:
                    if y == "menu" and os.path.exists(mPath):
                        self.layout['body']['children'][x][y] = json.load(open(mPath, 'r'))
                    if y == main and os.path.exists(pPath):
                        self.layout['body']['children'][x][y] = json.load(open(pPath, 'r'))
                    else:
                        self.layout['body']['children'][x][y] = "err404"

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
        body = self.tags['body'].format('Test')
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
        html = html.format(head, body)
        html = self.tags['doctype'].format(html)
        return html