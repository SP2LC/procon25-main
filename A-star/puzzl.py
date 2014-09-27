#-*- coding:utf-8 -*-
import random
import requests
from requests.auth import HTTPDigestAuth
import json
import sys
import communication
import config
import time

ALL_COST = 0

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
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

def exchange (board, selection_positon, exchange_positon):
    si,sj = selection_positon
    ei,ej = exchange_positon

    temp = board[si][sj]
    board[si][sj] = board[ei][ej]
    board[ei][ej] = temp

    return board

def make_problem(w, h):
    arr = []
    for i in range(w):
        column = []
        for j in range(h):
            column.append((i, j))
        arr.append(column)
    return arr

def check_matrix(matrix_A,matrix_B):
    ok_count = 0
    no_count = 0
    for i in range(len(matrix_A)):
        print ""
        for j in range(len(matrix_A[0])):
            if matrix_A[i][j] == matrix_B[i][j]: 
                print "OK ",
                ok_count += 1
            else:
                print "NO ",
                no_count += 1
    print ""
    print "  一致マス数",ok_count
    print "不一致マス数",no_count 

def position_up(board,selection_positon,answer_text):
    print "want to up",
    i,j = selection_positon
    new_board = exchange(board,(i,j),(i-1,j))
    new_answer_text = answer_text + "L"
    new_selection_position = (i-1,j)

    print "selection_positon U ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_down(board,selection_positon,answer_text):
    print "want to down",
    i,j = selection_positon
    new_board = exchange(board,(i,j),(i+1,j))
    new_answer_text = answer_text + "R"
    new_selection_position = (i+1,j)

    print "selection_positon D ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_right(board,selection_positon,answer_text):
    print "want to right",
    i,j = selection_positon
    new_board = exchange(board,(i,j),(i,j+1))
    new_answer_text = answer_text + "D"
    new_selection_position = (i,j+1)

    print "selection_positon R ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_left(board,selection_positon,answer_text):
    print "want to left",
    i,j = selection_positon
    new_board = exchange(board,(i,j),(i,j-1))
    new_answer_text = answer_text + "U"
    new_selection_position = (i,j-1)

    print "selection_positon L ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def search(board,selection):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == selection :
                return (i,j)

