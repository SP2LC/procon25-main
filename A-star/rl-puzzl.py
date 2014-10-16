#-*- coding:utf-8 -*-
from heapq import heappush, heappop
from copy import deepcopy
import random
import requests
from requests.auth import HTTPDigestAuth
import sys
import communication
import time
import json
import config

ALL_COST = 0

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if len(matrix[i][j]) == 3:
                if matrix[i][j][2] == True:
                    print matrix[i][j] ,"  ",
                else:
                    print matrix[i][j] ," ",
            else:
                print matrix[i][j] ," ",
        print ""

def make_answer(w,h):
    arr = make_problem(w,h)
    for i in range(len(arr)):
        random.shuffle(arr[i])
    arr = transpose(arr)
    for i in range(len(arr)):
        random.shuffle(arr[i])
    arr = transpose(arr)
    return arr

def transpose(arr2d): #転置した2次元配列を返す
    result = []
    for i in range(len(arr2d[0])):
        arr = []
        for j in range(len(arr2d)):
            arr.append(arr2d[j][i])
        result.append(arr)
    return result

def exchange(board, selection_positon, exchange_positon):
    si,sj = selection_positon
    ei,ej = exchange_positon
    new_board = deepcopy(board)

    #固定マスや範囲外はNoneを返す
    if board == None:#orでは区切れない
        return None        
    if not(0 <= ei < len(board) and 0 <= ej < len(board[0])):
        return None
    if board[ei][ej][2] == True: 
        return None

    temp = new_board[si][sj]
    new_board[si][sj] = new_board[ei][ej]
    new_board[ei][ej] = temp

    return new_board

def operation_exchange(board,selection_positon,operation):
    move_text = ""#使わない
    ans_board = deepcopy(board)
    for n in range(len(operation)):
        word = operation[n]
        if word == "U":
            ans_board,selection_positon,move_text = position_up(ans_board,selection_positon,move_text)
        if word == "D":
            ans_board,selection_positon,move_text = position_down(ans_board,selection_positon,move_text)
        if word == "L":
            ans_board,selection_positon,move_text = position_left(ans_board,selection_positon,move_text)
        if word == "R":
            ans_board,selection_positon,move_text = position_right(ans_board,selection_positon,move_text)
    return ans_board,selection_positon

def make_problem(w, h):
    arr = []
    for i in range(w):
        column = []
        for j in range(h):
            column.append((i, j))
        arr.append(column)
    return arr

def check_matrix(matrix_A,matrix_B,selection_positon):
    ok_count = 0
    no_count = 0
    for i in range(len(matrix_A)):
        print ""
        for j in range(len(matrix_A[0])):
            if matrix_A[i][j][0] == matrix_B[i][j][0] and matrix_A[i][j][1] == matrix_B[i][j][1]:

                print "OK ",
                ok_count += 1
            else:
                if selection_positon == (i,j):
                    print "SL ",
                else:
                    print "FF ",
                no_count += 1
    print ""
    print "  一致マス数",ok_count
    print "不一致マス数",no_count 


def matrix_flg_add(matrix):
    new_matrix = []
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix[0])):
            temp.append((matrix[i][j][0],matrix[i][j][1],False))
        new_matrix.append(temp)
    return new_matrix

def matrix_flg_substract(test):
    new_matrix = []
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix[0])):
            temp.append((matrix[i][j][0],matrix[i][j][1]))
        new_matrix.append(temp)
    return new_matrix

def distance_to_goal(table, board): #ノードとゴールノードまでの予測距離を返す。引数は(距離計算用テーブル,ゴールのボード)
    ans = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            key = (board[i][j][0],board[i][j][1])
            a = table[key]
            b = (i, j)
            x = abs(a[0] - b[0])
            y = abs(a[1] - b[1])
            ans += x + y
    return ans

def create_distance_table(goal): #距離計算用のテーブルを返す
    table = {}
    for i in range(len(goal)):
        for j in range(len(goal[0])):
            key = (goal[i][j][0],goal[i][j][1])
            table[key] = (i, j)
    return table

