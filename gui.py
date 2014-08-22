# -*- coding: utf-8 -*-
import Tkinter as Tk
import Image, ImageTk
import numpy as np
import copy

NORMAL = 0
SELECTED = 1

# 与えられたimagesを破壊的に変更するらしい

class ImageViewer(Tk.Frame):
  def __init__(self, images, splitImages):
    Tk.Frame.__init__(self, None)
    self.images = images
    self.original_images = copy.deepcopy(images)
    self.splitImages = splitImages

    self.state = NORMAL
    self.selected = None

    self.image_ids = []
    self.tk_images = []
    for j in range(len(images)):
      column = []
      tk_column = []
      for i in range(len(images[0])):
        column.append(None)
        tk_column.append(None)
      self.image_ids.append(column)
      self.tk_images.append(tk_column)

    self.img_width = splitImages[0][0].shape[1]
    self.img_height = splitImages[0][0].shape[0]
    self.width = len(splitImages) * self.img_width
    self.height = len(splitImages[0]) * self.img_height
    self.master.title("Image")

    self.canvas = Tk.Canvas(self, width=self.width, height=self.height)
    self.canvas.pack()
    self.mouseover_img = None
    self.canvas.bind("<Motion>", self.motion)

    self.ok_button = Tk.Button(self, text="OK", command=self.ok)
    self.ok_button.pack()

    self.reset_button = Tk.Button(self, text="Reset", command=self.reset)
    self.reset_button.pack()

    self.left_button = Tk.Button(self, text="Shift Left", command=self.shift_left)
    self.left_button.pack()
    
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
        self.canvas.tag_bind(self.image_ids[i][j], "<1>", self.onclick(i, j))

  def motion(self, event):
    i = event.x / self.img_width
    j = event.y / self.img_height
    if not self.mouseover_img != (i, j):
      return
    self.mouseover_img = (i, j)
    self.canvas.delete("mouseover")
    x1 = i * self.img_width
    y1 = j * self.img_height
    x2 = x1 + self.img_width
    y2 = y1 + self.img_height
    cx = self.canvas.canvasx
    cy = self.canvas.canvasy
    self.canvas.create_rectangle(x1, y1, x2, y2, width=2.0, outline="blue", tags="mouseover")

  def onclick(self, i, j):
    def func(event):
      if self.state == NORMAL:
        print "%d %d" % (i, j)
        x1 = i * self.img_width
        y1 = j * self.img_height
        x2 = x1 + self.img_width
        y2 = y1 + self.img_height
        cx = self.canvas.canvasx
        cy = self.canvas.canvasy
        self.canvas.create_rectangle(x1, y1, x2, y2, width=2.0, outline="red", tags="selection")
        self.selected = (i, j)
        self.state = SELECTED
      elif self.state == SELECTED:
        print "exchange %s to %s" % (self.selected, (i, j))
        self.state = NORMAL
        self.canvas.delete("selection")
        self.exchange(self.selected, (i, j))
    return func

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
      self.images[len(self.images[0]) - 1][j] = first_column[j]
    self.show_image()

def show(images, splitImages):
  iv = ImageViewer(images, splitImages)
  iv.mainloop()
  return iv.images
