import sys
from collections import Counter
from string import ascii_uppercase #alphabet
output = open("Battleship.out","w+")
not_reachable_files = []

def printer(str):
    """
    tab size 4
    """
    output.write(str)
    print(str, end= "")


try:
    try:
        player1_table = open(sys.argv[1],"r")
    except IOError:
        not_reachable_files.append(sys.argv[1])
        pass
    try:
        player2_table = open(sys.argv[2], "r")
    except IOError:
        not_reachable_files.append(sys.argv[2])
        pass
    try:
        player1_moves = open(sys.argv[3],"r")
    except IOError:
        not_reachable_files.append(sys.argv[3])
        pass
    try:
        player2_moves = open(sys.argv[4], "r")
    except IOError:
        not_reachable_files.append(sys.argv[4])
        pass
except IndexError:
    printer("The count of arguments must be 4")
    quit()
except Exception:
    printer("kaBOOM: run for your life!")
    quit()
finally:
    if not_reachable_files == []:
        pass
    else:
        file_names = " ".join(not_reachable_files)
        printer("IOError: {} file(s) is/are not reachable.".format(file_names))
        quit()



grids = {1 :[["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"]],
        
        2:[["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"],
          ["-","-","-","-","-","-","-","-","-","-"]]}

ships = {1 : [], 2 : []}    #indexes of ships: ships --> player ---> [[number index][letter index]] dict-->list

coordinates = {"C": {1:[],2:[]},
                "B": {1:[],2:[]},
                "D": {1:[],2:[]},
                "S": {1:[],2:[]},   #S and P coordinates removing from coordinates and carried to patrol_boat_combined and battleship_combined
                "P": {1:[],2:[]}}   #coordinates of ships: coordinates ---> ship type ---> player ---> [[letter][number]]   dict --> dict --> list
patrol_boat_combined = {1:{},2:{}}  #for example patrol_boat_combined[player]{[A,1]:1 ,[A,2]:1 ,[B,3]:2 ,[C,3]:2} 
battleship_combined = {1:{},2:{}}   #dict --> dict

"""
current values of ships."-" turns to "X" when ship is sunk.
"""
carrier = {1:["-"],2:["-"]}
battleship = {1:["-","-","-","-"],2:["-","-","-","-"]}
destroyer = {1:["-"],2:["-"]}
submarine = {1:["-"],2:["-"]}
patrol_boat = {1:["-","-","-","-"],2:["-","-","-","-"]}

# adds ships to ships dictionary
lines1 = player1_table.readlines()
lines2 = player2_table.readlines()
for line in lines1:
    line = line.replace("\n","")
    line = line.split(";")
    ships[1].append(line)

for line in lines2:
    line = line.replace("\n","")
    line = line.split(";")
    ships[2].append(line)
del(line,lines1,lines2)

"""
Functions
"""
def define_coordinates_of_ships(player):
    
    row_counter = 1
    
    for row in ships[player]:
        square_count = 0    
        for square in row: 
            if square != "":
                try:
                    if square == "C" or square == "D" or square == "S" or square =="P" or square == "B":
                        coordinates[square][player].append([(ascii_uppercase[square_count]),(row_counter)])
                        square_count += 1
                    else:
                        raise KeyError
                except KeyError:
                    printer("You entered invalid ship type")
                    quit()
            else:
                square_count += 1
                pass
        row_counter += 1  
    try:
        check(player)
        grouper(player)
        pass
    except Exception:
        printer("kaBOOM: run for your life!")
        quit()         

"""
neighbour_x is boolean variable(True when neighbour exists.)
return neighbour right and neighbour down
"""
def neighbour_finder(ship_type,player): 
    
    letter_index = ascii_uppercase.index(coordinates[ship_type][player][0][0])
    number = coordinates[ship_type][player][0][1]
    
    neighbour_right = False
    neighbour_down = False
    if [ascii_uppercase[letter_index + 1],number] in coordinates[ship_type][player]:    #right neighbour
        neighbour_right = True
    if [ascii_uppercase[letter_index],number + 1] in coordinates[ship_type][player]:    #down neighbour
        neighbour_down = True
    return neighbour_right, neighbour_down
    

