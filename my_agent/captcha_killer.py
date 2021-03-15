"""
    CoderOne Dungeons and Data Structures AI Sports Challenge
    Agent created by Nikhil Kalele and Aditya Sharma 
    Agent: Captcha_Killer
"""

import random

# import time
import numpy as np



class agent:
    def __init__(self):
        """
        Place any initialisation code for your agent here (if any)
        """
        global bombdict
        bombdict = {}

        self.planned_actions =  []
        global safegoal
        self.safegoal = None
        global tick_number
        self.tick_number = 0

        pass

    def next_move(self, game_state, player_state):
        """
        This method is called each time your Agent is required to choose an action
        If you're just starting out or are new to Python, you can place all your
        code within the ### CODE HERE ### tags. If you're more familiar with Python
        and how classes and modules work, then go nuts.
        (Although we recommend that you use the Scrims to check your Agent is working)
        """
        if (game_state.tick_number > self.tick_number):
            self.tick_number += 1
        
            # a list of all the actions your Agent can choose from
            actions = ["", "u", "d", "l", "r", "p"]
            movement = ["", "u", "d", "l", "r"]
            

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
            tg = ()
            ag = ()
            safetyflag = False

            

            explodingbombs = []
            explodingbombs.clear()

            gamemap = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8), (4, 9), (5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8), (5, 9), (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (8, 8), (8, 9), (9, 0), (9, 1), (9, 2), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (10, 0), (10, 1), (10, 2), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (11, 0), (11, 1), (11, 2), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (11, 9)]

            
            for bomb in game_state.bombs:
                if bomb not in bombdict:
                    bombdict[bomb] = game_state.tick_number

            if bombdict:
                for key in bombdict:
                    if game_state.tick_number - bombdict[key] >= 20:
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
            
            
            if ammo_drop:
                while(ammo_drop):
                    ammogoal = self.find_nearest_ammo(ammo_drop,self.location)
                    aa = self.path_to_bomb(ammo_drop, ammogoal)
                    if aa:
                        # print("AMMO GOAL IS ", ammogoal)
                        self.planned_actions.clear()
                        self.planned_actions = aa
                        # print("PATH TO AMMO IS ", aa)
                        # print("MY LOCATION IS ", self.location)
                        break
                    else:
                        ammo_drop.remove(ammogoal)
                        ammogoal = self.find_nearest_ammo(ammo_drop,self.location)
                if (not ammo_drop and treasure):
                    while(treasure):
                        tresgoal = self.find_nearest_ammo(treasure,self.location)
                        ta = self.path_to_bomb(treasure, tresgoal)
                        if ta:
                            self.planned_actions.clear()
                            self.planned_actions = ta
                            break
                        else:
                            treasure.remove(tresgoal)
                            tresgoal = self.find_nearest_ammo(treasure,self.location)
                if (not ammo_drop and not treasure):
                    if ammo > 1:
                        while(ammo > 1):
                            if self.planned_actions:
                                return self.planned_actions.pop(0)
                            sa = []
                            safegoal = ()

                            temp = self.shouldiplacebomb(self.location, gamemap, explodingbombs)
                    
                            if temp[0]:
                                sa = temp[1]
                                safegoal = temp[2]
                                # print("SAFEGOAL 0 IS ", temp[0], " 1 IS ", temp[1], " 2 IS ", temp[2])
                            if sa and self.destroycheck():

                                # print("DESTROYCHECK IS ", self.destroycheck(), "LCOATION IS ", self.location)

                                self.planned_actions.clear()
                                self.planned_actions = sa
                                return "p"
                                break
                            else:
                                break

            elif(treasure):
                while(treasure):
                    tresgoal = self.find_nearest_ammo(treasure,self.location)
                    ta = self.path_to_bomb(treasure, tresgoal)
                    if ta:
                        self.planned_actions.clear()
                        self.planned_actions = ta
                        break
                    else:
                        treasure.remove(tresgoal)
                        tresgoal = self.find_nearest_ammo(treasure,self.location)
            
            elif ammo > 1:
                while(ammo > 1):
                    if self.planned_actions:
                        return self.planned_actions.pop(0)
                    sa = []
                    safegoal = ()

                    temp = self.shouldiplacebomb(self.location, gamemap, explodingbombs)
                    
                    if temp[0]:
                        sa = temp[1]
                        safegoal = temp[2]
                        # print("SAFEGOAL 0 IS ", temp[0], " 1 IS ", temp[1], " 2 IS ", temp[2])
                    if sa and self.destroycheck():
                        # print("REACHING SA!")

                        self.planned_actions.clear()
                        self.planned_actions = sa
                        return "p"
                        break
                    else:
                        break

            if self.planned_actions:
                
                move = self.converter(self.planned_actions[0], self.location)
                x = self.planned_actions.pop(0)

                # if safetyflag:
                #     if move == self.safegoal:
                #         self.safegoal = None
                #         safetyflag = False
                #         self.planned_actions.clear()
                #         return x
                #     return x
                    
                if self.is_safe(move, explodingbombs) and self.planned_actions:
                    # print("ISSA SAFE MOVE BUT BOMBS EXPLODING LIKE ", explodingbombs)
                    
                    
                    
                    # print("next move is planned! : ", move)
                    
                    if move == tg:
                            # print("REACHED TRES GOAL")
                        tg == None
                        # print("CLEARING TRES GOAL")
                        self.planned_actions.clear()

                    if move == ag:
                            # print("REACHED GOAL")
                        ag == None
                        # print("CLEARING AMMO GOAL")
                        self.planned_actions.clear()
                    return x
                else:
                    return x
            
            


            random.shuffle(empty_tiles)

            for tile in empty_tiles:
                # print("REACHING HERE BOMB LIST IS ", len(explodingbombs))
                # print("REACHING HERE TILE LIST IS ", len(empty_tiles))
                # print("AM I SAFE ON ANY SURROUNDING TILES?: ", self.is_safe(tile, explodingbombs))
                # print("MY LCOATIO NIS: ", self.location)
                # for bomb in explodingbombs:
                    # print("THE BOMB ABOUT TO EXPLODE IS ", bomb)
                if self.is_safe(tile, explodingbombs):
                    
                    return self.move_to_tile(self.location, tile)
                else:
                    pass
                    # temp = self.bomb_placeable(empty_diagonals, empty_tiles, explodingbombs)
                    # if temp[0]:
                    #     planned_actions.append(temp[1])
                    #     return temp[2]

            return action
    def path_to_bomb(self, ammo_drop, closest_bomb):
        cost = 1
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

    def destroycheck(self):
        if self.game_state.entity_at((self.location[0]+1, self.location[1])) == "sb" or self.game_state.entity_at((self.location[0]+1, self.location[1])) == "ob":
            return True
        if self.game_state.entity_at((self.location[0]-1, self.location[1])) == "sb" or self.game_state.entity_at((self.location[0]-1, self.location[1])) =="ob":
            return True
        if self.game_state.entity_at((self.location[0], self.location[1]+1)) == "sb" or self.game_state.entity_at((self.location[0], self.location[1]+1)) =="ob":
            return True
        if self.game_state.entity_at((self.location[0], self.location[1]-1)) == "sb" or self.game_state.entity_at((self.location[0], self.location[1]-1))=="ob":
            return True
        return False

    def converter (self, actionplan, location):
        move = ""
        if actionplan == "u":
            move = (location[0], location[1]+1)
        elif actionplan == "d":
            move = (location[0], location[1]-1)
        elif actionplan == "l":
            move = (location[0]-1, location[1])
        elif actionplan == "r":
            move = (location[0]+1, location[1])
        return move

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
        
       
    def find_nearest_ammo(self, ammo_drop, location):
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

        return out
    
    def shouldiplacebomb(self, bombtile, gamemap, explodingbombslol):

        temp = explodingbombslol.copy()

        temp.append(bombtile)
        
        aoeout = self.dooby(temp)


        
        safemap = list(set(gamemap) - set(aoeout) - set(self.game_state.all_blocks))
        temp = self.find_nearest_ammo(safemap, self.location)
        path = (self.path_to_bomb(safemap, temp))
        if path:
            # print(" THE CLOSEST SAFE SPOT IS ", temp)
            # print("PATH IS ", path)
            return [True, path, temp]
        return [False, None, None]

    def dooby(self, explodingbombslmao):
        aoe = []
        for bomb in explodingbombslmao:
            aoecalc = self.bombradius(bomb)
            for xco in range(aoecalc[2], aoecalc[0]+1, 1):
                aoe.append((bomb[0]+xco,bomb[1]))

            for yco in range(aoecalc[3], aoecalc[1]+1, 1):
                aoe.append((bomb[0],bomb[1]+yco))
        return aoe

        



    # returns somethign like [x y -x -y]
    # bomb explodes in [1, 2, 1, 1]
    def bombradius(self, bombtile):
        out = [0, 0, 0, 0]
        if self.actually_occupied((bombtile[0]+2,bombtile[1])):
            out[0] = 1
        else:
            out[0] = 2
        if self.actually_occupied((bombtile[0]-2,bombtile[1])):
            out[2] = -1
        else:
            out[2] = -2
        if self.actually_occupied((bombtile[0],bombtile[1]+2)):
            out[1] = 1
        else:
            out[1] = 2
        if self.actually_occupied((bombtile[0],bombtile[1]-2)):
            out[3] = -1
        else:
            out[3] = -2
        if self.actually_occupied((bombtile[0]+1,bombtile[1])):
            out[0] = 0
        if self.actually_occupied((bombtile[0]-1,bombtile[1])):
            out[2] = 0
        if self.actually_occupied((bombtile[0],bombtile[1]+1)):
            out[1] = 0
        if self.actually_occupied((bombtile[0],bombtile[1]-1)):
            out[3] = 0
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
    
