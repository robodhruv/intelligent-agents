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
# Colors
RED = (255,51,51)
GREEN = (102,255,102)
BLUE = (0,0,255)
WHITE = (224,224,224)
BLACK = (64,64,64)


import numpy as np
import pygame
import matplotlib.pyplot as plt
from random import randint
pygame.init()

def initializeVariable():
	global observation_space, startPoint , endPoint, holes
	print "Enter number of rows:"
	rows = int(raw_input(">"))
	print "Enter number of cols:"
	cols = int(raw_input(">"))
	observation_space = [rows,cols]
	print "Input Board:"
	i = 0
	while(i < rows):
		r1 = raw_input()
		j = 0
		while(j < cols):
			if(r1[j] == "S"):
				startPoint = [j , i]
			elif(r1[j] == "H"):
				holes.append([j,i])
			elif(r1[j] == "G"):
				endPoint = [j,i]
			j += 1
		i += 1
	return

observation_space = []
startPoint = []
endPoint = []
holes = []
action_space = 4
alpha = 0.1
epsilon = 0.4 # Ratio of Exploitation vs Exploration
episodes = 10000


initializeVariable()

move_size = 40
size = [20+move_size*(observation_space[1]),20+move_size*(observation_space[0])]
screen = pygame.display.set_mode(size)
def drawBoard():
	global startPoint , endPoint , holes
	pygame.display.set_caption("Frozen Lake")
	pygame.draw.rect(screen,WHITE, [10,10,320,320],10)
	for i in range(observation_space[0]):
		for j in range(observation_space[1]):
			if([j,i] in holes):
				pygame.draw.rect(screen,RED,[10+move_size*j,10+move_size*i,move_size,move_size])
			elif ([j,i] == startPoint):
				pygame.draw.rect(screen,BLUE,[10+move_size*j,10+move_size*i,move_size,move_size])
			elif ([j,i] == endPoint):
				pygame.draw.rect(screen,GREEN,[10+move_size*j,10+move_size*i,move_size,move_size])
			else:
				pygame.draw.rect(screen,WHITE,[10+move_size*j,10+move_size*i,move_size,move_size])
	return

qTable = np.zeros((observation_space[0]*observation_space[1],action_space),np.float32)
count_exploration = 0
count_exploitation = 0

def step(state_i,move):
	global observation_space ,endPoint , startPoint, holes
	x_pos = state_i%(observation_space[1])
	y_pos = state_i/(observation_space[1])
	reward = 0
	done = False
	if(move == 0): #Right
		x_pos = min(x_pos+1,observation_space[1]-1)
	elif (move == 2): #Left
		x_pos = max(0,x_pos-1)
	elif (move == 1): #Up
		y_pos = max(0,y_pos-1)
	elif (move == 3): #Down
		y_pos = min(y_pos+1,observation_space[0]-1)

	if(x_pos == endPoint[0] and y_pos == endPoint[1]):
		reward = 1
		done = True
	elif ([x_pos , y_pos] in holes):
		reward = -1
		done = True
	return (observation_space[1]*y_pos+x_pos,reward,done)

def generateInitialPos():
	global startPoint, endPoint, holes,observation_space
	rows = observation_space[0]
	cols = observation_space[1]
	fate = randint(1,100)
	if(fate < 50):
		return rows*startPoint[0] + startPoint[1]
	else:
		randomPos = randint(0,rows*cols-1)
		if(([randomPos%cols,randomPos/cols] in holes) or ([randomPos%cols,randomPos/cols] == endPoint)):
			return generateInitialPos()
		else:
			return randomPos

def main():
	global qTable, count_exploitation , count_exploration
	for i in range(episodes):
		if((i+1) % 100 == 0):
			print (i+1)*100/episodes, "%"
		prev_state =  generateInitialPos()
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

def showAgent(n):
	global qTable, startPoint
	for i in range(n):
		prev_state = startPoint[0]+observation_space[1]*startPoint[1]
		done = False
		screen.fill((0,0,0))
		drawBoard()
		pygame.draw.circle(screen, (100,200,150) , [10+ move_size/2+move_size*(prev_state%(observation_space[1])) , 10+ move_size/2+move_size*(prev_state/(observation_space[1]))],15)
		pygame.display.flip()
		pygame.time.wait(1000)
		while(not done):
			print [(prev_state%(observation_space[1])) , (prev_state/(observation_space[1]))]
			max_state = max(qTable[prev_state,:])
			max_action_list = []
			for i,x in enumerate(qTable[prev_state,:]):
				if(x == max_state):
					max_action_list.append(i)
			max_action = max_action_list[randint(0,len(max_action_list)-1)]
			state_n , reward_n, done = step(prev_state,max_action)
			screen.fill((0,0,0))
			drawBoard()
			pygame.draw.circle(screen, (100,200,150) , [10+ move_size/2+move_size*(state_n%(observation_space[1])) , 10+ move_size/2+move_size*(state_n/(observation_space[1]))],15)
			pygame.display.flip()
			prev_state = state_n
			pygame.time.wait(1000)

if __name__ == '__main__':
	main()
	print qTable
	print "Exploitation : %r , Exploration : %r " %(count_exploitation,count_exploration)
	showAgent(2)