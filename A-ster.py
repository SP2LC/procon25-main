# -*- coding: utf-8 -*-

from collections import deque
from heapq import heappush, heappop
from copy import deepcopy,copy


LIMIT_SELECTION = 5 #選択上限、適宜変更
SELECTON_RATE = 1 #選択コストレート、適宜変更
EXCHANGE_RATE = 2 #交換コストレート、適宜変更

class Node :
    def __init__ (self, board, selection):
        self.board = board
        self.selection = selection

    def get_next_nodes(self): #渡したノードに隣接するノードを返す
        nodes_dic = {}
        board = self.board
        x,y = self.selection
        #右と交換
        nodes_dic["R"] = Node(exchange(board,(x, y), (x + 1, y)) , (x + 1, y))
        #左と交換
        nodes_dic["L"] = Node(exchange(board,(x, y), (x - 1, y)) , (x - 1, y))
        #上と交換
        nodes_dic["U"] = Node(exchange(board,(x, y), (x, y - 1)) , (x, y - 1))
        #下と交換
        nodes_dic["D"] = Node(exchange(board,(x, y), (x, y + 1)) , (x, y + 1))
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

problem = make_problem(3, 5)
answer = [[(0, 1), (1, 1), (1, 0), (1, 2), (2, 2)], [(0, 2), (2, 3), (0, 4), (2, 4), (1, 4)], [(0, 3), (2, 0), (2, 1), (1, 3), (0, 0)]]

distance_table = create_distance_table(answer)
queue = [] #空のキューを作成
for i in range(len(problem)):
    for j in range(len(problem[0])):
        queue.append((0+distance_to_goal(distance_table,problem),Node(problem, (i, j)),("S%d%d"%(i,j),()),1)) # (f*(n),(ボード2次元配列, 選択座標), 今まで辿ったノード)

checked_nodes = set() #チェック済みのノード集合

while  len(queue) != 0: #キューの長さ分くりかえすでー
    f_star, looking_node, operations, selection_count = heappop(queue) #キューの先頭を取り出す
    if looking_node.board == answer : #仮に取り出したキューが正答と一致したら終了
        print operations_to_list(operations)
        exit()
    checked_nodes.add(tuplenode(looking_node)) #chacked_nodes集合にチェック済みとして追加
    next_nodes = looking_node.get_next_nodes() #looking_nodeに隣接するノードたち(上下左右)を辞書型でnext_nodesに追加
    
    for direction in ["R","L","U","D"] : #中身全部取り出すぜー
        node = next_nodes[direction]
        if node.board != None and not(tuplenode(node) in checked_nodes): #各隣接ノードがcheckd_nodesに無ければキューに追加。
            heappush(queue, (caliculate_cost(operations)+distance_to_goal(distance_table,node.board),node,(direction, operations),selection_count))

    for i in range(len(problem)): #選択するマスを変えたノードをキューに追加する。
        for j in range(len(problem[0])):
            if selection_count < LIMIT_SELECTION and operations[0][0] != "S" :
                heappush(queue , (caliculate_cost(operations), Node(looking_node.board, (i, j)),("S%d%d"%(i,j),operations),selection_count+1))


print "出なかった"
