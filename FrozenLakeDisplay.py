import pygame
from random import randint
pygame.init()

# Colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Screen
size = [600,340]
move_size = 80
screen = pygame.display.set_mode(size)
def drawBoard():
	pygame.display.set_caption("Frozen Lake")
	pygame.draw.rect(screen,WHITE, [10,10,320,320],10)
	pygame.draw.rect(screen, BLUE, [10,10,80,80])
	pygame.draw.rect(screen, WHITE, [10,90,80,80])
	pygame.draw.rect(screen, WHITE, [10,170,80,80])
	pygame.draw.rect(screen, RED, [10,250,80,80])
	pygame.draw.rect(screen, WHITE, [90,10,80,80])
	pygame.draw.rect(screen, RED, [90,90,80,80])
	pygame.draw.rect(screen, WHITE, [90,170,80,80])
	pygame.draw.rect(screen, WHITE, [90,250,80,80])
	pygame.draw.rect(screen, WHITE, [170,10,80,80])
	pygame.draw.rect(screen, WHITE, [170,90,80,80])
	pygame.draw.rect(screen, WHITE, [170,170,80,80])
	pygame.draw.rect(screen, WHITE, [170,250,80,80])
	pygame.draw.rect(screen, WHITE, [250,10,80,80])
	pygame.draw.rect(screen, RED, [250,90,80,80])
	pygame.draw.rect(screen, RED, [250,170,80,80])
	pygame.draw.rect(screen, GREEN, [250,250,80,80])
	return

x_pos = 0
y_pos = 0

def movePlayer(move):
	global x_pos , y_pos
	if(move == 0):
		print x_pos,y_pos
		x_pos = min(x_pos+1,3)
	elif (move == 2):
		x_pos = max(0,x_pos-1)
	elif (move == 1):
		y_pos = max(0,y_pos-1)
	elif (move == 3):
		y_pos = min(y_pos+1,3)
	screen.fill((0,0,0))
	drawBoard()
	pygame.draw.circle(screen, (100,200,150) , [50+80*x_pos , 50+80*y_pos],20)
	print x_pos , y_pos
	return

while(True):
	drawBoard()
	pygame.draw.circle(screen, (100,200,150) , [50+80*x_pos , 50+80*y_pos],20)
	pygame.display.flip()
	mov = int(raw_input())
	print "Received : %r"%mov
	movePlayer(mov)