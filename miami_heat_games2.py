from bs4 import BeautifulSoup as bs
import urllib
import collections


def miami_heat_games():
  '''return a tuple containing a list of the team names and a list of scores
  of all previously played Miami Heat games'''
  page = urllib.urlopen("http://espn.go.com/nba/team/schedule/_/name/mia/year/2015/miami-heat")
  soup = bs(page)
  games = soup.find_all("tr")
  team_names = []
  scores = []
  for game in games:
    #if game has a score
      if game.find(class_="score"):
        score = game.find(class_="score").get_text().split('-')
        if ' ' in score[0]:
          score[0] = score[0][0:score[0].find(' ')]
        if ' ' in score[1]:
          print score[1][0:score[1].find(' ')]
          score[1] = score[1][0:score[1].find(' ')]

        difference =  float(score[0]) - float(score[1])
        team_names.append(game.find(class_="team-name").get_text())
        #if game was won, append positive point difference
        if game.find(class_="game-status win"):
          scores.append(difference)
        else:
          scores.append(-difference)
          '''
  page = urllib.urlopen("http://espn.go.com/nba/team/schedule/_/name/mia/miami-heat")
  soup = bs(page)
  print len(scores)
  games = soup.find_all("tr")

  for game in games:
    #if game has a score
      if game.find(class_="score"):
        score = game.find(class_="score").get_text().split('-')
        if ' ' in score[0]:
          score[0] = score[0][0:score[0].find(' ')]
        if ' ' in score[1]:
          print score[1][0:score[1].find(' ')]
          score[1] = score[1][0:score[1].find(' ')]

        difference =  float(score[0]) - float(score[1])
        team_names.append(game.find(class_="team-name").get_text())
        #if game was won, append positive point difference
        if game.find(class_="game-status win"):
          scores.append(difference)
        else:
          scores.append(-difference)
          '''
  return (team_names, scores)