def purpose_position_up(board,selection_positon,answer_text):#purposeの下からスタート
    board,selection_positon,answer_text = position_right(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_up(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_up(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_left(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_down(board,selection_positon,answer_text)

    return board,selection_positon,answer_text

def purpose_position_right(board,selection_positon,answer_text):
    board,selection_positon,answer_text = position_down(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_right(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_right(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_up(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_left(board,selection_positon,answer_text)

    return board,selection_positon,answer_text

def purpose_position_left(board,selection_positon,answer_text):

    board,selection_positon,answer_text = position_down(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_left(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_left(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_up(board,selection_positon,answer_text)
    board,selection_positon,answer_text = position_right(board,selection_positon,answer_text)

    return board,selection_positon,answer_text

def encode_answer_format(RLUD_text1,RLUD_text2,selection,answer):
    first_selection = answer[len(answer)-1][len(answer[0])-1]
    
    answer_text = ""

    if first_selection == selection:
        RLUD_text = RLUD_text1+RLUD_text2
        selection_count = 1
        answer_text = str(selection_count) + "\r\n" + "%X%X"%(first_selection[0],first_selection[1]) +"\r\n"+ str(len(RLUD_text)) +"\r\n"+ RLUD_text 

    else:
        selection_count = 2
        answer_text1 = str(selection_count) + "\r\n" + "%X%X"%(first_selection[0],first_selection[1])  +"\r\n"+ str(len(RLUD_text1)) +"\r\n"+RLUD_text1+"\r\n"
        answer_text2 = "%X%X"%(selection[0],selection[1]) +"\r\n"+ str(len(RLUD_text2)) + "\r\n"+ RLUD_text2
        answer_text = answer_text1+answer_text2

    return answer_text


def move(pi,pj,i,j,problem,selection_positon,answer_text,answer):

    purpose = answer[i][j]
    purpose_positon = search(problem,purpose)
    p_to_pp_dis = (pi - purpose_positon[0],pj - purpose_positon[1])
    s_to_p_dis = (purpose_positon[0] - selection_positon[0],purpose_positon[1] - selection_positon[1])
    print "目的ピース",purpose,"目的地",(pi,pj),"目的ピースポジション",purpose_positon,"目的ピースから目的地までの距離",p_to_pp_dis
    print "s_to_p","選択ピース位置",selection_positon,"選択ピースから目的ピースまでの距離",s_to_p_dis

    if p_to_pp_dis[0] == 0 and p_to_pp_dis[1] == 0:
        print "すでに目的地にいる"
        return  (problem,selection_positon,answer_text)

    left_edge = False
    right_edge = False
    under_edge = False
    exception = False
    right = False
    left = False
    loop = 0

    if purpose_positon[1] == 0 and purpose_positon[0] != len(problem) - 1:
        left_edge = True
        print "目的ピースは左端で目的ピースは左下角ではない"
        if p_to_pp_dis[1] == 0:
            print "真上に行きたい"
            if s_to_p_dis[0] == 0:
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
            
            if s_to_p_dis[0] > 0:
                print "選択ピースが目的ピースの上にある"
                for n in range(abs(s_to_p_dis[0]) + 1):
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
            if s_to_p_dis[0] < 0:
                print "選択ピースが目的ピースの下にある"
                for n in range(abs(s_to_p_dis[0]) - 1):
                    problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)                
            if p_to_pp_dis[0] != 0:
                print "testcase"
                for n in range(abs(s_to_p_dis[1])):
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[0])):
                problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
        else:
            if abs(s_to_p_dis[1] == 0):
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

            if abs(s_to_p_dis[1] == 0):
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)                
            else:
                for n in range(abs(s_to_p_dis[1])):
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

            for n in range(abs(p_to_pp_dis[1])-1):
                problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[0])):
                problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

    if purpose_positon[1] == len(problem) - 1 and purpose_positon[0] != len(problem) - 1:
        right_edge = True
        print "目的ピースは右端で、目的ピースが右下角ではない"

        if purpose_positon[0] == 0:
            print "目的ピースは右上角にある"
            
            if s_to_p_dis[1] == 0:
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            else:
                for n in range(abs(s_to_p_dis[1]) - 1 ):
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

            for n in range(abs(p_to_pp_dis[1])-1):
                problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)

        else:
            if p_to_pp_dis[1] != 0:
                loop = abs(s_to_p_dis[1])
                if s_to_p_dis[1] == 0:
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    loop += 1

                
                print "testcase"
                for n in range(abs(s_to_p_dis[1])-1):
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if s_to_p_dis[0] < 0:
                    for n in range(abs(s_to_p_dis[0])):
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                if s_to_p_dis[0] > 0:
                    for n in range(abs(s_to_p_dis[0])):
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                for n in range(abs(p_to_pp_dis[1])-1):
                    problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                for n in range(abs(p_to_pp_dis[0])):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)            
            else:
                for n in range(abs(s_to_p_dis[0])+1):
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                for n in range(abs(p_to_pp_dis[0])):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)            

    if purpose_positon[0] == len(problem) - 1:
        under_edge = True
        print "目的ピースは下端である"
        if p_to_pp_dis[1] == 0:
            print "目的地は真上"
            loop = abs(s_to_p_dis[0])

            if s_to_p_dis[0] == 0:
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                loop += 1
            if s_to_p_dis[1] > 0:
                for n in range(abs(s_to_p_dis[1])):
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            if s_to_p_dis[1] < 0:
                for n in range(abs(s_to_p_dis[1])):
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

            for n in range(loop):
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[0]) - 1):
                problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
        else:
            if purpose_positon[1] == 0 or purpose_positon[1] == len(problem[0])-1:
                print "目的ピースは角にあります"
                if s_to_p_dis[1] == 0:
                    if purpose_positon[1] == 0:
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    else: 
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        print "test"
                
                for n in range(abs(s_to_p_dis[0])):
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                if purpose_positon[1] == 0:
                    print "目的ピースは下左端"
                    if s_to_p_dis[1]  == 0:
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    else:
                        for n in range(abs(s_to_p_dis[1])):
                            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                    
                    
                    if abs(p_to_pp_dis[1] ) - 1 != 0:
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)                    
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)                    

                        for n in range(abs(p_to_pp_dis[1]) - 1):
                            problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)

                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                    
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)                    

                else:
                    print "目的ピースは下右端"
                    if s_to_p_dis[1] == 0:
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)              
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

                    else:
                        for n in range(abs(s_to_p_dis[1])):
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)              
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

                    if abs(p_to_pp_dis[1]) - 1 != 0:
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)

                        for n in range(abs(p_to_pp_dis[1])-1):
                            problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

                for n in range(abs(p_to_pp_dis[0]) - 1):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
            else:
                print "角ではない"

                if s_to_p_dis[1] == 0:
                    print "選択ピースと目的ピースのｘが一緒"
                    for n in range(abs(s_to_p_dis[0])):
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    if p_to_pp_dis[1] > 0:
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        for n in range(abs(p_to_pp_dis[1])):
                            problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

                    if p_to_pp_dis[1] < 0:
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        for n in range(abs(p_to_pp_dis[1])):
                            problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

                    for n in range(abs(p_to_pp_dis[0]) - 1):
                            problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

                else:
                    print "選択ピースと目的ピースのｘが一緒ではない"
                    loop = abs(s_to_p_dis[0])

                    if s_to_p_dis[0] == 0:
                            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                            loop += 1
                    if s_to_p_dis[1] < 0:#right
                        for n in range(abs(s_to_p_dis[1])):
                            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    if s_to_p_dis[1] > 0:#left
                        for n in range(abs(s_to_p_dis[1])):
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    
                    for n in range(loop):
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    
                    if p_to_pp_dis[1] != 0:
                        print "真上に目的地がない" 
                        if p_to_pp_dis[1] < 0:
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                            for n in range(abs(p_to_pp_dis[1])):
                                problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        if p_to_pp_dis[1] > 0:
                            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                            for n in range(abs(p_to_pp_dis[1])):
                                problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
                            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

                        for n in range(abs(p_to_pp_dis[0]) - 1):
                            problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
                    else:
                        print "真上に目的地がある" 
                        for n in range(abs(p_to_pp_dis[0])):
                            problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)


    #例外処理(同じ高さに選択と目的ピースが存在し、て行きたい方向が選択側だったとき)
    if selection_positon[0] == purpose_positon[0] and (s_to_p_dis[1] < 0 and p_to_pp_dis[1] > 0 or s_to_p_dis[1] > 0 and p_to_pp_dis[1] < 0) and left_edge == False and right_edge == False and under_edge == False:
        exception = True
        if s_to_p_dis[1] < 0 and p_to_pp_dis[1] > 0:#選択ピースが右にある かつ 目的ピースが右に行きたい
            print "選択ピースが右にある かつ 目的ピースは右に行きたい"
            for n in range(abs(s_to_p_dis[1])):
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[1]) - 1):
                problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
        if s_to_p_dis[1] > 0 and p_to_pp_dis[1] < 0:#選択ピースが左にある かつ 目的ピースが左に行きたい
            print "選択ピースが左にある かつ 目的ピースは左に行きたい"
            for n in range(abs(s_to_p_dis[1])):
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[1]) - 1):
                problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
        for n in range(abs(p_to_pp_dis[0])):
            problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
    if selection_positon[1] == purpose_positon[1] and s_to_p_dis[0] > 0 and p_to_pp_dis[0] < 0 and left_edge == False and right_edge == False and under_edge == False:
        print "選択ピースが上にある かつ 目的ピースは上に行きたい"
        exception = True
        if p_to_pp_dis[1] == 0:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

            for n in range(abs(s_to_p_dis[0])+1):
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

        if p_to_pp_dis[1] > 0:
            print "右に行きたい"
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[1])-1):
                problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

        if p_to_pp_dis[1] < 0:
            print "左に行きたい"
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[1])-1):
                problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

        for n in range(abs(p_to_pp_dis[0])):
            problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)


    if left_edge == False and right_edge == False and under_edge == False and exception == False:
        print "基本的にこれ 左・右・下端でなく、特殊条件でもない"
        loop = 0
        if s_to_p_dis[1] < 0:#right
            right = True
            print "選択ピースは目的ピースの右側にある"
            if p_to_pp_dis[1] > 0:#left
                print "目的ピースは右に行きたい"
                loop = abs(s_to_p_dis[1]) + 1
            if p_to_pp_dis[1] < 0:#right
                print "目的ピースは左に行きたい"
                loop = abs(s_to_p_dis[1]) - 1

            for n in range(loop):
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            #problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            #problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

        if s_to_p_dis[1] > 0:#left
            left = True
            print "選択ピースは目的ピースの左側にある"
            if p_to_pp_dis[1] > 0:
                print "目的ピースは右に行きたい"
                loop = abs(s_to_p_dis[1]) - 1
            if p_to_pp_dis[1] < 0:
                print "目的ピースは左に行きたい"
                loop = abs(s_to_p_dis[1]) + 1

            for n in range(loop):
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            #problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            #problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)


        if s_to_p_dis[0] == 0:
            print "同じ高さに選択ピースと目的ピースがある"
            if p_to_pp_dis[1] == 0:
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                for n in range(abs(s_to_p_dis[1])):
                    if right:
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    if left:
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                for n in range(abs(p_to_pp_dis[0])):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

            else:
                if right:
                    print "右にある"
                    #for n in range(abs(s_to_p_dis[1])-1):
                    #    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    for n in range(abs(p_to_pp_dis[1])):
                        problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                if left:
                    print "左にある"
                    #for n in range(abs(s_to_p_dis[1])-1):
                    #    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    for n in range(abs(p_to_pp_dis[1])):
                        problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)     
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                for n in range(abs(p_to_pp_dis[0])):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
        
        if s_to_p_dis[0] > 0:#up
            print "選択ピースは目的ピースの上側にある"
            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            
            if p_to_pp_dis[1] > 0:
                for n in range(abs(p_to_pp_dis[1])):
                    problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                
            if p_to_pp_dis[1] < 0:
                for n in range(abs(p_to_pp_dis[1])):
                    problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

            if p_to_pp_dis[1] == 0:
                print "真上に行きたい"
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                if left:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if right:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

            for n in range(abs(p_to_pp_dis[0])):
                problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)


        if s_to_p_dis[0] < 0:#down
            print "選択ピースは目的ピースの下側にある"
            if s_to_p_dis[1] == 0:
                print "同じ幅に選択ピースと目的ピースがある"

                if p_to_pp_dis[1] < 0:
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if p_to_pp_dis[1] > 0:
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            print "目的ピースの近くにきました"
            if p_to_pp_dis[1] < 0:#left
                print "目的ピースは左に行きたい"
                for n in range(abs(p_to_pp_dis[1])):
                    problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            if p_to_pp_dis[1] > 0:
                print "目的ピースは右に行きたい"
                for n in range(abs(p_to_pp_dis[1])):
                    problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

            if p_to_pp_dis[1] == 0:
                print "真上に行きたい"
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                if left:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if right:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

            print "目的ピースは上に行きたい"
            for n in range(abs(p_to_pp_dis[0])):
                problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

    return (problem,selection_positon,answer_text)



