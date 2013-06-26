#!/usr/bin/env python

import utils
import pygame

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super(Player, self).__init__()

		self.x = x
		self.y = y

		self.dx = 0
		self.dy = 0

		self.speed = 1

		self.image = utils.loadImage("player.png")

		self.width = self.image.get_width()
		self.height = self.image.get_height()

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

	def input(self, event):
		pass

	def update(self, delta):
		pass

	def render(self, surface):
		surface.blit(self.image, (self.x, self.y))