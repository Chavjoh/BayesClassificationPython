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
import math
import codecs

#------------------------------------------------------------------------------#
#                                                                              #
#                                   CLASSES                                    #
#                                                                              #
#------------------------------------------------------------------------------#
from pip._vendor.distlib.util import in_venv


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
        self.exceptionWords = keys['wordException']
        self.words = []
        self.wordsCount = {}

        if keys['isTagged']:
            self.loadTagged()
        else:
            self.load()

        self.removeExceptionWords()

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

    def removeExceptionWords(self):
        exception = []
        with codecs.open(self.exceptionWords, 'r', 'UTF-8') as file:
            exception = file.read().split("\r\n")

        for x in exception:
            try:
                self.words.remove(x)
            except ValueError:
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

        # print("+"+str(self.wordsCount))
        # print("+"+self.className+" "+str(self.words))

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

    def __init__(self, dataSetPath, isTagged, method):
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
        self.allWordList = []
        # self.wordsProbabilityPositive = {}
        # self.wordsProbabilityNegative = {}

        self.method = method

        self.debug = False
        self.load(self.dataPath)

        self.inventoryWord()

        if self.debug:
            for className in self.classes:
                print(str(className)+" "+str(len(self.data[className])))

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

                if not self.debug:
                    random.shuffle(fileNameList)

                for index, fileName in enumerate(fileNameList):
                    # print(directoryPath + '/' + fileName)
                    fileContent = ''.join(open(directoryPath + '/' + fileName, 'r', encoding="utf-8").readlines())

                    currentDataFile = DataFile(
                        fileContent=fileContent,
                        className=directorySplit,
                        isTagged=self.isTagged,
                        wordException=directoryPath+"/../uselessWords.txt"
                    )

                    try:
                        self.data[directorySplit].append(currentDataFile)
                    except:
                        self.data[directorySplit] = [currentDataFile]

            for subDirectory in subDirectoryList:
                self.load(path + "/" + subDirectory)

            break

    def calculateProbability(self, tab):
        """
        Calculate the probability for each word to be positive of negative
        :return: None
        """

        for className in self.classes:
            self.wordsProbability[className] = {}

            maxIndex = int(0.8 * len(self.data[className]))

            # 80% of data used for training
            wordsAll = self.reduceWordsCount(self.data[className][:maxIndex])
            if self.debug:
                print("- "+className+" "+str(wordsAll))

            for word, number in wordsAll.items():
                self.wordsProbability[className][word] = \
                    (wordsAll[word] + 1) / (sum(wordsAll.values()) + len(wordsAll))

            if self.debug:
                print(className + " " + str(self.wordsProbability[className]))

    def reduceWordsCount(self, dataList):
        """
        Reduce the count of all words to one dictionary
        :param dataList: DataFile list to reduce
        :type dataList: list of dataFile
        :return: None
        """

        wordsAll = self.inventoryWord()

        for data in dataList:
            # print("+"+str(data.wordsCount))
            for word, value in data.wordsCount.items():
                wordsAll[word] += value

        return wordsAll

    def division(self):
        self.train(0, (len(self.data)/2)*0.8)
        return self.test((len(self.data)/2)*0.8,len(self.data)/2 )

    def crossValidation(self):

        result = 0
        n = 5

        dataTrain = {}
        

        minIndex = 0
        maxIndex = (len(self.data)/2)/n

        for i in range(0, n):
            self.train()
            result += self.test()/n
        return result

    def train(self, tab):
        """
        Training for Bayes algorithm

        :return: None
        """

        self.calculateProbability(tab)

    def test(self, tab):
        """
        Testing results from bayes algorithm
        Save number of correct values

        :return: None
        """

        for className in self.classes:
            maxIndex = int(0.8 * len(self.data[className]))

            self.testSuccess[className] = 0

            for data in self.data[className][maxIndex:]:
                if self.classify(data) == className:
                    self.testSuccess[className] += 1

    def evaluate(self):
        """
        Accuracy calculation to evaluate training algorithm
        :return: float
        """
        # accuracy = self.testSuccess / (len(self.dataPositive) + len(self.negativePath))
        accuracy = sum(self.testSuccess.values())/math.ceil(0.2*sum(len(v) for v in self.data.values()))

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

    def inventoryWord(self):
        # TODO optimization
        dict = {}
        for className,data in self.data.items():
            for dataFile in data:
                for word in dataFile.wordsCount.keys():
                    dict[word] = 0

        return dict

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
    dataSet = DataSet("./dataFull/normal", False, 'division')
    # print(dataSet.dataPositive[500])
    dataSet.train()
    dataSet.test()
    print("Evaluation accuracy (normal) : " + str(dataSet.evaluate()))

    #
    # TAGGED DATA SET
    #
    dataSetTagged = DataSet("./dataFull/tagged", True, 'division')
    # print(dataSetTagged.dataPositive[500])
    dataSetTagged.train()
    dataSetTagged.test()
    print("Evaluation accuracy (tagged) : " + str(dataSetTagged.evaluate()))

    #
    # NORMAL DATA SET
    #
    dataSet = DataSet("./dataFull/normal", False, 'cross')
    # print(dataSet.dataPositive[500])
    dataSet.train()
    dataSet.test()
    print("Evaluation accuracy (normal) : " + str(dataSet.evaluate()))

    #
    # TAGGED DATA SET
    #
    dataSetTagged = DataSet("./dataFull/tagged", True, 'cross')
    # print(dataSetTagged.dataPositive[500])
    dataSetTagged.train()
    dataSetTagged.test()
    print("Evaluation accuracy (tagged) : " + str(dataSetTagged.evaluate()))