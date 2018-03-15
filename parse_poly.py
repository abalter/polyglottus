import re

def matchRE(pattern, text):
    try:
        match = re.match(pattern, text)
        groups = match.groups()
        return groups
    except AttributeError:
        return ()
        
def isBeginBlock(line):
    ### Pattern looks for:
    ### 1. line starts with %%
    ### 2. a string of text after that 
    ### 3. Includes anything that might be in a python function call
    ### 4. whitespace
    ### 5. Ends in a newline
    
    ### Patern captures only the function and function call
    pattern = '^%%[\s]*([a-zA-Z_][a-zA-Z0-9_\(\)\{\}\[\]:,= ]+)[\s]*\n$'
    matches = matchRE(pattern, line)
    if len(matches) == 1:
        return matches[0]
    else:
        return False

def isEndBlock(line):
    ### Pattern looks for:
    ### 1. line starts with /%%
    ### 2. whitespace
    ### 3. Ends in a newline
    
    ### Patern captures only the text
    #pattern = '^%%[\s]*([a-zA-Z_][a-zA-Z0-9_]+)[\s]*\n'
    pattern = '(^\/%%)'
    matches = matchRE(pattern, line)
    if len(matches) == 1:
        return True
    else:
        return False
    
def executeCode(opening, code_block, closing):
    ### This is where the cell would actually get run
    print("EXECUTING")
    print("opening: " + opening)
    print(code_block, end="")
    print("closing: " + closing, end="")
    print()
    ###

with open('polycode-magic.poly', 'r') as f:
    code_block = ""
    block_open = False
    block_close = False
    in_code = False
    n = 0
    
    while True:
        line = f.readline()
        if not line:
            break

        if isBeginBlock(line):
#            print("begin")
            opening = isBeginBlock(line)
            in_code = True
            line = f.readline()
            if not line:
                break
            
        if isEndBlock(line):
#            print("end")
            closing = line
            ########
            executeCode(opening, code_block, closing)
            ########
            code_block = ""
            in_code = False

        if in_code:
#            print("in code")
            code_block += line

            
