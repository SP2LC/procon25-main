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
import a_star

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

# 色を比較する
def compareColor(a, b):
    # 各要素の差の二乗は簡単に書ける。
    # -や*は、配列の各要素それぞれに対して実行される。
    # np.sumで合計を求める。
    return math.sqrt(np.sum((a-b)*(a-b)))

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
    #difference = 0.0
    #for i in range(len(lineA)):
    #  difference += compareColor(lineA[i], lineB[i])
    difference = np.sum(np.sqrt(np.sum((lineA-lineB)*(lineA-lineB), axis=1)))
    return difference / len(lineA)

def sortWorst(dic):
    #averages = {}
    #for k, v in dic.items():
    #  # 平均を求める
    #  avg = 0.0
    #  for candicate in v:
    #    avg += candicate[1]
    #  avg = avg / len(v)
    #  averages[k] = avg
    #return sorted(averages.items(), key=lambda a: a[1])
    minItems = {}
    for k, v in dic.items():
      minValue = min(v, key=lambda a: a[1])
      minItems[k] = minValue[1]
    return sorted(minItems.items(), key=lambda a: a[1])

def firstSame(listA, listB, key=lambda a: a):
    bSet = {key(b) for b in listB}
    for a in listA:
      if key(a) in bSet:
        for b in listB:
          if key(a) == key(b):
            return a
    return None

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

def firstSameN(lists, key=lambda a: a):
    #bSet = {key(b) for b in listB}
    sets = [set(map(key, lst)) for lst in lists]
    for a in lists[0]:
      if all([(key(a) in s) for s in sets]):
        return a
    return None

# リストの各要素どうしを足す
def arrayAdd(xs, ys):
    return map(lambda x, y: x + y, xs, ys)

# aがn個入ったリストを作る
def repeat(a, n):
    return [a for i in range(n)]

def average(xs):
    return sum(xs) / len(xs)


# TODO 2方向から攻める
# 水平に動いた方が向く画像とそうでない画像を見極めて，移動を偏らせる?
def sortImages2(resultAToBWidth, resultBToAWidth, resultAToBHeight, resultBToAHeight, startList, array):
    values = createArray(splitColumns, splitRows)
    width = len(array)
    height = len(array[0])
    # 左から，右から，上から，下から
    tables = [resultAToBWidth, resultBToAWidth, resultAToBHeight, resultBToAHeight]
    queue = deque([])
    for pos, img, value in startList:
      array[pos[0]][pos[1]] = img
      values[pos[0]][pos[1]] = value
      queue.append(pos)
    while len(queue) != 0:
      (x, y) = queue.popleft()
      thisImg = array[x][y]
      neighbours = getNeighbours(x, y, array)
      neighboursPosX = [x - 1, x + 1, x, x]
      neighboursPosY = [y, y, y - 1, y + 1]
      for i, neighbour in enumerate(neighbours):
        if neighbour != -1:# and neighbour == None:
          nextNeighbours = getNeighbours(neighboursPosX[i], neighboursPosY[i], array)
          nextNeighboursPosX = map(lambda a: a + neighboursPosX[i], [-1, 1, 0, 0])
          nextNeighboursPosY = map(lambda a: a + neighboursPosY[i], [0, 0, -1, 1])
          newImgs = []
          for j, img in enumerate(nextNeighbours):
            if img != -1 and img != None:
              newImg = tables[j][img][0]
              newImgs.append((values[nextNeighboursPosX[j]][nextNeighboursPosY[j]], newImg))
          if newImgs != []:
            print "-----"
            print newImgs
            #array[neighboursPosX[i]][neighboursPosY[i]] = min(newImgs, key=lambda a: a[1])[0]
            nextImg = min(newImgs, key=lambda a: a[1][1])
            #newValue = average(map(lambda a: a[0], newImgs)) + nextImg[1][1]
            #newValue = nextImg[0] + nextImg[1][1]
            newValue = nextImg[0] # やっつけ!結局一番角らしいやつを採用してるだけ!
            if array[neighboursPosX[i]][neighboursPosY[i]] == None or values[neighboursPosX[i]][neighboursPosY[i]] > newValue:
              if values[neighboursPosX[i]][neighboursPosY[i]] > newValue:
                print "rewrite %s to %s" % (values[neighboursPosX[i]][neighboursPosY[i]], newValue)
              array[neighboursPosX[i]][neighboursPosY[i]] = nextImg[1][0]
              values[neighboursPosX[i]][neighboursPosY[i]] = newValue
              queue.append((neighboursPosX[i], neighboursPosY[i]))
    print "values-----------"
    print(values)

