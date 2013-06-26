#!/usr/bin/env python

from playscene import PlayScene
from menuscene import MenuScene

class SceneManager(object):
	def __init__(self, window):
		self.window = window
		self.setScene(MenuScene())
		
	def setScene(self, scene):
		self.scene = scene
		self.scene.manager = self
		self.scene.window = self.window
		self.scene.setup()
														
	def reset(self):
		self.setScene(MenuScene())
																	
	def getScene(self):
		return self.scene
