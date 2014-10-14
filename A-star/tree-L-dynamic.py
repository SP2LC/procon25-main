# -*- coding: utf-8 -*-
import pairing_heap as pheap
from copy import deepcopy,copy
import threading
import Queue
import requests
from requests.auth import HTTPDigestAuth
import json
import sys
import communication
import config
import time
import tree_L_sprit

# グローバル変数の宣言
LIMIT_SELECTION = 0
SELECTON_RATE = 0
EXCHANGE_RATE = 0
MODE_CHANGE_THRESHOLD = 0.50
ALL_COST = 0

columns = 0
rows = 0

mode_flag = "N"
fwd_ahead = []
back_ahead = []

thresh = MODE_CHANGE_THRESHOLD

class Node :
    def __init__ (self, board, selection,exchange,distance):
        self.board = board
        self.selection = selection
        self.exchange = exchange
        self.mydistance = distance

    def get_next_nodes(self): #渡したノードに隣接するノードを返す

        nodes_dic = {}
        board = self.board

        for i in range(len(board)): #選択するマスを変えたノードをキューに追加する。
            for j in range(len(board[0])):
            
                x,y = (i,j)
                #右と交換
                nodes_dic[((i,j),"R")] = Node(exchange(board,(x, y), (x + 1, y)) , (x + 1, y),(x,y),0)
                #左と交換
                if x == 0:
                  # 左への移動は存在しない
                  nodes_dic[((i,j),"L")] = Node(None, (x - 1, y), (x,y),0)
                else:
                  # 一つ左の選択のRを流用する
                  #nodes_dic[((i,j),"L")] = Node(exchange(board,(x, y), (x - 1, y)) , (x - 1, y))
                  nodes_dic[((i,j),"L")] = Node(nodes_dic[((i - 1, j), "R")].board, (x - 1, y), (x, y),0)
                #上と交換
                if y == 0:
                  # 上への移動は存在しない
                  nodes_dic[((i,j),"U")] = Node(None, (x, y - 1), (x,y), 0)
                else:
                  # 一つ上の選択のDを流用する
                  #nodes_dic[((i,j),"U")] = Node(exchange(board,(x, y), (x, y - 1)) , (x, y - 1))
                  nodes_dic[((i,j),"U")] = Node(nodes_dic[((i, j - 1), "D")].board, (x, y - 1), (x,y), 0)
                #下と交換
                nodes_dic[((i,j),"D")] = Node(exchange(board,(x, y), (x, y + 1)) , (x, y + 1),(x,y),0)

        return nodes_dic


def make_problem(w, h):
    arr = []
    for i in range(w):
        column = []
        for j in range(h):
            column.append((i, j))
        arr.append(column)
    return arr

def transpose(arr2d): #転置した2次元配列を返す
    result = []
    for i in range(len(arr2d[0])):
        arr = []
        for j in range(len(arr2d)):
            arr.append(arr2d[j][i])
        result.append(arr)
    return result

def operations_to_list(operations): #operationsの型を普通のリストに戻した物を返す
    pair = operations
    lst = []
    while pair != ():
        lst.append(pair[0])
        pair = pair[1]
    return lst

def exchange (then_board, start, destination): # then_boadのstartとdestinationを交換したboardを返す
    # 変更されたcolumnだけをdeep copyする
    x, y = start
    new_x, new_y = destination

    if not(0 <= new_x < len(then_board) and 0 <= new_y < len(then_board[0])):
        return None

    startImg = then_board[x][y]
    destImg = then_board[new_x][new_y]

    return [
      then_board[x] if x != start[0] and x != destination[0]
      else [destImg if (x, y) == start
        else (startImg if (x, y) == destination else then_board[x][y])
        for y in range(len(then_board[0]))]
      for x in range(len(then_board))]

    board = copy(then_board)
    board[x] = deepcopy(then_board[x])

    if x != new_x:
      board[new_x] = deepcopy(then_board[new_x])

    destination_element = board[new_x][new_y]
    board[new_x][new_y] = board[x][y]
    board[x][y] = destination_element

    return board

def create_distance_table(goal): #距離計算用のテーブルを返す
    table = []
    for i in range(len(goal)):
      col = []
      for j in range(len(goal[0])):
        col.append(None)
      table.append(col)
    for i in range(len(goal)):
        for j in range(len(goal[0])):
            (goal_x, goal_y) = goal[i][j]
            table[goal_x][goal_y] = (i, j)
    return table  