def solve(sortedImages, splitColumns, splitRows, limit, sel_rate, exc_rate):
    global LIMIT_SELECTION, SELECTON_RATE, EXCHANGE_RATE, distance_table,answer_text, ALL_COST
    LIMIT_SELECTION = limit
    SELECTON_RATE = sel_rate
    EXCHANGE_RATE = exc_rate
    problem = make_problem(splitColumns, splitRows)
    answer =  sortedImages

    answer_text = ""
    print "answer"
    print_matrix(answer)

    print "problem"
    print_matrix(problem)

    selection = answer[splitRows-1][splitColumns-1]
    selection_positon = search(problem,selection)

    print "selection\n",selection
    

    #for i in range(len(problem)):
    for i in range(len(problem)-2):
        #for j in range(len(problem[0])):
        for j in range(len(problem[0])-2):
            if answer[i][j] != problem[i][j]:
                problem,selection_positon,answer_text = move(i,j,i,j,problem,selection_positon,answer_text,answer)
            print_matrix(problem)
            print ""
        #ここから車庫入れ処理


        print "後ろ2つ ---------------------------------------------------------------"

        if selection_positon[0] == i:
            print "選択ピースの位置が悪い"
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

        print "answer"
        print_matrix(answer)
        if answer[i]  != problem[i]:
            problem,selection_positon,answer_text = move(i,len(problem)-2,i,len(problem)-1,problem,selection_positon,answer_text,answer)
            print "problem"
            print_matrix(problem)


            
            #例外処理
            print "後入れ-----------------------------------------------------------------"
            if problem[i][len(problem)-1] == answer[i][len(problem)-2] :#or problem[i+1][len(problem)-1] == answer[i][len(problem)-2]:
                if selection_positon[1] != len(problem[0])-2:
                    for n in range(len(problem)-2 - selection_positon[1]):
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

                print "めんどくさいパターン"
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

                if selection_positon[0] == i:
                    print "選択ピースの位置が悪い"
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

                problem,selection_positon,answer_text = move(i+1,len(problem)-2,i,len(problem)-2,problem,selection_positon,answer_text,answer)
                print "test"

                if (selection_positon[0] == i+1 and selection_positon[1] == len(problem) -3) or (selection_positon[0] == i+1 and selection_positon[1] == len(problem) -1) or (selection_positon[0] == i+2 and selection_positon[1] == len(problem) -2) :
                    if selection_positon[0] == i+1 and selection_positon[1] == len(problem) -3:
                        print "パターン1"
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    if selection_positon[0] == i+1 and selection_positon[1] == len(problem) -1:
                        print "パターン2"
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
                    if selection_positon[0] == i+2 and selection_positon[1] == len(problem) -2:            
                        print "パターン3"
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

                else:
                    print "OKKKKKKKKKKK"
                    if i + 1 == selection_positon[0]:
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    if selection_positon[1] < len(problem[0])-2:
                        for n in range(abs(selection_positon[1] - (len(problem[0])-2))):
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    if selection_positon[1] > len(problem[0])-2:
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    print "パターン3"
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)


        #purpose = answer[i][len(problem)-1]
        #purpose_positon = search(problem,purpose)
        #purpose_position = (i,len(problem)-2)
        print i+1,"行目終わり！！*******************************************************"
        print "answer"
        print_matrix(answer)
        print "problem"
        print_matrix(problem)
        check_matrix(answer,problem)
        print "*****************************************************************"
    
    #ラスト２段処理開始
    print "ラスト2段処理！！！！xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    for j in range(len(problem)-2):
        print "answer"
        print_matrix(answer)
        print "problem"
        print_matrix(problem)        
        i = len(problem)-2
        print "i = ",i,"j = ",j
        problem,selection_positon,answer_text = move(i,j,i+1,j,problem,selection_positon,answer_text,answer)

        print "problem"
        print_matrix(problem)
        print "selection",selection    
        print "selection_positon",selection_positon
        if selection_positon == (i+1,j):
            print "選択ピースの位置が面倒"
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
        else:#奇跡に等しい
            print "奇跡に等しい神配置"
            if abs(selection_positon[0] - i) == 1:
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            for n in range(abs(j+1 - selection_positon[1])):
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

        print "answer"
        print_matrix(answer)
        print "problem"
        print_matrix(problem)    
               
        if problem[i+1][j] == answer[i][j]:
            print "めんどくさいパターン2"
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

        else:
            problem,selection_positon,answer_text = move(i,j+1,i,j,problem,selection_positon,answer_text,answer)
            print "problem"
            print_matrix(problem)

            if abs(selection_positon[0] - i) == 0:
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            for n in range(abs(j - selection_positon[1])):
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
        print "車庫入れver2"
        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)


    print "answer"
    print_matrix(answer)    
    print "problem"
    print_matrix(problem)
    check_matrix(answer,problem)
    flg = False
    print "右下4マス処理================================================================================"
    

    i = len(problem)-1
    j = len(problem[0])-1
    count = 0
    selection_count = 1
    answer_text2 = ""

    if problem[i][j] == answer[i][j]:
        count += 1
    if problem[i][j-1] == answer[i][j-1]:
        count += 1
    if problem[i-1][j] == answer[i-1][j]:
        count += 1

    static_selection_positon = selection_positon
    
    #木の下のどれか

    if count == 0:
        print "counte = 3"
        if problem[i-1][j] == answer[i-1][j-1] and flg == False:
            print "test"

            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            selection_positon = (i-1 ,j-1)
            print selection_positon
            selection_count += 1
            static_selection_positon = selection_positon
            problem,selection_positon,answer_text2 = position_right(problem,selection_positon,answer_text2)
            flg = True
        
        if problem[i][j-1] == answer[i-1][j-1] and flg == False:
            print "test"
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            selection_positon = (i-1 ,j-1)
            selection_count += 1
            static_selection_positon = selection_positon

            problem,selection_positon,answer_text2 = position_down(problem,selection_positon,answer_text2)
            flg = True

        if problem[i][j]   == answer[i-1][j-1] and flg == False:
            print "test"
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            selection_positon = (i,j-1)
            selection_count += 1
            static_selection_positon = selection_positon
            problem,selection_positon,answer_text2 = position_up(problem,selection_positon,answer_text2)
            problem,selection_positon,answer_text2 = position_right(problem,selection_positon,answer_text2)
            flg = True

    if count == 1:
        print "count = 1"
        if problem[i][j-1] == answer[i][j-1] and flg == False:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            flg = True
        
        if  problem[i-1][j] == answer[i-1][j] and flg == False:
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            flg = True

    if count == 2:
        print "count = 2"
        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
        selection_positon = (i-1,j)
        selection_count += 1
        print selection_positon
        static_selection_positon = selection_positon
        problem,selection_positon,answer_text2 = position_left(problem,selection_positon,answer_text2)

    print "表示テスト"
    print "selection_positon",selection_positon
    print "\nlast board"
    print answer_text
    print_matrix(problem)
    print "交換回数",len(answer_text)
    check_matrix(answer,problem)
    print selection_positon

    #answer_text = encode_answer_format(answer_text,answer_text2,selection,answer)
    #print encode_answer_format(answer_text,answer_text2,static_selection_positon,answer)
    ALL_COST = selection_count*SELECTON_RATE + (len(answer_text)+len(answer_text2))*EXCHANGE_RATE
    

    return encode_answer_format(answer_text,answer_text2,static_selection_positon,answer)

#main       
sortedImages = [[(3, 2), (1, 3), (2, 1), (2, 2)], [(3, 0), (0, 3), (0, 2), (3, 3)], [(2, 3), (1, 1), (0, 0), (1, 0)], [(2, 0), (3, 1), (1, 2), (0, 1)]]

#print "sortedImages"

#sortedImages = make_answer(4,4)


#sortedImages = [[(0, 3), (2, 1), (1, 2), (0, 1)], [(1, 0), (1, 1), (3, 2), (1, 3)], [(3, 0), (3, 1), (2, 2), (2, 3)], [(2, 0), (0, 0), (0, 2), (3, 3)]]

#print sortedImages
#solve(sortedImages,4,4,10,1,1)

#main
master = "" 
if len(sys.argv) == 2:
  master = sys.argv[1]
else:
  master = config.master

para = communication.get_problem(master)
ans_str = solve(para['answer'], para['columns'], para['rows'], para['lim_select'], para['selection_rate'], para['exchange_rate'])
print ans_str
r = requests.post("http://%s:8000/" % master, data = {'answer' : ans_str , 'cost' : ALL_COST})
print r.text
