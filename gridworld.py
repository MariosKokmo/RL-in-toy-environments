# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:45:07 2020

@author: mario
"""

import numpy as np

class world():
    
    def __init__(self,height, width, reward, initial, final_reward, cliff=False, simple=True):
        self.height = height
        self.width = width
        self.reward = reward
        self.initial = initial
        self.final_reward = final_reward
        self.cliff = cliff
        self.simple = simple
    
    
    
    def create_world(self):
        """
        
    
        Parameters
        ----------
        height : integer
            the height of the grid. (0,0) at the top left
        width : integer
            the width of the grid.
        reward : tuple
            the first item is the reward for a simple step
            the second item is the reward of the cliff.
        initial : tuple
            initial state.
        final_reward : integer
            reward of the goal state.
        cliff : boolean, optional
            Include a cliff. The default is False.
    
        Returns
        -------
        grid : 2D numpy array
            the grid with the (0,0) at the top left.
        rewards : 2D numpy array
            array of integers representing the received reward
            for every position on the grid.
    
        """
        rewards = self.reward[0] * np.ones((self.height,self.width))
        if self.cliff:
            if self.simple:
                rewards[-1][:]= self.reward[1]
            else:
                rewards[0][:]= self.reward[1]
                rewards[self.height//2][:self.width//2]= self.reward[1]
                rewards[-2][- self.width//2 + 1:]= self.reward[1]
                
        rewards[self.initial[0],self.initial[1]] = self.reward[0]
        rewards[-1,-1] = self.final_reward # final state is always bottom right
        grid = np.array([np.arange(self.width*i,self.width*(i+1)) for i in range(self.height)])
    
        return (grid,rewards)
    


    def reset(self):
        return (0,0)
    
    def transition(self,env, state, action):
        """
        
    
        Parameters
        ----------
        env : tuple consisting of grid and rewards numpy arrays
        grid : 2D numpy array 
            the position on the world.
        rewards : 2D numpy array
            contains the integer reward received
            when we move to that position.
        state : tuple
            contains the coordinates of the current state.
        action : integer
            0:UP, 1:DOWN, 2:RIGHT, 3:LEFT.
    
        Returns
        -------
        new_state_ : Tuple
            the new coordinates after the transition.
        reward : integer
            the reward for moving to the new position.
        done : boolean
            indicates we reached the final state.
    
        """
        grid = env[0]
        rewards = env[1]
        height_index = len(grid)-1
        width_index = len(grid[0])-1
        done = False
    
        
        if state[0]>height_index or state[1]>width_index:
            print("The state is out of the grid")
            return
        # if up stays at the same column
        if action == 0:
            new_state = grid[max(0,state[0]-1)][state[1]]
            reward = rewards[max(0,state[0]-1)][state[1]]
        elif action == 1: # if down
            new_state = grid[min(height_index,state[0]+1)][state[1]]
            reward = rewards[min(height_index,state[0]+1)][state[1]]
        elif action == 2: # if right
            new_state = grid[state[0]][min(state[1]+1,width_index)]
            reward = rewards[state[0]][min(state[1]+1,width_index)]
        else: # left
            new_state = grid[state[0]][max(state[1]-1,0)]
            reward = rewards[state[0]][max(state[1]-1,0)]
        
        # new_state is an integer
        # new_state_ in tupled coordinates
        
        if height_index >= width_index:
            for i in range(height_index+1):
                if (i*(width_index+1)<=new_state) and (new_state < (i+1)*(width_index+1)):
                    new_state_ = (i,(new_state % (width_index+1)))
                    break
        else:
            for i in range(height_index+1):
                if i*(width_index+1)<=new_state and new_state <= (i+1)*(width_index+1)-1:
                    new_state_ = (i,(new_state % (width_index+1)))
                    break
            
        
        # if we reach the goal or we fall down the cliff
        if new_state == grid[-1][-1] or rewards[new_state_[0],new_state_[1]] == -100:
            done = True
        
        return (new_state_, reward, done)

