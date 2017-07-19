import tensorflow as tf
import numpy as np
from random import randint
import matplotlib
import gym

env = gym.make('MountainCar-v0')
env.reset()
env.render()
done = False

while(not done):
	action = env.action_space.random 
	observation , reward , done , _ = env.step(action)