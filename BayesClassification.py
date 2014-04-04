#!/usr/bin/python
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

#------------------------------------------------------------------------------#
#                                                                              #
#                                   CLASSES                                    #
#                                                                              #
#------------------------------------------------------------------------------#


class DataFile:

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

    toto = DataFile("coucou je suis une grosse bite et je vous emmerde Monsieur le PD n'ha n'ha n'aire", True)
    print(toto)