def position_up(board,selection_positon,answer_text):
    #print "want to up",
    i,j = selection_positon
    new_board = exchange(board,(i,j),(i-1,j))
    new_answer_text = answer_text + "U"
    new_selection_position = (i-1,j)

    #print "selection_positon U ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_down(board,selection_positon,answer_text):
    #print "want to down",
    i,j = selection_positon
    new_board = exchange(board,(i,j),(i+1,j))
    new_answer_text = answer_text + "D"
    new_selection_position = (i+1,j)

    #print "selection_positon D ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_right(board,selection_positon,answer_text):
    #print "want to right",
    i,j = selection_positon
    new_board = exchange(board,(i,j),(i,j+1))
    new_answer_text = answer_text + "R"
    new_selection_position = (i,j+1)

    #print "selection_positon R ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_left(board,selection_positon,answer_text):
    #print "want to left",
    i,j = selection_positon
    new_board = exchange(board,(i,j),(i,j-1))
    new_answer_text = answer_text + "L"
    new_selection_position = (i,j-1)

    #print "selection_positon L ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def search(board,selection):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j][0] == selection[0] and board[i][j][1] == selection[1]:
                return (i,j)

def encode_answer_format(RLUD_text1,RLUD_text2,selection,first_selection):
    answer_text = ""

    if selection == (-1,-1):
        selection_count = 1
        answer_text  = str(selection_count) + "\r\n" + "%X%X"%(first_selection[1],first_selection[0]) +"\r\n"+ str(len(RLUD_text1)) +"\r\n"+ RLUD_text1 
    else:
        selection_count = 2
        answer_text1 = str(selection_count) + "\r\n" + "%X%X"%(first_selection[1],first_selection[0]) +"\r\n"+ str(len(RLUD_text1)) +"\r\n"+ RLUD_text1+"\r\n"
        answer_text2 = "%X%X"%(selection[1],selection[0]) +"\r\n"+ str(len(RLUD_text2)) + "\r\n"+ RLUD_text2
        answer_text = answer_text1+answer_text2

    return answer_text

def cut_matrix(matrix,start_i,start_j,end_i,end_j):
    arr = []
    for i in range(start_i,end_i):
        temp = []
        for j in range(start_j,end_j):
            temp.append(matrix[i][j])
        arr.append(temp)
    return arr         

