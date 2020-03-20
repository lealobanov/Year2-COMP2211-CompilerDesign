from datetime import datetime
import time
import sys
import string
import random

#Parse tree visualization modules
import anytree
import graphviz
from anytree import Node, RenderTree
from anytree.dotexport import RenderTreeGraph
from anytree.exporter import DotExporter

#Generate random ID strings to append to anytree Nodes for distinction
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#Specify file to read input from as 1st command line argument
try:
    IN_FILE = sys.argv[1]
except:
    print("Input file not specified.")
    sys.exit(1)

#Specify destination of output grammar 
current_timestamp = datetime.now()
timestamp_str = current_timestamp.strftime("%d-%b-%Y-%H:%M:%S")
OUT_FILE_GRAMMAR = timestamp_str + IN_FILE[:-4] + "-outputgrammar.txt"
OUT_FILE_PARSETREE = timestamp_str + IN_FILE[:-4] + "-outputparsetree.png"

#Append to log
def append_log(status, msg):
    #Generate timestamp for record in log file
    current_timestamp = datetime.now()
    timestamp_str = current_timestamp.strftime("%d-%b-%Y-%H:%M:%S")+"\t"+IN_FILE+"\t"+status+"\t"+msg+"\n"
    #Write tab-delimited lines to log file
    writing = timestamp_str
    with open("logfile.log", "a") as log:
        log.write(writing)
        log.flush()
    return 0

#Read from supplied input file
def read_input(filename):
    #Check if filename exists in current directory
    try:
        lines = []
        with open('./'+filename) as file:
            #Check supplied file is of correct type; .txt extension 
            if filename[-4:] == ".txt":
                #Read contents of the file
                line = file.readline()
                while line:
                    lines.append(line)
                    line = file.readline()
                return lines
            else:
                print("Specified file is of an invalid format; only files with .txt extension are accepted as valid input.")
                append_log("ERR", "Specified file is of an invalid format; only files with .txt extension are accepted as valid input.")
                #Log and close the running program
                return False
    except: 
        print("Specified input file not found.")
        append_log("ERR", "Specified input file not found.")
        #Log and close the running program
        return False


#Parse input file contents 
def parse_input(file_contents):
    #Initialize parsing criteria
    definitions = ['variables:', 'constants:', 'predicates:', 'equality:', 'connectives:', 'quantifiers:', 'formula:']
    variables = []
    constants = []
    predicates = []
    equality = []
    connectives = []
    quantifiers = []
    formula = []
    predicate_symbols = []
    for line in file_contents:
        #Initialize parsing criteria
        for category in definitions:
                if (category in line[0:12]) == True:
                    current_category = definitions.index(category)
                    new_line = 1
        #Parse variables
        if current_category == 0:
            if new_line == 1:
                contents = line[10:] + ' '
                new_line = 0
            else: 
                contents = line + ' '
            var = ''
            for c in contents:
                if c == ' ' or c == '\t' or c == '\n':
                    if len(var) > 0:
                        var = var.replace("\\", "\\\\")
                        variables.append(var)
                        var = ''
                else: 
                    var += c
        #Parse constants
        if current_category == 1: 
            if new_line == 1:
                contents = line[10:] + ' '
                new_line = 0
            else: 
                contents = line + ' '
            var = ''
            for c in contents:
                if c == ' ' or c == '\t' or c == '\n':
                    if len(var) > 0:
                        var = var.replace("\\", "\\\\")
                        constants.append(var)
                        var = ''
                else: 
                    var += c   
        #Parse predicate symbols and their associated arity
        if current_category == 2:
            if new_line == 1:
                contents = line[11:] + ' '
                new_line = 0
            else: 
                contents = line + ' '
            var = ''
            arity = ''
            parsing_arity = 0 
            for c in contents:
                if c == ' ' or c == '\t' or c == '\n':
                    if len(var) > 0:
                        var = var.replace("\\", "\\\\")
                        predicates.append([var, arity])
                        predicate_symbols.append(var)
                        var = ''
                        arity = ''
                else:
                    if c == "[":
                        parsing_arity = 1 
                    elif c == "]":
                        parsing_arity = 0
                    elif parsing_arity == 1 and c != "[":
                        arity +=c
                    else:
                        var += c
        #Parse equality
        if current_category == 3:
            if new_line == 1:
                contents = line[9:] + ' '
                new_line = 0
            else: 
                contents = line + ' '
            var = ''
            for c in contents:
                if c == ' ' or c == '\t' or c == '\n':
                    if len(var) > 0:
                        var = var.replace("\\", "\\\\")
                        equality.append(var)
                        var = ''
                else: 
                    var += c 
        #Parse connectives
        if current_category == 4:
            if new_line == 1:
                contents = line[12:] + ' '
                new_line = 0
            else: 
                contents = line + ' '
            var = ''
            for c in contents:
                if c == ' ' or c == '\t' or c == '\n':
                    if len(var) > 0:
                        var = var.replace("\\", "\\\\")
                        connectives.append(var)
                        var = ''
                else: 
                    var += c 
        #Parse quantifiers
        if current_category == 5:
            if new_line == 1:
                contents = line[12:] + ' '
                new_line = 0
            else: 
                contents = line + ' '
            var = ''
            for c in contents:
                if c == ' ' or c == '\t' or c == '\n':
                    if len(var) > 0:
                        var = var.replace("\\", "\\\\")
                        quantifiers.append(var)
                        var = ''
                else: 
                    var += c 
        #Parse formula token by token
        if current_category == 6:
            if new_line == 1:
                contents = line[8:] + ' '
                new_line = 0
            else: 
                contents = line + ' '
            var = ''
            for c in contents:
                #Account for possible white spaces, tabs, new lines, etc. in formula
                if c ==' ' or c == '\t' or c == '\n' or c == '':
                    if len(var) > 0:
                        var = var.replace("\\", "\\\\")
                        formula.append(var)
                        var = ''
                #Account for "(" ")" and "," as terminals
                elif c== '(' or c == ')' or c == ',':
                    if len(var) > 0:
                        var = var.replace("\\", "\\\\")
                        formula.append(var)
                    formula.append(c)
                    var = ''
                else: 
                    var += c 
    file_contents = [variables, constants, predicates, equality, connectives, quantifiers, formula, predicate_symbols]
    return file_contents

