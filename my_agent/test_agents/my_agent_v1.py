'''
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO: 
<Tell us about your Agent here>

'''

# import any external packages by un-commenting them
# if you'd like to test / request any additional packages - please check with the Coder One team
import random
# import time
import numpy as np
# import pandas as pd
# import sklearn

class agent:

	def __init__(self):
		'''
		Place any initialisation code for your agent here (if any)
		'''
		pass
	

	def next_move(self, game_state, player_state):
		'''
		This method is called each time your Agent is required to choose an action
		If you're just starting out or are new to Python, you can place all your 
		code within the ### CODE HERE ### tags. If you're more familiar with Python
		and how classes and modules work, then go nuts. 
		(Although we recommend that you use the Scrims to check your Agent is working)
		'''
		# a list of all the actions your Agent can choose from
		actions = ['','u','d','l','r','p']
		movement = ['','u','d','l','r']

		self.game_state = game_state
		self.location = player_state.location
		self.tick_number = 0

		ammo = player_state.ammo
		bombs = game_state.bombs
		ammo_drop = game_state.ammo
		#print(bombs)
		action = ''


		# get our surrounding tiles
		surrounding_tiles = self.get_surrounding_tiles(self.location)

		# get list of empty tiles around us
		empty_tiles = self.get_empty_tiles(surrounding_tiles)

		# get a list of safe tiles
		
		if game_state.tick_number > self.tick_number:
			random.shuffle(empty_tiles)
			if not bombs:
				#action = 'p'
				pass
			else:
				for tile in empty_tiles:
					if self.is_safe(tile,bombs):
						action = self.move_to_tile(self.location, tile)
					else:
						continue
		else:
			action = ''

		return action	


	# Helper Functions

	def manhattan_distance(self, start, end):
		distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
		return distance

	def get_surrounding_tiles(self, location):

		# find all the surrounding tiles relative to us
		# location[0] = col index; location[1] = row index
		tile_up = (location[0], location[1]+1)	
		tile_down = (location[0], location[1]-1)     
		tile_left = (location[0]-1, location[1]) 
		tile_right = (location[0]+1, location[1]) 		 

		# combine these into a list
		all_surrounding_tiles = [tile_up, tile_down, tile_left, tile_right]

		# we'll need to remove tiles that cross the border of the map
		# start with an empty list to store our valid surrounding tiles
		valid_surrounding_tiles = []

		# loop through our tiles
		for tile in all_surrounding_tiles:
			# check if the tile is within the boundaries of the game
			if self.game_state.is_in_bounds(tile):
				# if yes, then add them to our list
				valid_surrounding_tiles.append(tile)

		return valid_surrounding_tiles

	def get_empty_tiles(self, tiles):

		# empty list to store our empty tiles
		empty_tiles = []

		for tile in tiles:
			if not self.game_state.is_occupied(tile) or self.game_state.entity_at(tile) == 'a' or self.game_state.entity_at(tile)=='t':
				# the tile isn't occupied, so we'll add it to the list
				empty_tiles.append(tile)

		return empty_tiles

	def get_safe_tiles(self,tiles,bombs):
		safe_tiles = []
		for tile in tiles:
			for bomb in bombs:
				dist = tuple(x-y for x, y in zip(tile, bomb)) 
				if dist in [(0,1),(1,0),(0,-1),(-1,0),(0,0),(0,2),(2,0),(0,-2),(-2,0)]:
					pass
				else:
					safe_tiles.append(tile)

		return safe_tiles

	def is_safe(self,tile,bombs):
		if not bombs:
			return True
		for bomb in bombs:
			dist = tuple(x-y for x, y in zip(tile, bomb)) 
			if dist in [(0,1),(1,0),(0,-1),(-1,0),(0,0),(0,2),(2,0),(0,-2),(-2,0)]:
				return False
			else:
				return True

	def move_to_tile(self, location, tile):

		actions = ['', 'u', 'd', 'l','r','p']

		print(f"my tile: {tile}")

		# see where the tile is relative to our current location
		diff = tuple(x-y for x, y in zip(self.location, tile))

		# return the action that moves in the direction of the tile
		if diff == (0,1):
			action = 'd'
		elif diff == (1,0):
			action = 'l'
		elif diff == (0,-1):
			action = 'u'
		elif diff == (-1,0):
			action = 'r'
		else:
			action = ''

		return action