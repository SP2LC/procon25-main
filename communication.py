# -*- coding: utf-8 -*-
import requests
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from StringIO import StringIO
import sys
import re
import math

def get_problem(problem_id):
	r = requests.get('http://sp2lc.salesio-sp.ac.jp/procon.php',params = {'probID' : problem_id})
	if r.text == "error" :
		print "server error"
		exit()
	return r.content

def post_answer(answer_string, time, version_string, problem_id):
	r = requests.post('http://sp2lc.salesio-sp.ac.jp/procon.php',data = {'answer_string' : answer_string , 'time' : time , 'version' : version_string, 'probID' : problem_id})
	if r.text == "error" :
		print "server error"
		exit()
	elif r.text == "ok" :
		print "登録完了！"
	print r.text
	return r.text



