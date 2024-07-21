import enum as en


#--------------------------------------ANSI escape codes for colors----------------------------------------------------
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
END = '\033[0m'  # Resets color to default
#----------------------------------------------------------------------------------------------------------------

bout = 1 #global variable for round number

#class to control the validity of the teams or each player
#loser - lost the bet
#winner - won the beat
#valid - can still bet on this one
class tVal(en.Enum):
    
    loser = en.auto()
    valid = en.auto()
    winer = en.auto()
    tie = en.auto()
    betting = en.auto()

#player class
class player:
    def __init__(self, name = 'Null', money = 10, points = 0, joker2 = 1, joker3 = 1, teams = [], lock = -1, lost = 0):

        self.name = name #player name
        self.money = money #starting money for each player
        self.points = points #points gained from bets

        #jokers (2 or 3 if active, 1 if not active, -1 if not available)
        self.joker2 = joker2
        self.joker3 = joker3

        self.Team = teams #list with validity of each team

        self.lock = lock #index of the team the player locked their bet on
        self.lost = lost #control variable to determine if player lost or not in the sequence

#Function to format string so that the corresponding correct command is found
#
#Inputs: string to be formated
#
#Outputs: command candidate to be tested
def fstc(str):

    comcand = str.replace(' ', '').lower().strip() #format words
    return comcand

#Function to extract teams from txt file to a vector. The teams should be stored in a file
#named "equipas.txt". Each line of the txt should contain one team. The teams are then 
#organized alphabetically
#
#Pseudoinputs: txt file
#Outputs: vector with teams in alphabetical order
def storeteams():

    # Open teams file and save lines (teams) inside a vector
    with open('equipas.txt', 'r') as file:

        lines = file.readlines() #save lines

    # Create vector to store the participating teams
    teams = []

    # Store each team inside the vector
    for line in lines:

        teams.append(line.strip())
        teams = sorted(teams)

    return teams #return team list

#Function to initialize the player. Creates a vector of player structs. 
#Fills each struct with player names and marks every team as valid for each player
#i.e. each player can vote in whatever team
#
#Inputs: number of teams in the competition (nt)
#Outputs: vector with player structs
def getplayers(nt):

    nop = input('Número de jogadores: ') #get number of players
    while nop.isdigit() == False: #get nop until it is valid
        print("Invalid number of players.")
        nop = input('Número de jogadores: ') #get number of players

    Player = [] #empty vector to store players
    # Loop to create the right amount of players 
    for n in range(int(nop)):

        #create player struct and initialize it correctly
        Player.append(player())
        Player[n].name = input('Nome do ' + str((n + 1)) + ' jogador: ')
        teams = []
        for m in range(nt):
            teams.append(tVal.valid)

        Player[n].Team = teams

    return Player #return vector with all players