#!/usr/bin/env python

import MySQLdb, sys, os, re

"""Returns a database cursor object"""
def connect(**dbInfo):
    db = MySQLdb.connect(host=dbInfo['host'], user=dbInfo['user'], passwd=dbInfo['passwd'], db=dbInfo['db'])
    return db.cursor()
