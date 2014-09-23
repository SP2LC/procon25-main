# -*- coding: utf-8 -*-
import requests
from requests.auth import HTTPDigestAuth
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
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

def get_problem():
	r = requests.get("http://localhost:8000")
	print r.text
	if not(r.json() == None):
		para = r.json()
		sortedImages = make_problem(para['columns'],para['rows'])
		for i in range(len(para['answer'][0])):
			for j in range(len(para['answer'][1])):
				sortedImages[i][j] = (para['answer'][i][j][0],para['answer'][i][j][1])

	return {'answer' : sortedImages , 'columns' : para['columns'], 'rows' : para['rows'], 'lim_select' : para['lim_select'], 'selection_rate' : para['selection_rate'], 'exchange_rate' : para['exchange_rate']}

def post_answer(answer_string, time, version_string, problem_id,to_communication):
	if to_communication == "sp2lc":
		r = requests.post('http://sp2lc.salesio-sp.ac.jp/procon.php',data = {'answer_string' : answer_string , 'time' : time , 'version' : version_string, 'probID' : problem_id}, auth=HTTPDigestAuth(DIGEST_USER, DIGEST_PASS))
		if r.text == "error" :
			print "server error"
			exit()
		elif r.text == "ok" :
			print "登録完了！"
		print r.text
		return r.text
	elif to_communication == "procon":
		r = requests.post('http://192.168.11.220/SubmitAnswer',data = {'playerid' : "1", 'problemid' : problem_id, 'answer' : answer_string})
		print r
		return r.text
        else:
                r = requests.post("http://procon2014-practice.oknct-ict.org/solve/json/%d" % int(problem_id), data={"username": PRACTICE_USER, "passwd": PRACTICE_PASS, "answer_text": answer_string})
                print r.text
                return r.text



