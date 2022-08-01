import random, sys
clear = "\n" * 30

message1 = ""
message2 = ""
turn = "you"
enemybrain = {
    "foundship": "",
    "orientation": "",
    "originalx": "",
    "originaly": "",
    "lastx": "",
    "lasty": "",
    "firstmove": ""
}
possiblemoves = []
yourmoves = []
enemymoves = []

#converts letter to number
def l_n(letter):
    return ord(letter.upper()) - 64

#converts number to letter
def n_l(number):
    return chr(int(number) + 64)

#returns opposite direction
def opposite(direction):
    if direction == "left":
        return "right"
    if direction == "right":
        return "left"
    if direction == "up":
        return "down"
    if direction == "down":
        return "up"



#prints the current state of the board
def printboard():
    print("")
    print(""
          "[ENEMY'S BOARD]".center(33))
    print("    A  B  C  D  E  F  G  H  I  J ")
    for y in range(1, 10):
        print(f" {y} ", end="")
        for x in range(1, 11):
            print(f" {enemyboard[y][x]} ", end="")
        print("")
    print("10 ", end="")
    for x in range(1, 11):
        print(f" {enemyboard[10][x]} ", end="")
    print("")
    print("-------------------------------- ")
    print("[YOUR BOARD]".center(33))
    print("    A  B  C  D  E  F  G  H  I  J ")
    for y in range(1, 10):
        print(f" {y} ", end="")
        for x in range(1, 11):
            print(f" {yourboard[y][x]} ", end="")
        print("")
    print("10 ", end="")
    for x in range(1, 11):
        print(f" {yourboard[10][x]} ", end="")
    print(""
          )
    print("-------------------------------- ")
    print(message1.center(33))
    print(message2.center(33))
    print("-------------------------------- ")
    #print(enemyships) #debug
    #print(enemymoves) #debug
    #ddships) #debug
    #print(yourmoves) #debug
    #print(possiblemoves) #debug
    #print(enemybrain) #debug


#valid board positions
validx = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
validy = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

#set default board positions to all blank (.)
yourboard = []
enemyboard = []
for y in range(11):
    yourboard.append([])
    enemyboard.append([])
    for x in range(11):
        yourboard[y].append(".")
        enemyboard[y].append(".")

#randomize and generate enemy ship positions
shipsizes = {"carrier": 5, "battleship": 4, "cruiser": 3, "submarine": 2, "destroyer": 2}
enemyships = {}
for key in shipsizes:
    while True:
        tempship = []
        # random first position for ship
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        # random orientation (1 = horizontal, 2 = vertical)
        c = random.randint(1, 2)
        for n in range(shipsizes[key]):
            tempship.append(n_l(a) + str(b))
            if c == 1:
                b += 1
            else:
                a += 1
        if a < 11 and b < 11:
            if not any(pos in tempship for pos in [num for val in enemyships.values() for num in val]):
                enemyships.update({key: tempship})
                break
        tempship = []

#randomize and generate your ship positions
yourships = {}
for key in shipsizes:
    while True:
        tempship = []
        # random first position for ship
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        # random orientation (1 = horizontal, 2 = vertical)
        c = random.randint(1, 2)
        for n in range(shipsizes[key]):
            tempship.append(n_l(a) + str(b))
            if c == 1:
                b += 1
            else:
                a += 1
        if a < 11 and b < 11:
            if not any(pos in tempship for pos in [num for val in yourships.values() for num in val]):
                yourships.update({key: tempship})
                break
        tempship = []

#set your ship locations on the board with "O"
for key in yourships:
    for item in yourships[key]:
        yourmove = item
        x = int(l_n(yourmove[0]))
        if yourmove[1:3] == "10":
            y = 10
        else:
            y = int(yourmove[1])
        yourboard[y][x] = "O"

################################
###### [ MAIN GAME LOOP ] ######
################################

while True:

