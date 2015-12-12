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