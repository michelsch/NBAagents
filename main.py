#!/usr/bin/python

import random
import collections
import math
import sys
from collections import Counter
from util import *
from sklearn import datasets, svm, metrics
import numpy as np
import matplotlib.pyplot as plt
# Stochastic Gradient Descent
def SGD(trainExamples, testExamples, featureExtractor):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, return the weight vector (sparse feature vector) learned.
    '''
    weights = {}  # feature => weight
    numIters = 17
    eta = 0.1
    trainExamplesExtracted = []
    for trainExample in trainExamples:
        trainExamplesExtracted.append(featureExtractor(trainExample[0]))
    for i in range(numIters):
        trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        devError = evaluatePredictor(testExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
        print "iteration %d: train error = %s, dev error = %s" % (i, trainError, devError)
        for j in range(len(trainExamples)):
            index = j % len(trainExamples)
            gradient = {}
            y = trainExamples[index][1]
            phi_x = trainExamplesExtracted[index]
            if (dotProduct(weights, phi_x) * y < 1):
                # gradient of hinge loss = - phi_x (vector) * y (scalar)
                increment(gradient, -y, phi_x)
            increment(weights, -eta, gradient)
    return weights

# Support Vector Machine

def extractNBAFeatures(x):
    features = extractLast30DaysFeatures(x)
    features.update(extractLast10GamesFeatures(x))
    features.update(extractPlayerFeatures(x))
    return features

def extractLast30DaysFeatures(x):
    pass
def extractLast10GamesFeatures(x):
    pass
def extractPlayerFeatures(x):
    pass

def SVM(trainExamples, testExamples, featureExtractor):
    '''
    Given |trainExamples| and |testExamples| (each one is a list of (x,y)
    pairs), a |featureExtractor| to apply to x, and the number of iterations to
    train |numIters|, return the predictions for the testExamples.
    '''
    for trainExample in trainExamples:
        trainFeatures = featureExtractor(trainExamples)
'''
trainExamples = []
devExamples = []
featureExtractor = extractNBAFeatures
weights = learnPredictor(trainExamples, devExamples, featureExtractor)
outputWeights(weights, 'weights')
outputErrorAnalysis(devExamples, featureExtractor, weights, 'error-analysis')  # debugging
trainError = evaluatePredictor(trainExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
devError = evaluatePredictor(devExamples, lambda(x) : (1 if dotProduct(featureExtractor(x), weights) >= 0 else -1))
print "Official: train error = %s, dev error = %s" % (trainError, devError)
'''