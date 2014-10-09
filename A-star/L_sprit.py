# -*- coding: utf-8 -*-

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
def move(pi,pj,i,j,problem,selection_positon,answer_text,answer):

    purpose = answer[i][j]
    purpose_positon = search(problem,purpose)
    p_to_pp_dis = (pi - purpose_positon[0],pj - purpose_positon[1])
    s_to_p_dis = (purpose_positon[0] - selection_positon[0],purpose_positon[1] - selection_positon[1])
    print "目的ピース",purpose,"目的地",(pi,pj),"目的ピースポジション",purpose_positon,"目的ピースから目的地までの距離",p_to_pp_dis
    print "s_to_p","選択ピース位置",selection_positon,"選択ピースから目的ピースまでの距離",s_to_p_dis
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
            #print ""
        #ここから車庫入れ処理
        #print "後ろ2つ ---------------------------------------------------------------"
        print selection_positon,i
        if selection_positon[0] == i:
            #print "選択ピースの位置が悪い"
            problem,selection_positon,answer_text = position_down(problem,selection_positon,answer_text)

        #print "answer"
        #print_matrix(answer)
        if answer[i]  != problem[i]:
            problem,selection_positon,answer_text = move(i,len(problem[0])-2,i,len(problem[0])-1,problem,selection_positon,answer_text,answer)
            #print "problem"
            #print_matrix(problem)
            
            #例外処理
            #print "後入れ-----------------------------------------------------------------"
            if problem[i][len(problem[0])-1] == answer[i][len(problem[0])-2] :#or problem[i+1][len(problem)-1] == answer[i][len(problem)-2]:
                if selection_positon[1] != len(problem[0])-2:
                    if selection_positon[1] == len(problem[0])-1:
                        problem,selection_positon,answer_text = position_left(problem,selection_positon,answer_text)
                    else:
                        for n in range(len(problem[0])-2 - selection_positon[1]):
                            problem,selection_positon,answer_text = position_right(problem,selection_positon,answer_text)
                if selection_positon[0] != i :
                    for n in range(i - selection_positon[0]):
                        problem,selection_positon,answer_text = position_up(problem,selection_positon,answer_text)

                #print "めんどくさいパターン"
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

        print i,"行目終わり！！*******************************************************"
        check_matrix(answer,problem,selection_positon)
        print "*****************************************************************"
    
    return problem,selection_positon,answer_text

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

        problem = rotation(problem)
        answer  = rotation(answer)
        LRUD_text1 = rotation_operations(LRUD_text1)

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
        LRUD_text2 = rotation_operations(transpose_operations(LRUD_text2))
        matrixB = rotation(transpose(matrixB))
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
        LRUD_text2 = transpose_operations(LRUD_text2)
        matrixB = transpose(matrixB)

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
    LRUD_text = loop_encode_text(LRUD_text)

    answer_text = "%X%X"%(first_selection_position[1],first_selection_position[0]) +"\r\n"+ str(len(LRUD_text)) +"\r\n"+ LRUD_text 

    check_matrix(transpose(solve_answer),problem,selection_positon)
    problem = transpose(problem)
    return problem,answer_text

    


