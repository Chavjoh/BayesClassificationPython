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

    def __init__(self, **keys):
        """
        Create a new DataFile
        :param fileContent: Data file content (=message)
        :type fileContent: str
        :param isPositive: True if positive message, False otherwise
        :type isPositive: bool
        :rtype: str
        """
        self.isPositive = keys['isPositive']
        self.fileContent = keys['fileContent']
        self.words = []
        self.wordsCount = {}

        if keys['isTagged']:
            self.loadTagged()
        else:
            self.load()

        self.sumWords = sum(self.wordsCount.values())

    def load(self):

        self.words = self.fileContent.split()

        for word in self.words:
            try:
                self.wordsCount[word] += 1
            except KeyError:
                self.wordsCount[word] = 1

    def loadTagged(self):
        # TODO
        pass

    def __repr__(self):
        information = "Input file : " + self.fileContent + "\n"
        information += "============" + "\n"

        for key, value in self.wordsCount.items():
            information += str(key) + " " + str(value) + "\n"

        information += "============" + "\n"
        information += "Word count : " + str(self.sumWords) + "\n"

        return information

class DataSet:
    """ Contains all DataFile """

    def __init__(self, dataSetPath, isTagged):
        """
        :param dataSetPath: Path to data set folder that contains positive and negative folder messages
        :type dataSetPath: str
        :param isTagged: Indicate if dataSet is tagged (Different file structure)
        :type isTagged: bool
        :return: object
        """
        self.testSuccess = 0
        self.dataPositive = []
        self.dataNegative = []
        self.isTagged = isTagged
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

                    if isPositive:
                        self.dataPositive.append(DataFile(
                            fileContent=fileContent,
                            isPositive=isPositive,
                            isTagged=self.isTagged
                        ))
                    else:
                        self.dataNegative.append(DataFile(
                            fileContent=fileContent,
                            isPositive=isPositive,
                            isTagged=self.isTagged
                        ))

            for subDirectory in subDirectoryList:
                self.load(path + "/" + subDirectory)

            break

    def train(self):
        """
        Training for Bayes algorithm

        :return: null
        """
        maxIndexPositive = int(0.8 * len(self.dataPositive))
        maxIndexNegative = int(0.8 * len(self.dataNegative))

        for data in (self.dataPositive[:maxIndexPositive] + self.dataNegative[:maxIndexNegative]):
            # TODO
            pass

    def test(self):
        """
        Testing results from bayes algorithm
        Save number of correct values

        :return: null
        """
        maxIndexPositive = int(0.8 * len(self.dataPositive))
        maxIndexNegative = int(0.8 * len(self.dataNegative))

        for data in (self.dataPositive[maxIndexPositive:] + self.dataNegative[maxIndexNegative:]):
            # TODO
            # Update self.testSuccess
            pass

    def evaluate(self):
        """
        Accuracy calculation to evaluate training algorithm
        :return: float
        """
        accuracy = self.testSuccess / (len(self.dataPositive) + len(self.negativePath))

        return accuracy

    def classify(self, dataFile):
        """
        Classify a dataFile to positive or negative

        :param dataFile: DataFile to classify
        :type dataFile: DataFile
        :return: True if positive, False otherwise
        """

        # TODO
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

    dataSet = DataSet("./data", False)
    # print(dataSet.dataPositive[500])
    dataSet.train()
    dataSet.test()
    print(dataSet.evaluate())

    dataSetTagged = DataSet("./data/tagged", True)
    # print(dataSet.dataPositive[500])
    dataSetTagged.train()
    dataSetTagged.test()
    print(dataSetTagged.evaluate())