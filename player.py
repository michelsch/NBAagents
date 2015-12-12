import sys
import inspect
import heapq
import util
import math
import random
import player_data
import numpy

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
    self.home_team_score = 0
    self.away_team_score = 0

    self.home_players_and_minutes_played = [(player,latest_stats[home_team][player][2]) for player in latest_stats[home_team]]
    self.away_players_and_minutes_played = [(player,latest_stats[away_team][player][2]) for player in latest_stats[away_team]]

    self.home_team_picked_players = []
    self.away_team_picked_players = []

    #calculate all average stats for a team
    self.home_team_averages = [0]*28
    for player in latest_stats[home_team]:
      a = numpy.array(latest_stats[home_team][player])
      self.home_team_averages += numpy.add(self.home_team_averages,a)
    self.home_team_averages = numpy.divide(self.home_team_averages,len(latest_stats[home_team]))
    self.away_team_averages = [0]*28
    for player in latest_stats[away_team]:
      a = numpy.array(latest_stats[away_team][player])
      self.away_team_averages += numpy.add(self.away_team_averages,a)
    self.away_team_averages = numpy.divide(self.away_team_averages,len(latest_stats[away_team]))

  # Return the start state.
  #  returns a tuple of player holding the ball, team holding the ball
  # time left and respective scores for home and away teams
  def startState(self):
    for i in range(0,5):
      choices = WeightedChoice(self.home_players_and_minutes_played)
      picked_player = choices.pick()
      minutes = latest_stats[self.home_team][picked_player][2]
      self.home_team_picked_players.append((picked_player,minutes))
      self.home_players_and_minutes_played.remove((picked_player,minutes))
    for i in range(0,5):
      choices = WeightedChoice(self.away_players_and_minutes_played)
      picked_player = choices.pick()
      minutes = latest_stats[self.away_team][picked_player][2]
      self.away_team_picked_players.append((picked_player,minutes))
      self.away_players_and_minutes_played.remove((picked_player,minutes))

    player_holding = random.choice([player[0] for player in self.home_team_picked_players]+[player[0] for player in self.away_team_picked_players])
    if player_holding in latest_stats[self.home_team]:
      team_holding = self.home_team
    else:
      team_holding = self.away_team
    #print 'Game starting! Player in possesion: ' + player_holding + '. Team: ' + team_holding
    return (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)

    # Return set of actions possible from |state|.
  def actions(self, state):
    return ['stay','move','pass_ball','try_to_score']

    # Return a list of (newState, prob, reward) tuples corresponding to edges
    # coming out of |state|.
    # Mapping to notation from class:
    #   state = s, action = a, newState = s', prob = T(s, a, s'), reward = Reward(s, a, s')
    # If IsEnd(state), return the empty list.
  def succAndProbReward(self, state, action):

    if self.time_left == 0:
      #print 'Game over! Final Score: ' + self.home_team + '-'+ str(self.home_team_score) + ' ' + self.away_team + '-' + str(self.away_team_score)
      return []

    player_holding = state[0]
    team_holding = state[1]

    def player_scores_free_throw(player):
      try:
        percent = latest_stats[self.home_team][player][22]*100
      except:
        percent = latest_stats[self.away_team][player][22]*100
      return random.randrange(100) < percent

    def player_scores_field_goal(player):
      try:
        percent = latest_stats[self.home_team][player][16]*100
      except:
        percent = latest_stats[self.away_team][player][16]*100
      return random.randrange(100) < percent

    #all actions decrease the time
    if action == 'stay':
      #print player_holding + ' of ' + team_holding + ' is idle.'
      self.time_left -= 1
      #possibility 1 = nothing happens, but player decreases chance to score by 1%
      if player_holding in latest_stats[self.home_team]:
        latest_stats[self.home_team][player_holding][16] *= 0.99
      else:
        latest_stats[self.away_team][player_holding][16] *= 0.99
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      p1 = (newState,1.0/3,0)
      #possibility 2 = ball taken from player by opposing team
      if player_holding in latest_stats[self.home_team]:
        choices = WeightedChoice(self.away_team_picked_players)
        player_holding  = choices.pick()
        team_holding = self.away_team
      else:
        choices = WeightedChoice(self.home_team_picked_players)
        player_holding  = choices.pick()
        team_holding = self.home_team
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      p2 = (newState,1.0/3,-1)
      #possibility 3 = player commits a foul. assume same player as possiblity 2 has ball
      if player_scores_free_throw(player_holding):
        #print player_holding + ' of ' + team_holding + ' scores a free throw!'
        if team_holding == self.away_team:
          self.home_team_score += 1
        else:
          self.away_team_score +=1
      p3 = (newState,1.0/3,-1)
      return [p1,p2,p3]

    if action == 'move':
      #print player_holding + ' of ' + team_holding + ' is moving.'
      self.time_left -= 1
      #possibility 1 = nothing happens, but player increases chance to score by 1%
      if player_holding in latest_stats[self.home_team]:
        latest_stats[self.home_team][player_holding][16] *= 1.01
      else:
        latest_stats[self.away_team][player_holding][16] *= 1.01
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      p1 = (newState,1.0/3,0)
      #possibility 2 = ball taken from player by opposing team
      if player_holding in latest_stats[self.home_team]:
        choices = WeightedChoice(self.away_team_picked_players)
        player_holding  = choices.pick()
        team_holding = self.away_team
      else:
        choices = WeightedChoice(self.home_team_picked_players)
        player_holding  = choices.pick()
        team_holding = self.home_team
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      p2 = (newState,1.0/3,-1)
      #possibility 3 = player commits a foul. assume same player as possiblity 2 has ball
      if player_scores_free_throw(player_holding):
        #print player_holding + ' of ' + team_holding + ' scores a free throw!'
        if team_holding == self.away_team:
          self.home_team_score += 1
        else:
          self.away_team_score +=1
      p3 = (newState,1.0/3,-1)
      return [p1,p2,p3]

    if action == 'pass_ball':
      #print player_holding + ' of ' + team_holding + ' passing the ball!'
      self.time_left -= 1
      #possiblity 1 = another player in the team gains possesion of the ball
      if player_holding in latest_stats[self.home_team]:
        choices = WeightedChoice(self.home_team_picked_players)
        player_holding  = choices.pick()
      else:
        choices = WeightedChoice(self.away_team_picked_players)
        player_holding  = choices.pick()
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      p1 = (newState,4.0/5,1)
      #possiblity 2 = another player in the opposing team gains posession of the ball
      if player_holding in latest_stats[self.home_team]:
        choices = WeightedChoice(self.away_team_picked_players)
        player_holding  = choices.pick()
        team_holding = self.away_team
      else:
        choices = WeightedChoice(self.home_team_picked_players)
        player_holding  = choices.pick()
        team_holding = self.home_team
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      p2 = (newState,1.0/5,-1)
      return [p1,p2]

    if action == 'try_to_score':
      #print player_holding + ' of ' + team_holding + ' trying to score!'
      self.time_left -= 1
      #possiblity 1  = another player in the team gains possesion of the ball
      if player_holding in latest_stats[self.home_team]:
        choices = WeightedChoice(self.home_team_picked_players)
        player_holding  = choices.pick()
      else:
        choices = WeightedChoice(self.away_team_picked_players)
        player_holding  = choices.pick()
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      try:
        prob = (1-latest_stats[self.home_team][player_holding][16])/2
      except:
        prob = (1-latest_stats[self.away_team][player_holding][16])/2
      p1 = (newState,prob,1)
      #possiblity 2 = field goal
      if player_scores_field_goal(player_holding):
        #print player_holding + ' of ' + team_holding + ' scores a field goal!'
        if team_holding == self.away_team:
          self.home_team_score += 3
        else:
          self.away_team_score +=3
      if player_holding in latest_stats[self.home_team]:
        choices = WeightedChoice(self.home_team_picked_players)
        player_holding  = choices.pick()
      else:
        choices = WeightedChoice(self.away_team_picked_players)
        player_holding  = choices.pick()
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      try:
        prob = 1-latest_stats[self.home_team][player_holding][16]
      except:
        prob = 1-latest_stats[self.away_team][player_holding][16]
      p2 = (newState,prob,3)
      #possiblity 3 = another player in the opposing team gains posession of the ball
      newState = (player_holding,team_holding,self.time_left,self.home_team_score,self.away_team_score)
      try:
        prob = (1-latest_stats[self.home_team][player_holding][16])/2
      except:
        prob = (1-latest_stats[self.away_team][player_holding][16])/2
      p3 = (newState,prob,-1)
      return [p1,p2,p3]


  def discount(self): return 1

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

