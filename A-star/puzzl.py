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

def check_matrix(matrix_A,matrix_B,selection_positon):
    ok_count = 0
    no_count = 0
    for i in range(len(matrix_A)):
        #print ""
        for j in range(len(matrix_A[0])):
            if matrix_A[i][j] == matrix_B[i][j]: 
            #    print "OK ",
                ok_count += 1
            else:
            #    if selection_positon == (i,j):
            #        print "SL ",
            #    else:
            #        print "FF ",
                no_count += 1
    #print ""
    #print "  一致マス数",ok_count
    #print "不一致マス数",no_count 

    return ok_count,no_count

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

def encode_perfect_answer(LRUD_text):
    ans_LRUD = ""
    i = 0
    while (1):
        text = LRUD_text[i]+LRUD_text[i+1]
        if text == "LR" or text == "RL" or text == "UD" or text == "DU":
            i += 1
        else:
            ans_LRUD = ans_LRUD + LRUD_text[i]
        i+= 1
        if i > len(LRUD_text)-2:
            break
    ans_LRUD = ans_LRUD + LRUD_text[len(LRUD_text)-1]
    return ans_LRUD

def loop_encode_text(LRUD_text):
    while (1):
        old_text = LRUD_text
        LRUD_text = encode_perfect_answer(LRUD_text)
        if old_text == LRUD_text:
            return LRUD_text
