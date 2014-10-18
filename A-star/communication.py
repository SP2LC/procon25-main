# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPDigestAuth
from StringIO import StringIO
import sys
import re
import math
import json
import os.path
import time

DIGEST_USER = "sp2lc"
DIGEST_PASS = "********"

PRACTICE_USER = "sp2lc"
PRACTICE_PASS = "********"

def make_problem(w, h):
    arr = []
    for i in range(w):
        column = []
        for j in range(h):
            column.append((i, j))
        arr.append(column)
    return arr

def get_problem(masterIP):
        para = None
        if masterIP[0:6] == "local:":
          while(not os.path.exists("timing")):
            time.sleep(0.01)
          f = open("problem.json", "r")
          para = json.load(f)
          f.close()
        elif masterIP[0:6] == "zero4:":
          while(not os.path.exists("zero4-timing")):
            time.sleep(0.01)
          f = open("zero4-problem.json", "r")
          para = json.load(f)
          f.close()
        else:
          r = requests.get('http://%s:8000' % masterIP, timeout=10000000)
          print r.text
          if not(r.json() == None):
                  para = r.json()
        if para != None:
          sortedImages = make_problem(para['columns'],para['rows'])
          for i in range(len(para['answer'])):
                  for j in range(len(para['answer'][0])):
                          sortedImages[i][j] = (para['answer'][i][j][0],para['answer'][i][j][1])
          print sortedImages

	return {'answer' : sortedImages , 'columns' : para['columns'], 'rows' : para['rows'], 'lim_select' : para['lim_select'], 'selection_rate' : para['selection_rate'], 'exchange_rate' : para['exchange_rate']}


def post(master, ans_str):
  if master[0:6] == "local:" or master[0:6] == "zero4:":
    master = master[6:]
  print ans_str
  r = requests.post("http://%s:8000/" % master, data = {'answer' : ans_str})
  print r.text
