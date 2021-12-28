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


def among(x, y):
    return not null(y) and (equal(x, car(y)) or among(x, cdr(y)))


def pair(exp1, exp2):
    if (null(exp1) and null(exp2)):
        return "NIL"
    elif (not atom(exp1) and not atom(exp2)):
        return cons(cons(car(exp1), car(exp2)), pair(cdr(exp1), cdr(exp2)))


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
        return exp2
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


def hasItem(x, y):
    if atom(y):
        return False
    else:
        return x == car(car(y)) or hasItem(x, cdr(y))


g = "NIL"
gf = "NIL"


def eval(e):
    global g
    global gf
    if atom(e):
        result = assoc(e, g)
        if null(result) and not hasItem(e, g):
            return e
        else:
            return result
    elif atom(car(e)):
        if eq(car(e), "QUOTE"):
            return car(cdr(e))
        if eq(car(e), "ATOM"):
            return atom(eval(car(cdr(e))))
        elif eq(car(e), "EQ"):
            if str(eval(car(cdr(e)))) == str(eval(car(cdr(cdr(e))))):
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
        # elif eq(car(e), "SET"):
        #     g = put(eval(List(["QUOTE", car(cdr(e))])),
        #             eval(car(cdr(cdr(e)))), g)
        #     return "T"
        elif eq(car(e), "+"):
            return float(eval(car(cdr(e)))) + float(eval(car(cdr(cdr(e)))))
        elif eq(car(e), "-"):
            return float(eval(car(cdr(e)))) - float(eval(car(cdr(cdr(e)))))
        elif eq(car(e), "*"):
            return float(eval(car(cdr(e)))) * float(eval(car(cdr(cdr(e)))))
        elif eq(car(e), "/"):
            return float(eval(car(cdr(e)))) / float(eval(car(cdr(cdr(e)))))
        elif eq(car(e), "LIST"):
            return cdr(e)
        elif eq(car(e), "APPEND"):
            return append(eval(car(cdr(e))), eval(car(cdr(cdr(e)))))
        elif eq(car(e), "PRINT"):
            print(car(cdr(e)))
            return "T"
        # elif eq(car(e), "IF"):
        #     if not null(eval(car(cdr(e)))):
        #         return eval(car(cdr(cdr(e))))
        #     else:
        #         return eval(car(cdr(cdr(cdr(e)))))
        elif not null(assoc(car(e), gf)):
            result = assoc(car(e), gf)
            oldG = g
            g = append(pair(car(result), cdr(e)), g)
            interperateResult = interpreteBlock(cdr(result))
            g = oldG
            return interperateResult
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
        global g
        global gf
        if l[0] == "LET":
            oldG = g
            g = append(interpreteBlock(blocks[0]), g)
            result = eval(interpreteBlock(blocks[1]))
            g = oldG
            return result
        elif l[0] == "DEFUN":
            if null(assoc(blocks[0], gf)):
                gf = append(List([cons(blocks[0], cons(List(blocks[1][1:len(blocks[1])-1].split(" ")[1:]), blocks[2]))]), gf)
            else:
                gf = assocReplace(blocks[0], cons(List(blocks[1][1:len(blocks[1])-1].split(" ")[1:]), blocks[2]), gf)
            return "T"
        elif l[0] == "SET":
            if null(assoc(blocks[0], g)):
                g = append(List([cons(blocks[0], interpreteBlock(blocks[1]))]), g)
            else:
                g = assocReplace(blocks[0], blocks[1], g)
            return "T"
        elif l[0] == "IF":
            if not null(interpreteBlock(blocks[0])):
                return interpreteBlock(blocks[1])
            else:
                return interpreteBlock(blocks[2])
        elif l[0] == "PROGN":
            for block in blocks[:len(blocks)-1]:
                interpreteBlock(block)
            return interpreteBlock(blocks[-1])
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


inp = ""
while True:
    print("PyLisp> ", end="")
    inp = input()
    # debug stuff
    if inp == "quit":
        break
    elif inp == "pvars":
        print("variables:", g)
        print("functions:", gf)
    elif len(inp) > 5 and inp[0:5] == "load ":
        f = open(inp[5:], "r")
        print(interpreteBlocks(f.read().replace("\n", " ").replace("\t", " "), True))
        f.close()
    else:
        print(interpreteBlocks(inp, True))

# (defun rZ (list a) (if (eq a 0.0) (print 0) (progn (print a) (rZ (- a 1)))))
# (defun printall (list a) (if (eq (cdr a) nil) (print (car a)) (progn (print (car a)) (printall (cdr a)))))