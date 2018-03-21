import re
import sys

debug = lambda x: print(x if verbose else '', end='')

verbose = True

def matchRE(pattern, text):
    debug("in matchRE\n")
    try:
        match = re.match(pattern, text)
        groups = match.groups()
        debug("groups:\n")
        debug(groups)
        debug("\n")
        return groups
    except AttributeError:
        return ()

def isBeginBlock(line):
    debug("isBeginBlock\n")
    ### Pattern looks for:
    ### 1. line starts with %%
    ### 2. a string of text after that
    ### 3. Includes anything that might be in a python function call
    ### 4. whitespace
    ### 5. Ends in a newline

    ### Patern captures only the function and function call
    #pattern = '^%%[\s]*([a-zA-Z_][a-zA-Z0-9_\(\)\{\}\[\]:,= ]+)[\s]*\n$'
    pattern = '^%%[\s]?([a-zA-Z_][a-zA-Z0-9_]+)(:)?\n$'
    matches = matchRE(pattern, line)
    debug(matches)
    if len(matches) == 1:
        return matches[0], ''
    elif len(matches) == 2:
        return matches[0], matches[1]
    else:
        return False

def parseProcessor(block_opener):
    debug("in parseProcessor\n")
    debug(block_opener + "\n")
    pattern = '^%%([a-zA-Z_][a-zA-Z0-9_]+)\((.*?)\)'
    groups = matchRE(pattern, block_opener)
    debug("groups")
    debug(str(groups))
    processor = groups[0]
    if groups[2] is not '':
        kwargs = parseKWArgs(groups[2])
    else:
        kwargs = {}
    return processor, kwargs

def parseBlockDirectives()


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

def parsePoly(filename):
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
                debug("\n-------------------------\n")
    #            print("begin")
                opening = isBeginBlock(line)
                debug("opening: " + opening + "\n")
#                processor, kwargs = parseProcessor(opening)
#                debug("processor: " + processor + "\n")
#                debug("kwargs: " + kwargs + "\n")
                in_code = True
                line = f.readline()
                if not line:
                    break

            if isEndBlock(line):
                debug(code_block)
                debug("\n")
                debug("--------------------\n\n")
    #            print("end")
                closing = line
                ########
                ##executeCode(opening, code_block, closing)
                ########
                code_block = ""
                in_code = False

            if in_code:
    #            print("in code")
                code_block += line


if __name__ == "__main__":
#    print(sys.argv)
#    print(len(sys.argv))

    if len(sys.argv) == 1 or sys.argv[1] == '':
        filename = "polycode-magic.poly"
    else:
        filename = sys.argv[1]

    parsePoly(filename)



"""
1) Check if of the form processor[:]
2) if there a colon, then read stuff between --- and ---
3) return (will process as yaml)

Maybe findNextBlock, parseProcessor, parseBlockMeta, parseCodeBlock  back to beginning until end
"""