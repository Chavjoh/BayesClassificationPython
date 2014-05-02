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
from collections import defaultdict
import re
import string

#------------------------------------------------------------------------------#
#                                                                              #
#                                   CLASSES                                    #
#                                                                              #
#------------------------------------------------------------------------------#

class DataFile:
	""" Contains file analysis information """

	def __init__(self, **keys):
		"""
		Create a new DataFile.
		
		:rtype: str
		"""
		# Class name (positive / negative)
		self.className = keys['className']

		# Content of the DataFile (text)
		self.fileContent = keys['fileContent'].lower()

		# Path of files that contains all exception words
		self.exceptionWords = keys['wordException']

		# List that contains all words
		self.words = []

		# Dictionary that contains apparition number of each word
		self.wordsCount = defaultdict(int)
		
		# Remove punctuation from file content
		self.removePunctuation()

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
		Load words from fileContent for file that contains only message.
		
		:return: None
		"""

		self.words = self.fileContent.split()

	def loadTagged(self):
		"""
		Load words from fileContent for file that contains more information with message.
		
		:return: None
		"""
		for line in self.fileContent.split("\n"):
			try:
				self.words.append(line.split("\t")[2])
			except IndexError:
				pass

	def removeExceptionWords(self):
		"""
		Remove all words in exception list from file content.
		
		:return: None
		"""
		exception = []
		with codecs.open(self.exceptionWords, 'r', 'UTF-8') as file:
			exception = file.read().split("\r\n")

		for x in exception:
			try:
				self.words.remove(x)
			except ValueError:
				pass
	
	def removePunctuation(self):
		"""
		Remove punctuation from file content.
		
		:return: None
		"""
		regex = re.compile('[%s]' % re.escape(string.punctuation))
		self.fileContent = regex.sub('', self.fileContent)

	def calculateWordsCount(self):
		"""
		Calculate the number of occurrence of words.
		
		:return: None
		"""

		for word in self.words:
			self.wordsCount[word] += 1

	def __repr__(self):
		"""
		String representation of the DataFile.
		
		:return: str
		"""
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
		Create a new Dataset
		
		:param dataSetPath: Path to data set folder that contains positive and negative folder messages.
		:type dataSetPath: str
		:param isTagged: Indicate if dataSet is tagged (Different file structure)
		:type isTagged: bool
		:param random: Indicate if dataset is randomized when loading
		:type ramdom: bool
		:return: object
		"""
		
		# Add slash to dataset path if necessary
		if dataSetPath[-1] != "/":
			dataSetPath += "/"
		self.dataPath = dataSetPath

		# Classes (used for directories names)
		self.classes = ['positive', 'negative']
		
		# Contains all dataFile for each class
		self.data = {}

		# Contains the number of test passed with success
		self.testSuccess = {}

		# Indicates if we load tagged file
		self.isTagged = isTagged
		
		# Indicates if the dataset have to be loaded randomly
		self.random = random

		# Probability of apparition of each word for each class
		self.wordsProbability = {}

		# Inventory of each words of all DataFile
		self.inventory = {}
		
		# Indicates if debug mode is activate (to display more information during execution)
		self.debug = False
		
		# Load dataset
		self.load(self.dataPath)
		
		if self.debug:
			for className in self.classes:
				print(str(className)+" "+str(len(self.data[className])))

	def load(self, path):
		"""
		Load all dataset.
		
		:param path: Path to dataset to load
		:type path: str
		:return: None
		"""
		# Remove last slash if necessary
		if path[-1] == "/":
			path = path[0:-1]

		for (directoryPath, subDirectoryList, fileNameList) in walk(path):

			# Debug
			# print(fileNameList)
			# print(directoryPath)
			# print(subDirectoryList)
			
			# directorySplit = Class name
			directorySplit = directoryPath.split("/")[-1]
			
			if directorySplit in self.classes:

				if self.random:
					random.shuffle(fileNameList)

				for index, fileName in enumerate(fileNameList):
				
					# Read all line of the file
					fileContent = ''.join(open(directoryPath + '/' + fileName, 'r', encoding="utf-8").readlines())

					# Create a DataFile and parse fileContent
					currentDataFile = DataFile(
						fileContent=fileContent,
						className=directorySplit,
						isTagged=self.isTagged,
						wordException=directoryPath+"/../uselessWords.txt"
					)
					
					# Add DataFile to list
					try:
						self.data[directorySplit].append(currentDataFile)
					except:
						self.data[directorySplit] = [currentDataFile]

					# Add all words in inventory
					for word in currentDataFile.words:
						self.inventory[word] = 0

			for subDirectory in subDirectoryList:
				self.load(path + "/" + subDirectory)

			break

	def reduceWordsCount(self, dataList):
		"""
		Reduce the count of all words to one dictionary.
		
		:param dataList: DataFile list to reduce
		:type dataList: list of dataFile
		:return: None
		"""

		wordsAll = self.inventoryWord()

		for data in dataList:
			for word, value in data.wordsCount.items():
				wordsAll[word] += value

		return wordsAll

	def division(self):
		"""
		Execute division algorithm (80% training, 20% testing).
		
		:return: None
		"""
		dataTrain = {}
		dataTest = {}
		
		for j in range(0, len(self.classes)):
			total = len(self.data[self.classes[j]])
			dataTrain[self.classes[j]] = self.data[self.classes[j]][0 : round(total * 0.8)] # 80% Train
			dataTest[self.classes[j]] = self.data[self.classes[j]][round(total * 0.8) : total] # 20% Test
		
		self.train(dataTrain)
		self.test(dataTest)
		return self.evaluate(0.2)

	def crossValidation(self):
		"""
		Execute cross validation algorithm (window of 20% testing moving along 5 parts).
		
		:return: None
		"""
		result = 0
		n = 5
		
		# For each part
		for i in range(0, n):
			
			dataTrain = {}
			dataTest = {}
			
			# For each class
			for j in range(0, len(self.classes)):
				total = len(self.data[self.classes[j]])
				dataTrain[self.classes[j]] = []
				dataTest[self.classes[j]] = []
				
				if i > 0:
					dataTrain[self.classes[j]].extend(self.data[self.classes[j]][0 : round(i* (total / n))])
				if i < (n-1):
					dataTrain[self.classes[j]].extend(self.data[self.classes[j]][round((i + 1) * (total / n)) : total])
				
				dataTest[self.classes[j]].extend(self.data[self.classes[j]][round(i * (total / n)) : round((i + 1) * (total / n))])
				
				if self.debug:
					print("Class " + str(j) + " -> " +  str(len(dataTrain[self.classes[j]])))
			
			if self.debug:
				print("Total : " + str(len(dataTrain)))
			
			self.train(dataTrain)
			self.test(dataTest)
			result += self.evaluate(0.2) / n
			
		return result

	def train(self, data):
		"""
		Training for Bayes algorithm.
		
		:param data: Data to use for training
		:type data: list
		:return: None
		"""
		
		if self.debug:
			print("Training ...")
		
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

	def test(self, data):
		"""
		Testing results from bayes algorithm. Save number of correct values.
		Calculate the probability for each word to be positive of negative.
		
		:param data: Data to use for testing
		:type data: list
		:return: None
		"""
		
		if self.debug:
			print("Testing ...")
		
		for className in self.classes:
			self.testSuccess[className] = 0

			for dataEntry in data[className]:
				if self.classify(dataEntry) == className:
					self.testSuccess[className] += 1

	def evaluate(self, percentForTest):
		"""
		Accuracy calculation to evaluate training algorithm.

		:param percentForTest: Percent of the test in dataset
		:type percentForTest: float
		:return: float
		"""
		if self.debug:
			print("Evaluating ...")
		
		accuracy = sum(self.testSuccess.values())/math.ceil(percentForTest*sum(len(v) for v in self.data.values()))

		return accuracy

	def classify(self, dataFile):
		"""
		Classify a dataFile to positive or negative.

		:param dataFile: DataFile to classify
		:type dataFile: DataFile
		:return: True if positive, False otherwise
		"""
		
		probability = {}
		maxClass = None

		for className in self.classes:
			probability[className] = 1

			for word, wordProbability in self.wordsProbability[className].items():
				if word in dataFile.wordsCount:
					probability[className] *= pow(wordProbability, dataFile.wordsCount[word])

			if not maxClass or (probability[maxClass] < probability[className]):
				maxClass = className

		return maxClass

	def inventoryWord(self):
		"""
		Return an dictionary of all words, initialized with 0 apparition for each.
		
		:return: Dictionary of all words
		"""
		return dict.fromkeys(self.inventory, 0)

