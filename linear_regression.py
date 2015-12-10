from sklearn import linear_model
import miami_heat_games as mh
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
  #clf = linear_model.LinearRegression()
  #clf = linear_model.Ridge (alpha = .5)
  clf = linear_model.Lasso(alpha = 0.1)
  #only look at first 10 games
  clf.fit(array_X[:10],array_Y[:10])
  weights = clf.coef_

#check how the rest of the games fare
predictions_and_scores(array_X[11:],array_Y[11:],weights)
