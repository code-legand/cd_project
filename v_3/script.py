import re
import copy
from prettytable import PrettyTable as Table


with open('input.txt', 'r') as file:
    input_string = file.read()

program = input_string.split('\n')

# tokens
operators = {'=': 'Assignment Operator', '+': 'Additon Operator', '-': 'Substraction Operator', '>': 'comparision operator','/': 'Division Operator', '*': 'Multiplication Operator', '++': 'increment Operator', '--': 'Decrement Operator'}
optr_keys = operators.keys()

comments = {r'//': 'Single Line Comment', r'/*': 'Multiline Comment Start',r'*/': 'Multiline Comment End', '/**/': 'Empty Multiline comment'}
comment_keys = comments.keys()

header = {'.h': 'header file'}
header_keys = header.keys()
sp_header_files = {'<stdio.h>': 'Standard Input Output Header','<string.h>': 'String Manipulation Library'}

macros = {r'#\w+': 'macro'}
macros_keys = macros.keys()

datatype = {'int': 'Integer', 'float': 'Floating Point','char': 'Character', 'long': 'long int'}
datatype_keys = datatype.keys()

keyword = {'return': 'keyword that returns a value from a block'}
keyword_keys = keyword.keys()

delimiter = {';': 'terminator symbol semicolon (;)'}
delimiter_keys = delimiter.keys()

while_block = {'while': 'Enter While Loop','end while': 'Exit While Loop'}
while_block_keys = while_block.keys()

blocks = {'begin': 'Enter Block','end': 'Exit Block\n\nTokens generated successfully'}
block_keys = blocks.keys()

builtin_functions = {'printf': 'printf prints its argument on the console'}
non_identifiers = ['_', '-', '+', '/', '*', '`', '~', '!', '@', '#', '$', '%', '^','&', '*', '(', ')', '=', '|', '"', ':', ';', '{', '}', '[', ']', '<', '>', '?','/']
numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
dataFlag = False
start_symbol = 'S'
id = ''

# grammar
rules = []
nonterm_userdef = []
term_userdef = []

diction = {}
firsts = {}
follows = {}
count = 0


def print_table(header, data):
    table = Table(header)
    for row in data:
        table.add_row(row)
    print(table)

def construct_grammar():
    global rules, nonterm_userdef, term_userdef, id
    rules = [
        "S -> T M B A D",
        "T -> int",
        "M -> main()",
        "B -> begin",
        "D -> end",
        "A -> E W X",
        "E -> T "+id+" = 1 ;",
        "W -> while ( C ) P Q R | #",
        "C -> n > 1",
        "P -> "+id+" = "+id+" + 1 ;",
        "Q -> n = n / 2 ;",
        "R -> end while",
        "X -> return "+id +" | #"
        ]
    nonterm_userdef = ['S', 'T', 'M', 'B', 'D', 'A', 'E', 'W', 'P', 'Q', 'R', 'X', 'C']
    term_userdef = [id, 'n', 'int', 'main()', 'end', 'while', 'begin', '(', ')', '+', '/', 'end while', 'return', '1', '2', '>', '=', '0', ';']

