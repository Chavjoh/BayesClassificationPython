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
import time
from collections import defaultdict



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
		:rtype: str
		"""
		# Class name (positive / negative)
		self.className = keys['className']
		
		# Content of the DataFile (text)
		self.fileContent = keys['fileContent']
		
		# Path of files that contains all exception words
		self.exceptionWords = keys['wordException']
		
		# List that contains all words
		self.words = []
		
		# Dictionary that contains apparition number of each word
		self.wordsCount = {}

		# Loading tagged or normal content
		if keys['isTagged']:
			self.loadTagged()
		else:
			self.load()

		# Remove useless words in text
		self.removeExceptionWords()
		
		# Clean useless variable in memory (no needed any more)
		self.fileContent = ""
		self.exceptionWords = []

		# Count each words
		self.calculateWordsCount()
		
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
		"""
		Calculate the number of occurrence of words.
		:return: None
		"""
		try:
			exception = []
			with codecs.open(self.exceptionWords, 'r', 'UTF-8') as file:
				exception = file.read().split("\r\n")

			for x in exception:
				try:
					self.words.remove(x)
				except ValueError:
					pass
		except:
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
		information = "============" + "\n"

		for key, value in self.wordsCount.items():
			information += str(key) + " " + str(value) + "\n"

		information += "============" + "\n"
		information += "Word count : " + str(len(self.words)) + "\n"

		return information


class DataSet:
	""" Contains all DataFile """

	def __init__(self, dataSetPath, isTagged, random):
		"""
		:param dataSetPath: Path to data set folder that contains positive and negative folder messages.
		:type dataSetPath: str
		:param isTagged: Indicate if dataSet is tagged (Different file structure)
		:type isTagged: bool
		:return: object
		"""
		if dataSetPath[-1] != "/":
			dataSetPath += "/"

		# Classes are directories names
		self.classes = ['positive', 'negative']
		self.data = {}

		self.inventory = {}

		self.testSuccess = {}

		self.isTagged = isTagged
		self.random = random

		self.dataPath = dataSetPath

		self.wordsProbability = {}
		self.allWordList = []

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

				if self.random:
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

					for word in currentDataFile.words:
						self.inventory[word] = 0

			for subDirectory in subDirectoryList:
				self.load(path + "/" + subDirectory)

			break

		print("end load "+str(time.time()-temps))

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

		print("end reduceWords "+str(time.time()-temps))
		return wordsAll

	def division(self):
		dataTrain = {}
		dataTest = {}

		for j in range(0, len(self.classes)):
			total = len(self.data[self.classes[j]])
			dataTrain[self.classes[j]] = self.data[self.classes[j]][0 : round(total * 0.8)] # 80% Train
			dataTest[self.classes[j]] = self.data[self.classes[j]][round(total * 0.8) : total] # 20% Test

		self.train(dataTrain)
		self.test(dataTest)
		print("end divisions "+str(time.time()-temps))
		return self.evaluate(0.2)

	def crossValidation(self):

		result = 0
		n = 5

		for i in range(0, n):

			dataTrain = {}
			dataTest = {}

			for j in range(0, len(self.classes)):
				total = len(self.data[self.classes[j]])
				dataTrain[self.classes[j]] = []
				dataTest[self.classes[j]] = []
				# print("Class total : " + str(total))
				if i > 0:
					# dataTrain[self.classes[j]].extend(self.data[self.classes[j]][0: round(i* (total / n))])
					dataTrain[self.classes[j]] += self.data[self.classes[j]][0: round(i* (total / n))]
				if i < (n-1):
					# dataTrain[self.classes[j]].extend(self.data[self.classes[j]][round((i + 1) * (total / n)) : total])
					dataTrain[self.classes[j]] += self.data[self.classes[j]][round((i + 1) * (total / n)) : total]

				dataTest[self.classes[j]] += self.data[self.classes[j]][round(i * (total / n)): round((i + 1) * (total / n))]

				# print("Class " + str(j) + " -> " +  str(len(dataTrain[self.classes[j]])))

			# print("Total : " + str(len(dataTrain)))
			self.train(dataTrain)
			self.test(dataTest)
			result += self.evaluate(0.2) / n

		print("end crossvalidation "+str(time.time()-temps))
		return result

	def train(self, data):
		"""
		Training for Bayes algorithm

		:return: None
		"""

		for className in self.classes:
			self.wordsProbability[className] = {}

			wordsAll = self.reduceWordsCount(data[className])

			if self.debug:
				print("- " + className + " " + str(wordsAll))

			factor = sum(wordsAll.values()) + len(wordsAll)
			for word, number in wordsAll.items():
				self.wordsProbability[className][word] = (wordsAll[word] + 1) / factor

			if self.debug:
				print(className + " " + str(self.wordsProbability[className]))

		print("end train "+str(time.time()-temps))

	def test(self, data):
		"""
		Testing results from bayes algorithm
		Save number of correct values
		Calculate the probability for each word to be positive of negative

		:return: None
		"""
		for className in self.classes:
			self.testSuccess[className] = 0

			for dataEntry in data[className]:
				if self.classify(dataEntry) == className:
					self.testSuccess[className] += 1

	def evaluate(self, percentForTest):
		"""
		Accuracy calculation to evaluate training algorithm
		
		:param percentForTest: Percent of the test in dataset
		:type percentForTest: float
		:return: float
		"""
		# accuracy = self.testSuccess / (len(self.dataPositive) + len(self.negativePath))
		accuracy = sum(self.testSuccess.values())/math.ceil(percentForTest*sum(len(v) for v in self.data.values()))

		print("end evaluate "+str(time.time()-temps))
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
		return self.inventory


#------------------------------------------------------------------------------#
#                                                                              #
#                                     MAIN                                     #
#                                                                              #
#------------------------------------------------------------------------------#

# If this is the main module, run this
if __name__ == '__main__':
	temps = time.time()
	argsCount = len(sys.argv)
	argsIndex = 1

	random.seed()

	#
	# NORMAL DATA SET
	#
	print("Loading normal dataset ...")
	dataSet = DataSet("./dataFull/normal", False, True)

	print("Evaluation accuracy (normal) - Division : ")
	print("Accuracy -> " + str(dataSet.division()))
	print("Evaluation accuracy (normal) - CrossValidation : ")
	print("Accuracy -> " + str(dataSet.crossValidation()))

	#
	# TAGGED DATA SET
	#
	print("Loading tagged dataset ...")
	dataSetTagged = DataSet("./dataFull/tagged", True, True)

	print("Evaluation accuracy (tagged) - Division : ")
	print("Accuracy -> " + str(dataSetTagged.division()))
	print("Evaluation accuracy (tagged) - CrossValidation : ")
	print("Accuracy -> " + str(dataSetTagged.crossValidation()))