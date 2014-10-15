#-*- coding:utf-8 -*-
from heapq import heappush, heappop
from copy import deepcopy

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

def matrix_flg_substract(matrix):
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
def rotation(matrix):
    ans_matrix = []
    for i in reversed(xrange(len(matrix))):
        temp = []
        for j in reversed(xrange(len(matrix[0]))):
            temp.append(matrix[i][j])
        ans_matrix.append(temp)
    return ans_matrix 

def rotation_operations(LRUD_text):
    answer_text = ""
    for i in range(len(LRUD_text)):
        if LRUD_text[i] == "R":
            answer_text += "L"

        if LRUD_text[i] == "L":
            answer_text += "R"

        if LRUD_text[i] == "U":
            answer_text += "D"

        if LRUD_text[i] == "D":
            answer_text += "U"

    return answer_text         

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
        problem[purpose_positon[0]][purpose_positon[1]] =  (problem[purpose_positon[0]][purpose_positon[1]][0],problem[purpose_positon[0]][purpose_positon[1]][1],True)#目的ピースの固定
        problem,selection_positon,purpose_positon,answer_text = move_selection(pi,pj,problem,answer,purpose_positon,selection_positon,answer_text,table)
        problem[purpose_positon[0]][purpose_positon[1]] =  (problem[purpose_positon[0]][purpose_positon[1]][0],problem[purpose_positon[0]][purpose_positon[1]][1],False)#目的ピースの開放
    #print answer_text
    #print_matrix(problem)

    problem,selection_positon,answer_text = move_purpose(pi,pj,problem,purpose_positon,selection_positon,answer_text,table)
    problem[pi][pj] = (problem[pi][pj][0],problem[pi][pj][1],True )

    #print problem[i][j]

    #print_matrix(problem)
    #check_matrix(problem,answer,selection_positon)



    return problem,selection_positon,answer_text

def small_problem(i_max,j_max,problem,selection_positon,answer_text,answer):
	distance_table = create_distance_table(answer)
	problem = matrix_flg_add(problem)#一致マスのフラグをマトリックスに付与
	answer_text = ""
	#print "answer"
	#print_matrix(answer)

	#print "problem"
	#print_matrix(problem)
	#print selection,selection_positon

	#static_first_selection_positon = selection_positon
	#check_matrix(answer,problem,selection_positon)

	for i in range(i_max):
	    for j in range(j_max):
            
	        problem,selection_positon,answer_text = move(i,j,i,j,problem,answer,selection_positon,answer_text,distance_table)
	        #print answer_text
	        #print i,"行目",j,"番目","を整地＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝"

	    #print "後ろ2つ ---------------------------------------------------------------"

	    if answer[i]  != problem[i]:
	        #check_matrix(answer,problem,selection_positon)
	        problem,selection_positon,answer_text = move(i,len(problem[0])-2,i,len(problem[0])-1,problem,answer,selection_positon,answer_text,distance_table)
	        #例外処理
	        #print "後入れ-----------------------------------------------------------------"
	        if (problem[i][len(problem[0])-1][0] == answer[i][len(problem[0])-2][0] and problem[i][len(problem[0])-1][1] == answer[i][len(problem[0])-2][1]) :             
	            problem[i][len(problem[0])-2] = (problem[i][len(problem[0])-2][0],problem[i][len(problem[0])-2][1],False)
	            if selection_positon[1] != len(problem[0])-2:
	                if selection_positon[1] == len(problem[0])-1:
	                    problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
	                else:
	                    for n in range(len(problem[0])-2 - selection_positon[1]):
	                        problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
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
	            if ((selection_positon[0] == i and selection_positon[1] == len(problem[0])-1)and(problem[i+1][len(problem[0])-1][0] == answer[i][len(problem[0])-2][0] and problem[i+1][len(problem[0])-1][1] == answer[i][len(problem[0])-2][1])):
	                problem[i][len(problem[0])-2] = (problem[i][len(problem[0])-2][0],problem[i][len(problem[0])-2][1],False)  
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

	                problem,selection_positon,answer_text = move(i+1,len(problem[0])-2,i,len(problem[0])-2,problem,answer,selection_positon,answer_text,distance_table)
	                problem[i][len(problem[0])-2] = (problem[i][len(problem[0])-2][0],problem[i][len(problem[0])-2][1],False)
	                problem[i+1][len(problem[0])-2] = (problem[i+1][len(problem[0])-2][0],problem[i+1][len(problem[0])-2][1],False)


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
	                    if selection_positon[0] != i :
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
	    #print "problem"
	    #print problem
	    #check_matrix(answer,problem,selection_positon)

	    #print "後ろ二つを固定"
	    problem[i][len(problem[0])-2] = (problem[i][len(problem[0])-2][0],problem[i][len(problem[0])-2][1],True)
	    problem[i][len(problem[0])-1] = (problem[i][len(problem[0])-1][0],problem[i][len(problem[0])-1][1],True)
	    # i,"行目終わり！！*******************************************************"
	    #print "answer"
	    #print_matrix(answer)
	    #print "problem"
	    #print_matrix(problem)
	    #check_matrix(answer,problem,selection_positon)
	    #print "*****************************************************************"

	return matrix_flg_substract(problem),selection_positon,answer_text

