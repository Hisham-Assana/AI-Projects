RootVariables = {
    #"key1" : ["truth value", "value1", "leftover slot atm"]
}
LearnedVariables = {
    #"key2" : ["truth value", "value2", "leftover slot atm"]
}
Variables = {
    #key3 : value3
}
Facts = [] # Use just a list cause you need the data to be in order
Rules = []
Slist = []

def InputCommand(string):
    command = string.split()
    #print(command)
    if command[0] == "Teach":
        if (command[1] == "-R") or (command[1] == "-L"):
            Teach1(string)
        elif (command[-1] == "true") or (command[-1] == "false"):
            Teach2(string)
        elif "->" in command:
            Teach3(string)
    elif command[0] == "List":
        List()
    elif command[0] == "Learn":
        Learn()
    elif command[0] == "Query":
       if Query(command[1]):
           print("true")
       else:
           print("false")
    elif command[0] == "Why":
        if Query(command[1]):
           print("true")
        else:
           print("false")
        Why(command[1])
    else: 
        print("Invalid command")

    

def Teach1(string):
    command = string.split()
    #print(command)
    sentence = command[4]
    for i in range(5, len(command)) : 
        sentence += " " + command[i]
    #print(sentence)
    if (command[1] == "-R"):
        RootVariables[command[2]] = [None, sentence, "leftover slot"]
        Variables[command[2]] = sentence 
        #print(RootVariables)
    if (command[1] == "-L"):
        LearnedVariables[command[2]] = [None, sentence, "leftover slot"]
        Variables[command[2]] = sentence 
        #print(RootVariables)

def Teach2(string):
    global Facts
    command = string.split()
    #print(command)
    if command[1] not in RootVariables.keys():
        print("This is not a root variable.")
    else:
        if (command[-1] == "true"):
            #print(RootVariables[command[1]])
            for key in LearnedVariables.keys():
                LearnedVariables[key][0] = False
            RootVariables[command[1]][0] = True
            Facts = []
            for key in RootVariables.keys():
                if RootVariables[key][0]:
                    Facts.append(key)
            Facts.append(command[1])
        else: #((command[-1] == "false")):
            for key in LearnedVariables.keys():
                LearnedVariables[key][0] = False
            Facts = []
            for key in RootVariables.keys():
                if RootVariables[key][0]:
                    Facts.append(key)
            RootVariables[command[1]][0] = False

def Teach3(string):
    command = string.split()
    expression = command[1]
    for i in range(2, len(command)) : 
        expression += " " + command[i]
    Rules.append(expression)

def List():
    R = RootVariables.keys()
    L = LearnedVariables.keys()
    print("Root Variables:")
    for key in R:
        print("\t" + key + " = " + RootVariables[key][1] + "")

    print("Learned Variables:")
    for key in L:
        print("\t" + key + " = " + LearnedVariables[key][1] + "")

    print("Facts:")
    for fact in Facts:
        print("\t" + fact)
    
    print("Rules:")
    for rule in Rules:
        print("\t" + rule)

def Learn():
    i = 0
    while i < len(Rules):
        for rule in Rules:
            implication = rule.split()
            expression = tokenize(implication[0])
            if CompParan(expression):
                if recursion(expression[1:len(expression) - 1]):
                    LearnedVariables[implication[-1]][0] = True
                    if implication[-1] not in Facts:
                        Facts.append(implication[-1])
                        break
                else:
                    LearnedVariables[implication[-1]][0] = False
            else: 
                if len(expression) == 1:
                    if expression[0] in Facts:
                        LearnedVariables[implication[-1]][0] = True
                        Facts.append(implication[-1])
                        break
                    else: 
                        LearnedVariables[implication[-1]][0] = False
                else:
                    Touple = lastOP(expression)
                    OPIndex = Touple[0]
                    #x = recursion(expression[0:OPIndex])
                    #y = recursion(expression[OPIndex+1:])
                    if Touple[1] == "&":
                        if(recursion(expression[0:OPIndex]) and recursion(expression[OPIndex+1:])):
                            LearnedVariables[implication[-1]][0] = True
                            if implication[-1] not in Facts:
                                Facts.append(implication[-1])
                                break
                        else: 
                            LearnedVariables[implication[-1]][0] = False
                    elif Touple[1] == "|":
                        if(recursion(expression[0:OPIndex]) or recursion(expression[OPIndex+1:])):
                            LearnedVariables[implication[-1]][0] = True
                            if implication[-1] not in Facts:
                                Facts.append(implication[-1])
                                break
                        else: 
                            LearnedVariables[implication[-1]][0] = False
                    elif Touple[1] == "!":
                        if(not recursion(expression[1:])):
                            LearnedVariables[implication[-1]][0] = True
                            if implication[-1] not in Facts:
                                Facts.append(implication[-1])
                                break
                        else: 
                            LearnedVariables[implication[-1]][0] = False
                            break
        i += 1

