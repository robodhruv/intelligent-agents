import tensorflow as tf
import tensorflow.contrib.slim as slim
import tflearn
import numpy as np
from random import randint
import matplotlib.pyplot as plt
import gym

# The Environment runs for only 200 iteration after which done = True

episodes = 10000
gamma = 0.9

def discounted_reward(r):
	length = len(r)
	discounted = np.zeroes_like(r)
	acc = 0
	for i in reverse(range(length)):
		acc = gamma*acc + r[i]
		discounted[i] = acc
	return discounted

env = gym.make('MountainCar-v0')
obs_size = 2
a_size = 3

# Action space is discrete(3) ie 0,1,2
# Observation space is box(2,)
for i in range(20):
	s = env.reset()
	j = 0
	done = False
	total_reward = 0
	while(not done):
		inp = int(raw_input())
		s, r , done , _ = env.step(inp)
		print s
		env.render()
		total_reward += r
		j += 1
		print j , ":" , total_reward