"""
For Patrol boats and battleships
"""
def grouper(player):
    boat_counter = 1    #value of coordinates/for example = [A,1]:1 
    while coordinates["P"][player] != []:   #for patrol boats
            
        letter_index = ascii_uppercase.index(coordinates["P"][player][0][0])
        number = coordinates["P"][player][0][1]
        return_of_neighbour_finder = neighbour_finder("P",player)
        """
        Adding boats combined
        """
        if return_of_neighbour_finder == (True,False):  #when there is only neighbour in right
            patrol_boat_combined[player][ascii_uppercase[letter_index],number] = boat_counter 
            patrol_boat_combined[player][ascii_uppercase[letter_index + 1],number] = boat_counter
            #-->[A,1]:1, [B,1]:1
            
            coordinates["P"][player].pop(0)
            coordinates["P"][player].remove([ascii_uppercase[letter_index + 1],number])
            boat_counter += 1
            #removes the coordinates from coordinates dictionary

        elif return_of_neighbour_finder == (False,True):    #when there is only neighbour at bottom
            patrol_boat_combined[player][ascii_uppercase[letter_index],number] = boat_counter
            patrol_boat_combined[player][ascii_uppercase[letter_index],number + 1] = boat_counter
            #-->[A,1]:1, [A,2]:1
            
            coordinates["P"][player].pop(0)
            coordinates["P"][player].remove([ascii_uppercase[letter_index],number + 1 ])
            boat_counter += 1
            # removes the coordinates from coordinates dictionary
        
        elif return_of_neighbour_finder == (True,True):     #when there is neighbour both right and bottom
            """
            It groups with the right one.Otherwise it gives error in some positions
            """
            patrol_boat_combined[player][ascii_uppercase[letter_index],number] = boat_counter
            patrol_boat_combined[player][ascii_uppercase[letter_index + 1],number] = boat_counter
            # -->[A,1]:1,[B,1]:1

            coordinates["P"][player].pop(0)
            coordinates["P"][player].remove([ascii_uppercase[letter_index + 1],number])
            boat_counter += 1
        
        elif return_of_neighbour_finder == (False,False):   #no neighbour of P which is error
            raise(Exception)    
        else:
            pass
    
        

    boat_counter = 1
    
    
    while len(coordinates["B"][player]) != 0:   #for battleship
        try:    
                letter_index = ascii_uppercase.index(coordinates["B"][player][0][0])
                number = coordinates["B"][player][0][1]
                return_of_neighbour_finder = neighbour_finder("B",player)
                if return_of_neighbour_finder == (True,False): #neighbours at right
                    battleship_combined[player][ascii_uppercase[letter_index],number] = boat_counter
                    battleship_combined[player][ascii_uppercase[letter_index + 1],number] = boat_counter
                    battleship_combined[player][ascii_uppercase[letter_index + 2],number] = boat_counter
                    battleship_combined[player][ascii_uppercase[letter_index + 3],number] = boat_counter
                    #[A,1]:1,[B,1]:1,[C,1]:1,[D,1]:1 

                    coordinates["B"][player].pop(0)
                    coordinates["B"][player].remove([ascii_uppercase[letter_index + 1],number])
                    coordinates["B"][player].remove([ascii_uppercase[letter_index + 2],number])
                    coordinates["B"][player].remove([ascii_uppercase[letter_index + 3],number])
                    #removes the coordinates from coordinates dictionary

                    boat_counter += 1
                
                elif return_of_neighbour_finder == (False,True):   #neighbours at down
                    battleship_combined[player][ascii_uppercase[letter_index],number] = boat_counter
                    battleship_combined[player][ascii_uppercase[letter_index],number + 1] = boat_counter
                    battleship_combined[player][ascii_uppercase[letter_index],number + 2] = boat_counter
                    battleship_combined[player][ascii_uppercase[letter_index],number + 3] = boat_counter
                    #[A,1]:1,[A,2]:1,[A,3]:1,[A,4]:1

                    coordinates["B"][player].pop(0)
                    coordinates["B"][player].remove([ascii_uppercase[letter_index],number + 1])
                    coordinates["B"][player].remove([ascii_uppercase[letter_index],number + 2])
                    coordinates["B"][player].remove([ascii_uppercase[letter_index],number + 3])
                    
                    boat_counter += 1
                
                elif return_of_neighbour_finder == (True,True):     #neighbour at bottom and right
                    if [ascii_uppercase[letter_index + 2],number] in coordinates["B"][player]:     
                        battleship_combined[player][ascii_uppercase[letter_index],number] = boat_counter
                        battleship_combined[player][ascii_uppercase[letter_index + 1],number] = boat_counter
                        battleship_combined[player][ascii_uppercase[letter_index + 2],number] = boat_counter
                        battleship_combined[player][ascii_uppercase[letter_index + 3],number] = boat_counter

                        coordinates["B"][player].pop(0)
                        coordinates["B"][player].remove([ascii_uppercase[letter_index + 1],number])
                        coordinates["B"][player].remove([ascii_uppercase[letter_index + 2],number])
                        coordinates["B"][player].remove([ascii_uppercase[letter_index + 3],number])
                    
                    elif [ascii_uppercase[letter_index],number + 2] in coordinates["B"][player]:
                        battleship_combined[player][ascii_uppercase[letter_index],number] = boat_counter
                        battleship_combined[player][ascii_uppercase[letter_index],number + 1] = boat_counter
                        battleship_combined[player][ascii_uppercase[letter_index],number + 2] = boat_counter
                        battleship_combined[player][ascii_uppercase[letter_index],number + 3] = boat_counter


                        coordinates["B"][player].pop(0)
                        coordinates["B"][player].remove([ascii_uppercase[letter_index],number + 1])
                        coordinates["B"][player].remove([ascii_uppercase[letter_index],number + 2])
                        coordinates["B"][player].remove([ascii_uppercase[letter_index],number + 3])
                else:
                    raise(Exception)
        except:
            pass