###########################
###### [ YOUR TURN ] ######
###########################

    while turn == "you":
        print(clear)
        printboard()
        message1 = ""
        message2 = ""
        message3 = ""

        #request input for next move
        yourmove = input("Attack? ").strip().upper()

        #check if target is valid
        while True:
            if yourmove == "quit":
                sys.exit()
            elif len(yourmove) == 2 or (len(yourmove) == 3 and yourmove[1:3] == "10"):
                if yourmove[0].isalpha() and yourmove[0] in validx:
                    if yourmove[1] in validy:
                        # set coordinates as x and y
                        x = int(l_n(yourmove[0]))
                        if yourmove[1:3] == "10":
                            y = 10
                        else:
                            y = int(yourmove[1])
                        if enemyboard[y][x] == ".":
                            break
            yourmove = input("Invalid position. Attack? ").strip().upper()

        #check if you hit an enemy ship
        if yourmove in [num for val in enemyships.values() for num in val]:
            message1 = "You strike " + yourmove + ". Hit!"
            enemyboard[y][x] = "X"
            yourmoves.append(yourmove)
            turn = "enemy"
            #remove spot from enemyships
            for key in enemyships:
                if yourmove in enemyships[key]:
                    enemyships[key].remove(yourmove)
                    #check if ship is sunk
                    if enemyships[key] == []:
                        message2 = "You sunk  their " + key + "!"
                        #check if no enemy ships remaining
                        if [num for val in enemyships.values() for num in val] == []:
                            print(clear)
                            printboard()
                            print("You Win!".center(33))
                            sys.exit()

        else:
            message1 = "You strike " + yourmove + ". Miss!"
            enemyboard[y][x] = "*"
            yourmoves.append(yourmove)
            turn = "enemy"

    ############################
    ###### [ ENEMY TURN ] ######
    ############################

    while turn == "enemy":
        print(clear)
        printboard()
        input("Press enter to continue".center(33))
        message1 = ""
        message2 = ""
        message3 = ""

        #generate enemy move
        while True:
            #if previous move was a hit
            if enemybrain["foundship"] == "yes":
                #check for possible second moves
                if enemybrain["firstmove"] == "yes":
                    if enemybrain["originaly"] > 1:
                        if yourboard[enemybrain["originaly"] - 1][enemybrain["originalx"]] in (".", "O"):
                            possiblemoves.append("up")
                    if enemybrain["originaly"] < 10:
                        if yourboard[enemybrain["originaly"] + 1][enemybrain["originalx"]] in (".", "O"):
                            possiblemoves.append("down")
                    if enemybrain["originalx"] > 1:
                        if yourboard[enemybrain["originaly"]][enemybrain["originalx"] - 1] in (".", "O"):
                            possiblemoves.append("left")
                    if enemybrain["originalx"] < 10:
                        if yourboard[enemybrain["originaly"]][enemybrain["originalx"] + 1] in (".", "O"):
                            possiblemoves.append("right")
                    enemybrain["firstmove"] = ""
                #check if next adjacent move will be out of bounds
                if (
                    (enemybrain["orientation"] == "up" and enemybrain["lasty"] == 1) or
                    (enemybrain["orientation"] == "down" and enemybrain["lasty"] == 10) or
                    (enemybrain["orientation"] == "left" and enemybrain["lastx"] == 1) or
                    (enemybrain["orientation"] == "right" and enemybrain["lastx"] == 110)
                ):
                    if opposite(enemybrain["orientation"]) in possiblemoves:
                        temporientation = opposite(enemybrain["orientation"])
                        possiblemoves.remove(enemybrain["orientation"])
                        enemybrain["orientation"] = temporientation
                        temporientation = ""
                    else:
                        enemybrain["orientation"] = random.choice(possiblemoves)
                    enemybrain["lastx"] = enemybrain["originalx"]
                    enemybrain["lasty"] = enemybrain["originaly"]


                #generate a move adjacent to previous move
                if enemybrain["orientation"] == "":
                    enemybrain["orientation"] = random.choice(possiblemoves)
                if enemybrain["orientation"] == "up":
                    enemymovex = enemybrain["lastx"]
                    enemymovey = enemybrain["lasty"] - 1
                if enemybrain["orientation"] == "down":
                    enemymovex = enemybrain["lastx"]
                    enemymovey = enemybrain["lasty"] + 1
                if enemybrain["orientation"] == "left":
                    enemymovex = enemybrain["lastx"] - 1
                    enemymovey = enemybrain["lasty"]
                if enemybrain["orientation"] == "right":
                    enemymovex = enemybrain["lastx"] + 1
                    enemymovey = enemybrain["lasty"]
                enemymove = n_l(enemymovex) + str(enemymovey)
                break
            #otherwise randomly generate next move
            else:
                enemymovex = random.randint(1, 10)
                enemymovey = random.randint(1, 10)
                enemymove = n_l(enemymovex) + str(enemymovey)
                #check if move is valid
                if yourboard[enemymovey][enemymovex] in (".", "O"):
                    break

        #check if enemy hit your ship
        if enemymove in [num for val in yourships.values() for num in val]:
            message1 = "Enemy strikes " + enemymove + ". Hit!"
            yourboard[enemymovey][enemymovex] = "X"
            enemybrain["foundship"] = "yes"
            if enemybrain["originalx"] == "":
                enemybrain["originalx"] = enemymovex
                enemybrain["originaly"] = enemymovey
                enemybrain["firstmove"] = "yes"
            enemybrain["lastx"] = enemymovex
            enemybrain["lasty"] = enemymovey
            enemymoves.append(enemymove)
            turn = "you"
            #remove spot from yourships
            for key in yourships:
                if enemymove in yourships[key]:
                    yourships[key].remove(enemymove)
                    #check if ship is sunk
                    if yourships[key] == []:
                        message2 = "They sunk your " + key + "!"
                        enemybrain = {
                            "foundship": "",
                            "orientation": "",
                            "originalx": "",
                            "originaly": "",
                            "lastx": "",
                            "lasty": "",
                            "firstmove": ""
                        }
                        possiblemoves = []
                        #check if no ships remaining
                        if [num for val in yourships.values() for num in val] == []:
                            print(clear)
                            printboard()
                            print("They Win!".center(33))
                            sys.exit()

        else:
            message1 = "Enemy strikes " + enemymove + ". Miss!"
            yourboard[enemymovey][enemymovex] = "*"
            #choose oreintation for next move
            if enemybrain["foundship"] == "yes":
                if opposite(enemybrain["orientation"]) in possiblemoves:
                    temporientation = opposite(enemybrain["orientation"])
                    possiblemoves.remove(enemybrain["orientation"])
                    enemybrain["orientation"] = temporientation
                    temporientation = ""
                else:
                    possiblemoves.remove(enemybrain["orientation"])
                    enemybrain["orientation"] = random.choice(possiblemoves)
                enemybrain["lastx"] = enemybrain["originalx"]
                enemybrain["lasty"] = enemybrain["originaly"]
                # enemybrain["lastx"] = enemymovex
                # enemybrain["lasty"] = enemymovey
            lastx = ""
            lasty = ""
            enemymoves.append(enemymove)
            turn = "you"
