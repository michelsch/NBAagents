# NBAagents
Project for the Fall 2015 CS221 class at Stanford

master_scraper.py:

Contains functions used to scrape nba.com for game schedule and then player stats.
We used these functions to generate the pickled files that have both the schedule
of NBA games to date, as well as the stats for each individual player in each game
that we used to predict how NBA games will play out.

links:

Links to the pages of the NBA games this season.

nba_stats.p:

Pickled file that contains a list of games. Games are dictionaries with keys such
as 'home_team', 'away_team', 'home_team_player_stats', and 'away_team_player_stats'
. The player stats values are a list of players. Players are also dictionaries with
keys like the ones in the following example that depict their stats for that game:

player['name'] = 'Example Player'	# Name of player
player['starting_position'] = ''	# Starting Postion, '' if none
player['time_played'] = '00:00'		# Time played in MM:SS
player['fgm-a'] = '0-0'				# Field goals made - attempted
player['3pm-a'] = '0-0'				# 3pt shots made - attempted
player['ftm-a'] = '0-0'				# Freethrows made - attempted
player['+/-'] = '0'					# Plus/Minus
player['off'] = '0'					# Offensive Rebounds
player['def'] = '0'					# Defensive Rebounds
player['tot'] = '0'					# Total Rebounds
player['ast'] = '0'					# Assists
player['pf'] = '0'					# Personal Fouls
player['st'] = '0'					# Steals
player['to'] = '0'					# Turn Overs
player['bs'] = '0'					# Blocked Shots
player['ba'] = '0'					# Blocks Against
player['pts'] = '0'					# Points Scored

nba_teams.p:

List of all NBA team names as referenced by nba_stats.p

linear_regression.py: Uses a the feature extractor in player_data.py to do perform various linear regression algorithms using sklearn on the data from last year's season. Calculates an test error rate based on this year's games so far.'

miami_heat_games.py:

Returns a tuple containing a list of the team names and a list of scores
of all previously played Miami Heat games' for this year.'

player_data.py: 

Performs data scraping from ESNP.com to reuturn stats for each player in the form of a dict of teams which links to another dict for each player of that team whose value is a list of stats with the following indexes (phew!):
0 -> GP -- Games Played
1 -> GS -- Games Started
2 -> MIN -- Minutes per game
3-> PPG -- Points per game
4 -> OFFR -- Offensive Rebounds per game
5 -> DEFFR -- Defensive Rebounds per game
6-> RPG -- Rebounds per game
7 -> APG -- Assists per game
8 -> SPG -- Steals per game
9 -> BPG --  Blocks per game
10 -> TPG -- Turnovers per game
11 -> FPG -- Fouls per game
12 -> A/TO -- Assist to turnover ratio
13 -> PER -- Player efficiency rating
14 -> FGM --  Field Goals Made per game
15 -> FGA -- Field Goals Attempted per game
16 -> FG% --  Field Goals Percentage per game
17 -> 3PM -- Three-point Field Goals Made per game
18 -> 3PA -- Three-point Field Goals Attempted per game
19 -> 3P% -- Three-point Field Goals Percentage per game
20 -> FTM --  Free Throws Made per game
21 -> FTA --  Free Throws Attempted per game
22 -> FT% -- Free Throws Percentage per game
23 -> 2PM --  Two-point Field Goals Made per game
24 -> 2PA -- Two-point Field Goals Attempted per game
25 -> 2P% -- Two-point Field Goals Percentage per game
26 -> PPS -- Points Per Shot per game
27 -> AFG% -- Adjusted Field Goal Percentage per game

example usage:
teamsAndPlayerStats['Miami Heat']['Chris Bosh'][0]
games played for Chris Bosh, who is in the Miami Heat

player.py: 

Implements a Class team and a game MVP, which can be used for multiple Markov simulations. Transition probabilties are a combination of player stats and hard-coded constants to reduce noise. The algorithm still has room for refinement.

