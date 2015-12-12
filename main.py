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
import pickle
import master_scraper
from operator import attrgetter
from sklearn import linear_model, svm, datasets, metrics, preprocessing
import itertools

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

def convertTime(s):
    '''
    Takes a string s in the form 'MM:SS' and converts it to a float MM.xx... which represents number of minutes.
    '''
    first = s.partition(':')
    return float(first[0]) + float(first[2]) / 60.0
def extractMadeAttempted(s):
    '''
    Takes a string s in the form 'made-attempted' and returns (made, attempted).
    '''
    first = s.partition('-')
    return (float(first[0]),float(first[2]))

# Setup data pipeline
out = open("nba_stats.p", "rb")
stats = pickle.load( out ) # all previous game stats for this season
#print stats[0]
out.close()
teams = []

temp_stats = master_scraper.getLastNGameStats(stats, 5, 'Knicks', len(stats))
print temp_stats

allRelevantKeys =['time_played', 'fgm-a', '3pm-a', 'ftm-a', '+/-', 'off', 'def', 'tot', 'ast', 'pf', 'st', 'to', 'bs', 'ba', 'pts']
#relevantKeys =['fgm-a', '3pm-a', 'ftm-a', '+/-', 'off', 'def']
#relevantKeys =['time_played', 'fgm-a', '3pm-a', 'ftm-a', '+/-', 'off', 'def', 'tot', 'ast', 'pf', 'st', 'to', 'bs', 'ba', 'pts']
bestTestKeys = []
bestTestAcc = 0
bestTrainAcc = 0

relevantKeysPicked = [allRelevantKeys]
#relevantKeysPicked =
#relevantKeysPicked = itertools.combinations(allRelevantKeys, i)
#if selected
for i in range(1, len(allRelevantKeys)):
    for relevantKeys in relevantKeysPicked:
        print 'keys', relevantKeys
        # Find the starting point for training
        allFeatureLists = [] # list of lists of features (each list of features corresponds to the player stats from past 5 games)
        allOutcomes = [] # list of point differences / point spreads (home team score - away team score)
        for i in range(53, len(stats)):
            featureList = [] # List of features for a particular game
            game = stats[i]

            homeTeam = game['home_team']
            awayTeam = game['away_team']
            homeStats = master_scraper.getLastNGameStats(stats, 5, homeTeam, i)
            awayStats = master_scraper.getLastNGameStats(stats, 5, awayTeam, i)
            if len(homeStats) == 0 or len(awayStats) == 0:
                continue
            '''
            print 'home stats for games', i-5, 'to', i, homeStats
            print 'away stats for games', i-5, 'to', i, awayStats
            '''
            # convert minutes
            for stat in homeStats:
                #print 'stat', stat
                stat['time_played'] = convertTime(stat['time_played'])
            for stat in awayStats:
                stat['time_played'] = convertTime(stat['time_played'])
            homeStats = sorted(homeStats, key=lambda stat: stat['time_played'])
            awayStats = sorted(awayStats, key=lambda stat: stat['time_played'])
            for stat in homeStats:
                for key in relevantKeys:
                    if '-a' in key:
                        madeAttemptedFeatures = extractMadeAttempted(stat[key])
                        featureList.append(madeAttemptedFeatures[0])
                        featureList.append(madeAttemptedFeatures[1])
                    else:
                        featureList.append(float(stat[key]))
            allFeatureLists.append(featureList)

            homeScore = 0
            awayScore = 0

            for p in game['home_team_player_stats']:
                if p['name'] == 'Total':
                    homeScore = int(p['pts'])
            for p in game['away_team_player_stats']:
                if p['name'] == 'Total':
                    awayScore = int(p['pts'])
            allOutcomes.append(homeScore - awayScore)

        #print len(allOutcomes)


        #models = [linear_model.LinearRegression(),  linear_model.Ridge (alpha = .1),  linear_model.Ridge (alpha = .5), linear_model.Ridge (alpha = .9), linear_model.Lasso(alpha = 0.1, max_iter = 500000), linear_model.Lasso(alpha = 0.5, max_iter = 500000), linear_model.Lasso(alpha = 0.9, max_iter = 500000), svm.SVC(gamma=0.001, C = 1000), svm.SVC(kernel = 'linear',C = 1000, gamma = 0.0)]
        #models = [svm.SVC(gamma=0.001, C = 1000), svm.SVC(kernel = 'linear',C = 1000, gamma = 0.0), svm.SVC(kernel = 'linear',C = 100, gamma = 0.0), svm.SVC(kernel = 'linear',C = 10000, gamma = 0.0), svm.SVC(kernel = 'linear',C = 1000, gamma = 'auto'), svm.SVC(kernel = 'rbf',C = 1000, gamma = 'auto'), svm.SVC(kernel = 'rbf', gamma = 'auto'), svm.SVC(kernel = 'rbf',C = 10000, gamma = 'auto'), svm.SVC(kernel = 'poly',C = 1000, gamma = 'auto')]
        models = [linear_model.LogisticRegression(penalty='l1'), linear_model.LogisticRegression(penalty='l2')]
        for clf in models:
            clf.fit(allFeatureLists[:190],allOutcomes[:190])
            predictions = clf.predict(allFeatureLists)
            #print predictions
            #print allOutcomes
            correctCt = 0
            for i in range(0,190):
                #print predictions[i], allOutcomes[i], predictions[i] * allOutcomes[i] > 0
                if predictions[i] * allOutcomes[i] > 0:
                    correctCt += 1
            print 'training: ', correctCt, correctCt / 190.0
            trainAcc = correctCt / 190.0
            correctCt = 0
            for i in range(190,len(predictions)):
                #print predictions[i], allOutcomes[i], predictions[i] * allOutcomes[i] > 0
                if predictions[i] * allOutcomes[i] > 0:
                    correctCt += 1
            print 'test: ', correctCt, correctCt / 48.0
            if correctCt / 48.0 > bestTestAcc:
                bestTestAcc = correctCt / 48.0
                bestTestKeys = relevantKeys
                bestTrainAcc = trainAcc
print bestTestKeys
print bestTestAcc
print bestTrainAcc

