''' 
The aim of the agent is to move from initial point S to final point G without falling in holes H
The agent can move up/down/left/right from any point if that move is possible

SFFF       (S: starting point, safe)
FHFH       (F: frozen surface, safe)
FFFH       (H: hole, fall to your doom)
HFFG       (G: goal, where the frisbee is located)

A reward of 1 is given if the agent reaches G 
Initially all others Q(s,a) pairs are given value 0

Action space
	0 - Right
	1 - Up
	2 - Left
	3 - Down

The observation space is 16 cells on the board

Positions are given index = 4*row + col where row,col belongs to {0,1,2,3}
'''

import numpy as np
import matplotlib.pyplot as plt
from random import randint

observation_space = 16
action_space = 4
alpha = 0.1
epsilon = 0.5 # Ratio of Exploitation vs Exploration
episodes = 100

qTable = np.zeros((observation_space,action_space),np.float32)
count_exploration = 0
count_exploitation = 0

def step(state_i,move):
	x_pos = state_i%4
	y_pos = state_i/4
	reward = 0
	done = False
	if(move == 0):
		x_pos = min(x_pos+1,3)
	elif (move == 2):
		x_pos = max(0,x_pos-1)
	elif (move == 1):
		y_pos = max(0,y_pos-1)
	elif (move == 3):
		y_pos = min(y_pos+1,3)

	if(x_pos == 3 and y_pos == 3):
		reward = 1
		done = True
	elif ((x_pos == 3 and y_pos == 1) or (x_pos == 3 and y_pos == 2) or (x_pos == 1 and y_pos == 2)):
		reward = -1
		done = True
	return (4*y_pos+x_pos,reward,done)

def main():
	global qTable, count_exploitation , count_exploration
	for i in range(episodes):
		if (i % 100 == 0):
			print (i/100) , "%"
		prev_state = 0
		done = False
		while(not done):
			fate = randint(1,100)
			if (fate < 100.0*epsilon):
				count_exploitation += 1
				max_state = max(qTable[prev_state,:])
				max_action_list = []
				for i,x in enumerate(qTable[prev_state,:]):
					if(x == max_state):
						max_action_list.append(i)
				max_action = max_action_list[randint(0,len(max_action_list)-1)]
				state_n , reward_n, done = step(prev_state,max_action)
				qTable[prev_state,max_action] += reward_n + alpha*(max(qTable[state_n,:]) - qTable[prev_state,max_action])
				prev_state = state_n
			else:
				count_exploration += 1
				action = randint(0,3)
				state_n, reward_n , done = step(prev_state, action)
				prev_state = state_n

def display(table):
	print "-----------------------------------------------------"
	print "|    %.2f    |    %.2f    |    %.2f    |    %.2f    |" %(table[0][1],table[1][1],table[2][1],table[3][1])
	print "|%.2f    %.2f|%.2f    %.2f|%.2f    %.2f|%.2f    %.2f|" %(table[0][2],table[0][0],table[1][2],table[1][0],table[2][2],table[2][0],table[3][2],table[3][0])
	print "|    %.2f    |    %.2f    |    %.2f    |    %.2f    |" %(table[0][3],table[1][3],table[2][3],table[3][3])
	print "-----------------------------------------------------" 
	print "|    %.2f    |    %.2f    |    %.2f    |    %.2f    |" %(table[4][1],table[5][1],table[6][1],table[7][1])
	print "|%.2f    %.2f|%.2f    %.2f|%.2f    %.2f|%.2f    %.2f|" %(table[4][2],table[4][0],table[5][2],table[5][0],table[6][2],table[6][0],table[7][2],table[7][0])
	print "|    %.2f    |    %.2f    |    %.2f    |    %.2f    |" %(table[4][3],table[5][3],table[6][3],table[7][3])
	print "-----------------------------------------------------"
	print "|    %.2f    |    %.2f    |    %.2f    |    %.2f    |" %(table[8][1],table[9][1],table[10][1],table[11][1])
	print "|%.2f    %.2f|%.2f    %.2f|%.2f    %.2f|%.2f    %.2f|" %(table[8][2],table[8][0],table[9][2],table[9][0],table[10][2],table[10][0],table[11][2],table[11][0])
	print "|    %.2f    |    %.2f    |    %.2f    |    %.2f    |" %(table[8][3],table[9][3],table[10][3],table[11][3])
	print "-----------------------------------------------------"
	print "|    %.2f    |    %.2f    |    %.2f    |    %.2f    |" %(table[12][1],table[13][1],table[14][1],table[15][1])
	print "|%.2f    %.2f|%.2f    %.2f|%.2f    %.2f|%.2f    %.2f|" %(table[12][2],table[12][0],table[13][2],table[13][0],table[14][2],table[14][0],table[15][2],table[15][0])
	print "|    %.2f    |    %.2f    |    %.2f    |    %.2f    |" %(table[12][3],table[13][3],table[14][3],table[15][3])
	print "-----------------------------------------------------"


if __name__ == '__main__':
	main()
	display(qTable)
	print "Exploitation : %r , Exploration : %r " %(count_exploitation,count_exploration)