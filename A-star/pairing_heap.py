# -*- coding: utf-8 -*-
class Heap:
  def __init__(self, element, children, key=lambda x: x):
    self.element = element
    self.children = children
    self.key = key
    self.is_empty = False

  def find_min(self):
    if self.is_empty:
      return None
    else:
      return self.element

  # otherにEmptyを入れるのはダメゼッタイ
  def copy_to_self(self, other):
    self.is_empty = other.is_empty
    self.element = other.element
    self.children = other.children
    self.key = other.key

  def merge(self, other):
    if self.is_empty:
      self.copy_to_self(other)
    elif other.is_empty:
      pass # なにもしない
    elif self.key(self.element) < self.key(other.element):
      self.children = (other, self.children)
    else:
      new_heap = Heap(self.element, self.children, key=self.key)
      self.element = other.element
      self.children = (new_heap, other.children)

  def push(self, element):
    self.merge(Heap(element, (), key=self.key))

  def pop(self):
    if self.is_empty:
      return None
    elif self.children == ():
      self.is_empty = True
      return self.element
    else:
      minElement = self.element
      children = self.children[1]
      self.copy_to_self(self.children[0])
      while children != ():
        self.merge(children[0])
        children = children[1]
      return minElement

  def show(self, level=0):
    children = self.children
    print "  " * level + str(self.element)
    while children != ():
      children[0].show(level + 1)
      children = children[1]


class Empty(Heap):
  def __init__(self, key=lambda x: x):
    self.key = key
    self.is_empty = True
  def show(self, level=0):
    print "  " * level + "Empty"

if __name__ == "__main__":
  import random
  import heapq
  length = 1000
  array = range(length)
  random.shuffle(array)
  print "creating pairing heap"
  h = Heap(array[0], ())
  for a in array[1:]:
    h.push(a)
  print "get from pairing heap"
  while not h.is_empty:
    x = h.pop()
  print "creating heapq"
  q = []
  heapq.heapify(q)
  for a in array:
    heapq.heappush(q, a)
  print "get from heapq"
  while q != []:
    x = heapq.heappop(q)
  print "end"
