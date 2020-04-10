
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 18:14:32 2020

"""
from gridworld import world
from SARSA_agent import Agent
import numpy as np
import matplotlib.pyplot as plt

    
if __name__== '__main__' :
    height = 5
    width = 5
    penalties = (-1,-100) # penalty for each step and the cliff
    initial_state = (0,0)
    goal_state = (4,4)
    goal_state_reward = 100
    
    grid = world(height,width,penalties,initial_state,goal_state,goal_state_reward,cliff=True,simple=False)
    env = grid.create_world()
    
    agent = Agent(gamma= 1, alpha = 0.01, epsilon=0.9, n_actions=4,
                 eps_end = 0.005, eps_dec=5e-5)
    
    scores, eps_history, average = [], [], []
    n_games = 100000
    t_steps = 50
    n = 0
    avg_score_index = t_steps * 4
    dones=0
    
    for i in range(n_games):
        score = 0 
        done = False
        observation = grid.reset()
        t = 0
        action = agent.choose_action(observation)
        while not done and t < t_steps:
            observation_, reward, done = grid.transition(env,observation,action)
            action_ = agent.choose_action(observation_)
            agent.update(observation, action, action_, reward, observation_, done)
            if done:
                break
            score += reward
            # set the current state equal to the next, ready for
            # the next step
            observation = observation_
            action = action_
            t += 1
            
        scores.append(score)
        eps_history.append(agent.epsilon)
        avg_score = np.mean(scores[-avg_score_index:])
        average.append(avg_score)

        n += 1
        
        print('episode ',i, 'score %.2f' %score,
              'average score %.2f' % avg_score,
              'epsilon %.2f' % agent.epsilon)
        
        
    x = [i+1 for i in range(n)]
    #plot_learning_curve(x,scores,eps_history)
    plt.scatter(x,scores,marker='.')
    plt.xlabel('Episodes')
    plt.ylabel('Scores')
    print(env[0])
    print(env[1])
    print(agent.Q)
    V = np.zeros((5,5))
    for key,value in agent.Q.items():
        row = key[0]
        column = key[1]
        V[row][column] += max(value)
    print(V)
    
    
    
        
    
