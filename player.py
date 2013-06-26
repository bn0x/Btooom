#!/usr/bin/env python

import utils
import pygame
from pygame.locals import *

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y, surface):
		super(Player, self).__init__()

		self.x = x
		self.y = y

		self.dx = 0
		self.dy = 0

		self.speed = 0.2

		self.surface = surface

		self.image = utils.loadImage("player.png")

		self.width = self.image.get_width()
		self.height = self.image.get_height()

		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

		arrowKeys = {"up": 		K_UP,
					 "down": 	K_DOWN,
					 "left":	K_LEFT,
					 "right":	K_RIGHT}

		wasdKeys = {"up":		K_w,
					"down": 	K_s,
					"left":		K_a,
					"right":	K_d}

		self.chosenKeys = wasdKeys

		self.life = 100

	def input(self, event):
		keys = pygame.key.get_pressed()

		if keys[self.chosenKeys["left"]]:
			self.moveLeft()
		elif keys[self.chosenKeys["right"]]:
			self.moveRight()
		else:
			self.stopX()

		if keys[self.chosenKeys["down"]]:
			self.moveDown()
		elif keys[self.chosenKeys["up"]]:
			self.moveUp()
		else:
			self.stopY()

	def updatePosition(self, delta):
		self.x += self.dx * self.speed * delta
		self.y += self.dy * self.speed * delta

		self.rect.x = self.x
		self.rect.y = self.y

	def checkCollisions(self):
		if self.x <= 0:
			self.x = 0
		elif self.x >= self.surface.get_width() - self.width:
			self.x = self.surface.get_width() - self.width

		if self.y <= 0:
			self.y = 0
		elif self.y >= self.surface.get_height() - self.height:
			self.y = self.surface.get_height() - self.height

	def update(self, delta):
		self.updatePosition(delta)
		self.checkCollisions()

	def render(self):
		self.surface.blit(self.image, (self.x, self.y))

	def moveUp(self):
		self.dy = -1

	def moveDown(self):
		self.dy = 1

	def moveLeft(self):
		self.dx = -1

	def moveRight(self):
		self.dx = 1

	def stopY(self):
		self.dy = 0

	def stopX(self):
		self.dx = 0

	def getLife(self): return self.life
	def increaseLife(amount): self.life += amount
	def decreaseLife(amount): self.life -= amount 