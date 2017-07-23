#from __future__ import print_function
import gym
import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim
import tflearn
import matplotlib.pyplot as plt

'''
Action Space is Discrete(4):
	0 - 
	1 -  
	2 - 
	3 - 

Observation Space is Box(210,160,3):
The screen is 210*160 pixels in size
The last dimension in observation space is rgb value of the given pixel
	array([0,0,0]) -> Black -> Blank Positions on the Screen
	array([142,142,142]) -> Grey -> Walls, Points/Numbers on the top
	array([200,72,72]),array([198,108,58]),array([180,122,48]),array([162,162,42]),array([72,160,72]),array([66,72,200])->Rows of blocks to breakout
	array([200,72,72]) -> Ball and Slider
'''

# Constants and Parameters
gamma = 0.95
lr = 0.01
# Reward Function
def discounted_reward(r):
	discounted = np.zeros_like(r,dtype = np.float32)
	discounted_sum = 0.0
	for i in range(len(r)):
		discounted_sum = discounted_sum*gamma + r[len(r) - i -1]
		discounted[len(r) - i - 1] = discounted_sum
	return discounted

# Neural Network for Agent
class myAgent():
	def __init__ (self,lr):
		self.input = tf.placeholder(shape = (210,160,3), dtype = tf.float32)
		self.layer = slim.fully_connected(self.input , 16 , activation_fn = tf.nn.relu , biases_initializer = None)
		self.output = slim.fully_connected(self.layer , 4 , activation_fn = tf.nn.softmax , biases_initializer = None)
		self.action_taken = tf.argmax(self.output,1)

		# Learning Procedure
		self.action_holder = tf.placeholder(shape = None, dtype = tf.int32)
		self.reward_holder = tf.placeholder(shape = None, dtype = tf.float32)

		self.indexes = tf.range(0, tf.shape(self.output)[0]) * tf.shape(self.output)[1] + self.action_holder
		self.responsible_outputs = tf.gather(tf.reshape(self.output, [-1]), self.indexes)

		self.loss = -tf.reduce_mean(tf.log(self.responsible_outputs)*self.reward_holder)

		tvars = tf.trainable_variables()
		self.gradient_holders = []
		for idx,var in enumerate(tvars):
			placeholder = tf.placeholder(tf.float32,name=str(idx)+'_holder')
			self.gradient_holders.append(placeholder)

		self.gradients = tf.gradients(self.loss,tvars)

		optimizer = tf.train.AdamOptimizer(learning_rate=lr)
		self.update_batch = optimizer.apply_gradients(zip(self.gradient_holders,tvars))

# Creating the Environment
env = gym.make('Breakout-v0')
env.reset()

# Training the Agent
tf.reset_default_graph() #Clear the Tensorflow graph.
agent = myAgent(lr) #Load the agent.
total_episodes = 1000
max_ep = 200

init = tf.global_variables_initializer()

with tf.Session() as sess:
	sess.run(init)
	total_reward = 0
	total_length = 0
	i = 0
	gradBuffer = sess.run(tf.trainable_variables())

	for ix,grad in enumerate(gradBuffer):
		gradBuffer[ix] = 0

	while i < total_episodes:
		s = env.reset()
		running_reward = 0
		ep_history = []
		for j in range(max_ep):
	#Probabilistically pick an action given our network outputs.
			a_dist = sess.run(agent.output,feed_dict={agent.input:s})
			a = np.random.choice(a_dist[0],1)
			a = np.argmax(a_dist == a)
			#a = sess.run(agent.action_taken ,feed_dict= {agent.input:s})
			s1,r,d,_ = env.step(a) #Get our reward for taking an action given a bandit.
			ep_history.append([s,a,r,s1])
			s = s1
			running_reward += r
			if d == True:
			#Update the network.
				ep_history = np.array(ep_history)
				ep_history[:,2] = discounted_reward(ep_history[:,2])
				feed_dict={agent.reward_holder:ep_history[:,2],
				agent.action_holder:ep_history[:,1],agent.input:np.vstack(ep_history[:,0])}
				grads = sess.run(agent.gradients, feed_dict=feed_dict)
				for idx,grad in enumerate(grads):
					gradBuffer[idx] += grad

				if i % update_frequency == 0 and i != 0:
					feed_dict= dictionary = dict(zip(agent.gradient_holders, gradBuffer))
					_ = sess.run(agent.update_batch, feed_dict=feed_dict)
				for ix,grad in enumerate(gradBuffer):
					gradBuffer[ix] = grad * 0

				total_reward.append(running_reward)
				total_lenght.append(j)
				break
		if (i % 100 == 0):
			print np.mean(total_reward[-100:])
		i += 1

# Plots and Graphs


# Agent in Action