import sys

# Character classes
LETTER = 0
DIGIT = 1
UNKNOWN = 99

# token codes
reserved_word = 10 # 예약어  call, variable, print_ari
ident = 11  # 식별자 -> 영문자, 숫자, 밑줄(_)로 구성됨...첫 문자로 숫자가 나올 수 없음!
semi_colon = 12  # ;
comma = 13  # ,
left_paren = 14  # {
right_paren = 15  # }
func_name = 16 # ident 중에서 함수명인지
eof = 28  # $

# global declarations
charClass = 0  # char가 digit/letter인지 판별
token_string = ""  # lexeme 저장
tokenized_text = [] # 토큰화한 것 저장
token_index = 0  # input string의 인덱스
nextChar = ""  # 다음 문자받는 변수
next_token = 0  # token type 저장

# error declarations
syntax_error = False
syntax_error_msg = "Syntax Error.\n"
syntax_ok_msg = "Syntax O.K.\n"

# for getting inputs from txt file
f = open("sample.txt", 'r')  # txt파일 이름을 argv[1]로 인자로 받기 open(sys.argv[1], 'r')로 바꿔주기!!

txt = f.readlines()
input = ""
for statement in txt:
    input += statement.strip()
input += "$"

# functions for grammar
def start(): # <start> -> <functions>
    #print("start checking grammar")
    getChar()
    lexical()
    functions()
    if syntax_error == False:
        print(syntax_ok_msg)
    else: print(syntax_error_msg)
def functions(): # <functions> -> <function> | <function> <functions>
    function()
    if next_token != eof:
        lexical()
        functions()
    else:
        pass
def function(): # <function> -> <identifier> { <function_body> }
    global syntax_error, tokenized_text
    if next_token == ident:
        lexical()
        if next_token == left_paren:
            lexical()
            function_body()
            if next_token == right_paren:
                lexical()
            else :
                syntax_error = True
                print("오른쪽 괄호가 없음 function()")

def function_body(): # <function_body> -> <var_definitions> <statements> | <statements>
    if next_token == reserved_word and token_string == "variable":
        var_definitions()
        lexical()
        statements()
    else:
        lexical()
        statements()

def var_definitions(): # <var_definitions> -> <var_definition> | <var_definition> <var_definitions>
    var_definition()
    lexical()
    if next_token == reserved_word and token_string == "variable":
        var_definitions()
    else:
        pass

def var_definition(): # <var_definition> -> variable <var_list> ;
    global syntax_error
    if next_token == reserved_word and token_string == "variable":
        lexical()
        var_list()
        if next_token == semi_colon:
            pass
        else:
            syntax_error = True
            print("var_definition() 세미콜론 없음")
    else:
        syntax_error = True
        print("var_definition() variable로 시작 안함")
def var_list(): # <var_list> -> <identifier> | <identifier>, <var_list>
    if next_token == ident:
        lexical()
        if next_token == comma:
            lexical()
            var_list()
        else:
            pass
def statements(): # <statements> -> <statement> | <statement> <statements>
    statement()
    if next_token != right_paren:
        lexical()
        statements()
    else:
        pass

def statement(): # <statement> -> call <identifier>; | print_ari; | <identifier> ;
    global syntax_error
    if next_token == reserved_word and token_string == "call":
        lexical()
        if next_token == ident:
            lexical()
            if next_token == semi_colon:
                pass
            else:
                syntax_error =True
                print("statement() call ident 뒤에 세미콜론 없음")
        else:
            syntax_error = True
            print("staement() call 뒤에 ident 없음")
    elif next_token == reserved_word and token_string == "print_ari":
        lexical()
        if next_token == semi_colon:
            pass
        else:
            syntax_error = True
            print("statement() print_ari뒤에 세미콜론 없음")
    elif next_token == ident:
        lexical()
        if next_token == semi_colon:
            pass
        else:
            syntax_error = True
            print("statement() ident 뒤에 세미콜론 없음")
    else:
        pass

