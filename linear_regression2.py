from sklearn import linear_model, svm, datasets, metrics, preprocessing
import miami_heat_games2 as mh
import player_data as data
import numpy

teamsAndLinks = data.teamsAndLinks()
teamsAndStats = data.teamsAndStats(teamsAndLinks)
teamsAndPlayerStats = data.teamsAndPlayerStats(teamsAndStats)

team_names,scores = mh.miami_heat_games()


def feature_extractor(teamsAndPlayerStats,opponent):
  '''return all players' stats for a team'''
  features = []
  for each in teamsAndPlayerStats:
    #since the opponent team names are abbreviations, need to check for substring
    if opponent == 'NY Knicks':
      opponent = 'New York Knicks'
    if opponent in each:
      for player in teamsAndPlayerStats[each]:
        #print player
        #print each
        #print teamsAndPlayerStats[each][player]
        #print ''
        features.extend(teamsAndPlayerStats[each][player])
  return features

#check if all arrays in array  have the same dim
def check_dimensions(array, dim):
  for item in array:
    if len(item) != dim:
      return False
  return True

#print predictions (dot product of x,weights) vs. actual scores y
def predictions_and_scores(array_X,array_Y,weights):
  predictions = numpy.dot (array_X,weights)
  for i,each in enumerate(predictions):
    print each, array_Y[i]

#features
array_X = []
#actual scores
array_Y = scores
for opponent in team_names:
  #append the 28 stats only for first 13 players
  array_X.append(feature_extractor(teamsAndPlayerStats, opponent)[:(13*28)])
  #append score

if check_dimensions(array_X,13*28):
  #clf0 = linear_model.LinearRegression()
  #clf = linear_model.Ridge (alpha = .5)
  clf = linear_model.Lasso(alpha = 0.1, max_iter = 500000)
  #clf = svm.SVC(gamma=0.001)
  #only look at first 10 games
  clf.fit(array_X[:60],array_Y[:60])
  #weights = clf.coef_
  #print weights
  #for i in range(11,len(array_X)):

  #check how the rest of the games fare
  predictions = clf.predict(array_X)
  print predictions
  print array_Y
  correctCt = 0
  for i in range(60,len(predictions)):
    print predictions[i], array_Y[i], predictions[i] * array_Y[i] > 0
    if predictions[i] * array_Y[i] > 0:
      correctCt += 1
  print correctCt


