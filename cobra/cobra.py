# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sys
import re
import math
import itertools
import binascii
from collections import deque
from PIL import Image
from StringIO import StringIO
import threading
import Queue
import time
import communication
import heapq
import gui
import json
import cgi
import SimpleHTTPServer
import SocketServer
import logging
import socket
import config


VERSION = "プロコン本番用"
TO_COMMUNICATION = "sp2lc" #sp2lcのときは自鯖の回答サーバー、proconのときはlocalhostのProconSimpleServer、practiceの時は沖縄高専の練習場と通信します。
IMAGE_WINDOW = True
NO_POST = False

LIMIT_SELECTION = 0
SELECTON_RATE = 0
EXCHANGE_RATE = 0
splitColumns = 0
splitRows = 0
answer = []
start = 0
best_cost = 99999999999999

class Procon_Cobra_Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  def __init__(self,request, client_address, server):
    SimpleHTTPServer.SimpleHTTPRequestHandler.__init__(self,request, client_address, server)
    self.answer = []
    self.columns = 0
    self.rows = 0
    self.lim_select = 0
    self.selection_rate = 0
    self.exchange_rate = 0

  def do_POST(self):
    global best_cost
    form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':self.headers['Content-Type'],})
    runtime = int(time.time() - start)
    ans_str = form['answer'].value
    cost = calculation_cost_from_string(ans_str)
    true_cost = cost  + (runtime * 100)
    print 'cost is '+ str(cost)
    print 'time_cost is ' + str((runtime * 100))
    print 'all cost is '+ str(true_cost)
    print 'ans is \n'+ans_str
    print best_cost
    if true_cost < best_cost:
      best_cost = true_cost
      body = "send this answer!"
      if not(NO_POST):
        print (communication.post_answer(form['answer'].value, runtime, VERSION, sys.argv[1],TO_COMMUNICATION))
      self.send_response(200)
      self.wfile.write(body)
    else:
      body = "not send this answer..."
      self.send_response(200)
      self.send_header('Content-type', 'text/html; charset=utf-8')
      self.send_header('Content-length', len(body))
      self.end_headers()
      self.wfile.write(body)

  def do_GET(self):
    data = {'answer' : answer, 'columns': splitColumns , 'rows' : splitRows , 'lim_select' : LIMIT_SELECTION , 'selection_rate' : SELECTON_RATE, 'exchange_rate' : EXCHANGE_RATE}
    body = json.dumps(data)
    self.send_response(200)
    self.send_header('Content-type', 'text/html; charset=utf-8')
    self.send_header('Content-length', len(body))
    self.end_headers()
    self.wfile.write(body)

def calculation_cost_from_string(answer_string):
  cost = 0
  split_string = answer_string.split("\r\n")
  cost += int(split_string[0]) * SELECTON_RATE
  split_string.pop(0)
  for line in range(0,len(split_string),3):
    cost += int(split_string[line+1]) * EXCHANGE_RATE
  return cost

def split(img, columns, rows):
    images = []
    # shapeで画像サイズを取れるが、[高さ, 幅, 3]の順番になっているので注意
    fullWidth = img.shape[1]
    fullHeight = img.shape[0]
    splitWidth = fullWidth / columns
    splitHeight = fullHeight / rows
    for i in range(columns):
      column = []
      for j in range(rows):
        left = splitWidth * i
        right = left + splitWidth
        top = splitHeight * j
        bottom = top + splitHeight
        # 画像を切り出す
        # これは画像をコピーしないため高速
        # ただし、切り出した画像に書き込むと元画像にも書き込まれるので注意
        # [y, x] の順番なので注意
        splitImage = img[top:bottom, left:right]
        column.append(splitImage)
      images.append(column)
    return images

# 画像の辺を比較する
# flag=Trueの場合、aの右にbを置く
# flag=Falseの場合、aの下にbを置く
def compare(imgA, imgB, flag):
    width = imgA.shape[1]
    height = imgA.shape[0]
    if flag:
      # 横に比較する場合
      lineA = imgA[0:height, width - 1]
      lineB = imgB[0:height, 0]
    else:
      # 縦に比較する場合
      lineA = imgA[height - 1, 0:width]
      lineB = imgB[0, 0:width]
    # 配列の各ピクセルに対して、差の二乗を3色分足し合わせてルートを計算し、配列全体の合計を計算する。
    difference = np.sum(np.sqrt(np.sum((lineA-lineB)*(lineA-lineB), axis=1)))
    return difference / len(lineA)

def findRightBottom(resultW, resultH):
    lst = []
    for k, v in resultW.items():
      minValueW = min(v, key=lambda a: a[1])[1]
      minValueH = min(resultH[k], key=lambda a: a[1])[1]
      lst.append((k, minValueW * minValueH))
    lst.sort(key=lambda a: a[1])
    lst.reverse()
    return lst


def createArray(width, height):
    array = []
    for x in range(width):
      column = []
      for y in range(height):
        column.append(None)
      array.append(column)
    return array