# functions for lexical()
def lookup(ch):
    global next_token, token_string
    if ch == '{':
        addChar()
        next_token = left_paren
        #print(token_string)
        tokenized_text.append([token_string, next_token])
    elif ch == '}':
        addChar()
        next_token = right_paren
        #print(token_string)
        tokenized_text.append([token_string, next_token])
    elif ch == ',':
        addChar()
        next_token = comma
        #print(token_string)
        tokenized_text.append([token_string, next_token])
    elif ch == ';':
        addChar()
        next_token = semi_colon
        #print(token_string)
        tokenized_text.append([token_string, next_token])
    elif ch == '$':
        addChar()
        next_token = eof
        tokenized_text.append([token_string, next_token])

def addChar():
    global token_string, nextChar
    token_string += nextChar

def getChar():
    global nextChar, token_index, charClass
    nextChar = input[token_index]
    token_index += 1

    if nextChar != '$':
        if nextChar.isalpha() or nextChar == '_':  # c identifier rule에서 ident은 영문자, 밑줄문자(_), 숫자(0~9)를 가질 수 있으므로
            charClass = LETTER  # 영문자와 밑줄문자를 letter로 인식하도록 했다.
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = eof


def getNonBlank():
    while nextChar.isspace():
        getChar()


def lexical():
    global charClass, next_token, token_string
    token_string = ""
    getNonBlank()

    if charClass == LETTER:  # ident의 시작은 숫자로 할 수는 없으므로 처음에는 영문자나 밑줄(_)이어야 한다.
        addChar()
        getChar()
        while charClass == LETTER or charClass == DIGIT:
            addChar()
            getChar()
        if token_string == "call":
            next_token = reserved_word
            #print(token_string)
            tokenized_text.append([token_string,next_token])
        elif token_string == "print_ari":
            next_token = reserved_word
            #print(token_string)
            tokenized_text.append([token_string,next_token])
        elif token_string == "variable":
            next_token = reserved_word
            #print(token_string)
            tokenized_text.append([token_string,next_token])
        else:
            next_token = ident
            #print(token_string)
            tokenized_text.append([token_string,next_token])
    elif charClass == UNKNOWN:
        lookup(nextChar)
        getChar()
    elif charClass == eof:
        next_token = eof
        tokenized_text.append([token_string, next_token])

    # 입력한 파일에 대한 파싱 결과 출력 부분
    if next_token == eof:
        pass


# ========파싱 시작 및 문법 확인========
start()

# ===========프로그램 실행=============
activation_record_instance = {}
ari = [] # 진짜 ari
main_list = []
func_list = [0,0]
dynamic_link = ["main",]
function_line = 0
function_idx = [] # tokenized_text에서 function들 있는 위치 기억하는 곳
function_name = [] # tokenized_text에서 정의된 함수명 저장
ep = 0
main = False

