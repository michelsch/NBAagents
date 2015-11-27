from bs4 import BeautifulSoup as bs
import urllib

def teamsAndLinks():
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
  #print len(teamsAndLinks)
  #30 is the number of NBA teams
  assert len(teamsAndLinks) == 30
  return teamsAndLinks

def teamsAndStats(teamDict):
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

teamsAndLinks = teamsAndLinks()
teamsAndStats(teamsAndLinks)
