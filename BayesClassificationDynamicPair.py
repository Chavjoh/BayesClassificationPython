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
        self.className = keys['className']
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
        :param dataSetPath: Path to data set folder that contains positive and negative folder messages.
        :type dataSetPath: str
        :param isTagged: Indicate if dataSet is tagged (Different file structure)
        :type isTagged: bool
        :return: object
        """
        if dataSetPath[-1] != "/":
            dataSetPath += "/"

        # classes are directories names
        self.classes = ['positive', 'negative']
        self.data = {}

        self.testSuccess = {}

        self.isTagged = isTagged

        self.dataPath = dataSetPath
        # self.positivePath = self.dataPath + "/positive"
        # self.negativePath = self.dataPath + "/negative"

        self.wordsProbability = {}
        # self.wordsProbabilityPositive = {}
        # self.wordsProbabilityNegative = {}

        self.load(self.dataPath)

    def load(self, path):

        if path[-1] == "/":
            path = path[0:-1]

        # print("Directory" + path)
        for (directoryPath, subDirectoryList, fileNameList) in walk(path):

            # Debug
            # print(fileNameList)
            # print(directoryPath)
            # print(subDirectoryList)
            directorySplit = directoryPath.split("/")[-1]
            if directorySplit in self.classes:

                random.shuffle(fileNameList)

                for index, fileName in enumerate(fileNameList):
                    # print(directoryPath + '/' + fileName)
                    fileContent = ''.join(open(directoryPath + '/' + fileName, 'r', encoding="utf-8").readlines())

                    currentDataFile = DataFile(
                        fileContent=fileContent,
                        className=directorySplit,
                        isTagged=self.isTagged
                    )
                    try:
                        self.data[directorySplit].append(currentDataFile)
                    except:
                        self.data[directorySplit] = [currentDataFile]

            for subDirectory in subDirectoryList:
                self.load(path + "/" + subDirectory)

            break

    def calculateProbability(self):
        """
        Calculate the probability for each word to be positive of negative
        :return: None
        """

        for className in self.classes:
            self.wordsProbability[className] = {}
            maxIndex = int(0.8 * len(self.data[className]))

            # 80% of data used for training
            wordsAll = self.reduceWordsCount(self.data[className][:maxIndex])

            for word, number in wordsAll.items():
                self.wordsProbability[className][word] = \
                    (wordsAll[word] + 1) / (sum(wordsAll.values()) + len(wordsAll))

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

        for className in self.classes:
            maxIndex = int(0.8 * len(self.data[className]))

            for data in self.data[className][maxIndex:]:
                if self.classify(data) == className:
                    try:
                        self.testSuccess[className] += 1
                    except KeyError:
                        self.testSuccess[className] = 1

    def evaluate(self):
        """
        Accuracy calculation to evaluate training algorithm
        :return: float
        """
        # accuracy = self.testSuccess / (len(self.dataPositive) + len(self.negativePath))
        accuracy = sum(self.testSuccess.values())/sum(len(v) for v in self.data.values())
        return accuracy

    def classify(self, dataFile):
        """
        Classify a dataFile to positive or negative

        :param dataFile: DataFile to classify
        :type dataFile: DataFile
        :return: True if positive, False otherwise
        """

        # Initialization
        probability = {}
        maxClass = None

        for className in self.classes:
            probability[className] = 1

            for word, wordProbability in self.wordsProbability[className].items():
                try:
                    probability[className] *= pow(wordProbability, dataFile.wordsCount[word])
                except KeyError:
                    pass

            if not maxClass or (probability[maxClass] < probability[className]):
                maxClass = className

        return maxClass

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