if not syntax_error:
    # 함수 위치 알아내기
    for i in range(len(tokenized_text)):
        if tokenized_text[i][0] == '{':
            function_name.append(tokenized_text[i-1][0])
            function_idx.append(i-1)

    # main 함수가 정의되지 않은 경우 오류 메세지 출력후 종료
    if 'main' in function_name:
        main = True
    else:
        print("“No starting function.”")

    # 샘플 ari 만들어주기
    for i in range(len(tokenized_text)):
        if tokenized_text[i][0] == '{':
            j = i
            while 1:
                if tokenized_text[j+1][0] == '}':
                    break

                j += 1
                if tokenized_text[j][0] == "variable":
                    while 1:
                        j += 1
                        if tokenized_text[j][0] != ';':
                            if tokenized_text[j][1] == 11:
                                if tokenized_text[i-1][0] == "main":
                                    main_list.append(tokenized_text[j][0])
                                else:
                                    func_list.append(tokenized_text[j][0])
                        else:
                            break

            if tokenized_text[i-1][0] == "main":
                activation_record_instance[tokenized_text[i-1][0]]=main_list
                main_list = []
            else :
                activation_record_instance[tokenized_text[i-1][0]]=func_list
                func_list = [0, 0]
            i = j

    # main함수 있는 경우 프로그램 실행!
    if main:
        caller_func=''
        ari.append(['main', activation_record_instance['main']])
        i = function_idx[function_name.index('main')]
        i += 1 # '{'
        while 1:
            i += 1
            if tokenized_text[i][0] == '}': # main 끝나면 종료
                break
            elif tokenized_text[i][0] == 'variable':
                function_line -= 1
            elif tokenized_text[i][0] == ';':
                function_line += 1
            elif tokenized_text[i][0] == "print_ari":  # print_ari 나오면 ari 출력해주기
                print("hi ari~", ari)
            elif (tokenized_text[i - 1][0] == '{' and tokenized_text[i][1] == 11) or (
                    tokenized_text[i - 1][0] == ';' and tokenized_text[i][1] == 11):
                link_count = 0
                local_offset = 0
                found = False
                sample_idx = function_name.index('main') + 1

                while 1:
                    if sample_idx < 0:
                        break
                    while 1:
                        if ari[sample_idx][1][local_offset] == tokenized_text[i][0]:
                            found = True
                            break
                        else:
                            local_offset += 1
                            if local_offset >= len(ari[sample_idx][1]):
                                local_offset = 0
                                break
                    if found:
                        sample_string = "main" + ":" + str(tokenized_text[i][0]) + " => " + str(
                            link_count) + ", " + str(local_offset) +"\n"
                        print(sample_string)
                        link_count = 0
                        local_offset = 0
                        break
                    link_count += 1
                    sample_idx -= 1
                    local_offset = 0
            elif tokenized_text[i][0] == 'call':
                func_list = activation_record_instance[tokenized_text[i+1][0]]
                func_list[0] = ['main', function_line + 1]
                func_list[1] = ep
                ep += 2
                ari.append([tokenized_text[i+1][0], func_list])
                func = tokenized_text[i+1][0]
                caller_func = func
                dynamic_link.append(func)

                # 메인에서 호출한 first 함수로 넘어감
                j = function_idx[function_name.index(func)]
                j += 1 # '{'
                while 1:
                    j += 1
                    function_line1 = 0
                    if tokenized_text[j][0] == '}':  # first sub function 끝나면 종료
                        ari.pop()
                        #print("after finishing first and pop first ", ari)
                        break
                    elif tokenized_text[j][0] == 'variable':
                        function_line1 -= 1
                    elif tokenized_text[j][0] == ';':
                        function_line1 += 1
                    elif tokenized_text[j][0] == "print_ari":  # print_ari 나오면 ari 출력해주기
                        print("hi ari~", ari)
                    elif (tokenized_text[j - 1][0] == '{' and tokenized_text[j][1] == 11) or (
                            tokenized_text[j - 1][0] == ';' and tokenized_text[j][1] == 11):
                        link_count = 0
                        local_offset = 0
                        found = False
                        sample_idx = function_name.index(caller_func) + 1

                        while 1:
                            if sample_idx < 0:
                                break
                            while 1:
                                if ari[sample_idx][1][local_offset] == tokenized_text[j][0]:
                                    found = True
                                    break
                                else:
                                    local_offset += 1
                                    if local_offset >= len(ari[sample_idx][1]):
                                        local_offset = 0
                                        break
                            if found:
                                sample_string = caller_func+":"+str(tokenized_text[j][0])+" => "+str(link_count)+", "+str(local_offset) +"\n"
                                print(sample_string)
                                link_count = 0
                                local_offset = 0
                                break
                            link_count += 1
                            sample_idx -= 1
                            local_offset = 0
                    elif tokenized_text[j][0] == 'call':
                        func_list = activation_record_instance[tokenized_text[j + 1][0]]
                        func_list[0] = [caller_func, function_line1 + 1]
                        func_list[1] = ep
                        ep += len(func_list)
                        ari.append([tokenized_text[j + 1][0], func_list])
                        func = tokenized_text[j + 1][0]
                        dynamic_link.append(func)

                        # first에서 호출한 second 함수로 넘어감
                        k = function_idx[function_name.index(func)]
                        k += 1 # '{'
                        caller_func = func
                        while 1:
                            k += 1
                            function_line2 = 0
                            if tokenized_text[k][0] == '}': # second sub function 끝나면 종료
                                dynamic_link.pop()
                                caller_func = dynamic_link.pop()
                                ari.pop()
                                #print("after finishing second and pop second ", ari)
                                break
                            elif tokenized_text[k][0] == "print_ari":  # print_ari 나오면 ari 출력해주기
                                #print("hi ari!~", ari)
                                for ari_idx in range(len(ari)-1,-1,-1):
                                    for stack_idx in range(len(ari[ari_idx][1])-1,-1,-1):
                                        if ari[ari_idx][0] == 'main':
                                            if stack_idx == len(ari[ari_idx][1])-1:
                                                local_string = str(ari[ari_idx][0])+":Local variable: "+str(ari[ari_idx][1][stack_idx])
                                                print(local_string)
                                            else:
                                                local_string = "Local variable: "+str(ari[ari_idx][1][stack_idx])
                                                print(local_string)
                                        else:
                                            if stack_idx == len(ari[ari_idx][1])-1:
                                                local_string = str(ari[ari_idx][0])+":Local variable: "+str(ari[ari_idx][1][stack_idx])
                                                print(local_string)
                                            elif stack_idx == 0: # ret
                                                ret_string = "Return Address: "+str(ari[ari_idx][1][stack_idx][0])+":"+str(ari[ari_idx][1][stack_idx][1])+"\n"
                                                print(ret_string)
                                            elif stack_idx == 1: # dynamic link
                                                dynamic_string = "Dynamic Link: "+str(ari[ari_idx][1][stack_idx])
                                                print(dynamic_string)
                                            else:
                                                local_string = "Local variable: "+str(ari[ari_idx][1][stack_idx])
                                                print(local_string)

                                    if ari[ari_idx][0] == 'main':
                                        print("\n")



                            elif (tokenized_text[k-1][0] == '{' and tokenized_text[k][1] == 11) or (tokenized_text[k-1][0] == ';' and tokenized_text[k][1] == 11):
                                link_count = 0
                                local_offset = 0
                                found = False
                                sample_idx = function_name.index(caller_func)+1

                                while 1:
                                    if sample_idx < 0:
                                        break
                                    while 1:
                                        if ari[sample_idx][1][local_offset] == tokenized_text[k][0]:
                                            found = True
                                            break
                                        else:
                                            local_offset += 1
                                            if local_offset >= len(ari[sample_idx][1]):
                                                local_offset = 0
                                                break
                                    if found:
                                        sample_string = caller_func + ":" + str(tokenized_text[k][0]) + " => " + str(
                                            link_count) + ", " + str(local_offset)+"\n"
                                        print(sample_string)
                                        link_count = 0
                                        local_offset = 0
                                        break
                                    link_count += 1
                                    sample_idx -= 1
                                    local_offset = 0

                                func_list = [0,0]
                                k += 1

                        func_list = [0,0]
                        j += 1
                func_list = [0,0]
                i += 1


    #print("ari ", ari)

    # ari에 dynamic link 넣어주기, ep 넣어주기...호출한 함수의 가장 밑의 주소
    #for

    # ari에 return address 넣어주기, 함수명: 실행문 위치

#print(tokenized_text)
#print(activation_record_instance)
#print(function_idx)
#print(function_name)

'''
for i in tokenized_text:
    print(i[0])
'''