"""
For wrong ship implacements
"""
def check(player):
    if len(coordinates["C"][player]) == 5:  #length of carrier
        for check in range (4):    
            """
            Check if Carriers are attached
            """
            if coordinates["C"][player][check][0] == coordinates["C"][player][check + 1][0]:
                return None
            elif coordinates["C"][player][check][1] == coordinates["C"][player][check + 1][1]:
                return None
            else:
                raise Exception
                
    else:
        raise Exception

    if len(coordinates["D"][player]) == 3:  #length of Destroyer
        for check in range (2):
            """
            Check if Destroyers are attached
            """
            if coordinates["D"][player][check][0] == coordinates["D"][player][check + 1][0]:
                return None
            elif coordinates["D"][player][check][1] == coordinates["D"][player][check + 1][1]:
                return None
            else:
                raise Exception
    else:
        raise Exception
    
    if len(coordinates["S"][player]) == 3:  #length of Submarine
        for check in range (2):
            """
            Check if submarines are attached
            """
            if coordinates["S"][player][check][0] == coordinates["S"][player][check + 1][0]:
                pass
            elif coordinates["S"][player][check][1] == coordinates["S"][player][check + 1][1]:
                pass
            else:
                raise Exception
    else:
        raise Exception
    
    if len(coordinates["P"][player]) == 8:
        return None
    elif len(coordinates["P"][player]) != 8:
        raise Exception
    
    if len(coordinates)["B"][player] == 8:
        return None
    else:
        raise Exception

