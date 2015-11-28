from bs4 import BeautifulSoup as bs
import urllib

def teamsAndLinks():
  filen = '/users/michelschoemaker/teams_and_links'
  '''returns a dict of team names and links to their respective ESPN pages'''
  team_page = urllib.urlopen('http://espn.go.com/nba/players').read()
  soup = bs(team_page)
  #find all list items on website
  teams = soup.find_all("li")
  teamsAndLinks = {}
  for team in teams:
    try:
      #find all list items whose format corresponds to a team name, add the link
      teamsAndLinks[team.find(style="padding-top:5px;padding-left:0px;").get_text()] = team.a["href"]
      #print team.find(style="padding-top:5px;padding-left:0px;").get_text()
      #print team.a["href"]
      #print ''
    except:
      continue
  #print teamsAndLinks
  #30 is the number of NBA teams
  assert len(teamsAndLinks) == 30
  return teamsAndLinks

def teamsAndStats(teamsAndLinks):
  ''' returns a dict of team names and links to their respective
      ESPN stats pages'''
  teamsAndStats = {}
  for team in teamsAndLinks:
    page = urllib.urlopen(teamsAndLinks[team])
    soup = bs(page)
    #find all relevant links
    stats = soup.find_all("span",class_="link-text")
    for item in stats:
      #filter to the link titled Stats
      if 'Stats' == item.get_text():
        teamsAndStats[team] = item.parent["href"]
        #print item.parent["href"]
  #30 is the number of NBA teams
  assert len(teamsAndStats) == 30
  #print teamsAndStats
  return teamsAndStats

def teamsAndPlayerStats(teamsAndStats):
  all_teams = {}
  for each_team in teamsAndStats:
    team = {}
    page = urllib.urlopen(teamsAndStats[each_team])
    soup = bs(page)
    players = soup.find_all("tr")
    for i in range(2,16):
      stats = []
      try:
        for j in range (2,15):
          try:
            stats.append(players[i].find_all('td')[j].get_text())
            #print players[i].find_all('td')[j].get_text()
            #print ''
          except:
            print 'parsing failed for ' + players[i].find_all('td')[j].get_text()
            continue
        team[players[i].a.get_text()] = stats
      except:
        print 'parsing failed or over bounds for player in ' + each_team
        continue
    all_teams[each_team] = team
  print len(all_teams)
  #assert len(all_teams) == 30
  #print all_teams
  return all_teams


teamsAndLinks = teamsAndLinks()
teamsAndStats = teamsAndStats(teamsAndLinks)
#teamsAndPlayerStats = teamsAndPlayerStats(teamsAndStats)
