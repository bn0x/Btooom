#!/usr/bin/env python

import sys
import pygame
from scene import Scene
from player import Player
from pygame.locals import *

class PlayScene(Scene):
	def __init__(self):
		super(PlayScene, self).__init__()

	def input(self):
		for event in pygame.event.get():

			self.player.input(event)

			if event.type == QUIT:
				pygame.quit()
				sys.exit(0)

	def update(self):
		self.player.update(self.delta)

	def render(self):
		self.window.fill((0, 0, 0))

		self.player.render()
		
		pygame.display.update()
		self.delta = self.clock.tick(60)

	def setup(self):
		self.clock = pygame.time.Clock()

		self.player = Player(0, 0, self.window)

		self.delta = 0