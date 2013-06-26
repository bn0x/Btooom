#!/usr/bin/env python

class Scene(object):
	def __init__(self):
		pass

	def input(self):
		raise NotImplementedError

	def update(self):
		raise NotImplementedError

	def render(self):
		raise NotImplementedError

	def setup(self):
		raise NotImplementedError