#Check validity of supplied input file
def check_validity(file_contents):
    #Check all necessary elements are present in equality, connectives, and quantifiers sets
    #Variable, constant, and predicate sets may be empty
    if len(file_contents[3]) != 1:
        print("Incorrect cardinality; exactly 1 equality symbol must be supplied.")
        append_log("ERR", "Incorrect cardinality; exactly 1 equality symbol must be supplied.")
        return False
    
    if len(file_contents[4]) != 5:
        print("Incorrect cardinality; exactly 5 logical connectives must be supplied.")
        append_log("ERR", "Incorrect cardinality; exactly 5 logical connectives must be supplied.")
        return False

    if len(file_contents[5]) != 2:
        print("Incorrect cardinality; exactly 2 quantifiers must be supplied.")
        append_log("ERR", "Incorrect cardinality; exactly 2 quantifiers must be supplied.")
        return False
    
    #Check that arity of predicates is an int and convert type str to int
    for predicate in file_contents[2]:
        try:
            predicate[1] = int(predicate[1])
        except:
            print("Supplied predicate arity is not an integer.")
            append_log("ERR", "Supplied predicate arity is not an integer.")
            return False

    #Check for duplicates within individual sets
    #Variables
    if len(file_contents[0]) != len(set(file_contents[0])):
        print("Detected duplicate variables.")
        append_log("ERR", "Detected duplicate variables.")
        return False
    #Constants
    if len(file_contents[1]) != len(set(file_contents[1])):
        print("Detected duplicate constants.")
        append_log("ERR", "Detected duplicate constants.")
        return False
    #Predicate symbols
    if len(file_contents[7]) != len(set(file_contents[7])):
        print("Detected duplicate predicate symbols.")
        append_log("ERR", "Detected duplicate predicate symbols.")
        return False
    #Connectives
    if len(file_contents[4]) != len(set(file_contents[4])):
        print("Detected duplicate connectives.")
        append_log("ERR", "Detected duplicate connectives.")
        return False
    #Quantifiers
    if len(file_contents[5]) != len(set(file_contents[5])):
        print("Detected duplicate connectives.")
        append_log("ERR", "Detected duplicate connectives.")
        return False


    #Check for duplicate variables, constants, predicate symbols, quantifiers, connectives, equality across all sets
    for variable in file_contents[0]:
        #Var in constants
        if variable in file_contents[1]:
            print("Found a duplicate in variables and constants: ", variable)
            append_log("ERR", "Found a duplicate in variables and constants: " + variable)
            return False
        #Var in predicate symbols
        elif variable in file_contents[7]:
            print("Found a duplicate in variables and predicate symbols: ", variable)
            append_log("ERR", "Found a duplicate in variables and predicate symbols: " + variable)
            return False
        #Var in quantifiers
        elif variable in file_contents[5]: 
            print("Found a duplicate in variables and quantifiers: ", variable)
            append_log("ERR", "Found a duplicate in variables and quantifers: " + variable)
            return False
        #Var in connectives
        elif variable in file_contents[4]: 
            print("Found a duplicate in variables and connectives: ", variable)
            append_log("ERR", "Found a duplicate in variables and connectives: " + variable)
            return False
        #Var in equality
        elif variable in file_contents[3]: 
            print("Found a duplicate in variables and equality: ", variable)
            append_log("ERR", "Found a duplicate in variables and equality: " + variable)
            return False

    for constant in file_contents[1]:
        #Constant in predicate symbols
        if constant in file_contents[7]:
            print("Found a duplicate in constants and predicate symbols: ", constant)
            append_log("ERR", "Found a duplicate in constants and predicate symbols: " + constant)
            return False
        #Constant in quantifiers
        elif constant in file_contents[5]: 
            print("Found a duplicate in constants and quantifiers: ", constant)
            append_log("ERR", "Found a duplicate in constants and quantifers: " + constant)
            return False
        #Constant in connectives
        elif constant in file_contents[4]: 
            print("Found a duplicate in constants and connectives: ", constant)
            append_log("ERR", "Found a duplicate in constants and connectives: " + constant)
            return False
        #Constant in equality
        elif constant in file_contents[3]: 
            print("Found a duplicate in constants and equality: ", constant)
            append_log("ERR", "Found a duplicate in constants and equality: " + constant)
            return False
    
    for predsymbol in file_contents[7]:
        #Predicate symbols in quantifiers
        if predsymbol in file_contents[5]: 
            print("Found a duplicate in predicate symbols and quantifiers: ", predsymbol)
            append_log("ERR", "Found a duplicate in predicate symbols and quantifers: " + predsymbol)
            return False
        #Predicate symbols in connectives
        elif predsymbol in file_contents[4]: 
            print("Found a duplicate in predicate symbols and connectives: ", predsymbol)
            append_log("ERR", "Found a duplicate in predicate symbols and connectives: " + predsymbol)
            return False
        #Predicate symbols in equality
        elif predsymbol in file_contents[3]: 
            print("Found a duplicate in predicate symbols and equality: ", predsymbol)
            append_log("ERR", "Found a duplicate in predicate symbols and equality: " + predsymbol)
            return False

    for quantifier in file_contents[5]:
        #Quantifiers in connectives
        if quantifier in file_contents[4]: 
            print("Found a duplicate in quantifiers and connectives: ", quantifier)
            append_log("ERR", "Found a duplicate in quantifiers and connectives: " + quantifier)
            return False
        #Quantifiers in equality
        elif quantifier in file_contents[3]: 
            print("Found a duplicate in quantifiers and equality: ", quantifier)
            append_log("ERR", "Found a duplicate in quantifiers and equality: " + quantifier)
            return False
    
    for connective in file_contents[4]: 
        #Connectives in equality
        if connective in file_contents[3]: 
            print("Found a duplicate in connectives and equality: ", connective)
            append_log("ERR", "Found a duplicate in connectives and equality: " + connective)
            return False
    
    #Check if any variables, constants, predicate symbols, quantifiers, equality, connectives are forbidden symbols
    for variable in file_contents[0]:
        if variable in ["(", ")", ","]:
            print("Variable cannot be one of '(', ')', or ',' ")
            append_log("ERR", "Variable cannot be one of '(', ')', or ',' ")
            return False
    for constant in file_contents[1]:
        if constant in ["(", ")", ","]:
            print("Constant cannot be one of '(', ')', or ',' ")
            append_log("ERR", "Constant cannot be one of '(', ')', or ',' ")
            return False
    for predicate_symbol in file_contents[7]:
        if predicate_symbol in ["(", ")", ","]:
            print("Predicate symbols cannot be one of '(', ')', or ',' ")
            append_log("ERR", "Predicate symbol cannot be one of '(', ')', or ',' ")
            return False
    for quantifier in file_contents[5]:
        if quantifier in ["(", ")", ","]:
            print("Quantifiers cannot be one of '(', ')', or ',' ")
            append_log("ERR", "Quantifier cannot be one of '(', ')', or ',' ")
            return False
    for connective in file_contents[4]:
        if connective in ["(", ")", ","]:
            print("Connectives cannot be one of '(', ')', or ',' ")
            append_log("ERR", "Connective cannot be one of '(', ')', or ',' ")
            return False
    for equality in file_contents[3]:
        if equality in ["(", ")", ","]:
            print("Equality cannot be one of '(', ')', or ',' ")
            append_log("ERR", "Equality cannot be one of '(', ')', or ',' ")
            return False

    #If input file contents are valid, return True 
    return True 