# lexically analyzer code
def lexicalAnalyzer():
    global operators, optr_keys, comments, comment_keys, header, header_keys, macros, macros_keys, datatype, datatype_keys, keyword, keyword_keys, delimiter, delimiter_keys, while_block, while_block_keys, blocks, block_keys, builtin_functions, non_identifiers, numerals, dataFlag, id, count
    for line in program:
        count = count+1
        print('\033[1m' + "Line #", count, line + '\033[0m')
        tokens = line.split(' ')
        if 'end' in tokens and 'while' in tokens:
            tokens = ['end while']
        while '' in tokens:
            tokens.remove('')
        print("Tokens are", tokens)
        print('properties:')
        for token in tokens:
            if '\r' in token:
                position = token.find('\r')
                token = token[:position]
            if token in while_block_keys:
                print(while_block[token])
            if token in block_keys:
                print(blocks[token])
            if token in optr_keys:
                print("Operator is: ", operators[token])
            if token in comment_keys:
                print("Comment Type: ", comments[token])
            if token in macros_keys:
                print("Macro is: ", macros[token])
            if '.h' in token:
                print("Header File is: ", token, sp_header_files[token])
            if '()' in token:
                print("Function named", token)
            if dataFlag == True and (token not in non_identifiers) and ('()' not in token) and (token not in numerals):
                print("Identifier: ", token)
            if token in numerals:
                print("Numeral: ", token)
            if token in datatype_keys:
                print("type is: ", datatype[token])
                dataFlag = True
            if token in keyword_keys:
                print(keyword[token])
            if token in delimiter:
                print("Delimiter", delimiter[token])
            if '#' in token:
                match = re.search(r'#\w+', token)
                print("Header", match.group())
            if token in numerals:
                print(token, type(int(token)))
            if token not in optr_keys and token not in comment_keys and token not in macros_keys and token not in header_keys and token not in datatype_keys and token not in keyword_keys and token not in delimiter_keys and token not in while_block_keys and token not in block_keys and token not in non_identifiers and token not in numerals:
                id = token
        dataFlag = False
        print()


def removeLeftRecursion(diction):
    store = {}
    for A in diction:
        alpha = []
        beta = []
        for rule in diction[A]:
            if rule[0] == A:
                alpha.append(rule[1:])
            else:
                beta.append(rule)
        if len(alpha) != 0:
            newNT = A + "'"
            while newNT in diction.keys() or newNT in store.keys():
                newNT += "'"
            for rule in beta:
                rule.append(newNT)
            diction[A] = beta
            for rule in alpha:
                rule.append(newNT)
            store[newNT] = alpha
    for A in store:
        diction[A] = store[A]
    return diction

def LeftFactoring(diction):
    # global rules, nonterm_userdef, term_userdef, firsts
    new_diction = {}
    for A in diction:
        all_rules = diction[A]
        temp = dict()
        for rule in all_rules:
            if rule[0] not in temp.keys():
                temp[rule[0]] = [rule]
            else:
                temp[rule[0]].append(rule)
        new_rule = []
        temp_dict = {}
        for key in temp:
            allStartingWithTermKey = temp[key]
            if len(allStartingWithTermKey) > 1:
                A_new = A + "'"
                while(A_new in diction.keys() or A_new in new_diction.keys()):
                    A_new += "'"
                new_rule.append([key, A_new])
                ex_rules = []
                for rule in allStartingWithTermKey:
                    ex_rules.append(rule[1:])
                temp_dict[A_new] = ex_rules
            else:
                new_rule.append(allStartingWithTermKey[0])
        new_diction[A] = new_rule
        for key in temp_dict:
            new_diction[key] = temp_dict[key]
    return new_diction

def first(rule):
    global rules, nonterm_userdef, term_userdef, diction, firsts
    stack = [rule]
    result = []

    while stack:
        current_rule = stack.pop(0)

        if len(current_rule) != 0 and (current_rule is not None):
            if current_rule[0] in term_userdef:
                result.append(current_rule[0])
            elif current_rule[0] == '#':
                result.append('#')  # epsilon

        if len(current_rule) != 0:
            if current_rule[0] in list(diction.keys()):
                rhs_rules = diction[current_rule[0]]
                for itr in rhs_rules:
                    stack.insert(0, itr)

                if '#' not in result:
                    continue
                else:
                    result.remove('#')
                    if len(current_rule) > 1:
                        ans_new = first(current_rule[1:])
                        if ans_new is not None:
                            if type(ans_new) is list:
                                result += ans_new
                            else:
                                result += [ans_new]
                        else:
                            continue
                    else:
                        result.append('#')

    return result