class ValueIteration(MDP):
    '''
    Solve the MDP using value iteration.  Your solve() method must set
    - self.V to the dictionary mapping states to optimal values
    - self.pi to the dictionary mapping states to an optimal action
    Note: epsilon is the error tolerance: you should stop value iteration when
    all of the values change by less than epsilon.
    The ValueIteration class is a subclass of util.MDPAlgorithm (see util.py).
    '''
    def solve(self, mdp, epsilon=0.001):
        mdp.computeStates()
        def computeQ(mdp, V, state, action):
            # Return Q(state, action) based on V(state).
            return sum(prob * (reward + mdp.discount() * V[newState]) \
                            for newState, prob, reward in mdp.succAndProbReward(state, action))

        def computeOptimalPolicy(mdp, V):
            # Return the optimal policy given the values V.
            pi = {}
            for state in mdp.states:
                pi[state] = max((computeQ(mdp, V, state, action), action) for action in mdp.actions(state))[1]
            return pi

        V = collections.Counter()  # state -> value of state
        numIters = 0
        while True:
            newV = {}
            for state in mdp.states:
                newV[state] = max(computeQ(mdp, V, state, action) for action in mdp.actions(state))
            numIters += 1
            if max(abs(V[state] - newV[state]) for state in mdp.states) < epsilon:
                V = newV
                break
            V = newV

        # Compute the optimal policy now
        pi = computeOptimalPolicy(mdp, V)
        print "ValueIteration: %d iterations" % numIters
        self.pi = pi
        self.V = V

def simulate_games(home_team,away_team):
  home_wins = 0
  away_wins = 0
  for i in range(0,1000):
    test_game = MDP(home_team,away_team)
    test_game.computeStates()
    if test_game.home_team_score > test_game.away_team_score:
      home_wins += 1
    elif test_game.home_team_score < test_game.away_team_score:
      away_wins += 1
  print home_team + " wins " + str(home_wins*100/(home_wins+away_wins)) + " percent of the time!"
  return home_wins*100/(home_wins+away_wins)

'''Predictions for 6 of Friday's NBA Games'''
simulate_games('Cleveland Cavaliers','Orlando Magic')
simulate_games('Miami Heat','Indiana Pacers')
simulate_games('Milwaukee Bucks','Toronto Raptors')
simulate_games('Charlotte Hornets','Memphis Grizzlies')
simulate_games('Oklahoma City Thunder','Utah Jazz')
simulate_games('Los Angeles Lakers','San Antonio Spurs')
