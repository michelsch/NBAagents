from bs4 import BeautifulSoup as bs
import urllib2
import datetime
from datetime import timedelta
import pickle

def generateLinks():
	result = []

	gameday = datetime.date(2015, 10, 27)
	delta = timedelta(days = 1)
	currentdate = datetime.date.today() - delta

	# Generate Links to All Games
	
	while gameday != currentdate:
		print 'Scraping date ' + str(gameday)
		url = 'http://www.nba.com/gameline/' + str(gameday.year) + str(gameday.month).zfill(2) + str(gameday.day).zfill(2)
		game_page = urllib.urlopen(url).read()
		soup = bs(game_page, "lxml")
		
	  	for link in soup.find_all("a", { "class" : "recapAnc" }):
	  		result.append( 'http://www.nba.com' + str(link.get('href')) + '#nbaGIboxscore' )

	  	gameday = gameday + delta
  	
  	f1 = open('./links', 'w+')
  	for link in result:
  		f1.write(link + '\n')

  	print 'obtained links for ' + str(len(result)) + ' total games over ' + str((currentdate - datetime.date(2015, 11, 27)).days) + ' days'

def readLinks(filename, container):
	f1 = open(filename, 'r')
	for line in f1:
		container += line

def printStats(player):
	print player['name'], player['starting_position'], player['time_played'] \
	, player['fgm-a'], player['3pm-a'], player['ftm-a'], player['+/-'] \
	, player['off'], player['def'], player['tot'], player['ast'], player['pf'] \
	, player['st'], player['to'], player['bs'], player['ba'], player['pts']

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
	for row in rows[3:]:
		new_player = {}
		entries = row.find_all('td')
		if len(entries) == 17:
			new_player['name'] = str(entries[0].get_text())
			new_player['starting_position'] = entries[1].get_text().encode('utf-8').strip()
			new_player['time_played'] = entries[2].get_text().encode('utf-8').strip()
			new_player['fgm-a'] = entries[3].get_text().encode('utf-8').strip()
			new_player['3pm-a'] = entries[4].get_text().encode('utf-8').strip()
			new_player['ftm-a'] = entries[5].get_text().encode('utf-8').strip()
			new_player['+/-'] = entries[6].get_text().encode('utf-8').strip()
			new_player['off'] = entries[7].get_text().encode('utf-8').strip()
			new_player['def'] = entries[8].get_text().encode('utf-8').strip()
			new_player['tot'] = entries[9].get_text().encode('utf-8').strip()
			new_player['ast'] = entries[10].get_text().encode('utf-8').strip()
			new_player['pf'] = entries[11].get_text().encode('utf-8').strip()
			new_player['st'] = entries[12].get_text().encode('utf-8').strip()
			new_player['to'] = entries[13].get_text().encode('utf-8').strip()
			new_player['bs'] = entries[14].get_text().encode('utf-8').strip()
			new_player['ba'] = entries[15].get_text().encode('utf-8').strip()
			new_player['pts'] = entries[16].get_text().encode('utf-8').strip()
		if len(entries) == 2:
			new_player['name'] = str(entries[0].get_text())
			new_player['starting_position'] = entries[1].get_text().encode('utf-8').strip()
			new_player['time_played'] = 'DNP'
			new_player['fgm-a'] = 'DNP'
			new_player['3pm-a'] = 'DNP'
			new_player['ftm-a'] = 'DNP'
			new_player['+/-'] = 'DNP'
			new_player['off'] = 'DNP'
			new_player['def'] = 'DNP'
			new_player['tot'] = 'DNP'
			new_player['ast'] = 'DNP'
			new_player['pf'] = 'DNP'
			new_player['st'] = 'DNP'
			new_player['to'] = 'DNP'
			new_player['bs'] = 'DNP'
			new_player['ba'] = 'DNP'
			new_player['pts'] = 'DNP'
		team1_player_stats.append(new_player)

	result['home_team_player_stats'] = team1_player_stats

	#Home team name
	result['home_team'] = str(team1.find('thead').get('class')[0][5:])
	
	team2 = soup.find_all('table', {"id" : "nbaGITeamStats"})[1]

	team2_player_stats = []
	rows = team2.find_all('tr')
	for row in rows[3:]:
		new_player = {}
		entries = row.find_all('td')
		if len(entries) == 17:
			new_player['name'] = str(entries[0].get_text())
			new_player['starting_position'] = entries[1].get_text().encode('utf-8').strip()
			new_player['time_played'] = entries[2].get_text().encode('utf-8').strip()
			new_player['fgm-a'] = entries[3].get_text().encode('utf-8').strip()
			new_player['3pm-a'] = entries[4].get_text().encode('utf-8').strip()
			new_player['ftm-a'] = entries[5].get_text().encode('utf-8').strip()
			new_player['+/-'] = entries[6].get_text().encode('utf-8').strip()
			new_player['off'] = entries[7].get_text().encode('utf-8').strip()
			new_player['def'] = entries[8].get_text().encode('utf-8').strip()
			new_player['tot'] = entries[9].get_text().encode('utf-8').strip()
			new_player['ast'] = entries[10].get_text().encode('utf-8').strip()
			new_player['pf'] = entries[11].get_text().encode('utf-8').strip()
			new_player['st'] = entries[12].get_text().encode('utf-8').strip()
			new_player['to'] = entries[13].get_text().encode('utf-8').strip()
			new_player['bs'] = entries[14].get_text().encode('utf-8').strip()
			new_player['ba'] = entries[15].get_text().encode('utf-8').strip()
			new_player['pts'] = entries[16].get_text().encode('utf-8').strip()
		if len(entries) == 2:
			new_player['name'] = str(entries[0].get_text())
			new_player['starting_position'] = entries[1].get_text().encode('utf-8').strip()
			new_player['time_played'] = 'DNP'
			new_player['fgm-a'] = 'DNP'
			new_player['3pm-a'] = 'DNP'
			new_player['ftm-a'] = 'DNP'
			new_player['+/-'] = 'DNP'
			new_player['off'] = 'DNP'
			new_player['def'] = 'DNP'
			new_player['tot'] = 'DNP'
			new_player['ast'] = 'DNP'
			new_player['pf'] = 'DNP'
			new_player['st'] = 'DNP'
			new_player['to'] = 'DNP'
			new_player['bs'] = 'DNP'
			new_player['ba'] = 'DNP'
			new_player['pts'] = 'DNP'
		team2_player_stats.append(new_player)

	result['away_team_player_stats'] = team2_player_stats

	#Away team name
	result['away_team'] = str(team2.find('thead').get('class')[0][5:])
	
	#Add entry to game list
	stats.append( result )
'''
links = open('./links').read().splitlines()

stats = []

for link in links:
	extractStats(link, stats)

pickle.dump(stats, open( "nba_stats.p", "wb" ))
'''
stats = pickle.load( open( "nba_stats.p", "rb" ) )

printStats(stats[0]['home_team_player_stats'][0])