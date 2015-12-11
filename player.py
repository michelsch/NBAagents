import sys
import inspect
import heapq
import util
import math
import random
import player_data

teamsAndLinks = player_data.teamsAndLinks()
teamsAndStats = player_data.teamsAndStats(teamsAndLinks)
latest_stats = player_data.teamsAndPlayerStats(teamsAndStats)

'''NBA Teams:

  Atlantic:
    Boston Celtics
    Brooklyn Nets
    New York Knicks
    Philadelphia 76ers
    Toronto Raptors

  Southwest:
    Dallas Mavericks
    Houston Rockets
    Memphis Grizzlies
    New Orleans Pelicans
    San Antonio Spurs

  Central:
    Chicago Bulls
    Cleveland Cavaliers
    Detroit Pistons
    Indiana Pacers
    Milwaukee Bucks

  Northwest:
    Denver Nuggets
    Minnesota Timberwolves
    Oklahoma City Thunder
    Portland Trail Blazers
    Utah Jazz

  Southeast:
    Atlanta Hawks
    Charlotte Hornets
    Miami Heat
    Orlando Magic
    Washington Wizards

  Pacific:
    Golden State Warriors
    Los Angeles Clippers
    Los Angeles Lakers
    Phoenix Suns
    Sacramento Kings
'''
class Team:

 '''
 Defines a team composed of players and a coachg
 Useful published stats about a game (assume given as avg. per game):
 '''
 def __init__(self, team_data):
    self.team_data = team_data
    self.players = []
    for player in team_data:
      self.players.append(player)


#this implementation taken from http://stackoverflow.com/questions/1556232/how-to-select-an-item-from-a-list-with-known-percentages-in-python
class WeightedChoice(object):
  def __init__(self, weights):
    self._total_weight = 0
    self._item_levels = []
    for item, weight in weights:
      self._total_weight += weight
      self._item_levels.append((self._total_weight, item))

  def pick(self):
    pick = self._total_weight * random.random()
    for level, item in self._item_levels:
      if level >= pick:
        return item

# An abstract class representing a Markov Decision Process (MDP).
class MDP:

  def __init__(self, home_team, away_team):
    self.time_left = 42
    self.home_team = home_team
    self.away_team = away_team
    self.home_players_and_minutes_played = [(player,latest_stats[home_team][player][2]) for player in latest_stats[home_team]]
    self.away_players_and_minutes_played = [(player,latest_stats[away_team][player][2]) for player in latest_stats[away_team]]
    self.home_team_score = 0
    self.away_team_score = 0
    self.home_team_picked_players = []
    self.away_team_picked_players = []

  # Return the start state.
  #a tuple of starting players and initial time left of 42 min
  def startState(self):
    for i in range(0,5):
      choices = WeightedChoice(self.home_players_and_minutes_played)
      picked_player = choices.pick()
      self.home_team_picked_players.append(picked_player)
      minutes = latest_stats[self.home_team][picked_player][2]
      self.home_players_and_minutes_played.remove((picked_player,minutes))
    for i in range(0,5):
      choices = WeightedChoice(self.away_players_and_minutes_played)
      picked_player = choices.pick()
      self.away_team_picked_players.append(picked_player)
      minutes = latest_stats[self.away_team][picked_player][2]
      self.away_players_and_minutes_played.remove((picked_player,minutes))
    return (self.home_team_picked_players,self.away_team_picked_players,self.time_left)

    # Return set of actions possible from |state|.
    def actions(self, state): raise NotImplementedError("Override me")

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    # Mapping to notation from class:
    #   state = s, action = a, newState = s', prob = T(s, a, s'), reward = Reward(s, a, s')
    # If IsEnd(state), return the empty list.
    def succAndProbReward(self, state, action): raise NotImplementedError("Override me")

    def discount(self): raise NotImplementedError("Override me")

    # Compute set of states reachable from startState.  Helper function for
    # MDPAlgorithms to know which states to compute values and policies for.
    # This function sets |self.states| to be the set of all states.
    def computeStates(self):
        self.states = set()
        queue = []
        self.states.add(self.startState())
        queue.append(self.startState())
        while len(queue) > 0:
            state = queue.pop()
            for action in self.actions(state):
                for newState, prob, reward in self.succAndProbReward(state, action):
                    if newState not in self.states:
                        self.states.add(newState)
                        queue.append(newState)
        # print "%d states" % len(self.states)
        # print self.states

"""
 Data structures useful for implementing SearchAgents
"""

class Stack:
  "A container with a last-in-first-out (LIFO) queuing policy."
  def __init__(self):
    self.list = []

  def push(self,item):
    "Push 'item' onto the stack"
    self.list.append(item)

  def pop(self):
    "Pop the most recently pushed item from the stack"
    return self.list.pop()

  def isEmpty(self):
    "Returns true if the stack is empty"
    return len(self.list) == 0

class Queue:
  "A container with a first-in-first-out (FIFO) queuing policy."
  def __init__(self):
    self.list = []

  def push(self,item):
    "Enqueue the 'item' into the queue"
    self.list.insert(0,item)

  def pop(self):
    """
      Dequeue the earliest enqueued item still in the queue. This
      operation removes the item from the queue.
    """
    return self.list.pop()

  def isEmpty(self):
    "Returns true if the queue is empty"
    return len(self.list) == 0

class PriorityQueue:
  """
    Implements a priority queue data structure. Each inserted item
    has a priority associated with it and the client is usually interested
    in quick retrieval of the lowest-priority item in the queue. This
    data structure allows O(1) access to the lowest-priority item.

    Note that this PriorityQueue does not allow you to change the priority
    of an item.  However, you may insert the same item multiple times with
    different priorities.
  """
  def  __init__(self):
    self.heap = []

  def push(self, item, priority):
      pair = (priority,item)
      heapq.heappush(self.heap,pair)

  def pop(self):
      (priority,item) = heapq.heappop(self.heap)
      return item

  def isEmpty(self):
    return len(self.heap) == 0


test_game = MDP('Miami Heat','Orlando Magic')
test_game.startState()
