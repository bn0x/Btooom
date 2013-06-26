#!/usr/bin/env python

import sys
import pygame
from pygame.locals import *

class Game(object):
	def __init__(self, width=640, height=480, caption="Btooom"):
		self.width = width
		self.height = height
		self.caption = caption
		
		self.setupPygame()
		self.setupObjects()
		self.gameLoop()
		
	def input(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit(0)
				
			# Handle input here
		
	def update(self):
		# Update stuff such as game objects here
		pass
		
	def render(self):
		self.window.fill((0, 0, 0)) # Fill the screen with black
		
		# Draw everything here
		
		pygame.display.update()
		self.delta = self.clock.tick(60) # Keep the game running at 60 FPS
		
	def gameLoop(self):
		while True:
			self.input()
			self.update()
			self.render()
		
	def setupObjects(self):
		self.clock = pygame.time.Clock()
		
	def setupPygame(self):
		pygame.init()
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.caption)
		
if __name__ == "__main__":
	game = Game()