def distance_to_goal(table, board): #ノードとゴールノードまでの予測距離を返す。引数は(距離計算用テーブル,ゴールのボード)
    ans = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            (board_x, board_y) = board[i][j]
            a = table[board_x][board_y]
            b = (i, j)
            x = abs(a[0] - b[0])
            y = abs(a[1] - b[1])
            ans += x + y
    return ans * EXCHANGE_RATE

def point_md(point,board, table):
    table_x, table_y = board[point[0]][point[1]]
    a = table[table_x][table_y]
    x = abs(a[0] - point[0])
    y = abs(a[1] - point[1])
    ans = x + y
    return ans
def fast_distance_to_goal(looking_node,node, table):

    parent_distance = looking_node.mydistance
    parent_board = looking_node.board
    
    selection = node.selection
    exchange = node.exchange
    child_board = node.board

    exchange_distance  = point_md(selection,parent_board, table) - point_md(exchange ,child_board, table)
    selection_distance = point_md(exchange ,parent_board, table) - point_md(selection,child_board, table)

    child_distance = parent_distance - (exchange_distance + selection_distance)

    node.mydistance = child_distance

    return child_distance * EXCHANGE_RATE

def tuplenode (node) : #ノードをtupleの形にした物を返す
    return (tuple([tuple(a) for a in node.board]) , node.selection)

def caliculate_cost (operations): #現在のoperationsのコストを返す
    pair = operations
    cost = 0
    lst = []
    while pair != ():
        if pair[0][0] == "S":
            cost += SELECTON_RATE
        else:
            cost += EXCHANGE_RATE 
        pair = pair[1]
    return cost

def count_missmatch_image(board1, board2):#board1とboard2間の不一致画像の数を返す
    counts = 0
    for i in range(len(board1)):
      for j in range(len(board1[0])):
        try:
          if board1[i][j] != board2[i][j]:
            counts += 1
        except:
          print "----"
          print board1
          print board2
          sys.exit()
    return counts



def count_selection(operations): #選択を数える
    count = 0
    for op in operations:
        if op[0] == "S":
            count += 1
    return count

def encode_answer_format(operations_list,L_answer_text): 
    selectcount = 1
    changecount = 0
    ans = ""
    word = ""
    for i in range(len(operations_list)):
        if((operations_list[i] == "L")or(operations_list[i] == "R")or(operations_list[i] == "U")or(operations_list[i] == "D")):
            word += operations_list[i]
            changecount +=1
        else:   
            ans = "\r\n" + word[::-1] + ans
            ans = "\r\n"  + str(changecount)  +ans
            ans = "\r\n" + operations_list[i][1:] + ans
            word = ""
            changecount = 0
            selectcount += 1

    ans = str(selectcount) + "\r\n" +L_answer_text+ ans
    return ans

# リストの先頭から順番に実行する
def move_position(move_list, pos):
  pos = list(pos)
  for move in move_list:
    if move == "L":
      pos[0] -= 1
    elif move == "R":
      pos[0] += 1
    elif move == "U":
      pos[1] -= 1
    elif move == "D":
      pos[1] += 1
  return tuple(pos)

def reverse_operations(operations):
  reverse_table = {
    "L": "R",
    "R": "L",
    "U": "D",
    "D": "U"
  }
  result = []
  moves = []
  for op in operations:
    if op[0] == "S":
      pos = (int(op[1], 16), int(op[2], 16))
      rev_moves = [reverse_table[a] for a in moves]
      new_pos = move_position(reversed(moves), pos)
      new_op = "S%X%X" % new_pos
      result.append(new_op)
      result += rev_moves
      moves = []
    else:
      moves.append(op)
  rev_moves = [reverse_table[a] for a in moves]
  result += rev_moves
  return result