def Query(expression):
    #Learn()  Should always have learn run before a query
    
    expression = tokenize(expression)
    #print(expression)
    if len(expression) == 1:
        if expression[0] in Facts:
            return True
        for rule in Rules:
            implication = rule.split()
            if expression[0] == implication[-1]:
                if Query(implication[0]):
                    return True
        else:
            return False

    if CompParan(expression):
        if recursion(expression[1:len(expression) - 1]):
            return True
        else:
            return False
    else:
        Touple = lastOP(expression)
        OPIndex = Touple[0]
        #x = recursion(expression[0:OPIndex])
        #y = recursion(expression[OPIndex+1:])
        if Touple[1] == "&":
            return Query(expression[0:OPIndex]) and Query(expression[OPIndex+1:])
        elif Touple[1] == "|":
            return Query(expression[0:OPIndex]) or Query(expression[OPIndex+1:])
        elif Touple[1] == "!":
            return not Query(expression[1:])
        else:
            return False
    return False

def Why(expression):
    return whyRecursion(tokenize(expression), 0)

#Helper functions
def tokenize(string):
    NonVar = ["(",")","&","|","!"]
    tokens = ["("]
    for token in string:
        if (tokens[-1] not in NonVar) and (token not in NonVar):
            tokens[-1] += token
        else:
            tokens.append(token)
    return tokens[1:]

def recursion(Slist):
    #print(Slist)
    if len(Slist) == 1:
        if Slist[0] in Facts:
            return True
        else: 
            return False
    else:
        if CompParan(Slist):
            return recursion(Slist[1:len(Slist) - 1])
        else: 
            Touple = lastOP(Slist)
            OPIndex = Touple[0]
            #x = recursion(Slist[0:OPIndex])
            #print(x)
            #y = recursion(Slist[OPIndex+1:])
            #print(y)
            if Touple[1] == "&":
                return recursion(Slist[0:OPIndex]) and recursion(Slist[OPIndex+1:])
            elif Touple[1] == "|":
                return recursion(Slist[0:OPIndex]) or recursion(Slist[OPIndex+1:])
            elif Touple[1] == "!":
                return not recursion(Slist[1:])

def whyRecursion(Slist, p):
    if len(Slist) < 1:
        return False
    if len(Slist) == 1:
        for rule in Rules:
            implication = rule.split()
            if implication[-1] == Slist[0]:
                if Query(implication[0]):
                    Why(implication[0])
                    print("BECAUSE " + Translate(implication[0]) + " I KNOW THAT " + Translate(Slist[0]))
                    return True
        if Slist[0] in RootVariables.keys():
            if RootVariables[Slist[0]][0] == True:
                print("I KNOW THAT " + Variables[Slist[0]][1:-1])
                return True
            else: 
                print("I KNOW IT IS NOT TRUE THAT " + Variables[Slist[0]][1:-1])
                return False
                
                
        elif Slist[0] in LearnedVariables.keys():
            if LearnedVariables[Slist[0]][0] == True:
                print("I KNOW THAT " + Variables[Slist[0]][1:-1])
                return True
            else: 
                print("I KNOW IT IS NOT TRUE THAT " + Variables[Slist[0]][1:-1])
                return False
        else: 
            print("I KNOW IT IS NOT TRUE THAT " + Variables[Slist[0]][1:-1])
            return False
    else:
        if CompParan(Slist):
            return whyRecursion(Slist[1:len(Slist) - 1], 1)
        else: 
            Touple = lastOP(Slist)
            OPIndex = Touple[0]
            if Touple[1] == "&":
                if Query(Slist[0:OPIndex]) and Query(Slist[OPIndex+1:]): 
                    whyRecursion(Slist[0:OPIndex], 0) 
                    whyRecursion(Slist[OPIndex+1:], 0) 
                    if p == 0:
                        print("I THUS KNOW THAT " + Translate(Slist[0:OPIndex]) + " AND " + Translate(Slist[OPIndex+1:]) )
                    if p == 1:
                        print("I THUS KNOW THAT (" + Translate(Slist[0:OPIndex]) + " AND " + Translate(Slist[OPIndex+1:]) + ")")
                    return True
                else:
                    if Query(Slist[0:OPIndex]):
                        whyRecursion(Slist[OPIndex+1:], 0)
                        if p == 0:
	                        print("THUS I CANNOT PROVE " + Translate(Slist[0:OPIndex]) + " AND " + Translate(Slist[OPIndex+1:]))
                        if p == 1:
                            print("THUS I CANNOT PROVE (" + Translate(Slist[0:OPIndex]) + " AND " + Translate(Slist[OPIndex+1:]) + ")")
                    else:
                        whyRecursion(Slist[0:OPIndex], 0)
                        if p == 0:
	                        print("THUS I CANNOT PROVE " + Translate(Slist[0:OPIndex]) + " AND " + Translate(Slist[OPIndex+1:]))
                        if p == 1:
                            print("THUS I CANNOT PROVE (" + Translate(Slist[0:OPIndex]) + " AND " + Translate(Slist[OPIndex+1:]) + ")")
                    return False
            elif Touple[1] == "|":
                if Query(Slist[0:OPIndex]) or Query(Slist[OPIndex+1:]):
                    if Query(Slist[0:OPIndex]):
                        whyRecursion(Slist[0:OPIndex], 0)
                        if p == 0:
	                        print("I THUS KNOW THAT " + Translate(Slist[0:]) )
                        if p == 1:
                            print("I THUS KNOW THAT (" + Translate(Slist[0:]) + ")")
                    else:
                        whyRecursion(Slist[OPIndex+1:], 0)
                        if p == 0:
	                        print("I THUS KNOW THAT " + Translate(Slist[0:]) )
                        if p == 1:
                            print("I THUS KNOW THAT (" + Translate(Slist[0:]) + ")")
                    return True
                else:
                    whyRecursion(Slist[0:OPIndex], 0)
                    whyRecursion(Slist[OPIndex+1:], 0)
                    if p == 0:
                        print("THUS I CANNOT PROVE " + Translate(Slist[0:]))
                    if p == 1:
                        print("THUS I CANNOT PROVE (" + Translate(Slist[0:]) + ")")
                    return False
            elif Touple[1] == "!":
                if Query(Slist[1:]):
                    whyRecursion(Slist[1:], 0)
                    if p == 0:
	                    print("THUS I CANNOT PROVE NOT " + Translate(Slist[1:]))
                    if p == 1:
                        print("THUS I CANNOT PROVE NOT (" + Translate(Slist[1:]) + ")")
                    return False
                else:
                    whyRecursion(Slist[1:], 0)
                    if p == 0:
	                    print("I THUS KNOW THAT NOT " + Translate(Slist[1:]))
                    if p == 1:
                        print("I THUS KNOW THAT NOT (" + Translate(Slist[1:]) + ")")
                    return True