def follow(nt):
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    stack = [nt]
    solset = set()
    processed = set()

    while stack:
        current_nt = stack.pop()
        if current_nt == start_symbol:
            solset.add('$')
        if current_nt not in processed:
            processed.add(current_nt)

            for curNT in diction:
                rhs = diction[curNT]
                for subrule in rhs:
                    if current_nt in subrule:
                        index_nt = subrule.index(current_nt)
                        subrule = subrule[index_nt + 1:]

                        while subrule and subrule[0] in term_userdef:
                            solset.add(subrule[0])
                            break

                        if not subrule:  # If the subrule is empty, follow curNT
                            stack.append(curNT)
                        elif subrule[0] in nonterm_userdef:
                            stack.append(subrule[0])

    return list(solset)

def computeAllFirsts():
    global rules, nonterm_userdef, term_userdef, diction, firsts
    for rule in rules:
        k = rule.split("->")
        k[0] = k[0].strip()
        k[1] = k[1].strip()
        rhs = k[1]
        multirhs = rhs.split('|')
        for i in range(len(multirhs)):
            multirhs[i] = multirhs[i].strip()
            multirhs[i] = multirhs[i].split()
        diction[k[0]] = multirhs
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print(f"\nRules: \n")
    for y in diction:
        production = ''
        for x in diction[y]:
            production += f"{' '.join(x)} | "
        production = production[:-2]
        print(f"{y} -> {production}")
    print()
        # print(f"{y} -> {diction[y]}")
    # print()
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    diction = removeLeftRecursion(diction)
    print(f"\nAfter elimination of left recursion:\n")
    for y in diction:
        production = ''
        for x in diction[y]:
            production += f"{' '.join(x)} | "
        production = production[:-2]
        print(f"{y} -> {production}")
    print()
    # print(f"{y}->{diction[y]}")
    # print()
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    
    diction = LeftFactoring(diction)
    print("\nAfter left factoring:\n")
    for y in diction:
        production = ''
        for x in diction[y]:
            production += f"{' '.join(x)} | "
        production = production[:-2]
        print(f"{y} -> {production}")
    print()
    # print(f"{y}->{diction[y]}")
    for y in list(diction.keys()):
        t = set()
        for sub in diction.get(y):
            res = first(sub)
            if res != None:
                if type(res) is list:
                    for u in res:
                        t.add(u)
                else:
                    t.add(res)
        firsts[y] = t
    # print()
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print("\nCalculated firsts:\n")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) => {firsts.get(gg)}")
        index += 1
    print()
        
def computeAllFollows():
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset
    # print()
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print("\nCalculated follows:\n")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]}) => {follows[gg]}")
        index += 1
    print()

# parsing table code
def createParseTable():
    global diction, firsts, follows, term_userdef
    # print()
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    print("\nFirsts and Follow Result table:\n")
    mx_len_first = 0
    mx_len_fol = 0
    for u in diction:
        k1 = len(str(firsts[u]))
        k2 = len(str(follows[u]))
        if k1 > mx_len_first:
            mx_len_first = k1
        if k2 > mx_len_fol:
            mx_len_fol = k2

    print_table(['Non-Terminal', 'FIRST', 'FOLLOW'], [[u, str(firsts[u]), str(follows[u])] for u in diction])
    print()
    # print(f"{{:<{10}}} {{:<{mx_len_first + 5}}} {{:<{mx_len_fol + 5}}}".format("Non-T", "FIRST", "FOLLOW"))
    # for u in diction:
    #     print(f"{{:<{10}}} {{:<{mx_len_first + 5}}} {{:<{mx_len_fol + 5}}}".format(u, str(firsts[u]), str(follows[u])))
    
    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)

    terminals.remove('(')
    terminals.remove(')')
    terminals.remove('+')
    terminals.remove('/')
    terminals.remove('=')
    terminals.remove('1')
    terminals.remove('2')
    terminals.remove('0')
    terminals.remove(';')
    terminals.remove('>')
    terminals.remove('end while')
    terminals.append('$')

    mat = []
    for x in diction:
        row = []
        for y in terminals:
            row.append('')
        mat.append(row)
    
    grammar_is_LL = True
    for lhs in diction:
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)
            if '#' in res:
                if type(res) == str:
                    firstFollow = []
                    fol_op = follows[lhs]
                    if fol_op is str:
                        firstFollow.append(fol_op)
                    else:
                        for u in fol_op:
                            firstFollow.append(u)
                    res = firstFollow
                else:
                    res.remove('#')
                    res = list(res) + list(follows[lhs])
            
            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)
            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] = mat[xnt][yt] + f"{lhs}->{' '.join(y)}"
                else:
                    if f"{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] = mat[xnt][yt] + f",{lhs}->{' '.join(y)}"
    # print()
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    # print()
    print("\nGenerated parsing table:\n")
    # frmt = "{:>15}" * len(terminals)

    print_table(['Non-Terminal', *terminals], [[ntlist[i], *mat[i]] for i in range(len(ntlist))])
    print()
    # print(frmt.format(*terminals))
    # j = 0
    # for y in mat:
    #     frmt1 = "{:>15}" * len(y)
    #     print(f"{ntlist[j]} {frmt1.format(*y)}")
    #     j += 1
    
    return mat, terminals, grammar_is_LL