def move_selection(pi,pj,problem,answer,purpose_positon,selection_positon,answer_text,table):
    class Node :
        def __init__ (self, board, selection):
            self.board = board
            self.selection = selection#(position)


        def get_next_nodes(self): #渡したノードに隣接するノードを返す
            nodes_dic = {}
            board = self.board
            i,j = self.selection
            #右と交換            
            nodes_dic[("R")] = Node(exchange(board,(i, j), (i, j + 1)) , (i, j + 1))
            #左と交換
            nodes_dic[("L")] = Node(exchange(board,(i, j), (i, j - 1)) , (i, j - 1))
            #上と交換
            nodes_dic[("U")] = Node(exchange(board,(i, j), (i - 1, j)) , (i - 1, j))
            #下と交換
            nodes_dic[("D")] = Node(exchange(board,(i, j), (i + 1, j)) , (i + 1, j))

            return nodes_dic 
    #print "選択ピースを目的地周辺まで動かす"

    p_to_pp_dis = (pi - purpose_positon[0],pj - purpose_positon[1])

    Top = False
    Bottom = False#常にFalse
    Right = False
    Left = False
    first_top_sp   = -1
    first_left_sp  = -1
    first_right_sp = -1
    top_sp = -1
    left_sp = -1
    right_sp = -1

    if p_to_pp_dis[0] < 0:#目的ピースは上に行きたい    
        Top = True
        first_top_sp = abs(purpose_positon[0] - selection_positon[0] - 1) + abs(purpose_positon[1] - selection_positon[1])
    if p_to_pp_dis[1] < 0:#目的ピースは左に行きたい
        Left = True
        first_left_sp = abs(purpose_positon[0] - selection_positon[0]) + abs(purpose_positon[1] - selection_positon[1] - 1)
    if p_to_pp_dis[1] > 0:#目的ピースは右に行きたい
        Right = True
        first_right_sp = abs(purpose_positon[0] - selection_positon[0]) + abs(purpose_positon[1] - selection_positon[1] + 1)

    #print Top,Left,Right 

    pi,pj = purpose_positon
    si,sj = selection_positon
    if  ((si,sj) == (pi,pj+1) and Right)or((si,sj) == (pi,pj-1) and Left)or((si,sj) == (pi-1,pj) and Top):#条件に合えば終了
        #print "目的地周辺に来ました"
        return  problem,selection_positon,purpose_positon,answer_text


    queue = []
    next_nodes = Node(problem,(selection_positon)).get_next_nodes()
    for key,node in next_nodes.items():
        if node.board != None:
            selection_positon = node.selection
            #目的ピース周辺までの距離測定
            h_star = 0
            if Top:
                h_star += abs(purpose_positon[0] - selection_positon[0] - 1) + abs(purpose_positon[1] - selection_positon[1])
            if Left:
                h_star += abs(purpose_positon[0] - selection_positon[0]) + abs(purpose_positon[1] - selection_positon[1] - 1)
            if Right:
                h_star += abs(purpose_positon[0] - selection_positon[0]) + abs(purpose_positon[1] - selection_positon[1] + 1)

            move_text = key[0]
            c_star = distance_to_goal(table,node.board)#盤面係数
            f_star =h_star*100 +100+ c_star
            heappush(queue,(f_star,node,move_text,h_star))
    
    #print "queue",len(queue)

    while len(queue) != 0:
        dummy,looking_node,look_move_text,look_h_star = heappop(queue)
        if look_h_star <= 2:#選択ピースが目的ピースの近くに来たとき
            pi,pj = purpose_positon
            si,sj = looking_node.selection
            if  ((si,sj) == (pi,pj+1) and Right)or((si,sj) == (pi,pj-1) and Left)or((si,sj) == (pi-1,pj) and Top):#条件に合えば終了
                #print "目的地周辺に来ました"
                answer_text += look_move_text
                return looking_node.board,looking_node.selection,purpose_positon,answer_text
        next_nodes = looking_node.get_next_nodes()
        for key,node in next_nodes.items():
            if node.board != None:
                selection_positon = node.selection
                h_star = 0
                if Top:
                    h_star += abs(purpose_positon[0] - selection_positon[0] - 1) + abs(purpose_positon[1] - selection_positon[1])
                if Left:
                    h_star += abs(purpose_positon[0] - selection_positon[0]) + abs(purpose_positon[1] - selection_positon[1] - 1)
                if Right:
                    h_star += abs(purpose_positon[0] - selection_positon[0]) + abs(purpose_positon[1] - selection_positon[1] + 1)               
                
                new_move_text = look_move_text + key[0]
                c_star = distance_to_goal(table,node.board)
                g_star = len(new_move_text)
                f_star = h_star*100 + g_star*100 + c_star 
                heappush(queue,(f_star,node,new_move_text,h_star))    

