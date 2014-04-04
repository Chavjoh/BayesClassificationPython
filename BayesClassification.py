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
import random

#------------------------------------------------------------------------------#
#                                                                              #
#                                   CLASSES                                    #
#                                                                              #
#------------------------------------------------------------------------------#


class DataFile:
    """ Contains file analysis information """

    def __init__(self, fileLine, isPositive):
        """
        Create a new DataFile
        :param fileLine: Data file content (=message) in one line
        :type fileLine: str
        :param isPositive: True if positive message, False otherwise
        :type isPositive: bool
        :rtype: str
        """
        self.isPositive = isPositive
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
        information = "Input file : " + self.fileLine + "\n"
        information += "============" + "\n"

        for key, value in self.wordsCount.items():
            information += str(key) + " " + str(value) + "\n"

        information += "============" + "\n"
        information += "Word count : " + str(self.sumWords) + "\n"

        return information

class DataSet:
    """ Contains all DataFile """

    def __init__(self, dataSetPath):
        """
        :param dataSetPath: Path to data set folder that contains positive and negative folder messages
        :type dataSetPath: str
        :return: object
        """
        self.dataPositive = []
        self.dataNegative = []
        self.dataPath = dataSetPath
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
                isPositive = True if directoryPath == self.positivePath else False

                random.shuffle(fileNameList)

                for index, fileName in enumerate(fileNameList):
                    # print(directoryPath + '/' + fileName)
                    fileContent = ''.join(open(directoryPath + '/' + fileName, 'r', encoding="utf-8").readlines())

                    if isGood:
                        self.dataPositive.append(DataFile(fileContent, isGood))
                    else:
                        self.dataNegative.append(DataFile(fileContent, isGood))


            for subDirectory in subDirectoryList:
                self.load(path + "/" + subDirectory)

            break

    def train(self):
        """
        Training for Bayes algorithm

        :return: null
        """
        maxIndexPositive = int(0.8 * self.dataPositive.count())
        maxIndexNegative = int(0.8 * self.dataNegative.count())

        for data in (self.dataPositive[:maxIndexPositive] + self.dataNegative[:maxIndexNegative]):

            pass

    def test(self):
        """
        Testing results from bayes algorithm

        :return: null
        """
        maxIndexPositive = int(0.8 * self.dataPositive.count())
        maxIndexNegative = int(0.8 * self.dataNegative.count())

        for data in (self.dataPositive[maxIndexPositive:] + self.dataNegative[maxIndexNegative:]):

            pass

    def classify(self, dataFile):
        """
        Classify a dataFile to positive or negative

        :param dataFile: DataFile to classify
        :return: True if positive, False otherwise
        """

        pass

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

    random.seed()

    dataSet = DataSet("./data")
    print(dataSet.dataPositive[500])
