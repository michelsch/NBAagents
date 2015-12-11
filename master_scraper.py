from bs4 import BeautifulSoup as bs
import urllib2
import datetime
from datetime import timedelta
import pickle
from sets import Set
import urllib

def generateLinks(startDate, endDate):
	result = []

	gameday = startDate
	delta = timedelta(days = 1)
	currentdate = endDate - delta

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

  	print 'obtained links for ' + str(len(result)) + ' total games over ' + str((currentdate - datetime.date(2015, 10, 27)).days) + ' days'

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
			team1_player_stats.append(new_player)
		if len(entries) == 2:
			new_player['name'] = str(entries[0].get_text())
			new_player['starting_position'] = ''
			new_player['time_played'] = '00:00'
			new_player['fgm-a'] = '0-0'
			new_player['3pm-a'] = '0-0'
			new_player['ftm-a'] = '0-0'
			new_player['+/-'] = '+0'
			new_player['off'] = '0'
			new_player['def'] = '0'
			new_player['tot'] = '0'
			new_player['ast'] = '0'
			new_player['pf'] = '0'
			new_player['st'] = '0'
			new_player['to'] = '0'
			new_player['bs'] = '0'
			new_player['ba'] = '0'
			new_player['pts'] = '0'
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
			if new_player['starting_position'] == '\xc2\xa0':
				new_player['starting_position'] = ''
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
			team2_player_stats.append(new_player)
		if len(entries) == 2:
			new_player['name'] = str(entries[0].get_text())
			new_player['starting_position'] = ''
			new_player['time_played'] = '00:00'
			new_player['fgm-a'] = '0-0'
			new_player['3pm-a'] = '0-0'
			new_player['ftm-a'] = '0-0'
			new_player['+/-'] = '+0'
			new_player['off'] = '0'
			new_player['def'] = '0'
			new_player['tot'] = '0'
			new_player['ast'] = '0'
			new_player['pf'] = '0'
			new_player['st'] = '0'
			new_player['to'] = '0'
			new_player['bs'] = '0'
			new_player['ba'] = '0'
			new_player['pts'] = '0'
			team2_player_stats.append(new_player)

	result['away_team_player_stats'] = team2_player_stats

	#Away team name
	result['away_team'] = str(team2.find('thead').get('class')[0][5:])

	#Add entry to game list
	stats.append( result )

'''
Teams:
['Knicks', 'Thunder', 'Hawks', 'Wizards', 'Nuggets', 'Cavaliers', 'Jazz', 'Timberwolves', 'Clippers', 'Bulls', 'Heat', 'Warriors', 'Celtics', 'Magic', 'Mavericks', 'Pelicans', 'Lakers', 'Pacers', 'CHA_Hornets', 'Rockets', 'Kings', 'Raptors', 'Spurs', 'Blazers', 'Pistons', 'Grizzlies', 'Suns', 'Bucks', 'Sixers', 'Nets'])
'''

def getLastGamePlayers(data, team):
	result = []
	for game in reversed(data):
		if game['home_team'] == team:
			team = game['home_team_player_stats']
			break
		if game['away_team'] == team:
			team = game['away_team_player_stats']
			break

	for player in team:
		if player['name'] != 'Total':
			result.append(player['name'])

	return result

def getLastNGames(data, numGames, team, gameStart):
	result = []
	for game in reversed(data[0:gameStart]):
		if game['home_team'] == team:
			result.append(game['home_team_player_stats'])
		if game['away_team'] == team:
			result.append(game['away_team_player_stats'])
		if len(result) == numGames:
			return result

	print 'only ' + str(len(result)) + ' games found, returning games'
	return result

def addDash(stat1, stat2):
	first = stat1.partition('-')
	second = stat2.partition('-')
	return str(int(first[0]) + int(second[0])) + '-' + str(int(first[2]) + int(second[2]))

def addTime(time1, time2):
	first = time1.partition(':')
	second = time2.partition(':')
	seconds = int(first[2]) + int(second[2])
	carryover = seconds / 60
	seconds = seconds % 60
	minutes = int(first[0]) + int(second[0]) + carryover

	return str(minutes) + ':' + str(seconds)

# Returns a list containing the stats of each player over the last [numGames] games that played in the last game
def getLastNGameStats(data, numGames, team, gameStart):
	result = []
	players = getLastGamePlayers(data, team)
	games = getLastNGames(data, numGames, team, gameStart)

	for player in players:
		new_player = {}
		new_player['name'] = player
		for game in games:
			for person in game:
				if person['name'] == new_player['name']:
					if len(new_player) == 1:
						new_player['starting_position'] = person['starting_position']
						new_player['time_played'] = person['time_played']
						new_player['fgm-a'] = person['fgm-a']
						new_player['3pm-a'] = person['3pm-a']
						new_player['ftm-a'] = person['ftm-a']
						new_player['+/-'] = person['+/-']
						new_player['off'] = person['off']
						new_player['def'] = person['def']
						new_player['tot'] = person['tot']
						new_player['ast'] = person['ast']
						new_player['pf'] = person['pf']
						new_player['st'] = person['st']
						new_player['to'] = person['to']
						new_player['bs'] = person['bs']
						new_player['ba'] = person['ba']
						new_player['pts'] = person['pts']
					else:
						if person['time_played'] == 'DNP':
							break
						new_player['time_played'] = addTime(person['time_played'], new_player['time_played'])
						new_player['fgm-a'] = addDash(person['fgm-a'], new_player['fgm-a'])
						new_player['3pm-a'] = addDash(person['3pm-a'], new_player['3pm-a'])
						new_player['ftm-a'] = addDash(person['ftm-a'], new_player['ftm-a'])
						new_player['+/-'] = str(int(person['+/-']) + int(new_player['+/-']))
						new_player['off'] = str(int(person['off']) + int(new_player['off']))
						new_player['def'] = str(int(person['def']) + int(new_player['def']))
						new_player['tot'] = str(int(person['tot']) + int(new_player['tot']))
						new_player['ast'] = str(int(person['ast']) + int(new_player['ast']))
						new_player['pf'] = str(int(person['pf']) + int(new_player['pf']))
						new_player['st'] = str(int(person['st']) + int(new_player['st']))
						new_player['to'] = str(int(person['to']) + int(new_player['to']))
						new_player['bs'] = str(int(person['bs']) + int(new_player['bs']))
						new_player['ba'] = str(int(person['ba']) + int(new_player['ba']))
						new_player['pts'] = str(int(new_player['pts']) + int(person['pts']))
		result.append(new_player)

	return result
'''
generateLinks(datetime.date(2015, 10, 27), datetime.date.today())

links = open('./links').read().splitlines()

stats = []

for link in links:
	extractStats(link, stats)

pickle.dump(stats, open( "nba_stats.p", "wb" ))


out = open("nba_stats.p", "rb")
stats = pickle.load( out )
out.close()
teams = []

temp_stats = getLastNGameStats(stats, 5, 'Knicks', len(stats))
print temp_stats
# printStats(stats[0]['home_team_player_stats'][0])
'''