def move_purpose(pi,pj,problem,purpose_positon,selection_positon,answer_text,table):
    class Node :
        def __init__ (self, board, selection,purpose_positon,top,left,right):
            self.board = board
            self.selection = selection
            self.purpose_positon = purpose_positon
            self.top = top
            self.left = left
            self.right = right
        def get_next_nodes(self): #渡したノードに隣接するノードを返す

            nodes_dic = {}
            i,j = self.purpose_positon
            if self.top:
                #目的ピースを右に移動(1)

                board,selection_positon = operation_exchange(self.board,self.selection,"RUL")
                nodes_dic[("RUL")]   = Node(board,selection_positon,(i,j+1),False,False,True)
                #目的ピースを左に移動(1)
                board,selection_positon = operation_exchange(self.board,self.selection,"LUR")                
                nodes_dic[("LUR")]   = Node(board,selection_positon,(i,j-1),False,True,False)
                #目的ピースを上に移動(1)
                board,selection_positon = operation_exchange(self.board,self.selection,"RUULD")
                nodes_dic[("RUULD")] = Node(board,selection_positon,(i-1,j),True,False,False)
                #目的ピースを上に移動(2)
                board,selection_positon = operation_exchange(self.board,self.selection,"LUURD")
                nodes_dic[("LUURD")] = Node(board,selection_positon,(i-1,j),True,False,False)

            if self.left:
                #目的ピースを上に移動(1)
                board,selection_positon = operation_exchange(self.board,self.selection,"ULD")
                nodes_dic[("ULD")]   = Node(board,selection_positon,(i-1,j),True,False,False)
                #目的ピースを左に移動(1)
                board,selection_positon = operation_exchange(self.board,self.selection,"ULLDR")
                nodes_dic[("ULLDR")] = Node(board,selection_positon,(i,j-1),False,True,False)
                #目的ピースを左に移動(2)
                board,selection_positon = operation_exchange(self.board,self.selection,"DLLUR")
                nodes_dic[("DLLUR")] = Node(board,selection_positon,(i,j-1),False,True,False)                

            if self.right:
                #目的ピースを上に移動(1)
                board,selection_positon = operation_exchange(self.board,self.selection,"URD")
                nodes_dic[("URD")]   = Node(board,selection_positon,(i-1,j),True,False,False)
                #目的ピースを右に移動(1)
                board,selection_positon = operation_exchange(self.board,self.selection,"URRDL")
                nodes_dic[("URRDL")] = Node(board,selection_positon,(i,j+1),False,False,True)
                #目的ピースを右に移動(2)
                board,selection_positon = operation_exchange(self.board,self.selection,"DRRUL")
                nodes_dic[("DRRUL")] = Node(board,selection_positon,(i,j+1),False,False,True)

            return nodes_dic    

    #print "目的ピースを目的地まで動かす"
    #print "選択ピースポジション",selection_positon
    #print "目的ピースポジション",purpose_positon
    if purpose_positon == (pi,pj):#目的地にすでにいるとき
        #print "既に目的地にいる"
        return problem,selection_positon,answer_text
    Top = False
    Right = False
    Left = False
    move_text = ""
    #選択ピース位置
    if purpose_positon[0] - 1 == selection_positon[0]:
        Top = True
        problem,selection_positon,move_text = position_down(problem,selection_positon,move_text)
        purpose_positon = (purpose_positon[0]-1,purpose_positon[1])
    if purpose_positon[1] - 1 == selection_positon[1]:
        Left = True
        problem,selection_positon,move_text = position_right(problem,selection_positon,move_text)
        purpose_positon = (purpose_positon[0],purpose_positon[1]-1)
    if purpose_positon[1] + 1 == selection_positon[1] and Left != True:
        Right = True
        problem,selection_positon,move_text = position_left(problem,selection_positon,move_text)
        purpose_positon = (purpose_positon[0],purpose_positon[1]+1)
    #print_matrix(problem)
    

    #print "一回移動後\n","Top =",Top,"\nLeft =",Left,"\nRight =",Right
    #print "選択ピースポジション",selection_positon
    #print "目的ピースポジション",purpose_positon
    first_h_star = abs(purpose_positon[0] - pi) + abs(purpose_positon[1] - pj)
    #print "first_h_star",first_h_star
    if first_h_star == 0:#目的地にすでにいるとき
        return problem,selection_positon,answer_text+move_text
    queue = []
    next_nodes = Node(problem,selection_positon,(purpose_positon),Top,Left,Right).get_next_nodes()
    for key ,node in next_nodes.items():
        new_move_text = move_text + key
        if node.board != None:
            h_star = abs(node.purpose_positon[0] - pi)+abs(node.purpose_positon[1] - pj)
            #print h_star
            c_star = distance_to_goal(table,node.board)
            f_star = h_star*100 +100 + c_star
            heappush(queue,(f_star,node,new_move_text,h_star,1))

    while  len(queue) != 0:
        dummy,looking_node,look_move_text,look_h_star,g_star = heappop(queue)
        g_star += 1
        if look_h_star == 0:
            answer_text += look_move_text
            return looking_node.board,looking_node.selection,answer_text
        next_nodes = looking_node.get_next_nodes()
        for key,node in next_nodes.items():
            if node.board != None:
                #print node.purpose_positon
                new_move_text = look_move_text + key
                h_star = abs(node.purpose_positon[0] - pi)+abs(node.purpose_positon[1] - pj)
                c_star = distance_to_goal(table,node.board)
                f_star = h_star*100 + g_star*100 + c_star
                heappush(queue,(f_star,node,new_move_text,h_star,g_star))

