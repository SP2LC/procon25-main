# -*- coding: utf-8 -*-
from heapq import heappush, heappop
from copy import deepcopy,copy
import time

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


def L_exchange (board, selection_positon, exchange_positon):
    si,sj = selection_positon
    ei,ej = exchange_positon

    temp = board[si][sj]
    board[si][sj] = board[ei][ej]
    board[ei][ej] = temp

    return board
def check_matrix(matrix_A,matrix_B,selection_positon):
    ok_count = 0
    no_count = 0
    for i in range(len(matrix_A)):
        print ""
        for j in range(len(matrix_A[0])):
            if matrix_A[i][j] == matrix_B[i][j]: 
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

def position_up(board,selection_positon,answer_text):
    print "want to up",
    i,j = selection_positon
    new_board = L_exchange(board,(i,j),(i-1,j))
    new_answer_text = answer_text + "U"
    new_selection_position = (i-1,j)

    print "selection_positon U ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_down(board,selection_positon,answer_text):
    print "want to down",
    i,j = selection_positon
    new_board = L_exchange(board,(i,j),(i+1,j))
    new_answer_text = answer_text + "D"
    new_selection_position = (i+1,j)

    print "selection_positon D ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_right(board,selection_positon,answer_text):
    print "want to right",
    i,j = selection_positon
    new_board = L_exchange(board,(i,j),(i,j+1))
    new_answer_text = answer_text + "R"
    new_selection_position = (i,j+1)

    print "selection_positon R ",selection_positon," -> ",new_selection_position

    return new_board,new_selection_position,new_answer_text

def position_left(board,selection_positon,answer_text):
    print "want to left",
    i,j = selection_positon
    new_board = L_exchange(board,(i,j),(i,j-1))
    new_answer_text = answer_text + "L"
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

def transpose_operations(LRUD_text):
    answer_text = ""
    for i in range(len(LRUD_text)):
        if LRUD_text[i] == "R":
            answer_text += "D"
        if LRUD_text[i] == "L":
            answer_text += "U"
        if LRUD_text[i] == "U":
            answer_text += "L"
        if LRUD_text[i] == "D":
            answer_text += "R" 
    return answer_text

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

def small_problem(i_max,j_max,problem,selection_positon,answer_text,answer):

    for i in range(i_max):
        for j in range(j_max):
            if answer[i][j] != problem[i][j]:
                problem,selection_positon,answer_text = move(i,j,i,j,problem,selection_positon,answer_text,answer)
            #print_matrix(problem)
            print ""
        #ここから車庫入れ処理
        print "後ろ2つ ---------------------------------------------------------------"

        if selection_positon[0] == i:
            print "選択ピースの位置が悪い"
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

        #print "answer"
        #print_matrix(answer)
        if answer[i]  != problem[i]:
            problem,selection_positon,answer_text = move(i,len(problem[0])-2,i,len(problem[0])-1,problem,selection_positon,answer_text,answer)
            print "problem"
            #print_matrix(problem)
            
            #例外処理
            print "後入れ-----------------------------------------------------------------"
            if problem[i][len(problem[0])-1] == answer[i][len(problem[0])-2] :#or problem[i+1][len(problem)-1] == answer[i][len(problem)-2]:
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
                print "test"
                problem,selection_positon,answer_text = move(i+1,len(problem[0])-2,i,len(problem[0])-2,problem,selection_positon,answer_text,answer)
                print "test"

                if (selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -3) or (selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -1) or (selection_positon[0] == i+2 and selection_positon[1] == len(problem[0]) -2) :
                    if selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -3:
                        print "パターン1"
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)
                    if selection_positon[0] == i+1 and selection_positon[1] == len(problem[0]) -1:
                        print "パターン2"
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                        problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)                
                    if selection_positon[0] == i+2 and selection_positon[1] == len(problem[0]) -2:            
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

        #print i,"行目終わり！！*******************************************************"
        #print "answer"
        #print_matrix(answer)
        #print "problem"
        #print_matrix(problem)
        #check_matrix(answer,problem,selection_positon)
        #print "*****************************************************************"
    
    return problem,selection_positon,answer_text

def L_sprit(target_columns,target_rows,solve_problem,solve_answer):
    problem = transpose(solve_problem)
    answer =  transpose(solve_answer)
    h = target_rows
    w = target_columns

    selection = answer[len(answer)-1][len(answer[0])-1]
    selection_positon = search(problem,selection)
    first_selection_position = selection_positon
    
    #print "selection ",selection," selection_positon",selection_positon
    ip_max = len(problem)-w
    jp_max = len(problem[0])-2
    answer_text = ""
    problem,selection_positon,LRUD_text1 = small_problem(ip_max,jp_max,problem,selection_positon,answer_text,answer)  
    
    print "l字の左端をソート"    
    matrixB = []
    matrixB_answer = []
    for i in range(len(problem)):
        if i >= ip_max:
            matrixB.append(problem[i])            
            matrixB_answer.append(answer[i])

    check_matrix(answer,problem,selection_positon)
    
    matrixB = transpose(matrixB)
    matrixB_answer = transpose(matrixB_answer)
    selection_positon = search(matrixB,selection)
    ib_max = len(matrixB)-h
    jb_max = len(matrixB[0])-2
    answer_text = ""

    matrixB,selection_positon,LRUD_text2 = small_problem(ib_max,jb_max,matrixB,selection_positon,answer_text,matrixB_answer) 


    matrixB = transpose(matrixB)
    count = 0
    for i in range(len(problem)):
        if i >= len(problem)-h:
            problem[i] = matrixB[count]
            count += 1

    LRUD_text = LRUD_text1 + transpose_operations(LRUD_text2)
    LRUD_text = loop_encode_text(LRUD_text)
    answer_text = "%X%X"%(first_selection_position[1],first_selection_position[0]) +"\r\n"+ str(len(LRUD_text)) +"\r\n"+ LRUD_text 

    check_matrix(answer,problem,selection_positon)
    
    problem = transpose(problem)
    return problem,answer_text

def solve(sortedImages, splitColumns, splitRows, limit, sel_rate, exc_rate):
    global LIMIT_SELECTION, SELECTON_RATE, EXCHANGE_RATE, distance_table
    LIMIT_SELECTION = limit
    SELECTON_RATE = sel_rate
    EXCHANGE_RATE = exc_rate
    problem = make_problem(splitColumns, splitRows)
    answer =  sortedImages

    problem,L_answer_text = L_sprit(4,4,problem,answer)
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
                if h_star <= min_distance:
                     min_distance = h_star
                     print "%s distance=%d" % (operations_to_list(added_operation), h_star)
                     if int(h_star) == 0:
                       cost = -1000000000
                       print "stop!"
                if select:
                  new_selection_count = selection_count + 1
                else:
                  new_selection_count = selection_count
                if new_selection_count <= LIMIT_SELECTION:
                  heappush(queue, (f_star + cost + EXCHANGE_RATE, node, added_operation, new_selection_count))



    print "出なかった"
    return False