"""
player --> 1 , 2 or "tie"
game --> "ongoing" or "over"
"""
def game_table(player,game):
        
    if game == "ongoing":
        printer("""
Player{}'s Move\n
Round : {}\t\t\t\t\tGrid size: 10x10\n\n""".format(player,round + 1))
    if game == "over":
        if player == 1:
            printer("Player1 Wins!\n\n")
        if player == 2:
            printer("Player2 Wins!\n\n")
        if player == "tie":
            printer("It's a tie\n\n")
        printer("Final information\n\n")

    if game == "ongoing":
        printer("Player1's Hidden Board\t\tPlayer2's Hidden Board\n  A B C D E F G H I J\t\t  A B C D E F G H I J")
    elif game == "over":
        printer("Player1's Board\t\t\t\tPlayer2's Board\n  A B C D E F G H I J\t\t  A B C D E F G H I J")


    
    
    #This for loops prints rows both player1 and player2
    for column in range(10):
        printer("\n"  + "%-2s" %(str(column + 1)))
        row_index = 0
        p1_column = ""
        for row in grids[1][column]:
            if game == "over":
                if row == "-" and ships[1][column][row_index] != '':
                    p1_column += ("%-2s"%str(ships[1][column][row_index]))
                    row_index += 1
                else:
                    p1_column += ("%-2s"%row)
                    row_index += 1
            else:
                p1_column += ("%-2s"%row)
                row_index += 1
        p1_column = p1_column[:-1]
        printer(p1_column)    
        

        printer("\t\t%-2s" %(str(column + 1)))
        row_index = 0
        p2_column = ""
        for row in grids[2][column]:
            if game == "over":
                if row == "-" and ships[2][column][row_index] != '':
                    p2_column += ("%-2s"%str(ships[2][column][row_index]))
                    row_index += 1
                else:
                    p2_column += ("%-2s"%row)
                    row_index += 1
            else:
                p2_column += ("%-2s"%row)
                row_index += 1  
        p2_column = p2_column[:-1]
        printer(p2_column)
    
    """
    In below part print and write functions tabs doesn't match.So print and write written differently
    """
    printer("\n\nCarrier\t\t%s\t\t\t\tCarrier\t\t%s"     %(str(carrier[1][0]),str(carrier[2][0])))
    printer("\nBattleship\t%s %s\t\t\t\tBattleship\t%s %s"     %(battleship[1][0],battleship[1][1],battleship[2][0],battleship[2][1]))
    printer("\nDestroyer\t%s\t\t\t\tDestroyer\t%s"     %(str(destroyer[1][0]),str(destroyer[2][0])))
    printer("\nSubmarine\t%s\t\t\t\tSubmarine\t%s"     %(str(submarine[1][0]),str(submarine[2][0])))
    printer("\nPatrol Boat\t%s %s %s %s\t\t\tPatrol Boat\t%s %s %s %s\n\n"     %(str(patrol_boat[1][0]),str(patrol_boat[1][1]),str(patrol_boat[1][2]),str(patrol_boat[1][3]),str(patrol_boat[2][0]),str(patrol_boat[2][1]),str(patrol_boat[2][2]),str(patrol_boat[2][3])))
    if game == "ongoing":
        printer("Enter Your move: %s,%s\n\n"%(moves[player][round][0],moves[player][round][1]))
    return None, None

"""
where the - turns O or X in game screen
player variable must be the one who gets bombed
ValueError happens here
"""
def change_grids(number,lttr,player):
    
            lttr_index = int(ascii_uppercase.index(lttr))   
            number = int(number)
            assert not( (lttr_index > 9) or (number > 10) or (number < 0)) #AssertionError: Index out of range
                
            if grids[player][number - 1][lttr_index] == "-":  
                if ships[player][number - 1][lttr_index] != "":
                    grids[player][number - 1][lttr_index] = "X"
                    ship_type = ships[player][number - 1][lttr_index]
                    remove_coordinate(number,lttr,ship_type,player)
                else:
                    grids[player][number - 1][lttr_index] = "O"
            else:
                raise AssertionError    #AssertionError: Bombing 2 squares twice
           
            