def move(pi,pj,i,j,problem,answer,selection_positon,answer_text,table):
    purpose = answer[i][j]
    purpose_positon = search(problem,purpose)



    #print_matrix(problem)
    #print "目的ピース",purpose,"目的地",(pi,pj),"目的ピースポジション",purpose_positon
    #print "選択ピース位置",selection_positon
    if purpose_positon != (pi,pj):#目的ピースが目的地になかったとき
        #print "すでに目的地にピースがある"
    #else:
        problem[purpose_positon[0]][purpose_positon[1]] =  (problem[purpose_positon[0]][purpose_positon[1]][0],problem[purpose_positon[0]][purpose_positon[1]][1],True)#目的ピースの固定
        problem,selection_positon,purpose_positon,answer_text = move_selection(pi,pj,problem,answer,purpose_positon,selection_positon,answer_text,table)
        problem[purpose_positon[0]][purpose_positon[1]] =  (problem[purpose_positon[0]][purpose_positon[1]][0],problem[purpose_positon[0]][purpose_positon[1]][1],False)#目的ピースの開放
    #print answer_text
   # print_matrix(problem)

    problem,selection_positon,answer_text = move_purpose(pi,pj,problem,purpose_positon,selection_positon,answer_text,table)
    problem[pi][pj] = (problem[pi][pj][0],problem[pi][pj][1],True)

   # print problem[i][j]

    #print_matrix(problem)
    #check_matrix(problem,answer,selection_positon)



    return problem,selection_positon,answer_text

def set_row(i, problem, answer, selection_positon, distance_table, answer_text, direction):
  if direction == "R":
    for j in range(len(problem[0])-2):

        problem,selection_positon,answer_text = move(i,j,i,j,problem,answer,selection_positon,answer_text,distance_table)
        #print answer_text
        #print i,"行目",j,"番目","を整地＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝"
  else:
    # 逆順
    for j in range(len(problem[0])-1, 1, -1):
        problem,selection_positon,answer_text = move(i,j,i,j,problem,answer,selection_positon,answer_text,distance_table)
        #print answer_text
        #print i,"行目",j,"番目","を整地＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝"

  #print "後ろ2つ ---------------------------------------------------------------"

  if answer[i]  != problem[i]:
      #check_matrix(answer,problem,selection_positon)
      if direction == "R":
        x = len(problem[0])-2
        x_ans = len(problem[0])-1
      else:
        x = 0
        x_ans = 1
      problem,selection_positon,answer_text = move(i,x,i,x_ans,problem,answer,selection_positon,answer_text,distance_table)
      #例外処理
      #print "後入れ-----------------------------------------------------------------"
      if (problem[i][x_ans][0] == answer[i][x][0] and problem[i][x_ans][1] == answer[i][x][1]) :             
          problem[i][x] = (problem[i][x][0],problem[i][x][1],False)
          if selection_positon[1] != x:
              if selection_positon[1] == x_ans:
                  if direction == "R":
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                  else:
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

              else:
                  for n in range(x - selection_positon[1]):
                    if direction == "R":
                      problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    else:
                      problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

          if selection_positon[0] != i:
              for n in range(i - selection_positon[0]):
                  problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)

          problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
          problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
      else:
          if ((selection_positon[0] == i and selection_positon[1] == x_ans)and(problem[i+1][x_ans][0] == answer[i][x][0] and problem[i+1][x_ans][1] == answer[i][x][1])):
              problem[i][x] = (problem[i][x][0],problem[i][x][1],False)  
              problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
              problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
          else:

              problem,selection_positon,answer_text = move(i+1,x,i,x,problem,answer,selection_positon,answer_text,distance_table)
              problem[i][x] = (problem[i][x][0],problem[i][x][1],False)
              problem[i+1][x] = (problem[i+1][x][0],problem[i+1][x][1],False)


              if direction == "R" and ((selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -3) or (selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -1) or (selection_positon[0] == i+2 and selection_positon[1] == len(problem[0]) -2)) :
                  if selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -3:
                      #print "パターン1"
                      problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                  if selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -1:
                      #print "パターン2"
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
                  if selection_positon[0] == i+2 and selection_positon[1] == len(problem[0]) -2:            
                      #print "パターン3"
                      problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
              elif(selection_positon[0] == i+1 and selection_positon[1] == 1) or (selection_positon[0] == i+2 and selection_positon[1] == 0) :
                  if selection_positon[0] == i+1 and selection_positon[1] == 1:
                      #print "パターン2"
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
                  if selection_positon[0] == i+2 and selection_positon[1] == 0: 
                      #print "パターン3"
                      problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                  
              else:
                  #print "OKKKKKKKKKKK"
                  if selection_positon[0] != i :
                      if i + 1 == selection_positon[0]:
                          problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                      if selection_positon[1] < x:
                          for n in range(abs(selection_positon[1] - (x))):
                              problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                      if selection_positon[1] > x:
                          for n in range(abs(selection_positon[1] - (x))):
                              problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                      #print "パターン3"
                      problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                      problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                  problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                  problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
  #print "problem"
  #print problem
  #check_matrix(answer,problem,selection_positon)
  if direction == "R":
      #print "後ろ二つを固定"
      problem[i][len(problem[0])-2] = (problem[i][len(problem[0])-2][0],problem[i][len(problem[0])-2][1],True)
      problem[i][len(problem[0])-1] = (problem[i][len(problem[0])-1][0],problem[i][len(problem[0])-1][1],True)
  else:
      #print "前二つを固定"
      problem[i][0] = (problem[i][0][0],problem[i][0][1],True)
      problem[i][1] = (problem[i][1][0],problem[i][1][1],True)
  #print i,"行目終わり！！*******************************************************"
  #print "answer"
  #print_matrix(answer)
  #print "problem"
  #print_matrix(problem)
  #check_matrix(answer,problem,selection_positon)
  #print "*****************************************************************"
  return problem, selection_positon, answer_text