def CompParan(Slist):
    if len(Slist) <=0 or Slist[0] != "(":
        return False
    else:
        IndexCount = 1
        ParanCount = 1
        while ParanCount != 0:
            if Slist[IndexCount] == "(":
                ParanCount += 1
            if Slist[IndexCount] == ")":
                ParanCount -= 1
            IndexCount += 1
        if IndexCount != len(Slist):
            return False
        else: 
            return True

def lastOP(Slist):
    Op = ["&","|","!"]
    OpLoc = {
        "|" : [] ,
        "&" : [] ,
        "!" : []
    }
    ParanCount = 0
    IndexCount = 0
    for token in Slist:
        if (token in Op) and (ParanCount == 0):
            OpLoc[token].append(IndexCount)
            IndexCount += 1
        else:
            if Slist[IndexCount] == "(":
                ParanCount += 1
            if Slist[IndexCount] == ")":
                ParanCount -= 1
            IndexCount += 1
    if len(OpLoc["|"])  != 0:
        return (OpLoc["|"][0], "|")
    elif len(OpLoc["&"]) != 0:
        return (OpLoc["&"][0], "&")
    elif len(OpLoc["!"]) != 0:
        return (OpLoc["!"][0], "!")
    
def Untokenize(Slist):
    expression = ""
    for token in Slist:
        expression += token
    return expression

def Translate(Slist):
    InEnglish = []
    expression = tokenize(Slist)
    for token in expression:
        if token in Variables.keys():
            InEnglish.append(Variables[token][1:-1])
        elif token == "|":
            InEnglish.append("OR")
        elif token == "&":
            InEnglish.append("AND")
        elif token == "!":
            InEnglish.append("NOT")
    sentence = ""
    for thing in InEnglish:
        sentence = sentence + thing
        if thing != InEnglish[-1]:
            sentence += " "
    #print("The list: ", InEnglish)
    #print("The sentence: ", sentence)
    return sentence
            
            
#Brainstorming

# (A&B&X) = [(,A,&,B,&,X,)] [A], [B], [X]
# Need to determine X is false (I can do this)
# Identify that X is the consequence of an implication and not just a base variable (How do I do this)
# X is false because M is false and N is false


# M|N -> X

#Run commands here to test shtuffs

# InputCommand("Teach -R S = Sam likes Ice Cream")
# InputCommand("Teach S = true")
# InputCommand("Teach S -> V")
# InputCommand("List")
# InputCommand("Learn")
# InputCommand("Query (S&V)")
#InputCommand("Why (S&V)")

# InputCommand("Learn")



# InputCommand("Teach -R M = Men like Ice Cream")
# InputCommand("Teach M = true")
# InputCommand("Teach -R S = Sam is a man")
# InputCommand("Teach S = true")
# InputCommand("Teach -R A = Sam is Kamran")
# InputCommand("Teach A = false")
# InputCommand("Teach -R B = Sam is a nerd")
# InputCommand("Teach B = true")
# InputCommand("Teach -L V = Sam eats ice cream")
# InputCommand("Teach -L W = Sam hates ice cream")
# InputCommand("Teach V -> W")
# InputCommand("Teach ((M&S)&(B|A)) -> V")
# InputCommand("List")
# InputCommand("Query !((M&S)&(B&A))")
# InputCommand("Learn")
# InputCommand("Query !((M&S)&(B&W))")
# InputCommand("List")
# InputCommand("Why ((M&S)&(B|A))")

def main():
    while True:
        user_input = input()
        if user_input == "0":
	        break
        InputCommand(user_input)
        
if __name__ == "__main__":
    main()

