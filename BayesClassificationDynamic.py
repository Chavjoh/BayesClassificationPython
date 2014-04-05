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
import os
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
        self.classe = keys['classe']
        self.fileContent = keys['fileContent']
        self.words = []
        self.wordsCount = {}

        if keys['isTagged']:
            self.loadTagged()
        else:
            self.load()

        self.calculateWordsCount()
        self.wordsSum = sum(self.wordsCount.values())

    def load(self):
        """
        Load words from fileContent for file that contains only message
        :return: None
        """

        self.words = self.fileContent.split()

    def loadTagged(self):
        """
        Load words from fileContent for file that contains more information with message
        :return: None
        """
        for line in self.fileContent.split("\n"):
            try:
                self.words.append(line.split("\t")[2])
            except IndexError:
                pass

    def calculateWordsCount(self):
        """
        Calculate the number of occurrence of words.
        :return: None
        """

        for word in self.words:
            try:
                self.wordsCount[word] += 1
            except KeyError:
                self.wordsCount[word] = 1

    def __repr__(self):
        information = "Input file : " + self.fileContent + "\n"
        information += "============" + "\n"

        for key, value in self.wordsCount.items():
            information += str(key) + " " + str(value) + "\n"

        information += "============" + "\n"
        information += "Word count : " + str(self.wordsSum) + "\n"

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

        self.datas = []

        self.isTagged = isTagged

        self.dataPath = dataSetPath
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # find all directories
        self.wordsProbability = []  # array of dictionaries

        self.dirs = [name for name in os.listdir(self.dataPath) if os.path.isdir(os.path.join(self.dataPath, name))]
        if 'tagged' in self.dirs:
            self.dirs.remove('tagged')

        for i in range(len(self.dirs)):
            self.dirs[i] = self.dataPath+"/"+self.dirs[i]
            self.wordsProbability.append({})
            self.datas.append([])
        # print(self.dirs)
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        self.load(self.dataPath)

    # load files content
    def load(self, path):

        # parcours chaque repertoire
        #     chaque repertoire est une classe, donc plusieurs dataset
        for directory in self.dirs:
            classIndex = 0  # TODO should be integrated to the next for loop
            for (directoryPath, subDirectoryList, fileNameList) in walk(directory):
                random.shuffle(fileNameList)

                for index, fileName in enumerate(fileNameList):  # TODO index useless
                    # print(directoryPath + '/' + fileName)
                    fileContent = ''.join(open(directoryPath + '/' + fileName, 'r', encoding="utf-8").readlines())

                    self.datas[classIndex].append(DataFile(
                        fileContent=fileContent,
                        classe=classIndex,
                        isTagged=self.isTagged
                    ))

                classIndex += 1

    def calculateProbability(self):
        """
        Calculate the probability for each word to be positive of negative
        :return: None
        """
        maxIndex = []
        for data in self.datas:
            maxIndex.append(int(0.8 * len(data)))

        # 80% of data used for training
        wordsAll = []
        for index, data in enumerate(self.datas):
            wordsAll.append(self.reduceWordsCount(data[:maxIndex[index]]))  # lol if its works

        for index, blabla in enumerate(wordsAll):
            for word, number in blabla.items():  # number useless
                self.wordsProbability[index][word] = (blabla[word] + 1) / (sum(blabla.values()) + len(blabla))

    @staticmethod
    def reduceWordsCount(dataList):
        """
        Reduce the count of all words to one dictionary
        :param dataList: DataFile list to reduce
        :type dataList: list of dataFile
        :return: None
        """

        wordsAll = {}

        for data in dataList:
            for word, value in data.wordsCount.items():
                try:
                    wordsAll[word] += value
                except KeyError:
                    wordsAll[word] = value

        return wordsAll

    def train(self):
        """
        Training for Bayes algorithm

        :return: None
        """

        self.calculateProbability()

    def test(self):
        """
        Testing results from bayes algorithm
        Save number of correct values

        :return: None
        """

        maxIndex = []
        for data in self.datas:
            maxIndex.append(int(0.8 * len(data)))

        for index, datas in enumerate(self.datas):
            for data2 in datas:
                if self.classify(data2) == index:  # TODO FUCKED UP
                    self.testSuccess += 1

    def evaluate(self):
        """
        Accuracy calculation to evaluate training algorithm
        :return: float
        """
        somme = 0
        for data in self.datas:
            somme += len(data)

        accuracy = self.testSuccess / somme

        return accuracy

    def classify(self, dataFile):
        """
        Classify a dataFile to positive or negative

        :param dataFile: DataFile to classify
        :type dataFile: DataFile
        :return: True if positive, False otherwise
        """

        # Initialization
        probability = []
        for data in self.datas:
            probability.append(1)

        for index, wordsProbability in enumerate(self.wordsProbability):
            for word, probability2 in wordsProbability.items():
                try:
                    probability[index] *= pow(probability2, dataFile.wordsCount[word])
                except KeyError:
                    pass

        return max(probability)

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

    #
    # NORMAL DATA SET
    #
    dataSet = DataSet("./data", False)
    # print(dataSet.dataPositive[500])
    dataSet.train()
    dataSet.test()
    print("Evaluation accuracy (normal) : " + str(dataSet.evaluate()))

    #
    # TAGGED DATA SET
    #
    dataSetTagged = DataSet("./data/tagged/tagged", True)
    # print(dataSetTagged.dataPositive[500])
    dataSetTagged.train()
    dataSetTagged.test()
    print("Evaluation accuracy (tagged) : " + str(dataSetTagged.evaluate()))