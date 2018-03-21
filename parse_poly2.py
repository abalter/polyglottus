import re
import sys
import yaml

def debug(s):
    if verbose:
        print(s)

verbose = False

#block_open_pattern = '(^%%)?[\s]?([a-zA-Z_]?[a-zA-Z0-9_]*)(:)?$'
special_character = "~"
block_open_pattern = '(^%%)?[\s]?([a-zA-Z_]?[a-zA-Z0-9_]*)(' + special_character + ')?$'
block_close_pattern = '(^\/%%$)?'
meta_open_pattern = "(^" + special_character + "-+" + ")?$"
meta_close_pattern = "(^" + "-+" + special_character + ")?$"

line = ""

def isBlockOpen(line):
    debug("in isBlockOpen")
    matches = re.findall(block_open_pattern, line)[0]
    debug(matches)
    if matches[0] == '%%' and matches[1] != '':
        return matches
    else:
        return False

def isBlockClose(line):
    debug("in isBlockClose")
    matches = re.findall(block_close_pattern, line)[0]
    debug(matches)
    return matches

def isMetaOpen(line):
    debug("in isMetaOpen")
    matches = re.findall(meta_open_pattern, line)[0]

    debug(matches)
    if matches is not '':
        return matches
    else:
        return False

def isMetaClose(line):
    debug("in isMetaClose")
    matches = re.findall(meta_close_pattern, line)[0]
    debug(matches)
    if matches is not '':
        return matches
    else:
        return False

def findNextBlock():
    for line in f:
        debug("line: " + line)
        matches = isBlockOpen(line)
        if matches:
            processor = matches[1] or False
            is_meta = (matches[2] == special_character)

            debug("processor: " + str(processor))
            debug("is_meta: " + str(is_meta))
            return line

def parseBlockOpen(line):
    matches = isBlockOpen(line)
    processor = matches[1]
    is_meta = (matches[2] == special_character)

    debug("processor: " + str(processor))
    debug("is_meta: " + str(is_meta))

    return processor, is_meta


def getMeta():
    debug("in getMeta")
    meta = ""
    line = f.readline()
    debug(line)
    imo = isMetaOpen(line)
    debug("imo: " + str(imo))
    if not imo:
        print("ERRRRORRRR in meta formatting")
        return False

    debug("reading meta")
    for line in f:
        debug(line)
        imc = isMetaClose(line)
        debug("imc: " + str(imc))
        if imc:
            debug("meta close")
            break
        else:
            meta += line
            debug("meta: " + meta)

    return meta


def getCode():
    debug("in getCode")
    code = ""
    for line in f:
        debug("line: " + line)
        if isBlockClose(line):
            break
        else:
            code += line

    return code



text = """
blah

%%shell1
a=10
%%

blah
blah

blah

You can import variables by doing:

%%R1~
~---
imports:
    myvar: shell1.var1
    the_title: shell1.a
    data: python1.data
stdout: hide
stderr: show
graphics: inline
---~
plot(data);
title(the_title);
/%%

blah
blah
"""


f = open("small_parse_test.txt")
for line in f:
#    print("line" + line)
    temp = findNextBlock()
#    print("temp: " + str(temp))
    if temp:
        p,im = parseBlockOpen(temp)
        print("p: " + str(p) + "  im: " + str(im))
        if im:
            meta = getMeta()
            print(meta)
            print(yaml.load(meta))
        print("getting code")
        c = getCode()
        print("code")
        print(c)
    else:
        break


"""
line = findNextBlock()
print(line)
p,im = parseBlockOpen(line)
print("p: " + str(p) + "  im: " + str(im))
if im:
    print(getMeta())

line = findNextBlock()
print(line)
p,im = parseBlockOpen(line)
print("p: " + str(p) + "  im: " + str(im))
if im:
    meta = getMeta()
print(meta)

print(yaml.load(meta))
"""