def L_sprit(target_columns,target_rows,solve_problem,solve_answer,corner_text):
    if len(corner_text) != 2:
        print "L字にする四つ角を選択して、引数としてください（UL,DL,UR,DR）"
        return 0
    h = target_rows
    w = target_columns
    answer_text = ""
    if corner_text[0] == "U":#上側をソート
        problem = transpose(solve_problem)
        answer = transpose(solve_answer)

        if corner_text[1] == "R":
            selection = answer[len(answer)-1][0]
            selection_positon = search(problem,selection)
            first_selection_position = selection_positon
        if corner_text[1] == "L":
            selection = answer[len(answer)-1][len(answer[0])-1]
            selection_positon = search(problem,selection)
            first_selection_position = selection_positon

        ip_max = len(problem)-h
        jp_max = len(problem[0])-2
        problem,selection_positon,LRUD_text1 = small_problem(ip_max,jp_max,problem,selection_positon,answer_text,answer)  

        matrixB = []
        matrixB_answer = []
        for i in range(len(problem)):
            if i >=  len(problem)-h:
                matrixB.append(problem[i])
                matrixB_answer.append(answer[i])

    if corner_text[0] == "D":#下側をソート
        problem = rotation(transpose(solve_problem))
        answer =  rotation(transpose(solve_answer))

        if corner_text[1] == "R":
            selection = answer[len(answer)-1][len(answer[0])-1]
            selection_positon = search(problem,selection)

            selection = transpose(solve_answer)[0][0]
            first_selection_position = search(transpose(solve_problem),selection)
        if corner_text[1] == "L":
            selection = answer[len(answer)-1][0]
            selection_positon = search(problem,selection)

            selection = transpose(solve_answer)[0][len(transpose(solve_answer)[0])-1]
            first_selection_position = search(transpose(solve_problem),selection)


        ip_max = len(problem)-h
        jp_max = len(problem[0])-2
        problem,selection_positon,LRUD_text1 = small_problem(ip_max,jp_max,problem,selection_positon,answer_text,answer)  
        LRUD_text1 = rotation_operations(LRUD_text1)
        problem = rotation(problem)
        answer  = rotation(answer)

        matrixB = []
        matrixB_answer = []
        for i in range(len(problem)):
            if i < h:
                matrixB.append(problem[i])
                matrixB_answer.append(answer[i])
    #print "半分終わった---------------------------------------------------------------------------------------------------------------------------"
    answer_text = ""
    if corner_text[1] == "R":#右側をソート

        matrixB = transpose(rotation(matrixB))
        matrixB_answer = transpose(rotation(matrixB_answer))
        selection_positon = search(matrixB,selection)

        ib_max = len(matrixB)-w
        jb_max = len(matrixB[0])-2

        matrixB,selection_positon,LRUD_text2 = small_problem(ib_max,jb_max,matrixB,selection_positon,answer_text,matrixB_answer) 
        matrixB = rotation(transpose(matrixB))
        LRUD_text2 = rotation_operations(transpose_operations(LRUD_text2))
        count = 0
        if corner_text[0] == "U":
            for i in range(len(problem)):
                if i >=  len(problem)-h:
                    problem[i] = matrixB[count]
                    count += 1                     

        if corner_text[0] == "D":
            for i in range(len(problem)):
                if i < h:
                    problem[i] = matrixB[count]
                    count += 1        

    if corner_text[1] == "L":#左側をソート
        matrixB = transpose(matrixB)
        matrixB_answer = transpose(matrixB_answer)
        selection_positon = search(matrixB,selection)

        print selection_positon
        ib_max = len(matrixB)-w
        jb_max = len(matrixB[0])-2

        matrixB,selection_positon,LRUD_text2 = small_problem(ib_max,jb_max,matrixB,selection_positon,answer_text,matrixB_answer) 
        matrixB = transpose(matrixB)
        LRUD_text2 = transpose_operations(LRUD_text2)
        count = 0
        if corner_text[0] == "U":
            for i in range(len(problem)):
                if i >=  len(problem)-h:
                    problem[i] = matrixB[count]
                    count += 1     

        if corner_text[0] == "D":
            for i in range(len(problem)):
                if i < h:
                    problem[i] = matrixB[count]
                    count += 1  


    LRUD_text = LRUD_text1 + LRUD_text2

    answer_text = "%X%X"%(first_selection_position[1],first_selection_position[0]) +"\r\n"+ str(len(LRUD_text)) +"\r\n"+ LRUD_text 

    check_matrix(transpose(solve_answer),problem,selection_positon)
    problem = transpose(problem)


    #LRUD_text1 = rotation_operations(LRUD_text1)


    #LRUD_text2 = transpose_operations(LRUD_text2)


    return problem,answer_text

def corner_L_sprit(target_columns,target_rows,solve_problem,solve_answer):
    A_problem,A_answer_text = L_sprit(target_columns,target_rows,solve_problem,solve_answer,"UL")
    B_problem,B_answer_text = L_sprit(target_columns,target_rows,solve_problem,solve_answer,"UR")
    if len(A_answer_text) > len(B_answer_text):
        A_problem = B_problem
        A_answer_text = B_answer_text
    B_problem,B_answer_text = L_sprit(target_columns,target_rows,solve_problem,solve_answer,"DL")
    if len(A_answer_text) > len(B_answer_text):
        A_problem = B_problem
        A_answer_text = B_answer_text    
    B_problem,B_answer_text = L_sprit(target_columns,target_rows,solve_problem,solve_answer,"DR")
    if len(A_answer_text) > len(B_answer_text):
        A_problem = B_problem
        A_answer_text = B_answer_text
    return A_problem,A_answer_text  
