import re
import sys
import yaml

class PolyParser(object):

    def __init__(self, file, verbose=False):

        #cell_open_pattern = '(^%%)?[\s]?([a-zA-Z_]?[a-zA-Z0-9_]*)(:)?$'
        self.special_character = "~"

        self.cell_open_pattern = '' \
            + '(^%%)?[\s]?([a-zA-Z_]?[a-zA-Z0-9_]*)(' \
            + self.special_character \
            + ')?$'

        self.cell_close_pattern = '(^\/%%$)'

        self.meta_open_pattern = '' \
            + "(^" \
            + self.special_character \
            + "-+" \
            + ")?$"

        self.meta_close_pattern = '' \
            + "(^" \
            + "-+" \
            + self.special_character \
            + ")?$" \

        self.line = ""

        self.f = open(file)

        self.verbose = verbose


    def debug(self, s):
        if self.verbose:
            print(s)

    def parseFile(self):
        self.debug("in parseFile")
        for line in self.f:
            self.debug("line: " + line)
            cell_open = self.findNextCell()
            self.debug("temp: " + str(cell_open))
            if cell_open:
                processor, is_meta = self.parseCellOpen(cell_open)
                self.debug("processor: " + processor + "  is_meta: " + str(is_meta))
                print("\n---------- " + processor.upper() + " -----------\n")
                if is_meta:
                    meta = self.getMeta()
                    self.debug(meta)
                    print("META:")
                    print(yaml.load(meta))
                self.debug("getting code")
                code = self.getCode()
                print()
                print("CODE")
                print(code)
                print("----------------------------------\n")
            else:
                break

    def getNextCell(self):
        self.debug("in getNextCell")
        cell_open = self.findNextCell()
        self.debug("temp: " + str(cell_open))
        if cell_open:
            processor, is_meta = self.parseCellOpen(cell_open)
            self.debug("processor: " + processor + "  is_meta: " + str(is_meta))
            if is_meta:
                meta = self.getMeta()
                self.debug(meta)
                meta = yaml.load(meta)
            else:
                meta = None
            self.debug("getting code")
            code = self.getCode()
            cell_data = dict \
            (
                processor=processor,
                meta=meta,
                code=code
            )
        else:
            cell_data = None

        return cell_data


    def isCellOpen(self, line):
        self.debug("in isCellOpen")
        matches = re.findall(self.cell_open_pattern, line)[0]
        self.debug(matches)
        if matches[0] == '%%' and matches[1] != '':
            return matches
        else:
            return False

    def isCellClose(self, line):
        self.debug("in isCellClose")
        matches = re.findall(self.cell_close_pattern, line)
        self.debug(matches)
        if len(matches) > 0 and matches[0] == '/%%':
            return True
        else:
            return False

    def isMetaOpen(self, line):
        self.debug("in isMetaOpen")
        matches = re.findall(self.meta_open_pattern, line)[0]

        self.debug(matches)
        if matches is not '':
            return matches
        else:
            return False

    def isMetaClose(self, line):
        self.debug("in isMetaClose")
        matches = re.findall(self.meta_close_pattern, line)[0]
        self.debug(matches)
        if matches is not '':
            return matches
        else:
            return False

    def findNextCell(self):
        self.debug("in findNextCell")
        for line in self.f:
            self.debug("line: " + line)
            matches = self.isCellOpen(line)
            if matches:
                processor = matches[1] or False
                is_meta = (matches[2] == self.special_character)

                self.debug("processor: " + str(processor))
                self.debug("is_meta: " + str(is_meta))
                return line

    def parseCellOpen(self, line):
        matches = self.isCellOpen(line)
        processor = matches[1]
        is_meta = (matches[2] == self.special_character)

        self.debug("processor: " + str(processor))
        self.debug("is_meta: " + str(is_meta))

        return processor, is_meta

    def getMeta(self):
        self.debug("in getMeta")
        meta = ""
        line = self.f.readline()
        self.debug(line)
        imo = self.isMetaOpen(line)
        self.debug("imo: " + str(imo))
        if not imo:
            print("ERRRRORRRR in meta formatting")
            return False

        self.debug("reading meta")
        for line in self.f:
            self.debug(line)
            is_meta_close = self.isMetaClose(line)
            self.debug("is_meta_close: " + str(is_meta_close))
            if is_meta_close:
                self.debug("meta close")
                break
            else:
                meta += line
                self.debug("meta: " + meta)

        return meta

    def getCode(self):
        self.debug("in getCode")
        code = ""
        for line in self.f:
            self.debug("line: " + line)
            if self.isCellClose(line):
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


#pp = PolyParser("small_parse_test.txt", verbose=False)
#pp.parseFile()


pp = PolyParser('poly-magic5.poly')
#pp.parseFile()

"""
for line in f:
#    print("line" + line)
    temp = findNextCell()
#    print("temp: " + str(temp))
    if temp:
        p,im = parseCellOpen(temp)
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
"""
line = findNextCell()
print(line)
p,im = parseCellOpen(line)
print("p: " + str(p) + "  im: " + str(im))
if im:
    print(getMeta())

line = findNextCell()
print(line)
p,im = parseCellOpen(line)
print("p: " + str(p) + "  im: " + str(im))
if im:
    meta = getMeta()
print(meta)

print(yaml.load(meta))
"""