parsed = parse_input(read_input(IN_FILE))

#If supplied input file is valid, generate corresponding grammar 
def generate_grammar(file_contents, OUT_FILE_GRAMMAR, IN_FILE):
    intro = ["A formal grammar is defined as a quadruple (V_t, V_n, P, S), where:","- V_t is a set of terminal symbols","- V_n is a set of non-terminal symbols","- P is set of production rules","- S is the start symbol, which is a non-terminal" ]
    with open(OUT_FILE_GRAMMAR, "a") as output:
        for line in intro:
            output.write(line)
            output.write("\n")
        output.write("\n")
        intro2 = "See program documentation for meaning of each non-terminal symbol in the grammar below. The formal grammar for the supplied input file, " + str(IN_FILE) + ", is defined by the sets V_t, V_n, P, and S as follows:\n"
        output.write(intro2)
        output.write("\n")
        terminals = "V_t = {"
        for variable in file_contents[0]:
            variable = variable.replace("\\\\", "\\")  
            var_str = variable + ", "
            terminals += var_str
        for constant in file_contents[1]:
            constant = constant.replace("\\\\", "\\")  
            const_str = constant + ", "
            terminals += const_str
        for predicate_symbol in file_contents[2]:
            predicate_symbol[0] =  predicate_symbol[0].replace("\\\\", "\\")  
            pred_str = predicate_symbol[0] + ", "
            terminals += pred_str
        for connective in file_contents[4]:
            connective = connective.replace("\\\\", "\\")  
            conn_str = connective + ", "
            terminals += conn_str
        for quantifier in file_contents[5]:
            quantifier = quantifier.replace("\\\\", "\\")  
            quant_str = quantifier + ", "
            terminals += quant_str
        for equality in file_contents[3]:
            equality = equality.replace("\\\\", "\\")  
            equality_str = equality
            terminals += equality


        output.write(terminals+"}\n\n")
        non_terminals = "V_n = {F*, P*, Z*, T*, V*, C*, K*, Q*, J*}\n\n"
        output.write(non_terminals)
        productions = ["F* -> ( F* C* F* ) | Q* V* F* | "+ file_contents[4][4].replace("\\\\", "\\") +" F* | ( T* "+ file_contents[3][0].replace("\\\\", "\\") + " T* ) | P*",
        "T* -> V* | K*",
        "C* -> ", 
        "Q* -> ", 
        "P* -> Z* ( J* )",
        "J* -> V* | V* , J*",
        "Z* -> ", 
        "K* -> ", 
        "V* -> "]
        i = 0
        for connective in file_contents[4]:
            connective = connective.replace("\\\\", "\\")
            num = len(file_contents[4])
            if i < num-1:
                conn_str = connective + " | "
                productions[2] += conn_str
                i += 1
            else:
                productions[2] += connective
        i = 0
        for quantifier in file_contents[5]:
            quantifier = quantifier.replace("\\\\", "\\")
            num = len(file_contents[5])
            if i < num-1:
                quant_str = quantifier + " | "
                productions[3] += quant_str
                i += 1
            else:
                productions[3] += quantifier
        i = 0
        for predicate_symbol in file_contents[2]:
            predicate_symbol[0] = predicate_symbol[0].replace("\\\\", "\\")
            num = len(file_contents[2])
            if i < num-1:
                pred_str = predicate_symbol[0] + " | "
                productions[6] += pred_str
                i += 1
            else:
                productions[6] += predicate_symbol[0]
        i = 0
        for constant in file_contents[1]:
            constant = constant.replace("\\\\", "\\")
            num = len(file_contents[1])
            if i < num-1:
                const_str = constant + " | "
                productions[7] += const_str
                i += 1
            else:
                productions[7] += constant
        i = 0
        for variable in file_contents[0]:
            variable = variable.replace("\\\\", "\\")
            num = len(file_contents[0])
            if i < num-1:
                var_str = variable + " | "
                productions[8] += var_str
                i += 1
            else:
                productions[8] += variable
        #Format the grammar for writing in a text file        
        output.write("P = {\n\n")
        for line in productions:
            output.write(line)
            output.write("\n")
        output.write("\n}\n")
        start = "S = {F*}\n"
        output.write("\n")
        output.write(start)
    return True

    
