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
import config
import time

RETRY_MAX = 10
RETRY_INTERVAL = 0.2

DIGEST_USER = "sp2lc"
DIGEST_PASS = "********"

PRACTICE_USER = "sp2lc"
PRACTICE_PASS = "********"

def get_problem(problem_id,to_communication):
	if to_communication == "sp2lc":
		r = requests.get('http://sp2lc.salesio-sp.ac.jp/procon25-test/procon.php',params = {'probID' : problem_id}, auth=HTTPDigestAuth(DIGEST_USER, DIGEST_PASS))
		if r.text == "error" :
			print "server error"
			exit()
		return r.content
	elif to_communication == "procon":
                for i in range(RETRY_MAX):
                  r = requests.get("http://%s/problem/prob%02d.ppm" % (config.serverIP, int(problem_id)))
                  if r.status_code == 403:
                    print "フライング i=%d" % i
                    time.sleep(RETRY_INTERVAL)
                  else:
		    return r.content
                return ""
        else:
                # practice
                r = requests.get("http://procon2014-practice.oknct-ict.org/problem/ppm/%d" % int(problem_id))
                return r.content


def post_answer(answer_string, time, version_string, problem_id,to_communication):
	if to_communication == "sp2lc":
		r = requests.post('http://sp2lc.salesio-sp.ac.jp/procon25-test/procon.php',data = {'answer_string' : answer_string , 'time' : time , 'version' : version_string, 'probID' : problem_id}, auth=HTTPDigestAuth(DIGEST_USER, DIGEST_PASS))
		if r.text == "error" :
			print "server error"
			exit()
		elif r.text == "ok" :
			print "登録完了！"
		print r.text
		return r.text
	elif to_communication == "procon":
		r = requests.post('http://%s/SubmitAnswer' % config.serverIP,data = {'playerid' : config.token, 'problemid' : problem_id, 'answer' : answer_string})
		print r
		return r.text
        else:
                r = requests.post("http://procon2014-practice.oknct-ict.org/solve/json/%d" % int(problem_id), data={"username": PRACTICE_USER, "passwd": PRACTICE_PASS, "answer_text": answer_string})
                print r.text
                return r.text
