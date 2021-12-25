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
    if eq(car(car(exp2)), exp1):
        return car(cdr(car(exp2)))
    else:
        return assoc(exp1, cdr(exp2))


def sub2(exp1, exp3):
    if null(exp1):
        return exp3
    elif eq(car(car(exp1)), exp3):
        return car(cdr(car(exp1)))
    else:
        return sub2(cdr(exp1), exp3)


def sublis(exp1, exp2):
    if atom(exp2):
        return sub2(exp1, exp2)
    else:
        return cons(sublis(exp1, car(exp2)), sublis(exp1, cdr(exp2)))


def eval(e):
    if atom(e):
        return e
    elif atom(car(e)):
        if eq(car(e), "QUOTE"):
            return car(cdr(e))
        elif eq(car(e), "ATOM"):
            return atom(eval(car(cdr(e))))
        elif eq(car(e), "EQ"):
            return eval(car(cdr(e))) == eval(car(cdr(cdr(e))))
        # elif eq(car(e), "COND"):
        #     return evcon(cdr(e))
        elif eq(car(e), "CAR"):
            return car(eval(car(cdr(e))))
        elif eq(car(e), "CDR"):
            return cdr(eval(car(cdr(e))))
        elif eq(car(e), "CONS"):
            return cons(eval(car(cdr(e))), eval(car(cdr(cdr(e)))))
        # elif eq(car(e), "LIST"):
        #     return
        else:
            return e


def interprete(code):
    l = code[1:len(code)-1].upper().split(" ")
    innerFlag = False
    index = 0
    openBracket = 0
    closeBracket = 0
    for element in l:
        if (element[0] == "(" and not innerFlag):
            innerFlag = True
            openBracket = index
        if (element[-1] == ")" and innerFlag):
            closeBracket = index
            l[openBracket] = interprete(
                " ".join(l[openBracket:closeBracket+1]))
            del l[openBracket+1:closeBracket+1]
            break
        index += 1
    return eval(List(l))


inp = ""
while True:
    print("PyLisp> ", end="")
    inp = input()
    if inp == "quit":
        break
    print(interprete(inp))
