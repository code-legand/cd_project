"""
This script reads an input file and performs lexical analysis on the input code.
It identifies various tokens such as operators, comments, headers, macros, datatypes, keywords, delimiters, while blocks, blocks, built-in functions, identifiers, and numerals.
It also constructs a grammar and removes left recursion from the grammar.
# """

import re
import copy
from prettytable import PrettyTable as Table

# Read input from the file
with open('input.txt', 'r') as file:
    input_string = file.read()

# Split the input into lines for lexical analysis
program = input_string.split('\n')

# Tokens and their corresponding types

# Operators
operators = {'=': 'Assignment Operator', '+': 'Addition Operator', '-': 'Subtraction Operator', '>': 'Comparison Operator', '/': 'Division Operator', '*': 'Multiplication Operator', '++': 'Increment Operator', '--': 'Decrement Operator'}
optr_keys = operators.keys()

# Comments
comments = {r'//': 'Single Line Comment', r'/*': 'Multiline Comment Start', r'*/': 'Multiline Comment End', '/**/': 'Empty Multiline comment'}
comment_keys = comments.keys()

# Header
header = {'.h': 'header file'}
header_keys = header.keys()
sp_header_files = {'<stdio.h>': 'Standard Input Output Header', '<string.h>': 'String Manipulation Library'}

# Macros
macros = {r'#\w+': 'macro'}
macros_keys = macros.keys()

# Datatypes
datatype = {'int': 'Integer', 'float': 'Floating Point', 'char': 'Character', 'long': 'long int'}
datatype_keys = datatype.keys()

# Keywords
keyword = {'return': 'keyword that returns a value from a block'}
keyword_keys = keyword.keys()

# Delimiters
delimiter = {';': 'terminator symbol semicolon (;)'}
delimiter_keys = delimiter.keys()

# While blocks
while_block = {'while': 'Enter While Loop', 'end while': 'Exit While Loop'}
while_block_keys = while_block.keys()

# Blocks
blocks = {'begin': 'Enter Block', 'end': 'Exit Block\n\nTokens generated successfully'}
block_keys = blocks.keys()

# Builtin Functions
builtin_functions = {'printf': 'printf prints its argument on the console'}

# Non-Identifier Tokens
non_identifiers = ['_', '-', '+', '/', '*', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '|', '"', ':', ';', '{', '}', '[', ']', '<', '>', '?', '/']

# Numerals
numerals = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

# Flags and Symbol Definitions
dataFlag = False
start_symbol = 'S'
id = ''

# Grammar Definitions

# Rules of the Grammar
rules = []
nonterm_userdef = []
term_userdef = []

# Dictionary to store grammar rules
diction = {}
firsts = {}
follows = {}
count = 0


def print_table(header, data):
    """
    Prints a table using the PrettyTable library.

    Parameters:
    - header: List of strings representing the table header.
    - data: List of lists representing the table data.

    Returns:
    None
    """
    table = Table(header)
    for row in data:
        table.add_row(row)
    print(table)

def construct_grammar():
    """
    Constructs the grammar rules and initializes nonterminals and terminals.

    Modifies the global variables rules, nonterm_userdef, term_userdef, and id.

    Returns:
    None
    """
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

