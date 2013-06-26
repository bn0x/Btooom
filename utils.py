#!/usr/bin/env python

import os
import sys
import pygame

def loadImage(fileName):
	return pygame.image.load(os.path.join("Images", fileName))

def loadSound(fileName):
	return pygame.mixer.Sound(os.path.join("Sounds", fileName))

def quit(exitCode=0):
	sys.exit(exitCode)