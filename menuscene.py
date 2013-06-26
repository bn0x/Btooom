#!/usr/bin/env python

import utils
import pygame
from scene import Scene
from pygame.locals import *

class MenuScene(Scene):
	def __init__(self):
		super(MenuScene, self).__init__()

	def input(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				utils.quit()

	def update(self):
		pass

	def render(self):
		self.window.blit(self.gameListSurface, (0, 0))
		self.window.blit(self.chatSurface, (0, self.gameListSurface.get_height()))
		self.window.blit(self.infoSurface, (self.gameListSurface.get_width(), 0))

	def setup(self):
		self.gameListSurface = pygame.Surface((self.window.get_width() - 200,
											   self.window.get_height() - 200))

		self.chatSurface = pygame.Surface((self.window.get_width(), 200))

		self.infoSurface = pygame.Surface((self.gameListSurface.get_width(),
												  self.gameListSurface.get_height()))