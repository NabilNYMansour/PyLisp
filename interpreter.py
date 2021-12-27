class Expression:
    def __init__(self, h, t):
        self.h = h
        self.t = t

    def __str__(self):
        return "(" + str(self.h) + " . " + str(self.t) + ")"


def atom(expression):
    return not type(expression).__name__ == "Expression"


def car(expression):
    return expression.h


def cdr(expression):
    return expression.t


def cons(h, t):
    return Expression(h, t)


def eq(exp1, exp2):
    return atom(exp1) and atom(exp2) and exp1 == exp2


def List(l):
    for element in l:
        return Expression(element, List(l[1:]))
    return "NIL"


def ff(exp):
    if (atom(exp)):
        return exp
    else:
        return ff(car(exp))


def subst(exp1, exp2, exp3):
    if (atom(exp3)):
        if (eq(exp2, exp3)):
            return exp1
        else:
            return exp3
    else:
        return cons(subst(exp1, exp2, car(exp3)), subst(exp1, exp2, cdr(exp3)))


def equal(exp1, exp2):
    return (atom(exp1) and atom(exp2) and eq(exp1, exp2)) or (not atom(exp1) and not atom(exp2) and equal(car(exp1), car(exp2)) and equal(cdr(exp1), cdr(exp2)))


def null(exp):
    return atom(exp) and eq(exp, "NIL")


def append(exp1, exp2):
    if null(exp1):
        return exp2
    else:
        return cons(car(exp1), append(cdr(exp1), exp2))


def among(exp1, exp2):
    return not null(exp2)


def pair(exp1, exp2):
    if (null(exp1) and null(exp2)):
        return "NIL"
    elif (not atom(exp1) and not atom(exp2)):
        return cons(List([car(exp1), car(exp2)]), pair(cdr(exp1), cdr(exp2)))


def assoc(exp1, exp2):
    if null(exp2):
        return "NIL"
    elif eq(car(car(exp2)), exp1):
        return cdr(car(exp2))
    else:
        return assoc(exp1, cdr(exp2))


def assocReplace(exp1, val, exp2):
    if null(exp2):
        return "NIL"
    elif eq(car(car(exp2)), exp1):
        exp2.h.t = val
        return "T"
    else:
        return assocReplace(exp1, val, cdr(exp2))


def put(x, y, a):
    result = assoc(x, a)
    if null(result):
        if null(a):
            return List([cons(x, y)])
        else:
            if null(cdr(a)):
                return List([car(a), cons(x, y)])
            else:
                return cons(car(a), put(x, y, cdr(a)))
    else:
        assocReplace(x, y, a)
        return a


def remove(x, y):
    if null(y):
        return "NIL"
    else:
        if equal(x, car(y)):
            return remove(x, cdr(y))
        else:
            return cons(car(y), remove(x, cdr(y)))

def removeAll(x, y):
    if null(x):
        return y
    else:
        # removeAll(cdr(x), y)
        # return remove(car(x), y)
        return removeAll(cdr(x), remove(car(x), y))


g = "NIL"


def eval(e):
    global g
    if atom(e):
        result = assoc(e, g)
        if null(result):
            return e
        else:
            return result
    elif atom(car(e)):
        if eq(car(e), "QUOTE"):
            return car(cdr(e))
        if eq(car(e), "ATOM"):
            return atom(eval(car(cdr(e))))
        elif eq(car(e), "EQ"):
            if eval(car(cdr(e))) == eval(car(cdr(cdr(e)))):
                return "T"
            else:
                return "NIL"
        elif eq(car(e), "CAR"):
            return car(eval(car(cdr(e))))
        elif eq(car(e), "CDR"):
            return cdr(eval(car(cdr(e))))
        elif eq(car(e), "CONS"):
            return cons(eval(car(cdr(e))), eval(car(cdr(cdr(e)))))
        elif eq(car(e), "ASSOC"):
            return assoc(eval(car(cdr(e))), eval(car(cdr(cdr(e)))))
        elif eq(car(e), "SET"):
            g = put(eval(List(["QUOTE", car(cdr(e))])),
                    eval(car(cdr(cdr(e)))), g)
            # print("Debug", g)
            return "T"
        elif eq(car(e), "+"):
            return int(eval(car(cdr(e)))) + int(eval(car(cdr(cdr(e)))))
        elif eq(car(e), "-"):
            return int(eval(car(cdr(e)))) + int(eval(car(cdr(cdr(e)))))
        elif eq(car(e), "*"):
            return int(eval(car(cdr(e)))) * int(eval(car(cdr(cdr(e)))))
        elif eq(car(e), "/"):
            return int(eval(car(cdr(e)))) / int(eval(car(cdr(cdr(e)))))
        elif eq(car(e), "LIST"):
            return cdr(e)
        elif eq(car(e), "APPEND"):
            return append(eval(car(cdr(e))), eval(car(cdr(cdr(e)))))
    return e


def interpreteBlock(code):
    l = code.upper().split(" ")
    if len(l) == 1:
        return eval(l[0])
    else:
        l = []
        funcall = ""
        foundFuncall = False
        index = 0
        for char in code[1:len(code)-1]:
            if (char == " "):
                foundFuncall = True
            if not foundFuncall:
                funcall += char
            else:
                l.append(code[1:index+1])
                l.append(code[index+2:len(code)-1])
                break
            index += 1
        blocks = interpreteBlocks(l[1], False)
        l = [l[0]]
        if (l[0] == "LET"):
            global g
            oldG = g
            g = append(interpreteBlock(blocks[0]), g)
            result = eval(interpreteBlock(blocks[1]))
            g = oldG
            return result
        else:
            for block in blocks:
                l.append(interpreteBlock(block))
            return eval(List(l))


def interpreteBlocks(code, toEvalBlocks):
    l = code.upper().split(" ")
    foundBlock = 0
    openBracket = 0
    closeBracket = 0
    index = 0
    hasFound = False
    blocks = []
    for element in l:
        # if (element[0] == "(" and element[-1] ==")"):
        #     blocks.append(element)
        if (element[0] == "("):
            foundBlock += 1
            if not hasFound:
                openBracket = index
            hasFound = True
        elif (element[-1] == ")"):
            for char in element:
                if char == ")":
                    foundBlock -= 1
            closeBracket = index
        elif (not hasFound):
            blocks.append(element)
        if foundBlock == 0 and hasFound:
            hasFound = False
            blocks.append(" ".join(l[openBracket:closeBracket+1]))
        index += 1
    if toEvalBlocks:
        for block in blocks[:len(blocks)-1]:
            # print("Interpreter Debug", interpreteBlock(block))
            interpreteBlock(block)
        return interpreteBlock(blocks[-1])
    else:
        return blocks


# print(interpreteBlocks("(let (list (cons a 2) (cons b 3)) (+ a b))", True))
# print(interpreteBlocks("(lambda (+ 1 2))", True))

inp = ""
while True:
    print("PyLisp> ", end="")
    inp = input()
    # debug stuff
    if inp == "quit":
        break
    elif inp == "pvars":
        print(g)
    elif len(inp) > 5 and inp[0:5] == "load ":
        f = open(inp[5:], "r")
        print(interpreteBlocks(f.read().replace("\n", " ").replace("\t", " "), True))
        f.close()
    else:
        print(interpreteBlocks(inp, True))