def lexicalAnalyzer():
    """
    Performs lexical analysis on the input code.

    Modifies global variables for operators, comments, headers, macros, datatypes, etc.

    Returns:
    None
    """
    global operators, optr_keys, comments, comment_keys, header, header_keys, macros, macros_keys, datatype, datatype_keys, keyword, keyword_keys, delimiter, delimiter_keys, while_block, while_block_keys, blocks, block_keys, builtin_functions, non_identifiers, numerals, dataFlag, id, count

    # Loop through each line of the program
    for line in program:
        count = count + 1
        print('\033[1m' + "Line #", count, line + '\033[0m')
        tokens = line.split(' ')

        # Special case handling for 'end while' token
        if 'end' in tokens and 'while' in tokens:
            tokens = ['end while']

        # Remove empty tokens
        while '' in tokens:
            tokens.remove('')

        print("Tokens are", tokens)
        print('Properties:')

        # Analyze each token and print its properties
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
                print("Type is: ", datatype[token])
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
    """
    Removes left recursion from the given grammar.

    Parameters:
    - diction: Dictionary representing the grammar rules.

    Returns:
    Modified grammar after removing left recursion.
    """
    store = {}

    # Iterate over each non-terminal A in the grammar
    for A in diction:
        alpha = []
        beta = []

        # Separate rules into alpha (left recursive) and beta (non-left recursive)
        for rule in diction[A]:
            if rule[0] == A:
                alpha.append(rule[1:])
            else:
                beta.append(rule)

        # If there is left recursion (alpha is not empty), create a new non-terminal A' and update rules
        if len(alpha) != 0:
            newNT = A + "'"
            while newNT in diction.keys() or newNT in store.keys():
                newNT += "'"

            # Update beta rules with the new non-terminal A'
            for rule in beta:
                rule.append(newNT)
            
            # Update alpha rules with the new non-terminal A'
            for rule in alpha:
                rule.append(newNT)
            
            # Update the original grammar with beta rules
            diction[A] = beta
            
            # Add new non-terminal A' and its rules to the store
            store[newNT] = alpha

    # Update the original grammar with the new non-terminals and rules
    for A in store:
        diction[A] = store[A]

    return diction

def LeftFactoring(diction):
    """
    Performs left factoring on the given grammar.

    Parameters:
    - diction: Dictionary representing the grammar rules.

    Returns:
    Modified grammar after left factoring.
    """
    new_diction = {}

    # Iterate over each non-terminal A in the grammar
    for A in diction:
        all_rules = diction[A]
        temp = dict()

        # Group rules based on their starting terminal
        for rule in all_rules:
            if rule[0] not in temp.keys():
                temp[rule[0]] = [rule]
            else:
                temp[rule[0]].append(rule)

        new_rule = []
        temp_dict = {}

        # Check for common prefixes and factor them out
        for key in temp:
            allStartingWithTermKey = temp[key]

            if len(allStartingWithTermKey) > 1:
                A_new = A + "'"
                while(A_new in diction.keys() or A_new in new_diction.keys()):
                    A_new += "'"

                # Add a new non-terminal A' for the common prefix
                new_rule.append([key, A_new])

                ex_rules = []

                # Update rules to exclude the common prefix
                for rule in allStartingWithTermKey:
                    ex_rules.append(rule[1:])

                # Store the updated rules for the new non-terminal A'
                temp_dict[A_new] = ex_rules
            else:
                new_rule.append(allStartingWithTermKey[0])

        # Update the original grammar with the new non-terminals and rules
        new_diction[A] = new_rule

        for key in temp_dict:
            new_diction[key] = temp_dict[key]

    return new_diction

def first(rule):
    """
    Compute the FIRST set for a given non-terminal symbol or production rule.

    Parameters:
    - rule (str): The production rule or non-terminal symbol.

    Returns:
    - list: The FIRST set for the given rule.
    """
    global rules, nonterm_userdef, term_userdef, diction, firsts
    stack = [rule]
    result = []

    while stack:
        current_rule = stack.pop(0)

        if len(current_rule) != 0 and (current_rule is not None):
            # If the first character of the rule is a terminal, add it to the result.
            if current_rule[0] in term_userdef:
                result.append(current_rule[0])
            # If epsilon is encountered, add it to the result.
            elif current_rule[0] == '#':
                result.append('#')

        if len(current_rule) != 0:
            if current_rule[0] in list(diction.keys()):
                # If the current symbol is a non-terminal, expand its rules.
                rhs_rules = diction[current_rule[0]]
                for itr in rhs_rules:
                    stack.insert(0, itr)

                # If epsilon is not in the result, continue; otherwise, remove epsilon and proceed.
                if '#' not in result:
                    continue
                else:
                    result.remove('#')
                    if len(current_rule) > 1:
                        # Recursively compute FIRST for the remaining part of the rule.
                        ans_new = first(current_rule[1:])
                        if ans_new is not None:
                            if type(ans_new) is list:
                                result += ans_new
                            else:
                                result += [ans_new]
                        else:
                            continue
                    else:
                        # If the rule is fully processed, add epsilon back to the result.
                        result.append('#')

    return result

