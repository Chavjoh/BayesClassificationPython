# !/usr/bin/python
# coding: latin-1

#------------------------------------------------------------------------------#
# Artificial Intelligence - Bayes Classification Algorithms                    #
# ============================================================================ #
# Organization: HE-Arc Engineering                                             #
# Developer(s): Etienne Frank                                                  #
#               Johan Chavaillaz                                               #
#                                                                              #
# Filename:     BayesClassification.py                                         #
# Version:      1.0                                                            #
#------------------------------------------------------------------------------#

#------------------------------------------------------------------------------#
#                                                                              #
#                               LIBRARIES IMPORT                               #
#                                                                              #
#------------------------------------------------------------------------------#

import sys
from os import walk

#------------------------------------------------------------------------------#
#                                                                              #
#                                   CLASSES                                    #
#                                                                              #
#------------------------------------------------------------------------------#


class DataFile:
    """ Contains file analysis information """
    def __init__(self, fileLine, isGood):
        """

        :rtype : object
        """
        self.isGood = isGood
        self.fileLine = fileLine
        self.wordsCount = {}

        self.words = fileLine.split()

        for word in self.words:
            try:
                self.wordsCount[word] += 1
            except KeyError:
                self.wordsCount[word] = 1

        self.sumWords = sum(self.wordsCount.values())

    def __repr__(self):
        print("input : "+self.fileLine)

        for key, val in self.wordsCount.items():
            print(str(key)+" "+str(val))

        print(str(self.sumWords))

        return ""

class DataSet:
    """ Contains all DataFile """

    def __init__(self):
        self.data = []
        self.dataPath = "./data"
        self.positivePath = self.dataPath + "/positive"
        self.negativePath = self.dataPath + "/negative"

        self.load(self.dataPath)

    def load(self, path):

        # print("Directory" + path)

        for (directoryPath, subDirectoryList, fileNameList) in walk(path):

            # Debug
            # print(fileNameList)
            # print(directoryPath)
            # print(subDirectoryList)

            if directoryPath in [self.positivePath, self.negativePath]:
                isGood = True if directoryPath == self.positivePath else False

                for fileName in fileNameList:
                    print(directoryPath + '/' + fileName)
                    fileContent = ''.join(open(directoryPath + '/' + fileName, 'r', encoding="utf-8").readlines())
                    self.data.append(DataFile(fileContent, isGood))

            for subDirectory in subDirectoryList:
                self.load(path + "/" + subDirectory)

            break

#------------------------------------------------------------------------------#
#                                                                              #
#                             UTILITIES FUNCTIONS                              #
#                                                                              #
#------------------------------------------------------------------------------#


#------------------------------------------------------------------------------#
#                                                                              #
#                               "MAIN" FUNCTION                                #
#                                                                              #
#------------------------------------------------------------------------------#

# If this is the main module, run this
if __name__ == '__main__':
    argsCount = len(sys.argv)
    argsIndex = 1

    dataset = DataSet()