#------------------------------------------------------------------------------#
#                                                                              #
#                                     MAIN                                     #
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
	print("======================================================================")
	print("Loading normal dataset ...")
	dataSet = DataSet("./dataFull/normal", False, False)
	
	print("Evaluation accuracy (normal) - Division : ")
	print("Accuracy -> " + str(dataSet.division()))
	print("Evaluation accuracy (normal) - CrossValidation : ")
	print("Accuracy -> " + str(dataSet.crossValidation()))
	
	print("======================================================================")
	print("Loading randomized normal dataset ...")
	dataSet = DataSet("./dataFull/normal", False, True)
	
	print("Evaluation accuracy (normal) (random) - Division : ")
	print("Accuracy -> " + str(dataSet.division()))
	print("Evaluation accuracy (normal) (random) - CrossValidation : ")
	print("Accuracy -> " + str(dataSet.crossValidation()))

	#
	# TAGGED DATA SET
	#
	print("======================================================================")
	print("Loading tagged dataset ...")
	dataSetTagged = DataSet("./dataFull/tagged", True, False)
	
	print("Evaluation accuracy (tagged) - Division : ")
	print("Accuracy -> " + str(dataSetTagged.division()))
	print("Evaluation accuracy (tagged) - CrossValidation : ")
	print("Accuracy -> " + str(dataSetTagged.crossValidation()))
	
	print("======================================================================")
	print("Loading randomized tagged dataset ...")
	dataSetTagged = DataSet("./dataFull/tagged", True, True)
	
	print("Evaluation accuracy (tagged) (random) - Division : ")
	print("Accuracy -> " + str(dataSetTagged.division()))
	print("Evaluation accuracy (tagged) (random) - CrossValidation : ")
	print("Accuracy -> " + str(dataSetTagged.crossValidation()))