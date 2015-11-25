import sys
import inspect
import heapq
import util
import math
import random

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

'''Defines a team composed of players and a coach

  Useful published stats about a game (assume given as avg. per game):
'''

  def __init__(self):

class Player(Team):

'''Defines a player for an NBA team
  Players can be modelled as an MDP
  nodes with corresponding probabilties
  of scoring, fouling, etc.

  Useful published stats about a player (assume given as avg. per game):
  AGE -- Age
  GP -- Games Played
  PTS -- Points scored
  FGM -- Field goals made (both 2 and 3 pointers)
  FGA -- Field goals attempted
  FG% -- Field goals percentage (made/attempted)
  3PM -- 3P Field goals made
  3PA -- 3P Field goals attempted
  3P% -- 3P Field Goal percentage
  FTM -- Free throws made
  FTA -- Free throws attempted
  FT% -- Free throws percentage
  OREB -- Offensive Rebounds
  DREB -- Defensive Rebounds
  REB --  Rebounds
  AST --  Assists (When a player completes a pass to a teammate
                        that directly leads to a made field goal)
  STL -- Steals (Causes a turnover)
  BLK -- Blocks
  TOV -- Turnovers (Losing the ball)
  PF -- Personal Fouls that a player OR team has committed

'''
  numPlayers = 0

  def __init__(self):

class Coach(Team):

'''Defines a coach for an NBA team.
   Coaches will choose player placements
   strategically following a minimax policy
   in regards to the other opposing coach
'''

  def __init__(self):



#Option: Model Players as Agents and follow an MDP:

# An abstract class representing a Markov Decision Process (MDP).
class MDP:
    # Return the start state.
    #For example, starting players and time
    def startState(self): raise NotImplementedError("Override me")

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


#Another Option: Model as an actual game


#Food for thought: Can we combine both


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