# validate input string
def validateStringUsingStackBuffer(parsing_table, grammarll1, table_term_list, input_string, term_userdef, start_symbol):
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    # print()
    print("\nValidate String:\n")
    if grammarll1 == False:
        return f"\nInput String = \"{input_string}\"\nGrammar is not LL(1)"

    stack = [start_symbol, '$']
    buffer = []
    input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string
    # print('------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
    # print()
    # print("{:>70} {:>10} {:>20}".format("Input\t\t\t\t\t\t\t\t\t\t", "Stack\t\t", "Action"))
    # print()

    parsingSteps = []
    while True:
        if stack == ['$'] and buffer == ['$']:
            parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), "Valid"])
            # print("{:>100} | {:>25} | {:>30}".format(' '.join(buffer), ' '.join(stack), "Valid"))
            result = "\nValid String!"
            return result, parsingSteps
        elif stack[0] not in term_userdef:
            x = list(diction.keys()).index(stack[0])
            y = table_term_list.index(buffer[-1])
            if parsing_table[x][y] != '':
                entry = parsing_table[x][y]
                parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), copy.deepcopy(entry)])
                # print("{:>100} | {:>25} | {:>30}".format(' '.join(buffer), ' '.join(stack), f"T[{stack[0]}][{buffer[-1]}] = {entry}"))
                
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                entryrhs = lhs_rhs[1].split()
                stack = entryrhs + stack[1:]
            else:
                result = f"\nInvalid String! No rule at Table[{stack[0]}][{buffer[-1]}]."
                return result, parsingSteps
                # return f"\nInvalid String! No rule at Table[{stack[0]}][{buffer[-1]}]."
        else:
            if stack[0] == buffer[-1]:
                parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), f"Matched:{stack[0]}"])
                # print("{:>100} | {:>25} | {:>30}".format(' '.join(buffer), ' '.join(stack), f"Matched:{stack[0]}"))
                buffer = buffer[:-1]
                stack = stack[1:]
            else:
                result = "\nInvalid String! Unmatched terminal symbols"
                return result, parsingSteps
                # return "\nInvalid String! Unmatched terminal symbols"

    else:
        if stack[0] == buffer[-1]:
            parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), f"Matched:{stack[0]}"])
            # print("{:>100} | {:>25} | {:>30}".format(' '.join(buffer), ' '.join(stack), f"Matched:{stack[0]}"))
            buffer = buffer[:-1]
            stack = stack[1:]
        else:
            result = "\nInvalid String! Unmatched terminal symbols"
            return result, parsingSteps
            # return "\nInvalid String! Unmatched terminal symbols"


if __name__ == "__main__":
    lexicalAnalyzer()
    construct_grammar()    
    computeAllFirsts()
    computeAllFollows()
    mat, terminals, grammar_is_LL = createParseTable()
    result, parsingSteps = validateStringUsingStackBuffer(parsing_table=mat, grammarll1=grammar_is_LL, table_term_list=terminals, input_string=input_string, term_userdef=term_userdef, start_symbol=start_symbol)
    print_table(['Input', 'Stack', 'Action'], parsingSteps)
    print()
    print(result)