# MARK: main

if len(sys.argv) < 2:
  print "引数が間違っておるぞ!"
  sys.exit(1)

# 分割数の読み込み
# 100という数字は決め打ち!すばらしい!
ppmFile = open(sys.argv[1], "rb").read(100)
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
# 上下逆で読まれるので、flipud関数で上下を反転させる
# 環境によっては必要ない？python2.7.6
if len(sys.argv) == 3 and sys.argv[2] == "-f":
  img = np.flipud(mpimg.imread(sys.argv[1]))
else:
  img = mpimg.imread(sys.argv[1])
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

# 一番下になる画像を探す
# ワーストsplitColumnsを取る
worstHeightAll = sortWorst(resultAToBHeight)
worstWidthAll = sortWorst(resultAToBWidth)
worstHeight = sortWorst(resultAToBHeight)[-splitColumns:]
worstWidth = sortWorst(resultAToBWidth)[-splitRows:]
print "worstHeight %d images" % splitColumns
for k, v in worstHeight:
  print "%s %f" % (k, v)
print "worstWidth %d images" % splitRows
for k, v in worstWidth:
  print "%s %f" % (k, v)
# 二つのワーストの両方に出てくる画像で、一番最初のものが右下っぽい
#rightBottom = firstSame(worstWidth, worstHeight, key=lambda a: a[0])
rightBottom = findRightBottom(resultAToBWidth, resultAToBHeight)
print "右下はこいつだ!"
print rightBottom[0]
# 逆引きリストを作る
worstImgNumsWidth = [imgNum for imgNum, v in worstWidth]
worstImgNumsHeight = [imgNum for imgNum, v in worstHeight]
resultBToAHeight = {}
resultBToAWidth = {}

for k, v in resultAToBWidth.items():
  for candicate in v:
    #if not k in worstImgNumsWidth:
    if True:
      if not candicate[0] in resultBToAWidth:
        resultBToAWidth[candicate[0]] = []
      resultBToAWidth[candicate[0]].append((k, candicate[1]))
      resultBToAWidth[candicate[0]].sort(key=lambda a: a[1])

for k, v in resultAToBHeight.items():
  for candicate in v:
    #if not k in worstImgNumsHeight:
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


print(worstWidth)
worstWidthDic = dict(worstWidthAll)
worstWidth = []
#column = list(range(splitRows))
nowImage = rightBottom[0][0]
#column[splitRows - 1] = (nowImage, 0)
worstWidth.append((nowImage, worstWidthDic[nowImage]))
for i in range(splitRows - 2, -1, -1):
  nowImage = resultBToAHeight[nowImage][0][0]
  #column[i] = nowImage
  worstWidth.append((nowImage, worstWidthDic[nowImage]))
print(worstWidth)
worstWidth.reverse()

#sortedImages = sortImages(resultBToAWidth, splitRows, splitColumns, worstWidth)
sortedImages = createArray(splitColumns, splitRows)
startList = [
  ((splitColumns - 1, splitRows - 1), rightBottom[0][0], rightBottom[0][1]),
  ((splitColumns - 1, 0), rightTop[0][0], rightTop[0][1]),
  ((0, splitRows - 1), leftBottom[0][0], leftBottom[0][1]),
  ((0, 0), leftTop[0][0], leftTop[0][1])]

sortImages2(resultAToBWidth, resultBToAWidth, resultAToBHeight, resultBToAHeight, startList, sortedImages)
print sortedImages

#np.hstack([np.vstack(map(lambda a: splitImages[a[1], a[0]], col)) for col in sortImages])
#newImg = np.hstack(
#  [np.vstack([splitImages[a[0]][a[1]] for a in col])
#    for col in sortedImages]
#)
newImg = np.hstack(
  [np.vstack([splitImages[a[0]][a[1]] for a in row])
#    for row in np.array(sortedImages).transpose((1, 0, 2))]
    for row in np.array(sortedImages)]
)

plt.imshow(newImg)
plt.show()#ここまで画像認識

a_star.solve(sortedImages, splitColumns, splitRows, LIMIT_SELECTION, SELECTON_RATE, EXCHANGE_RATE)
