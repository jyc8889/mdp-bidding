from util import *
from config import *
from mdp import *
import numpy as np
import math

def getPctrBucket(pctr, numBuckets, round=False):
  if pctr == 0:
    return numBuckets
  log2 = math.log(pctr)/math.log(2)
  if round:
    log2 = math.floor(log2 * 1000) / 1000
  pwr2 = max(log2, -numBuckets)
  return str(pwr2)

def basicFeatureExtractor(state, action):
  i, n, b, pctr, imps, cost = state
  features = []
  # budget = math.floor(b/100000)*100000
  # num = math.floor(n/1000)*1000
  # newPctr = math.floor(pctr*10) / 10
  features.append(((action, getPctrBucket(pctr, 10, False)), 1) )
  # features.append((action, 1))
  # features.append((round(pctr, 2), 1))
  # features.append((("action-pctr", action, getPctrBucket(pctr, 10, False)), 1) )
  # features.append((("action-pctr-budget", action, getPctrBucket(pctr, 10), budget), 1))
  # features.append((("action-budget", action, budget), 1) )
  # features.append((("action-num", action, num), 1) )
  # features.append((("budget-num", budget, num), 1) )
  #features.append(("pctr-big", pctr > .5)) #list of (key, value) pairs
  #features.append(("pctr-small", pctr <= .5)) #list of (key, value) pairs
  #features.append(("action = " + action, 1))
  #features.append( (("budget", math.floor(b/100)*100), 1) )
  #features.append(  (("impressions-left", math.floor(n/100)*100), 1)   )
  #features.append( (("pctr-small", pctr < 0.1 and pctr > 0.0), 1) )
  #features.append( (("pctr-big", pctr >= 0.1), 1) )
  return features

def main():
  camp = campaigns[1]

  resultPath = logPath + str(camp) + "/qlearning/v0-train.txt"
  mdp = makeMDP(camp=camp, c0=1./32, split="Train", augReward=True) #1323253
  explorationProb = 0.01
  qLearner = QLearningAlgorithm(mdp.actions, mdp.discount(), basicFeatureExtractor, explorationProb)
  simulate(mdp, qLearner, numTrials=5, maxIterations=1000000, verbose=True, sort=False, resultPath=resultPath, calculateLoss=False, incorporateFeedback=True)

  # mdpNew = makeMDP(camp=camp, c0=1./32, split="Train", augReward=False)
  # noAugRewardPath = logPath + str(camp) + "/qlearning/v0-train-pt2.txt"
  # simulate(mdpNew, qLearner, numTrials=10, maxIterations=1000000, verbose=True, sort=False, resultPath=noAugRewardPath, calculateLoss=False)

  weightsTrain = qLearner.weights
  qLearnerTest = QLearningAlgorithm(mdp.actions, mdp.discount(), basicFeatureExtractor, explorationProb=0, nearestNeighbor=1, weights=weightsTrain)

  mdpTest = makeMDP(camp=camp, c0=1./32, split="Test", augReward=True)
  testPath = logPath + str(camp) + "/qlearning/v0-test.txt"
  simulate(mdpTest, qLearnerTest, numTrials=1, maxIterations=10000000, verbose=True, sort=False, resultPath=testPath, calculateLoss=False, incorporateFeedback=False)
  # with open(logPath + str(camp) + "/qlearning/v0-weights.txt", 'w') as f:
  #   for key in qLearner.weights:
  #     f.write(str(key[0]) + " " + str(key[1]) + " " + str(key[2]) + " " + str(qLearner.weights[key]) + "\n")

if __name__ == '__main__':
  main()