#Check validity of supplied FO formula - parenthese and predicate arity
def check_formula(file_contents):
    raw_formula = file_contents[6]
    valid_formula = []
    open_parenth = 0
    close_parenth = 0
    i = 0
    for element in raw_formula:
        if element == "(":
            open_parenth +=1
        if element == ")":
            close_parenth +=1
        if element in file_contents[7]:
        #If detected a predicate symbol 
            predicate = element
            for entry in file_contents[2]:
                if entry[0] == predicate:
                    arity = entry[1]
            if raw_formula[i+1] != "(":
            #The next symbol must be an opening parenthese
                print("Predicate symbol must be directly followed by opening parenthese; incorrect arity")
                append_log("ERR", "Predicate symbol must be directly followed by opening parenthese; incorrect arity")
                return False
            #The final symbol must be a closing parenthese
            try:
                if raw_formula[i+(2*arity)+1] != ")":
                    print("Predicate symbol must conclude with a closing parenthese; incorrect arity")
                    append_log("ERR", "Predicate symbol must conclude with a closing parenthese; incorrect arity")
                    return False
            except:
                print("Predicate used in formula with incorrect arity")
                append_log("ERR", "Predicate used in formula with incorrect arity")
                return False
            #Followed by variables, separated by commas, of correct arity associated with that predicate symbol
            j = 0 
            while j < (2*arity):
                comma = 0 
                try:
                    if raw_formula[i+1+j] != ")":
                        if raw_formula[i+1+j] == "," and comma == 1:
                            print("Commas must alternate with variables")
                            append_log("ERR", "Commas must alternate with variables")
                            return False

                        elif raw_formula[i+1+j] == "," and comma == 0:
                            comma = 1
                        else: 
                            comma = 0
                    else: 
                        print("Predicate used in formula with incorrect arity")
                        append_log("ERR", "Predicate used in formula with incorrect arity")
                        return False 
                    j += 1
                except:
                    print("Predicate used in formula with incorrect arity")
                    append_log("ERR", "Predicate used in formula with incorrect arity")
                    return False
        i +=1
    #Check parentheses match up
    if open_parenth != close_parenth:
        print("Opening and closing parentheses in supplied formula do not match.")
        append_log("ERR", "Opening and closing parentheses in supplied formula do not match.")
        sys.exit(1)
    #If parenthese and arity checks passed, return True 
    return True