def astar_step(queue, checked_nodes, table, min_distance, tag, fwd_ahead, back_ahead):
    dummy, looking_node, operations, selection_count = queue.pop() #キューの先頭を取り出
    g_star = caliculate_cost(operations)

    checked_nodes[(tuplenode(looking_node),tag)] = operations #chacked_nodes集合にチェック済みとして追加
    next_nodes = looking_node.get_next_nodes() #looking_nodeに隣接するノードたち(上下左右)を辞書型でnext_nodesに追加

    for key, node in next_nodes.items() : #中身全部取り出すぜー
        cost = 0
        select = False

        if key[0] != looking_node.selection :
            select = True
            cost += SELECTON_RATE
            added_operation = (key[1],("S%X%X"%key[0],operations))
        else:
            added_operation = (key[1],operations)

        if node.board != None and not((tuplenode(node),tag) in checked_nodes): #各隣接ノードがcheckd_nodesに無ければキューに追加。
            h_star = fast_distance_to_goal(looking_node,node, table)
            f_star = g_star + h_star

            if select:
              new_selection_count = selection_count + 1
            else:
              new_selection_count = selection_count
            if new_selection_count <= LIMIT_SELECTION:
              queue.push((f_star + cost + EXCHANGE_RATE, node, added_operation, new_selection_count))
              if h_star <= min_distance:
                min_distance = h_star
                print "%s distance=%d tag=%s" % (operations_to_list(added_operation), h_star, tag)
                #if int(h_star) == 0:
                  #cost = -1000000000
                  #print "stop!"
    return min_distance

def forward(problem, answer, checked_nodes,L_answer_text, result_queue):
  global mode_flag ,fwd_ahead, back_ahead, thresh
  ans_status = 0
  distance_table = create_distance_table(answer)
  static_h_star = distance_to_goal(distance_table,problem)/EXCHANGE_RATE
  print static_h_star
  queue = pheap.Empty(key=lambda a: a[0]) #空のキューを作成
  forward_min = 999999999999
  my_tag = "f"
  back_tag = "b"
  true_ans = answer

  next_nodes = Node(problem,(0,0),(0,0),static_h_star).get_next_nodes() #problemに隣接するノードたち(上下左右)を辞書型でnext_nodesに追加
  for key, node in next_nodes.items(): #中身全部取り出すぜー
    added_operation = (key[1],("S%X%X"%key[0],()))
    if node.board != None :
      h_star = distance_to_goal(distance_table,node.board)
      h_star = fast_distance_to_goal(Node(problem,(0,0),(0,0),static_h_star),node, distance_table)
      queue.push((h_star+SELECTON_RATE+EXCHANGE_RATE, node, added_operation, 1))

  while not queue.is_empty:
    operations = queue.element[2]
    if queue.element[1].board == true_ans: #仮に取り出したキューが正答と一致したら終了
      print "forward goal"
      print operations_to_list(operations)
      print "cost=%d" % caliculate_cost(operations)
      ALL_COST = caliculate_cost(operations)
      result_queue.put(encode_answer_format(operations_to_list(operations)))
      return

    if (tuplenode(queue.element[1]),back_tag) in checked_nodes:
      print "ぶつかったforward"
      fwd_op = list(reversed(operations_to_list(operations)))
      fwd_cost = caliculate_cost(operations)

      back_op = checked_nodes[(tuplenode(queue.element[1]),back_tag)]
      back_cost = caliculate_cost(back_op) - SELECTON_RATE
      back_op = reverse_operations(operations_to_list(back_op))[1:]

      full_op = fwd_op + back_op
      full_cost = fwd_cost + back_cost
      ALL_COST = full_cost

      result_queue.put(encode_answer_format(list(reversed(full_op)), L_answer_text))
      return

    fwd_ahead = queue.element[1].board
    if count_missmatch_image(fwd_ahead, back_ahead) <= int(rows * columns * thresh):# and mode_flag == "N":
      print "mode change!"
      mode_flag = "A"
      thresh *= MODE_CHANGE_THRESHOLD
      ans_status = 0
    if mode_flag == "A" and ans_status == 0:
      print "change answer!"
      answer = back_ahead
      distance_table = create_distance_table(answer)
      print distance_table 
      ans_status = 1

    forward_min = min(forward_min, astar_step(queue, checked_nodes, distance_table, forward_min, my_tag, fwd_ahead, back_ahead))
    



