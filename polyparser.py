import sys
import yaml
import re

class PolyParser():

    def __init__(self):
        pass

    def loadFile(self, file):
        pass

    def findNextBlock(self):
        """read to start of next block"""
        pass

    def parseBlock(self, block):
        """collect processor, block meta, and code"""
        pass

    def isBlockOpen(self, line):
        """checks if line is a block opener"""
        pass

    def isBlockClose(self, line):
        """checks if line is a block closing"""
        pass

    def getProcessor(self, line):
        """collects the processor from the opening line"""
        pass

    def isStartMeta(self, line):
        """checks for start meta"""
        pass

    def isEndMeta(self, line):
        """checks for end meta"""
        pass

    def getNextBlock(self):
        """collect the next block"""
        pass

    def getAndExecuteNextBlock(self):
        """collect next block, parse meta, and execute"""
        pass

    def __del__(self):
        """break it down"""
        pass