#Recursive descent parser
class Parser():
    #Initialize parser class
    def __init__(self,tokenstream, variables, constants, connectives, predicates, quantifiers, equality):
        self.tokenstream = tokenstream
        #Append EOF to end of tokenstream
        self.tokenstream.append("$")

        self.variables = variables
        self.connectives = connectives
        self.predicates = predicates
        self.quantifiers = quantifiers
        self.equality = equality
        self.constants = constants

        #Intialize position to 0 and current token to first in stream
        self.pos = 0
        self.current = self.tokenstream[self.pos]

        #Initialize parse tree
        self.root = Node("F", parent=None, id = "F*")
        self.initialroot = Node("F", parent=None, id = "F*")
        self.parseF(self.root)

    #Parse productions of the form F -> 
    def parseF(self, _parent):

        #Parse productions of the form F -> (FCF)
        if self.current == "(" and self.tokenstream[self.pos+2] != self.equality[0]:
            LeftBr = Node("("+str(self.pos)+id_generator(), parent=_parent, id = "(")
            self.pos += 1
            self.current = self.tokenstream[self.pos]
            F= Node("F"+str(self.pos)+id_generator(), parent=_parent, id = "F*")
            self.parseF(F)
            C = Node("C"+str(self.pos)+id_generator(), parent=_parent, id = "C*")
            self.parseC(C)
            F= Node("F"+str(self.pos)+id_generator(), parent=_parent, id = "F*")
            self.parseF(F)
            if self.current == ")":
                RightBr = Node(")"+str(self.pos)+id_generator(), parent=_parent, id = ")")
                self.pos += 1
                self.current = self.tokenstream[self.pos]
            else:
                msg = "Expected ')' but received " + self.current
                print(msg)
                append_log("ERR", msg)
                return False
        
        #Parse productions of the form F -> (T=T)
        elif self.current == "(" and self.tokenstream[self.pos+2] == self.equality[0]:
            LeftBr = Node("("+str(self.pos)+id_generator(), parent=_parent, id = "(")
            self.pos += 1
            self.current = self.tokenstream[self.pos]
            T= Node("T"+str(self.pos)+id_generator(), parent=_parent, id = "T*")
            self.parseT(T)

            if self.current == self.equality[0]:
                Eq = Node(self.equality[0]+str(self.pos)+id_generator(), parent=_parent, id = self.current)
                self.pos += 1
                self.current = self.tokenstream[self.pos]
            else:
                msg = "Expected " + self.equality[0]+ " but received " + self.current
                print(msg)
                append_log("ERR", msg)
                return False

            T= Node("T"+str(self.pos)+id_generator(), parent=_parent, id = "T*")
            self.parseT(T)
            if self.current == ")":
                RightBr = Node(")"+str(self.pos)+id_generator(), parent=_parent, id = ")")
                self.pos += 1
                self.current = self.tokenstream[self.pos]
            else:
                msg = "Expected ')' but received " + self.current
                print(msg)
                append_log("ERR", msg)
                return False

        #Parse productions of the form F -> QVF
        elif self.current in self.quantifiers:
            Q = Node("Q"+str(self.pos)+id_generator(), parent=_parent, id = "Q*")
            self.parseQ(Q)
            V = Node("V"+str(self.pos)+id_generator(), parent=_parent, id = "V*")
            self.parseV(V)
            F= Node("F"+str(self.pos)+id_generator(), parent=_parent, id = "F*")
            self.parseF(F)

        #Parse productions of the form F -> notF
        elif self.current == self.connectives[4]:
            NEG = Node("N"+str(self.pos)+id_generator(), parent=_parent, id = self.current)
            self.pos += 1
            self.current = self.tokenstream[self.pos]
            F= Node("F"+str(self.pos)+id_generator(), parent=_parent, id = "F*")
            self.parseF(F)

        #If EOF reached, check for EOF symbol and return visualization of the parsetree
        elif self.current == "$":
            self.check_success()

        #Parse productions of the form F -> P
        else:
            P = Node("P"+str(self.pos)+id_generator(), parent=_parent, id = "P*")
            self.parseP(P)

     #Parse productions of the form Q (quantifier) -> 
    def parseQ(self, Qparent):
        if self.current in self.quantifiers:
            Q = Node(self.current+str(self.pos)+id_generator(), parent=Qparent, id = self.current)
            self.pos += 1
            self.current = self.tokenstream[self.pos]
        else:
            msg = "Expected a quantifier but received " + self.current
            print(msg)
            append_log("ERR", msg)
            return False
    
     #Parse productions of the form T (term) -> 
    def parseT(self, Tparent):
        if self.current in self.variables:
            V = Node("V"+str(self.pos)+id_generator(), parent=Tparent, id = "V*")
            self.parseV(V)
        elif self.current in self.constants:
            K = Node("K"+str(self.pos)+id_generator(), parent=Tparent, id = "K*")
            self.parseK(K)
        else: 
            msg = "Expected a variable or constant but received " + self.current
            print(msg)
            append_log("ERR", msg)
            return False

    #Parse productions of the form C (connective) -> 
    def parseC(self, Cparent):
        if self.current in [self.connectives[0],self.connectives[1],self.connectives[2],self.connectives[3]]:
            C = Node(self.current+str(self.pos)+id_generator(), parent=Cparent, id = self.current)
            self.pos += 1
            self.current = self.tokenstream[self.pos]
        else:
            msg = "Expected a connective but received " + self.current
            print(msg)
            append_log("ERR", msg)
            return False
    
    #Parse productions of the form V (variable) -> 
    def parseV(self, Vparent):
        if self.current in self.variables:
            V = Node(self.current+str(self.pos)+id_generator(), parent=Vparent, id = self.current)
            self.pos += 1
            self.current = self.tokenstream[self.pos]
        else:
            msg = "Expected a variable but received " + self.current
            print(msg)
            append_log("ERR", msg)
            return False

    #Parse productions of the form K (constant) -> 
    def parseK(self, Kparent):
        if self.current in self.constants:
            K = Node(self.current+str(self.pos)+id_generator(), parent=Kparent, id = self.current)
            self.pos += 1
            self.current = self.tokenstream[self.pos]
        else:
            msg = "Expected a constant but received " + self.current
            print(msg)
            append_log("ERR", msg)
            return False

    #Parse productions of the form P (predicate) -> 
    def parseP(self, Pparent):
        Z = Node("Z"+str(self.pos), parent=Pparent, id = "Z*")
        self.parseZ(Z)
        if self.current == "(":
            LeftBr = Node(self.current+str(self.pos)+id_generator(), parent=Pparent, id = "(")
            self.pos += 1
            self.current = self.tokenstream[self.pos]
        else:
            msg = "Expected '(' but received " + self.current
            print(msg)
            append_log("ERR", msg)
            return False

        self.parseJ(Pparent)
        if self.current == ")":
            RightBr = Node(self.current+str(self.pos)+id_generator(), parent=Pparent, id = ")")
            self.pos += 1
            self.current = self.tokenstream[self.pos]
        else:
            msg = "Expected ')' but received " + self.current
            print(msg)
            append_log("ERR", msg)
            return False

    #Parse productions of the form J (variable list inside predicate) -> 
    def parseJ(self, JParent):
        V = Node("V"+str(self.pos)+id_generator(), parent=JParent, id = "V*")
        self.parseV(V)
        if self.current == ",":
            Comma = Node(","+str(self.pos)+id_generator(), parent=JParent, id = ",")
            self.pos += 1
            self.current = self.tokenstream[self.pos]
            self.parseJ(JParent)         
    
    #Parse productions of the form Z (predicate symbol) -> 
    def parseZ(self,Zparent):
        if self.current in self.predicates:
            Z = Node(self.current+str(self.pos)+id_generator(), parent=Zparent, id = self.current)
            self.pos += 1
            self.current = self.tokenstream[self.pos]
        else:
            msg = "Expected a predicate symbol but received " + self.current
            print(msg)
            append_log("ERR", msg)
            return False

    #Check if end of token stream reached
    def check_success(self):
        if self.current == '$':
            append_log("OK", "FO formula parsed successfully")
            #Return the parse tree
            return self.root
        else:
            append_log("ERR", "Failed to parse FO formula")
            return False