# [left, right, top, bottom]
# -1は範囲外
# Noneは未設定
def getNeighbours(x, y, array):
    width = len(array)
    height = len(array[0])
    result = [-1, -1, -1, -1]
    if x - 1 >= 0:
      result[0] = array[x - 1][y]
    if x + 1 < width:
      result[1] = array[x + 1][y]
    if y - 1 >= 0:
      result[2] = array[x][y - 1]
    if y + 1 < height:
      result[3] = array[x][y + 1]
    return result

def average(xs):
    return sum(xs) / len(xs)

def addpos(a, b):
  return (a[0] + b[0], a[1] + b[1])

def showArray(sortedImages, splitImages):
  newImg = np.hstack(
    [np.vstack([splitImages[a[0]][a[1]] for a in row])
      for row in np.array(sortedImages)]
  )
  if IMAGE_WINDOW:
    plt.imshow(newImg)
    plt.show()

# 画像を並び替える
def sortImages2(resultAToBWidth, resultBToAWidth, resultAToBHeight, resultBToAHeight, array, correctImages={}):
  tables = [(resultAToBWidth, (1, 0)), (resultBToAWidth, (-1, 0)), (resultAToBHeight, (0, 1)), (resultBToAHeight, (0, -1))]
  queue = []
  imgs = {}
  if len(correctImages) == 0:
    # (類似度, 注目している画像, 現在座標)
    #heapq.heappush(queue, (0.0, (0, 0), (0, 0)))
    # 上下左右のテーブルでの1位と2位の差の合計が大きい順に並び替える
    def sort_key(img):
      return sum([tab[img][0][1] - tab[img][1][1] for tab, direction in tables])
    all_imgs = [(x, y) for x in range(len(array)) for y in range(len(array[0]))]
    start_img = min(all_imgs, key=sort_key)
    print "start_img=%s key=%f" % (start_img, sort_key(start_img))
    heapq.heappush(queue, (0.0, start_img, (0, 0)))
    used = set((0, 0))  # 使用した画像
  else:
    used = set()
    #imgs[(0, 0)] = (0, 0)
    #for pos, img, value in startList:
    a = 0
    for pos, img in correctImages.items():
      imgs[pos] = img
      used.add(img)
      for table, direction in tables:
        #for new_img in table[img]:
        new_img = table[img][0]
        new_img1 = table[img][1]
        if True:
          heapq.heappush(queue, (-(new_img1[1] - new_img[1]), new_img[0], addpos(pos, direction)))
      a += 1
  while len(queue) != 0:
    # 一番類似しているものから取り出す
    value, img, pos = heapq.heappop(queue)
    # すでに使った画像は使わない
    if img in used:
      #print "uszew"
      continue
    print img
    # 終了条件
    if len(imgs) == len(array) * len(array[0]):
      print "finish!"
      break
    # usedに追加
    used.add(img)
    print (value, img, pos)
    imgs[pos] = img
    # 隣をqueueに入れる
    for table, direction in tables:
      #for new_img in table[img]:
      new_img = table[img][0]
      new_img1 = table[img][1]
      if True:
        # new_img[1] - new_img1[1] == -(new_img[1] - new_img[1])
        # 類似していないほど値が大きくなるので、1位-2位は必ず負の値になる。
        # heapqは小さい値から取り出されるので、1位と2位が離れている(差が絶対値の大きい負数)のものから先にたどる。
        heapq.heappush(queue, (-(new_img1[1] - new_img[1]), new_img[0], addpos(pos, direction)))
  # 座標をシフトする
  print imgs
  if len(correctImages) == 0:
    minX = min(imgs.keys(), key=lambda a: a[0])[0]
    minY = min(imgs.keys(), key=lambda a: a[1])[1]
  else:
    minX = 0
    minY = 0
  print "minX=%d, minY=%d" % (minX, minY)
  #out = [] # はみ出し画像
  all_imgs = set([(x, y) for x in range(len(array)) for y in range(len(array[0]))])
  used_imgs = set()
  for k, v in imgs.items():
    x = k[0] - minX
    y = k[1] - minY
    if x >= len(array) or y >= len(array[0]):
      # はみ出し
      #out.append(v)
      print "out"
      print "%s %s" % ((x, y), v)
    else:
      if not (x, y) in correctImages:
        array[x][y] = v
        used_imgs.add(v)
  print array
  # はみ出している画像は適当に欠けているところに入れる
  out = all_imgs - used_imgs
  print out
  for i in range(len(array)):
    for j in range(len(array[0])):
      if array[i][j] == None:
        array[i][j] = out.pop()
  return array

# MARK: main

if len(sys.argv) < 2:
  print "引数が間違っておるぞ!"
  sys.exit(1)
time_start = time.clock()
# 分割数の読み込み
# 100という数字は決め打ち!すばらしい!

# 引数パース
options = set()
for arg in sys.argv[2:]:
  options.add(arg)

