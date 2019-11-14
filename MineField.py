# MineField.py

import random
import math
import time

def getRandomInBounds(bounds):
	return random.randint(bounds[0][0], bounds[1][0]),random.randint(bounds[0][1], bounds[1][1])

def bernoulli(p):
	return random.random() < p


class Mines:

	def __init__(self, num):
		bounds =  ((0, 0), (20, 20))
		self.mines = {}
		self.bot = Bot()
		self.bounds = bounds
		for i in range(num):
			self.mines[(getRandomInBounds(bounds), getRandomInBounds(bounds))] = random.random()

	def moveBotUp(self):
		if self.bot.getLocation()[0] > 0:
			self.bot.moveUp()
	
	def moveBotDown(self):
		if self.bot.getLocation()[0] < 19:
			self.bot.moveDown()

	def moveBotLeft(self):
		if self.bot.getLocation()[0] > 0:
			self.bot.moveLeft()

	def moveBotRight(self):
		if self.bot.getLocation()[0] < 19:
			self.bot.moveRight()

	def getBotLocation(self):
		return self.bot.getLocation()

	def processMinesList(self, rect=True):
		if rect:
			d = {}
			for mine in self.mines:
				a, b = mine
				low_x = min(a[0], b[0])
				low_y = min(a[1], b[1])
				high_x = max(a[0], b[0])
				high_y = max(a[1], b[1])
				newMine = ((low_x, low_y), (high_x, high_y))
				d[newMine] = self.mines[mine]
			self.mines = d

			return self.mines

	def getBoard(self):
		a = [[0 for i in range(20)] for j in range(20)]
		for mine in self.mines:

			low_x, low_y = mine[0]
			high_x, high_y = mine[1]

			prob = self.mines[mine]
			for x in range(low_x, high_x):
				for y in range(low_y, high_y):
					a[x][y] = prob
		return a
	def __str__(self):
		key = [" .", "..", " :", "::", " ;", ";;", " _", "__", " |", "||"]
		a = [['  ' for i in range(20)] for j in range(20)]
		for mine in self.mines:

			low_x, low_y = mine[0]
			high_x, high_y = mine[1]

			prob = self.mines[mine]
			for x in range(low_x, high_x):
				for y in range(low_y, high_y):
					a[x][y] = key[math.floor(prob * 10)]
		x, y = self.bot.getLocation()
		a[x][y] = 'x'
		s = ""
		for i in a:
			for item in i:
				s += item
			s += "\n"
		return s

class Bot:

	def __init__(self):
		self.location = [0, 0]

	def getLocation(self):
		return self.location

	def moveUp(self):
		self.location[0] -= 1

	def moveDown(self):
		self.location[0] += 1

	def moveLeft(self):
		self.location[1] -= 1

	def moveRight(self):
		self.location[1] += 1

def userPlay():

	print("Try and make it across the mine field.  Press arrow keys to move. Your x is your bot. Probability of dying are listed with their symbols below.")

	print([(i /10, thing) for i, thing in enumerate([" .", "..", " :", "::", " ;", ";;", " _", "__", " |", "||"])])
	print("Good luck!")

	i = Mines(8)
	i.processMinesList()
	board = i.getBoard()
	while True:
		print(i)
		user = input()
		LEFT = 68
		UP = 65
		RIGHT = 67
		DOWN = 66
		if len(user) == 3:
			num = ord(user[-1])
			if num == LEFT:
				i.moveBotLeft()
			elif num == RIGHT:
				i.moveBotRight()
			elif num == UP:
				i.moveBotUp()
			elif num == DOWN:
				i.moveBotDown()
		row, col = i.getBotLocation()
		if col == 19:
			print("You Win")
			break
		prob = board[row][col]

		dead = bernoulli(prob)
		if dead:
			print("DEAD")
			break




userPlay()



