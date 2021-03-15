"""
TEMPLATE for creating your own Agent to compete in
'Dungeons and Data Structures' at the Coder One AI Sports Challenge 2020.
For more info and resources, check out: https://bit.ly/aisportschallenge

BIO:
<Tell us about your Agent here>

"""

# import any external packages by un-commenting them
# if you'd like to test / request any additional packages - please check
# with the Coder One team
import random

# import time
import numpy as np

# import pandas as pd
# import sklearn


class agent:
    def __init__(self):
        """
        Place any initialisation code for your agent here (if any)
        """
        global bombdict
        bombdict = {}

        self.planned_actions =  []

        pass

    def next_move(self, game_state, player_state):
        """
        This method is called each time your Agent is required to choose an action
        If you're just starting out or are new to Python, you can place all your
        code within the ### CODE HERE ### tags. If you're more familiar with Python
        and how classes and modules work, then go nuts.
        (Although we recommend that you use the Scrims to check your Agent is working)
        """
        # a list of all the actions your Agent can choose from
        actions = ["", "u", "d", "l", "r", "p"]
        movement = ["", "u", "d", "l", "r"]
        
        if self.planned_actions:
            #print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            #print(self.planned_actions)
            # print(self.planted)
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            # print("$$$$$$$$$$$$$$$$$$$$$$$$$$")
            #print(self.planned_actions[0])
            return self.planned_actions.pop(0)

        self.game_state = game_state
        self.location = player_state.location
        

        ammo = player_state.ammo
        bombs = game_state.bombs
        ammo_drop = game_state.ammo
        treasure = game_state.treasure
        # print(bombs)
        action = ""

        # get our surrounding tiles
        surrounding_tiles = self.get_surrounding_tiles(self.location)

        # get list of empty tiles around us
        empty_tiles = self.get_empty_tiles(surrounding_tiles)

        # get list of diagonally empty tiles
        diagonal_tiles = self.get_diagonal_tiles(self.location)

        # empty diagonal tiles
        empty_diagonals = self.get_empty_tiles(diagonal_tiles)

        # bomb tracking
        itemstodel = []

        explodingbombs = []
        explodingbombs.clear()

        #### GO FOR AMMO FIRST, IF NO AMMO GO FOR TREASURE
        if(ammo_drop):
            self.planned_actions.extend(self.path_to_bomb(ammo_drop))
        elif(treasure):
            self.planned_actions.extend(self.path_to_bomb(treasure))
        else:
            pass
            



        for bomb in game_state.bombs:
            if bomb not in bombdict:
                bombdict[bomb] = game_state.tick_number

        if bombdict:
            for key in bombdict:
                if game_state.tick_number - bombdict[key] >= 27:
                    # add to list of bombs imminent explosion
                    explodingbombs.append(key)
                if game_state.tick_number - bombdict[key] == 35:
                    # print("######################################## bomb go
                    # boom at tick ", game_state.tick_number, " was init at ",
                    # bombdict[key])
                    itemstodel.append(key)
            # calc chain explosion
            for x in itemstodel:
                del bombdict[x]
        place = False
        if place:
            temp = self.bomb_placeable(empty_diagonals, empty_tiles, explodingbombs)
            if temp[0]:
                # self.planted = True
                # print("PLANTED A BOMB BRO")
                self.planned_actions.append(temp[1])
                self.planned_actions.append(temp[2])
                return "p"

        # for key in bombdict:
        # 	print("bomb at location x: ", key[0], " y: ", key[1], " was init at tick number ", bombdict[key], ".")
        # print("current tick : ", game_state.tick_number)
        # get a list of safe tiles

        
        random.shuffle(empty_tiles)
        for tile in empty_tiles:
            if self.is_safe(tile, explodingbombs):
                return self.move_to_tile(self.location, tile)
            else:
                pass
                # temp = self.bomb_placeable(empty_diagonals, empty_tiles, explodingbombs)
                # if temp[0]:
                #     planned_actions.append(temp[1])
                #     return temp[2]

        return action
    def path_to_bomb(self, ammo_drop):
        cost = 1
        closest_bomb = (self.find_nearest_ammo(ammo_drop,self.location))
        path = self.search(self.game_state,cost,self.location, closest_bomb)
        if path:
            # print(path)
            # path.pop(0)
            # print(path)
            i = 0
            planned_path = []
            while i < len(path)-1:
                planned_path.append(self.move_to_tile(path[i],path[i+1]))
                #print(path[i], " " , path[i+1])
                #print(self.move_to_tile(path[i],path[i+1]))
                i+=1
            #print(planned_path)
            return planned_path

    def path_to_treasure(self, treasure):
        cost = 1
        closest_treasure = (self.find_nearest_ammo(treasure,self.location))
        path = self.search(self.game_state,cost,self.location, closest_treasure)
        if path:
            # print(path)
            # path.pop(0)
            # print(path)
            i = 0
            planned_path = []
            while i < len(path)-1:
                planned_path.append(self.move_to_tile(path[i],path[i+1]))
                #print(path[i], " " , path[i+1])
                #print(self.move_to_tile(path[i],path[i+1]))
                i+=1
            #print(planned_path)
            return planned_path
        
       
    def find_nearest_ammo(self, ammo_drop,location):
        min = 999
        closest = location
        for a in ammo_drop:
            if (self.manhattan_distance(location,a)) < min:
                min = self.manhattan_distance(location,a)
                closest = a

        return closest


    def is_safe(self, tile, explodingbombs):
        out = True
        if not explodingbombs:
            out = True
        for bomb in explodingbombs:
            dist = tuple(x - y for x, y in zip(tile, bomb))
            if dist in [
                (0, 1),
                (1, 0),
                (0, -1),
                (-1, 0),
                (0, 0),
                (0, 2),
                (2, 0),
                (0, -2),
                (-2, 0),
            ]:
                out = False
                # print("########################")
                # print("#### DETECTED UNSAFE ###")
                # print("#### TILE AT ###########")
                # print("#### ", dist[0], " ", dist[1], " #####")
                # print("########################")
        return out

    def bomb_placeable(self, empty_diagonals, empty_tiles, explodingbombs):
        for tile in empty_diagonals:
            if self.is_safe(tile, explodingbombs):
                if tile == (self.location[0] - 1, self.location[1] + 1):
                    if (
                        self.location[0],
                        self.location[1] + 1,
                    ) in empty_tiles:
                        # print("GO UP THEN LEFT")
                        # self.planted = False
                        return [True, "l", "u"]
                    elif (
                        self.location[0] - 1,
                        self.location[1],
                    ) in empty_tiles:
                        # print("GO LEFT THEN UP")
                        # self.planted = False
                        return [True, "u", "l"]
                elif tile == (self.location[0] + 1, self.location[1] + 1):
                    if (
                        self.location[0],
                        self.location[1] + 1,
                    ) in empty_tiles:
                        # print("GO UP THEN RIGHT")
                        # self.planted = False
                        return [True, "r", "u"]
                    elif (
                        self.location[0] + 1,
                        self.location[1],
                    ) in empty_tiles:
                        # print("GO RIGHT THEN UP")
                        # self.planted = False
                        return [True, "u", "r"]
                elif tile == (self.location[0] - 1, self.location[1] - 1):
                    if (
                        self.location[0],
                        self.location[1] - 1,
                    ) in empty_tiles:
                        # print("GO DOWN THEN LEFT")
                        # self.planted = False
                        return [True, "l", "d"]
                    elif (
                        self.location[0] - 1,
                        self.location[1],
                    ) in empty_tiles:
                        # print("GO LEFT THEN DOWN")
                        # self.planted = False
                        return [True, "d", "l"]
                elif tile == (self.location[0] + 1, self.location[1] - 1):
                    if (
                        self.location[0],
                        self.location[1] - 1,
                    ) in empty_tiles:
                        # print("GO DOWN THEN RIGHT")
                        # self.planted = False
                        return [True, "r", "d"]
                    elif (
                        self.location[0] + 1,
                        self.location[1],
                    ) in empty_tiles:
                        # print("GO RIGHT THEN DOWN")
                        # self.planted = False
                        return [True, "d", "r"]
        # self.planted = False
        return [False, "", ""]

    def manhattan_distance(self, start, end):
        distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
        return distance

    def get_diagonal_tiles(self, location):
        tile_nw = (location[0] - 1, location[1] + 1)
        tile_ne = (location[0] + 1, location[1] + 1)
        tile_sw = (location[0] - 1, location[1] - 1)
        tile_se = (location[0] + 1, location[1] - 1)

        all_diagonals = [tile_ne, tile_nw, tile_se, tile_sw]

        valid_diagonal_tiles = []
        # loop through our tiles
        for tile in all_diagonals:
            # check if the tile is within the boundaries of the game
            if self.game_state.is_in_bounds(tile):
                # if yes, then add them to our list
                valid_diagonal_tiles.append(tile)
        return valid_diagonal_tiles

    def get_surrounding_tiles(self, location):

        # find all the surrounding tiles relative to us
        # location[0] = col index; location[1] = row index
        tile_up = (location[0], location[1] + 1)
        tile_down = (location[0], location[1] - 1)
        tile_left = (location[0] - 1, location[1])
        tile_right = (location[0] + 1, location[1])

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
            if (
                (not self.game_state.is_occupied(tile))
                or (self.game_state.entity_at(tile) == "a")
                or (self.game_state.entity_at(tile) == "t")
            ):
                # the tile isn't occupied, so we'll add it to the list
                empty_tiles.append(tile)

        return empty_tiles

    def get_safe_tiles(self, tiles, bombs):
        safe_tiles = []
        for tile in tiles:
            for bomb in bombs:
                dist = tuple(x - y for x, y in zip(tile, bomb))
                if dist in [
                    (0, 1),
                    (1, 0),
                    (0, -1),
                    (-1, 0),
                    (0, 0),
                    (0, 2),
                    (2, 0),
                    (0, -2),
                    (-2, 0),
                ]:
                    pass
                else:
                    safe_tiles.append(tile)

        return safe_tiles

    def move_to_tile(self, location, tile):

        actions = ["", "u", "d", "l", "r", "p"]

        # print(f"my tile: {tile}")

        # see where the tile is relative to our current location
        diff = tuple(x - y for x, y in zip(location, tile))

        # return the action that moves in the direction of the tile
        if diff == (0, 1):
            action = "d"
        elif diff == (1, 0):
            action = "l"
        elif diff == (0, -1):
            action = "u"
        elif diff == (-1, 0):
            action = "r"
        else:
            action = ""

        return action
    
    def actually_occupied(self, tile):
        if (self.game_state.is_occupied(tile)) and (not self.game_state.entity_at(tile) == "a") and ( not self.game_state.entity_at(tile) == "t"):
            return True
        else:
            return False
    # Function to return path of search
    def return_path(self,current_node,game_state):
        path = []
        current = current_node
        #print (current.position)
        while current is not None: 
            path.append(current.position)
            current = current.parent

        # Return reversed path
        path = path[::-1]
        return path

    def search(self,game_state, cost, start, end):
        # Returns a list of tuples as a path from given start to given end 

        start_node = Node(None, tuple(start))
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None,tuple(end))
        end_node.g = end_node.h = end_node.f = 0



        yet_to_visit_list = []

        visited_list = set() 

        yet_to_visit_list.append(start_node)


        move = [[-1,0],
                [0,-1],
                [1,0],
                [0,1]]
        
        no_columns = game_state.size[0]
        no_rows = game_state.size[1]

        while len(yet_to_visit_list) > 0:

            current_node = yet_to_visit_list[0]
            current_index = 0 
            for index, item in enumerate(yet_to_visit_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index


            if self.actually_occupied(end):
                #print ("GIVING UP ON PATH/ NO POSSIBLE PATh")
                return self.return_path(current_node,game_state)
            
            yet_to_visit_list.pop(current_index)
            visited_list.add(current_node)

            if current_node == end_node:
                #print("THIS IS HAPPENING")
                return self.return_path(current_node,game_state)
            

            children = []
            

            for new_position in move:


                node_position  = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
                

                # Make sure within range (check if within maze boundary)
                if not game_state.is_in_bounds(node_position):
                    #print("move out of bounds")
                    continue

                # Make sure walkable terrain
                if (self.game_state.is_occupied(node_position)) and (not self.game_state.entity_at(node_position) == "a") and ( not self.game_state.entity_at(node_position) == "t"):
                    #print("blocked tile")
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)
            
            ## Print all children ## 
            #for c in children:
                #print(c.position)
            for child in children:

                if child in visited_list:
                    continue

                child.g = current_node.g + cost

                child.h = self.manhattan_distance(child.position,end_node.position)
                
                child.f = child.g + child.h 

                # Child is already in the yet_to_visit list and g cost is already lower
                if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                    continue

                # Add the child to the yet_to_visit list
                yet_to_visit_list.append(child)

        #print("no possible path")
        return []




##### A* Search Algorithm Implementation #####
# 1. Generate a list of all possible next moves
# 2. Store children in priority queue
# 3. Select closest child and repeat until goal reached or no more children (i.e. no possible safe tiles remain)

class Node:
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0
    
    def __eq__(self,other):
        return self.position == other.position
    
    def __hash__(self):               #<-- added a hash method
        return hash(self.position)
    
