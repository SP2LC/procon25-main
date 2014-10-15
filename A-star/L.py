# -*- coding: utf-8 -*-
from heapq import heappush, heappop
from copy import deepcopy,copy
import time
import communication
import requests
import sys
import config
import L_sprit

# グローバル変数の宣言
LIMIT_SELECTION = 0
SELECTON_RATE = 0
EXCHANGE_RATE = 0

distance_table = {}

class Node :
    def __init__ (self, board, selection):
        self.board = board
        self.selection = selection

    def get_next_nodes(self): #渡したノードに隣接するノードを返す

        nodes_dic = {}
        board = self.board

        for i in range(len(board)): #選択するマスを変えたノードをキューに追加する。
            for j in range(len(board[0])):
            
                x,y = (i,j)
                #右と交換
                nodes_dic[((i,j),"R")] = Node(exchange(board,(x, y), (x + 1, y)) , (x + 1, y))
                #左と交換
                nodes_dic[((i,j),"L")] = Node(exchange(board,(x, y), (x - 1, y)) , (x - 1, y))
                #上と交換
                nodes_dic[((i,j),"U")] = Node(exchange(board,(x, y), (x, y - 1)) , (x, y - 1))
                #下と交換
                nodes_dic[((i,j),"D")] = Node(exchange(board,(x, y), (x, y + 1)) , (x, y + 1))

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
    table = {}
    for i in range(len(goal)):
        for j in range(len(goal[0])):
            table[goal[i][j]] = (i, j)
    return table  

def distance_to_goal(table, board): #ノードとゴールノードまでの予測距離を返す。引数は(距離計算用テーブル,ゴールのボード)
    ans = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            a = table[board[i][j]]
            b = (i, j)
            x = abs(a[0] - b[0])
            y = abs(a[1] - b[1])
            ans += x + y
    return ans * EXCHANGE_RATE

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

def selection_h_star(x,y):
    goal_point = distance_table[(x,y)]
    distance = abs(goal_point[0]-x)+abs(goal_point[1]-y)*1.0
    if distance == 0 :
      distance = 1
    distance = (1 / distance)
    return distance

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

def solve(sortedImages, splitColumns, splitRows, limit, sel_rate, exc_rate,target_columns,target_rows):
    global LIMIT_SELECTION, SELECTON_RATE, EXCHANGE_RATE, distance_table
    LIMIT_SELECTION = limit
    SELECTON_RATE = sel_rate
    EXCHANGE_RATE = exc_rate
    problem = make_problem(splitColumns, splitRows)
    answer =  sortedImages
    print "Reduction to " + str(target_columns) +"," + str(target_rows)
    problem,L_answer_text = L_sprit.corner_L_sprit(target_columns,target_rows,problem,answer)
    print problem
    LIMIT_SELECTION -= 1    

    distance_table = create_distance_table(answer)
    queue = [] #空のキューを作成

    next_nodes = Node(problem,(0,0)).get_next_nodes() #problemに隣接するノードたち(上下左右)を辞書型でnext_nodesに追加
    for key, node in next_nodes.items() : #中身全部取り出すぜー
        added_operation = (key[1],("S%X%X"%key[0],()))
        if node.board != None :
            h_star = distance_to_goal(distance_table,node.board)
            heappush(queue, (h_star+SELECTON_RATE+EXCHANGE_RATE, node, added_operation, 1))


    # (f*(n),(ボード2次元配列, 選択座標), 今まで辿ったノード)

    checked_nodes = set() #チェック済みのノード集合

    min_distance = 9999999

    counter = 0 # 処理速度計測用
    count_start = time.time()
    average_time = None

    while  len(queue) != 0: #キューの長さ分くりかえすでー
        dummy, looking_node, operations, selection_count = heappop(queue) #キューの先頭を取り出す
        g_star = caliculate_cost(operations)
        if looking_node.board == answer : #仮に取り出したキューが正答と一致したら終了
            print operations_to_list(operations)
            print "cost=%d" % caliculate_cost(operations)
            if average_time != None:
              print "%f nodes/s" % average_time
            else:
              print "%d nodes were checked" % counter
              print "%f nodes/s" % (counter / (time.time() - count_start))
            return encode_answer_format(operations_to_list(operations),L_answer_text)

        # 処理速度計測
        counter += 1
        if counter > 200:
          # 1000回到達したら
          count_time = counter / (time.time() - count_start)
          if average_time == None:
            average_time = count_time
          else:
            average_time = (average_time + count_time) / 2
          counter = 0
          count_start = time.time()
        # 計測終わり

        checked_nodes.add(tuplenode(looking_node)) #chacked_nodes集合にチェック済みとして追加
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

            if node.board != None and not(tuplenode(node) in checked_nodes): #各隣接ノードがcheckd_nodesに無ければキューに追加。
                h_star = distance_to_goal(distance_table,node.board)
                f_star = g_star + h_star
                if select:
                    new_selection_count = selection_count + 1
                else:
                    new_selection_count = selection_count
                if new_selection_count <= LIMIT_SELECTION:
                    heappush(queue, (f_star + cost + EXCHANGE_RATE, node, added_operation, new_selection_count))
                    if h_star <= min_distance:
                        min_distance = h_star
                        print "%s distance=%d" % (operations_to_list(added_operation), h_star)
                        if int(h_star) == 0:
                            cost = -1000000000
                            print "stop!"


    print "出なかった"
    return False

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

len(sys.argv) 
para = communication.get_problem(master)
ans_str = solve(para['answer'], para['columns'], para['rows'], para['lim_select'], para['selection_rate'], para['exchange_rate'],int(target_columns),int(target_rows))
communication.post(master, ans_str)