if "-p" in options:
  TO_COMMUNICATION = "procon"
  print "communication with Proocn Simple Server at localhost"
elif "-r" in options:
  TO_COMMUNICATION = "practice"
  print "communication with procon2014-practice.oknct-ict.org"
else:
  TO_COMMUNICATION = "sp2lc"
  print "communication with sp2lc.salesio-sp.ac.jp/procon.php"
if "-n" in options:
  IMAGE_WINDOW = False
  print "no window"
if "-d" in options:
  NO_POST = True
  print "no post"

def do_Image_recognition():
  global LIMIT_SELECTION, SELECTON_RATE, EXCHANGE_RATE, splitColumns, splitRows
  ppmFile_content = communication.get_problem(sys.argv[1],TO_COMMUNICATION)
  ppmFile = ppmFile_content[:100]
  splitStrings = re.split("[\t\r\n ]+", ppmFile)
  splitColumns = int(splitStrings[2]) # 横の分割数
  splitRows = int(splitStrings[3]) # 縦の分割数
  LIMIT_SELECTION = int(splitStrings[5]) #選択上限、適宜変更
  SELECTON_RATE = int(splitStrings[7]) #選択コストレート、適宜変更
  EXCHANGE_RATE = int(splitStrings[8]) #交換コストレート、適宜変更
  print LIMIT_SELECTION
  print SELECTON_RATE
  print EXCHANGE_RATE

  # 画像の読み込み
  img = np.asarray(Image.open(StringIO(ppmFile_content)))

  # 画像を分割する
  splitImages = split(img, splitColumns, splitRows)

  resultAToBHeight = {}
  resultAToBWidth = {}
  # こうすることで、4重ループを簡単に書ける。
  for imgANum in itertools.product(range(splitColumns), range(splitRows)):
    print "imgA=(%d, %d)" % imgANum
    resultsHeight = []
    resultsWidth = []
    for imgBNum in itertools.product(range(splitColumns), range(splitRows)):
      if imgANum == imgBNum:
        continue
      imgA = splitImages[imgANum[0]][imgANum[1]]
      imgB = splitImages[imgBNum[0]][imgBNum[1]]
      differenceHeight = compare(imgA, imgB, False)
      differenceWidth = compare(imgA, imgB, True)

      resultsHeight.append((imgBNum, differenceHeight))
      resultsWidth.append((imgBNum,differenceWidth))
    resultAToBHeight[imgANum] = sorted(resultsHeight, key=lambda a: a[1])
    resultAToBWidth[imgANum] = sorted(resultsWidth,key = lambda a: a[1])

    print "H  imgB=%s" % ["%s %f" % a for a in resultAToBHeight[imgANum][0:3]]
    print "W  imgB=%s" % ["%s %f" % a for a in resultAToBWidth[imgANum][0:3]]

  rightBottom = findRightBottom(resultAToBWidth, resultAToBHeight)
  print "右下はこいつだ!"
  print rightBottom[0]
  # 逆引きリストを作る
  resultBToAHeight = {}
  resultBToAWidth = {}

  for k, v in resultAToBWidth.items():
    for candicate in v:
      if True:
        if not candicate[0] in resultBToAWidth:
          resultBToAWidth[candicate[0]] = []
        resultBToAWidth[candicate[0]].append((k, candicate[1]))
        resultBToAWidth[candicate[0]].sort(key=lambda a: a[1])

  for k, v in resultAToBHeight.items():
    for candicate in v:
      if True:
        if not candicate[0] in resultBToAHeight:
          resultBToAHeight[candicate[0]] = []
        resultBToAHeight[candicate[0]].append((k, candicate[1]))
        resultBToAHeight[candicate[0]].sort(key=lambda a: a[1])

  leftBottom = findRightBottom(resultBToAWidth, resultAToBHeight)
  print "左下はこいつだ!"
  print leftBottom[0]
  leftTop = findRightBottom(resultBToAWidth, resultBToAHeight)
  print "左上はこいつだ!"
  print leftTop[0]
  rightTop = findRightBottom(resultAToBWidth, resultBToAHeight)
  print "右上はこいつだ!"
  print rightTop[0]

  sortedImages = createArray(splitColumns, splitRows)
  sortImages2(resultAToBWidth, resultBToAWidth, resultAToBHeight, resultBToAHeight, sortedImages)
  print sortedImages

  def retry(array, correctImages):
    sortImages2(resultAToBWidth, resultBToAWidth, resultAToBHeight, resultBToAHeight, array, correctImages=correctImages)

  gui.show(sortedImages, splitImages, retry=retry)
  #ここまで画像認識
  return sortedImages

start = time.time()

answer = do_Image_recognition()

host = socket.gethostbyname(socket.gethostname())
print "location is %s" % host
port = config.port
httpd = SocketServer.TCPServer((host, port), Procon_Cobra_Handler)

print('serving at port', port)
httpd.serve_forever()

runtime = str(int(time_end - time_start))
print "runtime = " + runtime