def follow(nt):
    """
    Compute the FOLLOW set for a given non-terminal symbol.

    Parameters:
    - nt (str): The non-terminal symbol.

    Returns:
    - list: The FOLLOW set for the given non-terminal symbol.
    """
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    stack = [nt]
    solset = set()
    processed = set()

    while stack:
        current_nt = stack.pop()
        if current_nt == start_symbol:
            # If the current non-terminal is the start symbol, add the end-of-input marker to the FOLLOW set.
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
                            # If the next symbol is a terminal, add it to the FOLLOW set.
                            solset.add(subrule[0])
                            break

                        if not subrule:
                            # If the current non-terminal is at the end of a production, backtrack to its parent non-terminal.
                            stack.append(curNT)
                        elif subrule[0] in nonterm_userdef:
                            # If the next symbol is a non-terminal, push it to the stack.
                            stack.append(subrule[0])

    return list(solset)

def computeAllFirsts():
    """
    Compute the FIRST sets for all non-terminal symbols based on the given grammar rules.
    Also, perform left recursion elimination and left factoring on the grammar.
    """
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

    print(f"\nRules: \n")
    for y in diction:
        production = ''
        for x in diction[y]:
            production += f"{' '.join(x)} | "
        production = production[:-2]
        print(f"{y} -> {production}")
    print()

    diction = removeLeftRecursion(diction)
    print(f"\nAfter elimination of left recursion:\n")
    for y in diction:
        production = ''
        for x in diction[y]:
            production += f"{' '.join(x)} | "
        production = production[:-2]
        print(f"{y} -> {production}")
    print()

    diction = LeftFactoring(diction)
    print("\nAfter left factoring:\n")
    for y in diction:
        production = ''
        for x in diction[y]:
            production += f"{' '.join(x)} | "
        production = production[:-2]
        print(f"{y} -> {production}")
    print()

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

    print("\nCalculated firsts:\n")
    key_list = list(firsts.keys())
    index = 0
    for gg in firsts:
        print(f"first({key_list[index]}) => {firsts.get(gg)}")
        index += 1
    print()

def computeAllFollows():
    """
    Compute the FOLLOW sets for all non-terminal symbols based on the given grammar rules.
    """
    global start_symbol, rules, nonterm_userdef, term_userdef, diction, firsts, follows
    for NT in diction:
        solset = set()
        sol = follow(NT)
        if sol is not None:
            for g in sol:
                solset.add(g)
        follows[NT] = solset

    print("\nCalculated follows:\n")
    key_list = list(follows.keys())
    index = 0
    for gg in follows:
        print(f"follow({key_list[index]}) => {follows[gg]}")
        index += 1
    print()

