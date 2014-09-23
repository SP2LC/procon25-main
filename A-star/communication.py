# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPDigestAuth
from StringIO import StringIO
import sys
import re
import math

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
	r = requests.get('http://%s:8000' % masterIP, timeout=10000000)
	print r.text
	if not(r.json() == None):
		para = r.json()
		sortedImages = make_problem(para['columns'],para['rows'])
		for i in range(len(para['answer'])):
			for j in range(len(para['answer'][0])):
				sortedImages[i][j] = (para['answer'][i][j][0],para['answer'][i][j][1])
		print sortedImages

	return {'answer' : sortedImages , 'columns' : para['columns'], 'rows' : para['rows'], 'lim_select' : para['lim_select'], 'selection_rate' : para['selection_rate'], 'exchange_rate' : para['exchange_rate']}