#If input file read sucessfully and passed all initial checks, feed FO formula to recursive descent parser    
if check_validity(parsed) == True:
    if check_formula(parsed) == True:
        variables = parsed[0]
        constants = parsed[1]

        predicates = []
        for predsymbol in parsed[2]:
            predicates.append(predsymbol[0])
        
        equality = parsed[3]

        connectives = parsed[4]

        quantifiers = parsed[5]

        tokenstream = parsed[6]

        #Check for forbidden tokens and escape characters in the tokenstream
        if "$" in tokenstream:
            print("$ is a forbidden input symbol; denotes end of file character")
            append_log("ERR","$ is a forbidden input symbol; denotes end of file character")
            sys.exit()
        
        #Initialize a Parser object
        parsing = Parser(tokenstream, variables, constants, connectives, predicates, quantifiers, equality)
        if parsing == False:
            print("Failed to generate visualization of parse tree; invalid FO formula")
            
        #If parsing was successful, visualize the PT
        tree = parsing.check_success()

        if tree != False and parsing.root != parsing.initialroot:
            generate_grammar(parsed, OUT_FILE_GRAMMAR, IN_FILE)
            DotExporter(tree, nodeattrfunc=lambda n: 'label="%s"' % (n.id)).to_picture(OUT_FILE_PARSETREE)
            print("Parsing successful; grammar output to " + OUT_FILE_GRAMMAR + " and parse tree output to " + OUT_FILE_PARSETREE)
        else:
            print("Failed to generate grammar and visualization of parse tree; invalid FO formula")
            append_log("ERR", "Failed to generate visualization of parse tree; invalid FO formula")
            sys.exit(1)

