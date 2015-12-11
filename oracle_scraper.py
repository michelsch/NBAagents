from bs4 import BeautifulSoup as bs
import urllib2 as urllib
import datetime
from datetime import timedelta
import pickle

def getPredictions():
	result = [] # result will contain tuples: (prediction, truth)

	gameday = datetime.date(2015, 10, 27)
	delta = timedelta(days = 1)
	currentdate = datetime.date.today() - delta

	# Generate Links to All Games

	while gameday != currentdate:
		print 'Scraping date ' + str(gameday)
		gameday = gameday + delta # next day

		url = 'http://www.cbssports.com/nba/expert-picks/' + str(gameday.year) + str(gameday.month).zfill(2) + str(gameday.day).zfill(2)
		game_page = urllib.urlopen(url).read()
		soup = bs(game_page, 'html5lib')



	  	for gameTable in soup.find_all("table", { "class" : "data border" }):
	  		#print gameTable
	  		#tbody = gameTable.get('tbody')
	  		tb = gameTable.find_all('tbody')[0]
	  		tr = tb.find_all('tr')[0]
	  		tds = tr.find_all('td')

	  		print tds[-3].find_all('a'), tds[-1].find_all('a')[0]
	  		result.append((tds[-3].find_all('a')[0].find_all('img')[0].get('src'), tds[-1].find_all('a')[0].find_all('img')[0].get('src')))
	  		#result.append( 'http://www.nba.com' + str(gameTable.get('href')) + '#nbaGIboxscore' )


	f1 = open('./oracle_predictions', 'w+') # write results
	print result
	numPCorrect = 0
	for game in result:
		status = '0'
		if game[0] == game[1]:
			status = '1'
			numPCorrect += 1
		f1.write(str(game) + ' ' + status + '\n')
	print 'oracle\'s correct prediction ratio', float(numPCorrect) / len(result)

	#print 'obtained links for ' + str(len(result)) + ' total games over ' + str((currentdate - datetime.date(2015, 11, 27)).days) + ' days'


def extractStats(link, stats):
	print 'beginning extraction on ' + link
	result = {}
	url = link
	game_page = urllib2.urlopen(url).read()
	soup = bs(game_page, 'html5lib')

	#Parsing both teams stats into game entry
	team1 = soup.find_all('table', {"id" : "nbaGITeamStats"})[0]

	team1_player_stats = []
	rows = team1.find_all('tr')


#pickle.dump(stats, open( "nba_stats.p", "wb" ))
getPredictions()