def createParseTable():
    """
    Create the LL(1) parsing table based on the given grammar rules, FIRST sets, and FOLLOW sets.

    Returns:
    - tuple: A tuple containing the parsing table, the list of terminals, and a flag indicating whether the grammar is LL(1).
    """
    global diction, firsts, follows, term_userdef
    print("\nFirsts and Follow Result table:\n")
    
    # Determine the maximum length of FIRST and FOLLOW sets for formatting the output table.
    mx_len_first = max(len(str(firsts[u])) for u in diction)
    mx_len_fol = max(len(str(follows[u])) for u in diction)

    # Print the FIRST and FOLLOW sets for each non-terminal.
    print_table(['Non-Terminal', 'FIRST', 'FOLLOW'], [[u, str(firsts[u]), str(follows[u])] for u in diction])
    print()

    # Extract non-terminals, prepare a list of terminals (excluding certain symbols), and initialize the parsing table matrix.
    ntlist = list(diction.keys())
    terminals = copy.deepcopy(term_userdef)
    # Remove specific symbols from the list of terminals.
    remove_symbols = ['(', ')', '+', '/', '=', '1', '2', '0', ';', '>', 'end while']
    for symbol in remove_symbols:
        terminals.remove(symbol)
    terminals.append('$')

    mat = [['' for _ in terminals] for _ in ntlist]
    grammar_is_LL = True

    # Fill in the LL(1) parsing table.
    for lhs in diction:
        rhs = diction[lhs]
        for y in rhs:
            res = first(y)

            # Handle epsilon in FIRST set by combining FOLLOW set.
            if '#' in res:
                if type(res) == str:
                    firstFollow = [res]
                    fol_op = follows[lhs]
                    if type(fol_op) == str:
                        firstFollow.append(fol_op)
                    else:
                        firstFollow.extend(fol_op)
                    res = firstFollow
                else:
                    res.remove('#')
                    res.extend(follows[lhs])

            ttemp = []
            if type(res) is str:
                ttemp.append(res)
                res = copy.deepcopy(ttemp)

            for c in res:
                xnt = ntlist.index(lhs)
                yt = terminals.index(c)
                if mat[xnt][yt] == '':
                    mat[xnt][yt] += f"{lhs}->{' '.join(y)}"
                else:
                    if f"{lhs}->{y}" in mat[xnt][yt]:
                        continue
                    else:
                        grammar_is_LL = False
                        mat[xnt][yt] += f",{lhs}->{' '.join(y)}"

    # Print the generated parsing table.
    print("\nGenerated parsing table:\n")
    print_table(['Non-Terminal', *terminals], [[ntlist[i], *mat[i]] for i in range(len(ntlist))])
    print()

    return mat, terminals, grammar_is_LL

def validateStringUsingStackBuffer(parsing_table, grammarll1, table_term_list, input_string, term_userdef, start_symbol):
    """
    Validate an input string using the LL(1) parsing table and the given grammar.

    Parameters:
    - parsing_table (list): The LL(1) parsing table.
    - grammarll1 (bool): A flag indicating whether the grammar is LL(1).
    - table_term_list (list): The list of terminals.
    - input_string (str): The input string to validate.
    - term_userdef (list): The list of user-defined terminal symbols.
    - start_symbol (str): The start symbol of the grammar.

    Returns:
    - tuple: A tuple containing the result message and the list of parsing steps.
    """
    print("\nValidate String:\n")

    if not grammarll1:
        return f"\nInput String = \"{input_string}\"\nGrammar is not LL(1)"

    stack = [start_symbol, '$']
    buffer = []
    input_string = input_string.split()
    input_string.reverse()
    buffer = ['$'] + input_string
    parsingSteps = []

    while True:
        if stack == ['$'] and buffer == ['$']:
            parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), "Valid"])
            result = "\nValid String!"
            return result, parsingSteps
        elif stack[0] not in term_userdef:
            x = list(diction.keys()).index(stack[0])
            y = table_term_list.index(buffer[-1])
            if parsing_table[x][y] != '':
                entry = parsing_table[x][y]
                parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), copy.deepcopy(entry)])
                lhs_rhs = entry.split("->")
                lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                entryrhs = lhs_rhs[1].split()
                stack = entryrhs + stack[1:]
            else:
                result = f"\nInvalid String! No rule at Table[{stack[0]}][{buffer[-1]}]."
                return result, parsingSteps
        else:
            if stack[0] == buffer[-1]:
                parsingSteps.append([copy.deepcopy(' '.join(buffer)), copy.deepcopy(' '.join(stack)), f"Matched:{stack[0]}"])
                buffer = buffer[:-1]
                stack = stack[1:]
            else:
                result = "\nInvalid String! Unmatched terminal symbols"
                return result, parsingSteps


if __name__ == "__main__":
    lexicalAnalyzer()
    construct_grammar()
    computeAllFirsts()
    computeAllFollows()
    mat, terminals, grammar_is_LL = createParseTable()
    result, parsingSteps = validateStringUsingStackBuffer(
        parsing_table=mat,
        grammarll1=grammar_is_LL,
        table_term_list=terminals,
        input_string=input_string,
        term_userdef=term_userdef,
        start_symbol=start_symbol
    )
    print_table(['Input', 'Stack', 'Action'], parsingSteps)
    print()
    print(result)