def back(problem, answer, checked_nodes, L_answer_text, result_queue):
  global mode_flag, fwd_ahead, back_ahead, thresh
  ans_status = 0
  distance_table = create_distance_table(problem)
  static_h_star = distance_to_goal(distance_table,answer)/EXCHANGE_RATE
  print static_h_star
  queue = pheap.Empty(key=lambda a: a[0]) #空のキューを作成
  back_min = 999999999999
  my_tag = "b"
  fwd_tag = "f"
  true_prob = problem

  next_nodes = Node(answer,(0,0), (0,0),static_h_star).get_next_nodes() #problemに隣接するノードたち(上下左右)を辞書型でnext_nodesに追加
  for key, node in next_nodes.items() : #中身全部取り出すぜー
    added_operation = (key[1],("S%X%X"%key[0],()))
    if node.board != None :
      h_star = fast_distance_to_goal(Node(answer,(0,0),(0,0),static_h_star),node, distance_table)
      queue.push((h_star+SELECTON_RATE+EXCHANGE_RATE, node, added_operation, 1))

  while not queue.is_empty:
    operations = queue.element[2]
    if queue.element[1].board == true_prob: #仮に取り出したキューが正答と一致したら終了
      print "back goal"
      print operations_to_list(operations)
      print "cost=%d" % caliculate_cost(operations)
      ALL_COST = caliculate_cost(operations)
      result_queue.put(encode_answer_format(list(reversed(reverse_operations(operations_to_list(operations))))))
      return

    if (tuplenode(queue.element[1]),fwd_tag) in checked_nodes:
      print "ぶつかったback"
      fwd_op = checked_nodes[(tuplenode(queue.element[1]),fwd_tag)]
      fwd_op = list(reversed(operations_to_list(fwd_op)))
      fwd_cost = caliculate_cost(operations)

      back_op = operations
      back_cost = caliculate_cost(back_op) - SELECTON_RATE
      back_op = reverse_operations(operations_to_list(back_op))[1:]

      full_op = fwd_op + back_op
      full_cost = fwd_cost + back_cost
      ALL_COST = full_cost
      result_queue.put(encode_answer_format(list(reversed(full_op)), L_answer_text))
      return
    back_ahead = queue.element[1].board

    if count_missmatch_image(fwd_ahead, back_ahead) <= int(rows * columns * thresh):# and mode_flag == "N":
      print "mode change!"
      mode_flag = "A"
      thresh *= MODE_CHANGE_THRESHOLD
      ans_status = 0
    if mode_flag == "A" and ans_status == 0:
      print "change answer!"
      problem = fwd_ahead
      distance_table = create_distance_table(problem)
      print distance_table 
      ans_status = 1

    back_min = min(back_min, astar_step(queue, checked_nodes, distance_table, back_min, my_tag, fwd_ahead, back_ahead))

def solve(sortedImages, splitColumns, splitRows, limit, sel_rate, exc_rate, target_columns, target_rows):
    global LIMIT_SELECTION, SELECTON_RATE, EXCHANGE_RATE, rows, columns, fwd_ahead, back_ahead
    LIMIT_SELECTION = limit
    SELECTON_RATE = sel_rate
    EXCHANGE_RATE = exc_rate
    problem = make_problem(splitColumns, splitRows)
    answer =  sortedImages
    columns = splitColumns
    rows = splitRows
    checked_nodes = {} #set() #チェック済みのノード集合

    problem,L_answer_text = tree_L_sprit.L_sprit(target_columns, target_rows, problem,answer,"UL")
    LIMIT_SELECTION -= 1

    fwd_ahead = problem
    back_ahead = answer
    result_queue = Queue.Queue()

    fwd_thr = threading.Thread(target=forward, name="fwd", args=(problem, answer, checked_nodes, L_answer_text, result_queue))
    back_thr = threading.Thread(target=back, name="back", args=(problem, answer, checked_nodes, L_answer_text, result_queue))

    fwd_thr.daemon = True
    back_thr.daemon = True

    fwd_thr.start()
    back_thr.start()

    while True:
      try:
        # 1秒ごとにタイムアウトする
        # タイムアウト時にキューに内容が無ければEmpty例外が出る
        return result_queue.get(True, 1)
      except Queue.Empty:
        # 例外が出ても何もしない
        pass
      except KeyboardInterrupt:
        print "aborting"
        # kill flagをセットしてスレッドを終了させる
        kill_flag = True
        sys.exit(0)


#main
master = "" 
target_columns = 4
target_rows = 4
if len(sys.argv) == 3:
  master = sys.argv[1]
  target_columns,target_rows = sys.argv[2].split("-")
elif len(sys.argv) == 2:
    if '.' in sys.argv[1]:
       master = sys.argv[1]
    elif '-' in sys.argv[1]:
       target_columns,target_rows = sys.argv[1].split("-")
       master = config.master
else:
  master = config.master

para = communication.get_problem(master)
ans_str = solve(para['answer'], para['columns'], para['rows'], para['lim_select'], para['selection_rate'], para['exchange_rate'],int(target_columns),int(target_rows))
communication.post(master, ans_str)
