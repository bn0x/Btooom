#!/usr/bin/env python

import sys
import pygame
from player import Player
from pygame.locals import *
from scenemanager import SceneManager

class Game(object):
	def __init__(self, width=1024, height=600, caption="Btooom"):
		self.width = width
		self.height = height
		self.caption = caption
		
		self.setupPygame()
		self.setupObjects()
		self.gameLoop()
		
	def input(self):
		self.sceneManager.getScene().input()
		
	def update(self):
		self.sceneManager.getScene().update()
		
	def render(self):
		self.sceneManager.getScene().render()
		
	def gameLoop(self):
		while True:
			self.input()
			self.update()
			self.render()
		
	def setupObjects(self):
		self.sceneManager = SceneManager(self.window)
		
	def setupPygame(self):
		pygame.init()
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption(self.caption)
		
if __name__ == "__main__":
	game = Game()
