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

def get_problem(problem_id,to_communication):
	if to_communication:
		r = requests.get('http://sp2lc.salesio-sp.ac.jp/procon.php',params = {'probID' : problem_id}, auth=HTTPDigestAuth(DIGEST_USER, DIGEST_PASS))
		if r.text == "error" :
			print "server error"
			exit()
		return r.content
	else:
		r = requests.get("http://localhost/problem/prob%02d.ppm" % int(problem_id))
		return r.content


def post_answer(answer_string, time, version_string, problem_id,to_communication):
	if to_communication:
		r = requests.post('http://sp2lc.salesio-sp.ac.jp/procon.php',data = {'answer_string' : answer_string , 'time' : time , 'version' : version_string, 'probID' : problem_id}, auth=HTTPDigestAuth(DIGEST_USER, DIGEST_PASS))
		if r.text == "error" :
			print "server error"
			exit()
		elif r.text == "ok" :
			print "登録完了！"
		print r.text
		return r.text
	else:
		r = requests.post('http://localhost/SubmitAnswer',data = {'playerid' : "1", 'problemid' : '00', 'answer' : answer_string})
		print r
		return r.text



