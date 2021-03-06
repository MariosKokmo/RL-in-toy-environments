# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 18:26:32 2020

@author: mario
"""
import numpy as np

class Agent():
    def __init__(self, gamma, alpha, epsilon, n_actions,
                 eps_end = 0.01, eps_dec=5e-3):
        # we initialise the parameters and the Q-table as
        # an empty dictionary
        self.gamma = gamma
        self.alpha = alpha
        self.epsilon = epsilon
        self.n_actions = n_actions
        self.eps_min = eps_end
        self.eps_dec = eps_dec
        self.action_space =[i for i in range(n_actions)]
        self.Q = {}
        self.steps_change_eps = 0
        self.change_every = 30
        
    def choose_action(self, state):
        # if the state has not been visited again,
        # we add it in the Q dictionary and initialise
        # its value to an empty array of size equal to 
        # the number of actions
        if state  not in self.Q:
            self.Q[state] = np.zeros(self.n_actions)
            
        # we select an action in an e-greedy way
        if np.random.random() > self.epsilon:
            action = np.argmax(self.Q[state])
        else:
            action = np.random.choice(self.action_space)
        
        # we decrease the epsilon accordingly
        self.steps_change_eps += 1
        if self.steps_change_eps % self.change_every == 0:
            self.epsilon -= self.eps_dec 
        if self.epsilon < self.eps_min:
            self.epsilon = self.eps_min
        
        return action
    
    def update(self,state, action0, action1, reward, next_state, done):
        # we update the Q table according to the SARSA algorithm
        next_action = action1
        # if we are done the value is set to all zeros
        if done :
            self.Q[state] = np.zeros(self.n_actions)
            return
        
        self.Q[state][action0] += self.alpha * (reward + self.gamma * self.Q[next_state][next_action] - self.Q[state][action0])
        return