def move(pi,pj,i,j,problem,selection_positon,answer_text,answer):

    purpose = answer[i][j]
    purpose_positon = search(problem,purpose)
    p_to_pp_dis = (pi - purpose_positon[0],pj - purpose_positon[1])
    s_to_p_dis = (purpose_positon[0] - selection_positon[0],purpose_positon[1] - selection_positon[1])
    #print "目的ピース",purpose,"目的地",(pi,pj),"目的ピースポジション",purpose_positon,"目的ピースから目的地までの距離",p_to_pp_dis
    #print "s_to_p","選択ピース位置",selection_positon,"選択ピースから目的ピースまでの距離",s_to_p_dis
    height = len(problem)-1
    width  = len(problem[0])-1 
    flg = False#目的ピースの位置判定で排他的になる用
    exception = False

    # すでに目的地に目的ピースがいる場合
    if p_to_pp_dis[0] == 0 and p_to_pp_dis[1] == 0:
        #print "すでに目的地にいる"
        return  (problem,selection_positon,answer_text)

    #目的ピースの位置判定
    if flg == False and purpose_positon[1] == 0 and purpose_positon[0] != height :#目的ピースが左端にあって左下角ではない
        flg = True
        if purpose_positon[0] == 0:#目的ピースが左上角にあったとき（このif文に入ることはない）
            print "入った！すごい！プログラムミスだ！"
        else :#目的ピースが左端にあったとき
            if p_to_pp_dis[1] == 0:#真上に行きたい(=目的ピースの下に回りこんで上に上げる)
                if s_to_p_dis[1] == 0:#目的ピースの真上（真下）に選択ピースがあったとき
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)              
                if s_to_p_dis[0] == 0:#選択ピースが目的ピースと同じ高さにあるときにあるとき
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
                if s_to_p_dis[0] > 0:#選択ピースが目的ピースの上側にある
                    for n in range(abs(s_to_p_dis[0]) + 1):
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
                if s_to_p_dis[0] < 0:#選択ピースが目的ピースの側下にある
                    for n in range(abs(s_to_p_dis[0]) - 1):
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)                
                if s_to_p_dis[1] == 0:#目的ピースの真上に選択ピースがあった時は右に一つ動かしたので左に一つ動かす
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)                
                else:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                for n in range(abs(p_to_pp_dis[0])):#目的ピースを上に動かす
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

            else:#真上以外に行きたいとき
                if s_to_p_dis[1] == 0:#目的ピースの真上（真下）に選択ピースがあったとき
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if s_to_p_dis[0] > 0:#選択ピースが目的ピースの上側にある
                    for n in range(abs(s_to_p_dis[0])):
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
                if s_to_p_dis[0] < 0:#選択ピースが目的ピースの側下にある
                    for n in range(abs(s_to_p_dis[0])):
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)    

                if s_to_p_dis[1] == 0:
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
            
    if flg == False and purpose_positon[1] == width and purpose_positon[0] != height :#目的ピースが右端にあって左角ではない
        flg = True
        if purpose_positon[0] == 0:#目的ピースが右上角にあったとき（このif文は入ると思う）     
            if s_to_p_dis[1] == 0:#目的ピースの真下に選択ピースがあったとき
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            else:
                for n in range(abs(s_to_p_dis[1]) - 1 ):
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            #ここまでで、目的ピースの左隣にくる
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[1])-1):
                problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
        else:#目的ピースが右端にあったとき
            loop = abs(s_to_p_dis[1])
            if s_to_p_dis[1] == 0:#選択ピースと目的ピースが同じ高さにある
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                loop += 1
            else:#揃ったピースを考慮するため
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
    
    if flg == False and purpose_positon[0] == height : #目的ピースが下端にある

        if p_to_pp_dis[1] == 0:#真上に行きたい(=目的ピースの下に回りこんで上に上げる)
            flg = True
            if s_to_p_dis[0] == 0:#目的ピースと選択ピースが同じ高さにあるとき
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            if s_to_p_dis[1] > 0:#目的ピースが選択ピースの右側にあるとき
                for n in range(abs(s_to_p_dis[1])):
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            if s_to_p_dis[1] < 0:#目的ピースが選択ピースの左側にあるとき
                for n in range(abs(s_to_p_dis[1])):
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            if s_to_p_dis[0] == 0:
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            else:   
                for n in range(abs(s_to_p_dis[0])):
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[0]) - 1):
                problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
        else:
            if purpose_positon[1] == 0:#目的ピースが左下角
                flg = True
                if s_to_p_dis[1] == 0:#目的ピースの上に選択ピースがある
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                for n in range(abs(s_to_p_dis[0])):
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                if s_to_p_dis[1]  == 0:
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                else:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

                if abs(p_to_pp_dis[1] ) - 1 != 0:#目的地が上じゃないとき
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)                    
                    problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)

                    for n in range(abs(p_to_pp_dis[1]) - 1):
                        problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                    
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

                for n in range(abs(p_to_pp_dis[0]) - 1):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

            if purpose_positon[1] == width:#目的ピースが右下角
                flg = True
                if s_to_p_dis[1] == 0:#目的ピースの上に選択ピースがある
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                for n in range(abs(s_to_p_dis[0])):
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                if s_to_p_dis[1]  == 0:
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                else:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

                if abs(p_to_pp_dis[1] ) - 1 != 0:#目的地が上じゃないとき
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)

                    for n in range(abs(p_to_pp_dis[1]) - 1):
                        problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                    
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

                for n in range(abs(p_to_pp_dis[0]) - 1):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)                    

            if flg == False:#普通に下端だったとき
                flg = True
                if s_to_p_dis[1] == 0:#目的ピースの真上に選択ピースがあったとき
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
                    loop = abs(s_to_p_dis[0])
                    if selection_positon[0] == pi and pi < height-1:
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                        loop -= 1 
                    if s_to_p_dis[0] == 0:#目的ピースと選択ピースが同じ高さにあるとき
                            problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                    if s_to_p_dis[1] < 0:#目的ピースが選択ピースの右側にあるとき
                        for n in range(abs(s_to_p_dis[1])):
                            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    if s_to_p_dis[1] > 0:#目的ピースが選択ピースの左側にあるとき
                        for n in range(abs(s_to_p_dis[1])):
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    if s_to_p_dis[0] == 0:
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    else:
                        for n in range(loop):
                            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    if p_to_pp_dis[1] < 0:#目的ピースが左側に行きたいとき
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        for n in range(abs(p_to_pp_dis[1])):
                            problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    if p_to_pp_dis[1] > 0:#目的ピースが右側に行きたいとき
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        for n in range(abs(p_to_pp_dis[1])):
                            problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    for n in range(abs(p_to_pp_dis[0]) - 1):#目的ピースを上に上げる
                        problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

    #例外処理
    if flg == False and s_to_p_dis[0] == 0 and ((s_to_p_dis[1] < 0 and p_to_pp_dis[1] > 0) or (s_to_p_dis[1] > 0 and p_to_pp_dis[1] < 0)):#選択ピースと目的ピースの行きたい方向がぶつかったとき
        flg = True
        if s_to_p_dis[1] < 0 and p_to_pp_dis[1] > 0:#選択ピースが右にある かつ 目的ピースが右に行きたい
            for n in range(abs(s_to_p_dis[1])):
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[1]) - 1):
                problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
        if s_to_p_dis[1] > 0 and p_to_pp_dis[1] < 0:#選択ピースが左にある かつ 目的ピースが左に行きたい
            for n in range(abs(s_to_p_dis[1])):
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[1]) - 1):
                problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
        for n in range(abs(p_to_pp_dis[0])):
            problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)  
    
    if flg == False and s_to_p_dis[1] == 0 and s_to_p_dis[0] > 0 and p_to_pp_dis[0] < 0: #縦にぶつかったとき
        flg = True
        if p_to_pp_dis[1] == 0:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(s_to_p_dis[0])+1):
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
        if p_to_pp_dis[1] > 0:#目的ピースは右に行きたい
            #print 
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            for n in range(abs(p_to_pp_dis[1])-1):
                problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

        if p_to_pp_dis[1] < 0:#目的ピースは左に行きたい
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
    
    if flg == False:#基本的にこれ 左・右・下端でなく、特殊条件でもない
        right = False
        left  = False
        loop = 0
        if selection_positon[0] == pi and s_to_p_dis[0] != 0:
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            exception = True

            if abs(s_to_p_dis[0]) - 1 == 0:
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                s_to_p_dis = (purpose_positon[0] - selection_positon[0],purpose_positon[1] - selection_positon[1])
        if s_to_p_dis[1] < 0:#選択ピースは目的ピースの右側にある
            right = True
            if p_to_pp_dis[1] > 0:#目的ピースは右に行きたい
                loop = abs(s_to_p_dis[1]) + 1
            if p_to_pp_dis[1] < 0:#目的ピースは左に行きたい
                loop = abs(s_to_p_dis[1]) - 1
            for n in range(loop):
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

        if s_to_p_dis[1] > 0:#選択ピースは目的ピースの左側にある
            left = True
            if p_to_pp_dis[1] > 0:#目的ピースは右に行きたい
                loop = abs(s_to_p_dis[1]) - 1
            if p_to_pp_dis[1] < 0:#目的ピースは左に行きたい
                loop = abs(s_to_p_dis[1]) + 1
            for n in range(loop):
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)

        if s_to_p_dis[0] == 0  :#同じ高さに選択ピースと目的ピースがある 
            if p_to_pp_dis[1] == 0:#目的地が真上だったとき
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                if right:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                if left:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                for n in range(abs(p_to_pp_dis[0])):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
            else:#目的地は真上ではない
                if right:#選択ピースは目的ピースの右側にある
                    for n in range(abs(p_to_pp_dis[1])):
                        problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                if left:#選択ピースは目的ピースの左側にある
                    for n in range(abs(p_to_pp_dis[1])):
                        problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)     
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                for n in range(abs(p_to_pp_dis[0])):
                    problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)
        
        if s_to_p_dis[0] > 0:#選択ピースは目的ピースの上側にある
            if exception == True:
                for n in range(abs(s_to_p_dis[0])-1):
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            else:
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

            if p_to_pp_dis[1] == 0:#真上に行きたい
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                if left:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if right:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)

            for n in range(abs(p_to_pp_dis[0])):
                problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

        if s_to_p_dis[0] < 0:#選択ピースは目的ピースの下側にある
            if s_to_p_dis[1] == 0:#同じ幅に選択ピースと目的ピースがある
                if p_to_pp_dis[1] < 0:
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if p_to_pp_dis[1] > 0:
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            for n in range(abs(s_to_p_dis[0])):
                problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
            if p_to_pp_dis[1] < 0:#目的ピースは左に行きたい
                for n in range(abs(p_to_pp_dis[1])):
                    problem,selection_positon,answer_text = purpose_position_left(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            if p_to_pp_dis[1] > 0:#目的ピースは右に行きたい
                for n in range(abs(p_to_pp_dis[1])):
                    problem,selection_positon,answer_text = purpose_position_right(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            if p_to_pp_dis[1] == 0:#真上に行きたい
                problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                if left:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if right:
                    for n in range(abs(s_to_p_dis[1])):
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
            #目的ピースは上に行きたい
            for n in range(abs(p_to_pp_dis[0])):
                problem,selection_positon,answer_text = purpose_position_up(problem,selection_positon,answer_text)

    return (problem,selection_positon,answer_text)

def solve(sortedImages, splitColumns, splitRows, limit, sel_rate, exc_rate):
    global LIMIT_SELECTION, SELECTON_RATE, EXCHANGE_RATE, distance_table,answer_text,ALL_COST
    LIMIT_SELECTION = limit
    SELECTON_RATE = sel_rate
    EXCHANGE_RATE = exc_rate
    problem = transpose(make_problem(splitColumns, splitRows))
    answer =  transpose(sortedImages)

    answer_text = ""
    #print "answer"
    #print_matrix(answer)

    #print "problem"
    #print_matrix(problem)

    selection = answer[len(answer)-1][len(answer[0])-1]
    selection_positon = search(problem,selection)

    static_first_selection_positon = selection_positon
    dummy,dummy= check_matrix(answer,problem,selection_positon)

    #print "selection\n",selection

    #for i in range(len(problem)):
    for i in range(len(problem)-2):
        #for j in range(len(problem[0])):
        for j in range(len(problem[0])-2):
            if answer[i][j] != problem[i][j]:
                problem,selection_positon,answer_text = move(i,j,i,j,problem,selection_positon,answer_text,answer)
            #print ""



            #dummy,dummy= check_matrix(answer,problem,selection_positon)
            #if i == 14 and j == 2:
            #    print "break"
            #    return answer_text

        #ここから車庫入れ処理


        #print "後ろ2つ ---------------------------------------------------------------"

        if selection_positon[0] == i:
            #print "選択ピースの位置が悪い"
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

        #print "answer"
        #print_matrix(answer)
        if answer[i]  != problem[i]:
            problem,selection_positon,answer_text = move(i,len(problem[0])-2,i,len(problem[0])-1,problem,selection_positon,answer_text,answer)
            #print "problem"
            #print_matrix(problem)

            dummy,dummy = check_matrix(answer,problem,selection_positon)
            
            #例外処理
            #print "後入れ-----------------------------------------------------------------"
            if problem[i][len(problem[0])-1] == answer[i][len(problem[0])-2] :#or problem[i+1][len(problem)-1] == answer[i][len(problem)-2]:
                if selection_positon[1] != len(problem[0])-2:
                    if selection_positon[1] == len(problem[0])-1:
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    else:
                        for n in range(len(problem[0])-2 - selection_positon[1]):
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if selection_positon[0] != i:
                    for n in range(i - selection_positon[0]):
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)

                dummy,dummy = check_matrix(answer,problem,selection_positon)
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
                    #print "選択ピースの位置が悪い"
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                #print "test"
                problem,selection_positon,answer_text = move(i+1,len(problem[0])-2,i,len(problem[0])-2,problem,selection_positon,answer_text,answer)
                #print "test"

                if (selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -3) or (selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -1) or (selection_positon[0] == i+2 and selection_positon[1] == len(problem[0]) -2) :
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

                else:
                    #print "OKKKKKKKKKKK"
                    if i + 1 == selection_positon[0]:
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    if selection_positon[1] < len(problem[0])-2:
                        for n in range(abs(selection_positon[1] - (len(problem[0])-2))):
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    if selection_positon[1] > len(problem[0])-2:
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    #print "パターン3"
                    problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)


        #print i,"行目終わり！！*******************************************************"
        #print "answer"
        #print_matrix(answer)
        #print "problem"
        #print_matrix(problem)
        #dummy,dummy = check_matrix(answer,problem,selection_positon)
        #print "*****************************************************************"
    
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
        problem,selection_positon,answer_text = move(i,j,i+1,j,problem,selection_positon,answer_text,answer)
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

        if problem[i+1][j] == answer[i][j]:
            #print "めんどくさいパターン2"
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
            problem,selection_positon,answer_text = move(i,j+1,i,j,problem,selection_positon,answer_text,answer)
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

    if problem[i][j] == answer[i][j]:
        count += 1
    if problem[i][j-1] == answer[i][j-1]:
        count += 1
    if problem[i-1][j] == answer[i-1][j]:
        count += 1

    static_selection_positon = (-1,-1)
    
    #木の下のどれか

    if count == 0:
        #print "counte = 3"
        if problem[i-1][j] == answer[i-1][j-1] and flg == False:
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            selection_positon = (i-1 ,j-1)
            #print selection_positon
            selection_count += 1
            static_selection_positon = selection_positon
            problem,selection_positon,answer_text2 = position_right(problem,selection_positon,answer_text2)
            flg = True
        
        if problem[i][j-1] == answer[i-1][j-1] and flg == False:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            selection_positon = (i-1 ,j-1)
            selection_count += 1
            static_selection_positon = selection_positon
            problem,selection_positon,answer_text2 = position_down(problem,selection_positon,answer_text2)
            flg = True

        if problem[i][j]   == answer[i-1][j-1] and flg == False:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            selection_positon = (i,j-1)
            selection_count += 1
            static_selection_positon = selection_positon
            problem,selection_positon,answer_text2 = position_up(problem,selection_positon,answer_text2)
            problem,selection_positon,answer_text2 = position_right(problem,selection_positon,answer_text2)
            flg = True

    if count == 1:
        if problem[i][j-1] == answer[i][j-1] and flg == False:
            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
            flg = True
        
        if  problem[i-1][j] == answer[i-1][j] and flg == False:
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

    print "表示テスト"
    print "selection_positon",selection_positon
    print "\nlast board"
    print_matrix(problem)
    print "交換回数",len(answer_text)
    dummy,no_count = check_matrix(answer,problem,selection_positon)
    #print answer_text
    answer_text = loop_encode_text(answer_text)
    ALL_COST = selection_count*SELECTON_RATE + (len(answer_text)+len(answer_text2))*EXCHANGE_RATE

    encode_text =  encode_answer_format(answer_text,answer_text2,static_selection_positon,static_first_selection_positon)
    #print answer_text
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