def solve(sortedImages, splitColumns, splitRows, limit, sel_rate, exc_rate):
    global LIMIT_SELECTION, SELECTON_RATE, EXCHANGE_RATE, distance_table,answer_text,ALL_COST
    LIMIT_SELECTION = limit
    SELECTON_RATE = sel_rate
    EXCHANGE_RATE = exc_rate
    problem = transpose(make_problem(splitColumns, splitRows))
    answer =  transpose(sortedImages)
    distance_table = create_distance_table(answer)

    problem = matrix_flg_add(problem)#一致マスのフラグをマトリックスに付与
    #print "starrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrRFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFff"
    answer_text = ""
    #print "answer"
    #print_matrix(answer)

    #print "problem"
    #print_matrix(problem)
    selection = answer[len(answer)-1][len(answer[0])-1]
    selection_positon = search(problem,selection)
    #print selection,selection_positon

    static_first_selection_positon = selection_positon
    #check_matrix(answer,problem,selection_positon)

    for i in range(len(problem)-2):
        problem_R = deepcopy(problem)
        problem_L = deepcopy(problem)
        problem_R, selection_positon_R, answer_text_R = set_row(i, problem_R, answer, selection_positon, distance_table, answer_text,"R")
        problem_L, selection_positon_L, answer_text_L = set_row(i, problem_L, answer, selection_positon, distance_table, answer_text,"L")
        if len(answer_text_R) > len(answer_text_L): 
        #if i % 4 == 0:        
            #problem_L, selection_positon_L, answer_text_L = set_row(i, problem, answer, selection_positon, distance_table, answer_text,"L")
            problem,selection_positon,answer_text = problem_L,selection_positon_L,answer_text_L
        else:
            #problem_R, selection_positon_R, answer_text_R = set_row(i, problem, answer, selection_positon, distance_table, answer_text,"R")
            problem,selection_positon,answer_text = problem_R,selection_positon_R,answer_text_R

    #ラスト２段処理開始
    #print "ラスト2段処理！！！！xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    for j in range(len(problem[0])-2):
        #print "answer"
        #print_matrix(answer)
        #print "problem"
        #print_matrix(problem)
        #dummy,dummy= check_matrix(answer,problem,selection_positon)

        i = len(problem)-2
        #print "i = ",i,"j = ",j
        problem,selection_positon,answer_text = move(i,j,i+1,j,problem,answer,selection_positon,answer_text,distance_table)
        #dummy,dummy= check_matrix(answer,problem,selection_positon)
        #print "problem"
        #print_matrix(problem)
        ##print "selection",selection    
        #print "selection_positon",selection_positon
        if selection_positon == (i+1,j):
            #print "選択ピースの位置が面倒"
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
        else:#奇跡に等しい
            #print "奇跡に等しい神配置"
            if abs(selection_positon[0] - i) == 1:
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            for n in range(abs(j+1 - selection_positon[1])):
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

        #print "answer"
        #print_matrix(answer)
        #print "problem"
        #print_matrix(problem)    
        #dummy,dummy= check_matrix(answer,problem,selection_positon)

        if problem[i+1][j][0] == answer[i][j][0] and problem[i+1][j][1] == answer[i][j][1]:
            #print "めんどくさいパターン2"
            problem[i][j] = (problem[i][j][0],problem[i][j][1],False)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

        else:
            problem,selection_positon,answer_text = move(i,j+1,i,j,problem,answer,selection_positon,answer_text,distance_table)
            problem[i][j] = (problem[i][j][0],problem[i][j][1],False)
            problem[i][j+1] = (problem[i][j+1][0],problem[i][j+1][1],False)
            
            #if i == 14 and j == 2:
            #    dummy,dummy= check_matrix(answer,problem,selection_positon)
            #    break
            #print "problem"
            #print_matrix(problem)

            if abs(selection_positon[0] - i) == 0:
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            for n in range(abs(j - selection_positon[1])):
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            #print "車庫入れver2"
            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

        problem[i][j] = (problem[i][j][0],problem[i][j][1],True)
        problem[i+1][j] = (problem[i+1][j][0],problem[i+1][j][1],True)

    #print "answer"
    #print_matrix(answer)    
    #print "problem"
    #print_matrix(problem)
    #dummy,dummy = check_matrix(answer,problem,selection_positon)
    #check_matrix(answer,problem,selection_positon)
    flg = False
    #print "右下4マス処理================================================================================"
    

    i = len(problem)-1
    j = len(problem[0])-1
    count = 0
    selection_count = 1
    answer_text2 = ""

    if problem[i][j][0] == answer[i][j][0] and problem[i][j][1] == answer[i][j][1]:
        count += 1
    if problem[i][j-1][0] == answer[i][j-1][0] and problem[i][j-1][1] == answer[i][j-1][1] :
        count += 1
    if problem[i-1][j][0] == answer[i-1][j][0] and problem[i-1][j][1] == answer[i-1][j][1]:
        count += 1

    static_selection_positon = (-1,-1)
    
    #木の下のどれか

    if count == 0:
        #print "counte = 3"
        if problem[i-1][j][0] == answer[i-1][j-1][0] and problem[i-1][j][1] == answer[i-1][j-1][1] and flg == False:
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            selection_positon = (i-1 ,j-1)
            #print selection_positon
            selection_count += 1
            static_selection_positon = selection_positon
            problem,selection_positon,answer_text2 = position_right(problem,selection_positon,answer_text2)
            flg = True
        
        if problem[i][j-1][0] == answer[i-1][j-1][0] and problem[i][j-1][1] == answer[i-1][j-1][1] and flg == False:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            selection_positon = (i-1 ,j-1)
            selection_count += 1
            static_selection_positon = selection_positon
            problem,selection_positon,answer_text2 = position_down(problem,selection_positon,answer_text2)
            flg = True

        if problem[i][j][0] == answer[i-1][j-1][0] and problem[i][j][1] == answer[i-1][j-1][1] and flg == False:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            selection_positon = (i,j-1)
            selection_count += 1
            static_selection_positon = selection_positon
            problem,selection_positon,answer_text2 = position_up(problem,selection_positon,answer_text2)
            problem,selection_positon,answer_text2 = position_right(problem,selection_positon,answer_text2)
            flg = True

    if count == 1:
        #print "count = 1"
        if problem[i][j-1][0] == answer[i][j-1][0] and problem[i][j-1][1] == answer[i][j-1][1] and flg == False:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            flg = True
        
        if  problem[i-1][j][0] == answer[i-1][j][0] and problem[i-1][j][1] == answer[i-1][j][1] and flg == False:
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            flg = True

    if count == 2:
        #print "count = 2"
        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
        selection_positon = (i-1,j)
        #print selection_positon
        selection_count += 1
        static_selection_positon = selection_positon
        problem,selection_positon,answer_text2 = position_left(problem,selection_positon,answer_text2)

    #print "表示テスト"
    #print "selection_positon",selection_positon
    #print "\nlast board"
    #print_matrix(problem)
    #print "交換回数",len(answer_text)
    #check_matrix(answer,problem,selection_positon)
    #print "\n\n"
    #print answer_text
    ALL_COST = selection_count*SELECTON_RATE + (len(answer_text)+len(answer_text2))*EXCHANGE_RATE

    encode_text =  encode_answer_format(answer_text,answer_text2,static_selection_positon,static_first_selection_positon)
    #print encode_text
    return encode_text

#main
master = "" 
if len(sys.argv) == 2:
  master = sys.argv[1]
else:
  master = config.master

para = communication.get_problem(master)
ans_str = solve(para['answer'], para['columns'], para['rows'], para['lim_select'], para['selection_rate'], para['exchange_rate'])
communication.post(master, ans_str)
