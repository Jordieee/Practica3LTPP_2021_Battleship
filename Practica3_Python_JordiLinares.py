import random
import copy

#Global vars
MAP_LETRAS = { 'A':0, 'B':1, 'C':2, 'D':3, 'E':4,'F':5, 'G':6, 'H':7, 'I':8, 'J':9 }
LETRAS_MAP = { 0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J' }
AIIntelligence = False
shotsDone = []
pdt = []
for i in range(10) :
    for j in range(10) :
        pdt.append((i,j))
letters = ['A','H','T']

#Initializing all the necessary boards needed
Ships = [] #List of ships where a ship is a list of its positions
AIBoard = [['~' for i in range(10)] for j in range(10)]
AIBoardCopy = [['~' for i in range(10)] for j in range(10)]


#Functions



def printBoard(board):

    """ Prints the board """
    
    number = 1
    print()
    print("   A B C D E F G H I J")
    for i in range(len(board)):
        if (number==10):
            print(str(number)+":",end='')
        else:
            print(" "+str(number)+":",end='')

        for j in range(len(board)):
            print(board[i][j], end=' ')
        print()
        number+=1



def check(board,pos,n,i,j):
    
    """ Check if it is possible to place a ship
    Boolean function which returns for
    each position in board True if it's
    possible to place a ship or False
    if it's not """
    
    placeable = True

    #We check here first if the coordinates given are in the borders
    initI = i-1
    initJ = j-1
    

    if(initI<0):
        initI = 0
    if(initJ<0):
        initJ = 0
    
    #Now we divide the output depending if the random pos is for horizontal(0)/vertical(1) 
    #Horizontal
  
    if(pos==0):
        finI = initI+2
        finJ = initJ+n+1

        #Checking again if we are in the borders
        if(finI>9):
            finI = 9
        if(finJ>9):
            finJ = 9
            
        for x in range(initI,finI+1):
            for y in range(initJ,finJ+1):
                if(board[x][y]==0):
                    return not placeable
             
            
    #Vertical
    
    else:
        finI = initI+n+1
        finJ = initJ+2

        #Checking again if we are in the borders
        if(finI>9):
            finI = 9
        if(finJ>9):
            finJ = 9
        for x in range(initI,finI+1):
            for y in range(initJ,finJ+1):
                if(board[x][y]==0):
                    return not placeable
        
            
    return placeable
    
    
    


def setShips(board,ships,n):
    
    """Set ship in the board: Main function of our program,
    it will set a ship and will call the previous function
    to check if it is placeable """
    
    pos = random.randint(0, 1);
    ship = []
    
    if(pos==0): #horizontal
        i = random.randint(0, 9) 
        j = random.randint(0, 10 - n) 
        while(not check(board,pos,n,i,j)):
            i = random.randint(0, 9) 
            j = random.randint(0, 10 - n)
        for x in range(0,n):
            board[i][j] = 0
            ship.append((i,j))
            j+=1

    else: #vertical
        i = random.randint(0, 10 - n) 
        j = random.randint(0, 9) 
        while(not check(board,pos,n,i,j)):
            i = random.randint(0, 10 - n) 
            j = random.randint(0, 9)
        for x in range(0,n):
            board[i][j] = 0
            ship.append((i,j))
            i+=1
    ships.append(ship)
    return board



def setAllShips(board,ships):

    """ Calling now setShips several times to set every required ship"""
    
    setShips(board,ships,4)
    setShips(board,ships,3)
    setShips(board,ships,3)
    setShips(board,ships,2)
    setShips(board,ships,2)
    setShips(board,ships,2)
    setShips(board,ships,1)
    setShips(board,ships,1)
    setShips(board,ships,1)
    setShips(board,ships,1)



def coordToPos(coord):

    """Coordinate(B1) to position(0,1)
    Passing a coordinate to a position(tuple)"""
    
    return int(coord[1:])-1, MAP_LETRAS[coord[0]] 


def posToCoord(pos):

    """Position(0,1) to coordinate(B2)
    Passing a position(tuple) to a coordinate"""
    
    coord0=str(LETRAS_MAP[pos[1]])
    coord1=str(int(pos[0])+1)
    
    return coord0+coord1

def shotBoard(ships,i,j):
    
    """Removing the position of the ship list"""
    
    for ship in ships:
        for pos in ship:
            if pos==(i,j):
                ship.remove((i,j))
                if len(ship)==0: #Sunk
                    return True
    
    return False
    

def checkMyShot(coord, AIBoard, ships):
    
    """Check my shot
    Checking the output of my shot"""
    
    if(AIBoard[coord[0]][coord[1]]!=0):
        print("Agua, que malo eres jajaja")
        
    else:
        if(shotBoard(ships,coord[0],coord[1])):
            print("Hundido :( ... me vengaré")
            AIBoard[coord[0]][coord[1]]='x'

        else:
            print("Tocado, eres bueno eh")
            AIBoard[coord[0]][coord[1]]='x'

def randomShot():
    
    """AI random shot
    Random AI shot from all the possible shots in pdt"""
    
    n = len(pdt)
    p = random.randint(0, n - 1)
    coord = posToCoord(pdt[p])
    shotsDone.append(pdt[p])
    i,j = pdt.pop(p) 
    return coord

def AIShot():

    """AI Intelligent Shot
    AI Intelligent Shot, it is not always activated,
   which means there's a certain "randomness" even in
   the AI shot, but it makes the AI "a bit" intelligent
   (my AI remembers just the previous shot).
   Returns the coordinate of the intelligent shot if this
   was done successfully, or a random shot if the intelligent
   shot was not in pdt """

    #randomizing the position that will be changed
    rand = random.randint(0,3)
    value = posToCoord(shotsDone[len(shotsDone)-1])
    
    #Different cases for each random position
    if(rand==0):
        coord = value[0] + str(int(value[1:])+1)
        
        if coordToPos(coord) in pdt:
            shotsDone.append(coordToPos(coord))
            pdt.pop(pdt.index(coordToPos(coord)))
            return coord
        
        else:
            return randomShot()
    if(rand==1):
        coord = value[0] + str(int(value[1:])-1)
        
        if coordToPos(coord) in pdt:
            shotsDone.append(coordToPos(coord))
            pdt.pop(pdt.index(coordToPos(coord)))
            return coord
        
        else:
            return randomShot()
    if(rand==2):
        coord = chr(ord(value[0])+1) + str(value[1:])
        
        if coordToPos(coord) in pdt:
            shotsDone.append(coordToPos(coord))
            pdt.pop(pdt.index(coordToPos(coord)))
            return coord
        
        else:
            return randomShot()
    if(rand==3):
        coord = chr(ord(value[0])-1) + str(value[1:])
        
        if coordToPos(coord) in pdt:
            shotsDone.append(coordToPos(coord))
            pdt.pop(pdt.index(coordToPos(coord)))
            return coord
        
        else:
            return randomShot()

def shotResult(result, pos, board):

    """Check the outcome of the AI shot
    Checking the result of the AI shot depending on our input(A,H or T)"""
    
    if (result == 'A'):
        print("Vaya, lo intentaré de nuevo")
        board[pos[0]][pos[1]] = '+'
        
    elif (result == 'T'):
        print("Jaja, voy a por ti")
        board[pos[0]][pos[1]] = 'x'
        
    elif (result == 'H'):
        print("Bien! Uno menos jajaja")
        board[pos[0]][pos[1]] = 'x'
        





#Main
"""Main code here"""

print("Bienvenido a Hundir la Flota!!!")
print("Voy a distribuir mis barcos ....")
print("Ya está. Podemos empezar:")
setAllShips(AIBoard, Ships)
pdtcopy = [posToCoord(i) for i in pdt]


#Main loop of the game
while(len(pdt)!=0):
    
    printBoard(AIBoard)
    printBoard(AIBoardCopy)

    #Checking if the input coordinate is correct
    move = str(input("Introduce tu jugada (ej. A5): "))
    while(move not in pdtcopy):
        move = str(input("Introduce tu jugada (ej. A5): "))
        
    checkMyShot(coordToPos(move),AIBoard,Ships)

    #Checking if the shot will be intelligent or not
    if(AIIntelligence):
        rand = AIShot() 
    else:
        rand = randomShot()
        
    print("Ahora tiro yo verás:", rand)

    #Checking if the input letter is correct
    result = input("¿Cómo ha resultado mi disparo (A:agua, T:tocado, H:hundido)?: ")
    while(result not in letters):
        result = input("¿Cómo ha resultado mi disparo (A:agua, T:tocado, H:hundido)?: ")

    #Detecting if the next shot will be intelligent or not
    if(result=='T'):
        AIIntelligence = True
    else:
        AIIntelligence = False

    shotResult(result,coordToPos(rand),AIBoardCopy)
