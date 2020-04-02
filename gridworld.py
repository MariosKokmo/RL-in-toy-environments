# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 19:45:07 2020

@author: mario
"""

import numpy as np

def create_world (height, width, reward, initial, final_reward, cliff=False):
    rewards = reward * np.ones((height,width))
    if cliff:
        rewards[0][:]=-100
        #rewards[initial[0] : (initial[0] + height//2) % height][width // 2] = -100
        rewards[height//2][:width//2]=-100
        rewards[-2][-width//2 + 1:]=-100
    rewards[initial[0],initial[1]] = reward
    rewards[-1,-1] = final_reward # final state is always bottom right
    
    grid = np.array([np.arange(width*i,width*(i+1)) for i in range(height)])
    
    return (grid,rewards)
    
# grid should be bigger than 5x5
env = create_world(5,5,-1,(0,1),100,True)
print(env[1])

def transition(state, action):
    pass
    return (new_state, reward, done)
