# -*- coding: utf-8 -*-
import Tkinter as Tk
import Image, ImageTk
import numpy as np
import copy

MAX_IMG_SIZE = 640

NORMAL = 0
SELECTING = 1
SELECTED = 2

# 与えられたimagesを破壊的に変更するらしい

class ImageViewer(Tk.Frame):
  def __init__(self, images, splitImages, retry):
    Tk.Frame.__init__(self, None)
    self.images = images
    self.original_images = copy.deepcopy(images)
    self.splitImages = splitImages
    self.retry_func = retry

    self.state = NORMAL
    self.selected = None
    self.selected_wh = (1, 1)

    self.image_ids = []
    self.tk_images = []
    self.wrong = []
    for j in range(len(images)):
      column = []
      tk_column = []
      wrong_column = []
      for i in range(len(images[0])):
        column.append(None)
        tk_column.append(None)
        wrong_column.append(False)
      self.image_ids.append(column)
      self.tk_images.append(tk_column)
      self.wrong.append(wrong_column)

    self.img_width = splitImages[0][0].shape[1]
    self.img_height = splitImages[0][0].shape[0]
    self.width = len(splitImages) * self.img_width
    self.height = len(splitImages[0]) * self.img_height
    self.master.title("Image")

    self.canvas = Tk.Canvas(self, width=self.width, height=self.height)
    self.canvas.pack()
    self.mouseover_img = None
    self.canvas.bind("<Motion>", self.motion)
    self.canvas.bind("<ButtonRelease-1>", self.release)

    self.ok_button = Tk.Button(self, text="OK", command=self.ok)
    self.ok_button.pack()

    self.reset_button = Tk.Button(self, text="Reset", command=self.reset)
    self.reset_button.pack()

    self.shift_frame = Tk.Frame(self)
    self.shift_frame.pack()

    self.left_button = Tk.Button(self.shift_frame, text="LEFT", command=self.shift_left)
    self.left_button.grid(column=0, row=1)

    self.up_button = Tk.Button(self.shift_frame, text="UP", command=self.shift_up)
    self.up_button.grid(column=1, row=0)

    self.right_button = Tk.Button(self.shift_frame, text="RIGHT", command=self.shift_right)
    self.right_button.grid(column=2, row=1)

    self.down_button = Tk.Button(self.shift_frame, text="DOWN", command=self.shift_down)
    self.down_button.grid(column=1, row=2)

    self.retry_button = Tk.Button(self, text="Retry", command=self.retry)
    self.retry_button.pack()
    
    self.pack()

    self.show_image()

  def ok(self):
    print "ok!"
    self.quit() # 閉じてない気がする

  def reset(self):
    print "reset!"
    for i in range(len(self.images)):
      for j in range(len(self.images[0])):
        self.images[i][j] = self.original_images[i][j]
    self.show_image()

  def retry(self):
    print "retry"
    correct_images = {}
    for i in range(len(self.images)):
      for j in range(len(self.images[1])):
        if not self.wrong[i][j]:
          correct_images[(i, j)] = self.images[i][j]
    print "corect img"
    print correct_images
    print len(correct_images)
    self.retry_func(self.images, correct_images)
    for i in range(len(self.images)):
      for j in range(len(self.images[1])):
        self.wrong[i][j] = False
    self.show_image()

  def show_image(self):
    for i in range(len(self.images)):
      for j in range(len(self.images[0])):
        # PhotoImageオブジェクトが使われる関数を抜けると画像が消える?
        # なのでインスタンス変数に保存する
        new_i, new_j = self.images[i][j]
        #new_i, new_j = (i, j)
        self.tk_images[i][j] = ImageTk.PhotoImage(Image.fromarray(self.splitImages[new_i][new_j]))
        x = i * self.img_width
        y = j * self.img_height
        # anchor="nw"を指定しないと画像がずれる。位置を北西(左上)に合わせるという意味。
        self.image_ids[i][j] = self.canvas.create_image(x, y, image=self.tk_images[i][j], anchor="nw")
        self.canvas.tag_bind(self.image_ids[i][j], "<ButtonPress-1>", self.onclick(i, j))
        self.canvas.tag_bind(self.image_ids[i][j], "<ButtonPress-2>", self.set_wrong(i, j))
        # wrong imageにマークを付ける
        #self.canvas.delete("wrong")
        if self.wrong[i][j]:
          self.canvas.create_line(x, y, x + self.img_width, y + self.img_height, width=5, fill="red", tags="wrong")

  def set_wrong(self, i, j):
    # 間違っている画像を指定する
    # todo 枠を付ける
    def func(event):
      if self.wrong[i][j]:
        self.wrong[i][j] = False
        print "correct (%d, %d)" % (i, j)
      else:
        self.wrong[i][j] = True
        print "wrong (%d, %d)" % (i, j)
      pass
      self.show_image()
    return func

  def motion(self, event):
    i = event.x / self.img_width
    j = event.y / self.img_height
    if not self.mouseover_img != (i, j):
      return
    self.mouseover_img = (i, j)
    if self.state == SELECTING:
      self.canvas.delete("selection")
      if i >= self.selected[0]:
        x1 = self.selected[0] * self.img_width
        x2 = (i + 1) * self.img_width
      else:
        x1 = (self.selected[0] + 1) * self.img_width
        x2 = i * self.img_width
      if j >= self.selected[1]:
        y1 = self.selected[1] * self.img_height
        y2 = (j + 1) * self.img_height
      else:
        y1 = (self.selected[1] + 1) * self.img_height
        y2 = j * self.img_height
      cx = self.canvas.canvasx
      cy = self.canvas.canvasy
      self.canvas.create_rectangle(x1, y1, x2, y2, width=2.0, outline="red", tags="selection")
    else:
      # 選択範囲が画像サイズをオーバーした時の処理
      if i + self.selected_wh[0] >= len(self.images):
        print "over x"
        i = len(self.images) - self.selected_wh[0]
      if j + self.selected_wh[1] >= len(self.images[0]):
        print "over y"
        j = len(self.images[0]) - self.selected_wh[1]
      self.canvas.delete("mouseover")
      x1 = i * self.img_width
      y1 = j * self.img_height
      x2 = x1 + self.selected_wh[0] * self.img_width
      y2 = y1 + self.selected_wh[1] * self.img_height
      cx = self.canvas.canvasx
      cy = self.canvas.canvasy
      self.canvas.create_rectangle(x1, y1, x2, y2, width=2.0, outline="blue", tags="mouseover")

  def onclick(self, i, j):
    def func(event):
      i_new, j_new = i, j
      if self.state == NORMAL:
        print "%d %d" % (i_new, j_new)
        self.selected = (i_new, j_new)
        self.state = SELECTING
      elif self.state == SELECTED:
        # 選択範囲が画像サイズをオーバーした時の処理
        if i_new + self.selected_wh[0] >= len(self.images):
          print "over x"
          i_new = len(self.images) - self.selected_wh[0]
        if j_new + self.selected_wh[1] >= len(self.images[0]):
          print "over y"
          j_new = len(self.images[0]) - self.selected_wh[1]
        for k in range(self.selected_wh[0]):
          for l in range(self.selected_wh[1]):
            orig = (self.selected[0] + k, self.selected[1] + l)
            dest = (i_new + k, j_new + l)
            print "exchange %s to %s" % (orig, dest)
            self.state = NORMAL
            self.canvas.delete("selection")
            self.exchange(orig, dest)
        self.selected_wh = (1, 1)
    return func

  def release(self, event):
    i = event.x / self.img_width
    j = event.y / self.img_height
    if self.state == SELECTING:
      # 右上がselectedになるようにする
      if i < self.selected[0]:
        # 左にドラッグしていたら
        tmp = self.selected[0]
        self.selected = (i, self.selected[1])
        i = tmp
      if j < self.selected[1]:
        # 上にドラッグしていたら
        tmp = self.selected[1]
        self.selected = (self.selected[0], j)
        j = tmp
      self.selected_wh = (i - self.selected[0] + 1, j - self.selected[1] + 1)
      print "release %s %s" % (self.selected, self.selected_wh)
      self.canvas.delete("selection")
      x1 = self.selected[0] * self.img_width
      x2 = x1 + self.selected_wh[0] * self.img_width
      y1 = self.selected[1] * self.img_height
      y2 = y1 + self.selected_wh[1] * self.img_height
      self.canvas.create_rectangle(x1, y1, x2, y2, width=2.0, outline="red", tags="selection")
      self.state = SELECTED

  def exchange(self, a, b):
    tmp = self.images[a[0]][a[1]]
    self.images[a[0]][a[1]] = self.images[b[0]][b[1]]
    self.images[b[0]][b[1]] = tmp
    self.show_image()

  def shift_left(self):
    print "shift left!"
    # 最初の列を保存
    first_column = []
    for j in range(len(self.images[0])):
      first_column.append(self.images[0][j])
    # 2列目以降をシフト
    for i in range(1, len(self.images)):
      for j in range(len(self.images[0])):
        self.images[i - 1][j] = self.images[i][j]
    # 最後の列をセット
    for j in range(len(self.images[0])):
      self.images[len(self.images) - 1][j] = first_column[j]
    self.show_image()

  def shift_right(self):
    print "shift right!"
    # 最後の列を保存
    last_column = []
    width = len(self.images)
    for j in range(len(self.images[width - 1])):
      last_column.append(self.images[width - 1][j])
    #  最初以外の列をシフト
    for i in range(len(self.images) - 2, -1, -1):
      for j in range(len(self.images[0])):
        self.images[i + 1][j] = self.images[i][j]
    # 最初の列をセット
    for j in range(len(self.images[0])):
      self.images[0][j] = last_column[j]
    self.show_image()

  def shift_up(self):
    print "shift up!"
    # 最初の行を保存
    first_row = []
    for i in range(len(self.images)):
      first_row.append(self.images[i][0])
    # 2行目以降をシフト
    for i in range(len(self.images)):
      for j in range(1, len(self.images[0])):
        self.images[i][j - 1] = self.images[i][j]
    # 最後の行をセット
    for i in range(len(self.images)):
      self.images[i][len(self.images[0]) - 1] = first_row[i]
    self.show_image()

  def shift_down(self):
    print "shift down!"
    # 最後の行を保存
    last_row = []
    height = len(self.images[0])
    for i in range(len(self.images)):
      last_row.append(self.images[i][height - 1])
    # 最後以外の行をシフト
    for i in range(len(self.images)):
      for j in range(len(self.images[0]) - 2, -1, -1):
        self.images[i][j + 1] = self.images[i][j]
    # 最初の行をセット
    for i in range(len(self.images)):
      self.images[i][0] = last_row[i]
    self.show_image()

def show(images, splitImages, retry=lambda a, b: 0):
  single_w = splitImages[0][0].shape[1]
  single_h = splitImages[0][0].shape[0]
  width = single_w * len(splitImages)
  height = single_h * len(splitImages[0])
  if width > MAX_IMG_SIZE:
    ratio = float(MAX_IMG_SIZE) / width
    splitImages = shrink(splitImages, ratio)
  if height > MAX_IMG_SIZE:
    ratio = float(MAX_IMG_SIZE) / height 
    splitImages = shrink(splitImages, ratio)
  iv = ImageViewer(images, splitImages, retry)
  iv.mainloop()
  return iv.images

def shrink(images_big, ratio):
  print ratio
  images = copy.deepcopy(images_big)
  for i in range(len(images)):
    for j in range(len(images[0])):
      pilimg = Image.fromarray(images[i][j])
      pilimg = pilimg.resize((int(pilimg.size[0] * ratio), int(pilimg.size[1] * ratio)))
      images[i][j] = np.asarray(pilimg)
  return images