"""
If bomb hits a ship, ship's coordinates will be removed
Also checks the current situation ships
"""
def remove_coordinate(number,lttr,ship_type,player):
    
    if ship_type == "C" or ship_type == "D" or ship_type == "S":
        coordinates[ship_type][player].remove([lttr,number])
        if len(coordinates["C"][player]) == 0:  # if carrier ship is sunked
            carrier[player][0] = "X"
            
        if len(coordinates["D"][player]) == 0:  # if destroyer ship is sunked
            destroyer[player][0] = "X"
        
        if len(coordinates["S"][player]) == 0:  # if submarine ship is sunked
            submarine[player][0] = "X"
    if ship_type == "P":
        del patrol_boat_combined[player][lttr,number]
        
        patrol_boat_count = len(Counter(patrol_boat_combined[player].values()))
        
        if patrol_boat_count == 3:
            patrol_boat[player] = ["X","-","-","-"]
        elif patrol_boat_count == 2:
            patrol_boat[player] = ["X","X","-","-"]
        elif patrol_boat_count == 1:
            patrol_boat[player] = ["X","X","X","-"]
        elif patrol_boat_count == 0:
            patrol_boat[player] = ["X","X","X","X"]
    
    if ship_type == "B":
        del battleship_combined[player][lttr,number]
        
        battleship_count = len(Counter(battleship_combined[player].values()))
        
        if battleship_count == 1:
            battleship[player] = ["X","-"]
        if battleship_count == 0:
            battleship[player] = ["X","X"]
    pass

"""
remove the wrong input in player.in
"""
def remove_the_problem(player,round):
    moves[player].pop(round)
    moves[player][round] = moves[player][round].split(",")


define_coordinates_of_ships(1) 
define_coordinates_of_ships(2)


p1_moves = player1_moves.read()
p2_moves = player2_moves.read()

p1_moves = p1_moves.replace("\n","")
p2_moves = p2_moves.replace("\n","")

p1_moves = p1_moves.split(";")
p2_moves = p2_moves.split(";")
moves = {1:p1_moves, 2:p2_moves}
del(player1_moves,player2_moves)

printer("Battle of Ships Game\n")    
for round in range(len(p1_moves)):   
    # if chains checks if the game is over
    if patrol_boat_combined == {1:{},2:{}} and battleship_combined == {1:{},2:{}} and coordinates["C"] == {1:[],2:[]} and coordinates["D"] == {1:[],2:[]} and coordinates["S"] == {1:[],2:[]}:
        game_table("tie","over")
        break
    elif patrol_boat_combined[1] == {} and battleship_combined[1] == {} and coordinates["C"][1] == [] and coordinates["D"][1] == [] and coordinates["S"][1] == []:
        game_table(2,"over")
        break
    elif patrol_boat_combined[2] == {} and battleship_combined[2] == {} and coordinates["C"][2] == [] and coordinates["D"][2] == [] and coordinates["S"][2] == []:          
        game_table(1,"over")
        break
    else:
        pass


    #Game Starting Here!!!!
    try:
        # player1's turn
        moves[1][round] = p1_moves[round].split(",")
        while True:    
            try:    
                game_table(1,"ongoing")
                if len(moves[1][round]) != 2 or '' in moves[1][round]:    #IndexError
                    raise IndexError
        
                change_grids(moves[1][round][0],moves[1][round][1],2)
                break
            
            except ValueError:
                remove_the_problem(1,round)
                printer("ValueError: Invalid Input.\n")
                continue    
            
            except IndexError:
                remove_the_problem(1,round)    
                printer("IndexError: Your input includes wrong number of arguments.\n")
                continue
    
        
        # player2's turn
        moves[2][round] = p2_moves[round].split(",")
        while True:    
            try:    
                game_table(2,"ongoing")
                if len(moves[2][round]) != 2 or '' in moves[2][round]:    #IndexError
                    raise IndexError
        
                change_grids(moves[2][round][0],moves[2][round][1],1)
                break
            
            except ValueError:
                remove_the_problem(2,round)
                printer("ValueError: Invalid Input.\n")
                continue
            
            except IndexError:
                remove_the_problem(2,round)    
                printer("IndexError: Your input includes wrong number of arguments.\n")
                continue
    
    #other unexpected errors
    except IndexError:
        printer("IndexError: Your input includes wrong number of arguments.\n")
        quit()
    except ValueError:
        printer("ValueError: Invalid Input.\n")
        quit()
    except AssertionError:
        printer("AssertionError: Invalid Operation.\n")
        quit()
    except Exception:
        printer("kaBOOM: run for your life!")
        quit()


