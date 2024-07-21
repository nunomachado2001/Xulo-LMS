import initialize as ini
import math as m

def save_game(Player):

    with open('save.txt', 'w') as file:

        file.write('bout = ' + str(ini.bout) + '\n')
        file.write('\n')
        
        for player in Player:
            file.write('name = ' + str(player.name) + '\n')
            file.write('money = ' + str(player.money) + '\n')
            file.write('points = ' + str(player.points) + '\n')
            file.write('joker2 = ' + str(player.joker2) + '\n')
            file.write('joker3 = ' + str(player.joker3) + '\n')
            file.write('teams = ' + str(player.Team) + '\n')
            file.write('lock = ' + str(player.lock) + '\n')
            file.write('lost = ' + str(player.lost) + '\n')

    return

def load_teams(line):

    line = line.split('=')[1].strip()
    teams = [eval(string.split(':')[0].split('<')[-1].strip()) for string in line]

    return teams


def load_game(Player):

    with open('save.txt') as file:

        Line = file.readlines()

    # Get round number
    bout = Line[0].split('=')
    bout = bout[1].strip()
    ini.bout = int(bout)

    # Get players' info
    l = 0
    for line in Line:

        line = line.split('=')
        if 'name' == line[0].strip:
            player = ini.player()

            player.name = line[1].strip()
            player.money = int(Line[l+1].split('=')[1].strip())
            player.points = int(Line[l+2].split('=')[1].strip())
            player.joker2 = int(Line[l+3].split('=')[1].strip())
            player.joker3 = int(Line[l+4].split('=')[1].strip())

            player.Team = load_teams(Line[l+5])

            player.lock = int(Line[l+6].split('=')[1].strip())
            player.lost = int(Line[l+7].split('=')[1].strip())

            Player.append(player)

            l += 7

            for n in range(7):
                continue

        l += 1

    return


#Function to start the game. First get the teams in txt file and then get the players information
#
#Outputs: Team and Player vectors
def start_game():

    #Get initial informatin (teams and players)
    Team = ini.storeteams()
    Player = ini.getplayers(len(Team))

    #Format the player names accordingly
    for i,player in enumerate(Player):

        player.name = ini.fstc(player.name) #remove spaces and lower case it

        #if any 2 players have the same name display error message and restart process
        for k in range(i):
            if player.name == Player[k].name:

                print("Os nomes dos jogadores têm de ser todos diferentes!")
                start_game(Team, Player)
                break #end secondary loop
        else:
            continue #continue main loop if "if" is not triggered

        break #exit main loop

    return Team, Player

def print_teams(player, Team):

    #print info saying it belongs to the corresponding player
    print()
    print('Jornada ' + str(ini.bout))
    print("Leque do " + player.name) 
    print()
    #-------------------------------------------------------

    for n, team in enumerate(Team):

        if player.Team[n] == ini.tVal.winer:
            print(ini.GREEN + team + ini.END)
        elif player.Team[n] == ini.tVal.tie:
            print(ini.YELLOW + team + ini.END)
        elif player.Team[n] == ini.tVal.loser:
            print(ini.RED + team + ini.END)
        elif player.Team[n] == ini.tVal.betting:
             print(ini.BLUE + team + ini.END)
        else:
            print(team)

    print()

    return

#Function to activate / deactivate the jokers of the current active player.
#1 is not active, -1 is active, 0 is not available
#
#Inputs: joker type, active player
def joker(jt,ap):

    #double points joker
    if jt == 2 and ap.joker2 == 1:
        ap.joker2 = 2
        print('Joker duplo ativado.')
    elif jt == 2 and ap.joker2 == 2:
        ap.joker2 = 1
        print('Joker duplo desativado.')
    elif jt == 2 and ap.joker2 == -1:
        print('Já não tens joker duplo!')

    #triple points joker
    if jt == 3 and ap.joker3 == 1:
        ap.joker3 = 3
        print('Joker triplo ativado.')
    elif jt == 3 and ap.joker3 == 3:
        ap.joker3 = 1
        print('Joker triplo desativado.')
    elif jt == 3 and ap.joker3 == -1:
        print('Já não tens joker triplo!')

    return

#Function to check if command given corresponds to the name of a player and, if it does,
#display the player's teams' pool
#
#Inputs: name to be tested, active player, player vector, team vector
#
#Outputs: active player and result (1 if success 0 if not)
def check_players(name, ap, Player, Team):

    #Check each player inside the vector
    for player in Player:
        if name == player.name:
            
            #print player's teams' pool
            print_teams(player, Team)
            
            return player, 1 #if player is found end loop
    return ap, 0 #if no player is found return NULL

#Function to check if given command corresponds to a team. If it does, that team is marked as being bet on, deselecting
#any teams the player was previously betting on
#
#Inputs: name to be tested, active player, team list
#
#Outputs: 1 if successfull, 0 if no team was found
def check_teams(name, ap, Team):

    # Check the name of every team and stop when corresponding team is found
    for i,team in enumerate(Team):
        if name == ini.fstc(team):

            # If player hasn't preaviously beat on this team then mark it as betting
            if (ap.Team[i] == ini.tVal.valid or ap.Team[i] == ini.tVal.betting) and ap.lock == -1:

                #remove previously team being betted on (mark as valid)
                for k,t in enumerate(ap.Team):

                    if t == ini.tVal.betting:
                        ap.Team[k] = ini.tVal.valid

                ap.Team[i] = ini.tVal.betting #mark selected team as being bet on
                print_teams(ap, Team) #print new team list
            
            #if player has already bet display corresponding error message
            elif ap.lock != -1:

                print()
                print("Já fizeste a tua aposta esta ronda!")
                print_teams(ap, Team)

            #if player chooses and invalid team display corresponding error message
            else:
                print()
                print("Já apostaste nessa equipa!")
                print_teams(ap, Team)

            return 1 #return 1 if successfull
    
    return 0 #return 0 if team is not found

#Function to lock player's choice
#
#Inputs: active player
def confirm_bet(ap, Team):
    
    # Find the team the player is betting on and change lock to corresponding index
    for n,team in enumerate(ap.Team):

        if team == ini.tVal.betting:
            ap.lock = n
            print_teams(ap, Team)
            return
        else: #print corresponding error message if player is not betting on anything
            print()
            print('Não estás a apostar em nenhuma equipa!')
            print_teams(ap, Team)
    
    return

#Function to get game results from each bout. The names of the clubs that one should be inside 
#jornadaX.txt where X is the bout number
#
#Outputs: list with winning teams
def get_results():

    filename = 'jornada' + str(ini.bout) #format file name to read teams from

    # Create sorted winning teams vector
    with open(filename, 'r') as file:
        lines = file.readlines()

    wteams = []
    for line in lines:
        wteams.append(line.strip())
    wteams = sorted(wteams)

    return wteams

#Function to advance the sequence when one finishes
#
#Inputs: player vector
def advance_sequence(Player):

    # Reset sequence by resetting the validity values of the teams of each player
    for player in Player:
        for n in range(len(player.Team)):
            player.Team[n] = ini.tVal.valid

    return

#Function to update the game results after one round of bets is finished
#
#Inputs: vector with winning teams for that round, player vector, teams vector
def update_results(Wteam, Player, Team):

    ini.bout += 1 #update round

    nlosses = 0 #tracks how many players have already lost
    for n,player in enumerate(Player):

        #by default assume player lost marking the team he bet on as lost and adding one to the loss counter
        player.Team[player.lock] = ini.tVal.loser
        nlosses += 1
        #after checking winning/tying teams, if player won update team value to winer and subtract one from loss counter
        for team in Wteam: 
            if team == Team[player.lock]: #case for winning
                player.Team[player.lock] = ini.tVal.winer
                player.points += 3 * abs(player.joker2) * abs(player.joker3)
                nlosses -= 1
                break
            elif team == Team[player.lock] + ' E': #case for tying
                player.Team[player.lock] = ini.tVal.tie
                player.points += 1 * abs(player.joker2) * abs(player.joker3)
                nlosses -= 1
                break
        
        # Consume jokers if used
        if player.joker2 == 2:
            player.joker2 = -1

        if player.joker3 == 3:
            player.joker3 = -1
             
        player.lock = -1 #reset locks of each player

    #if all players lost, advance the sequence
    if nlosses >= n + 1 or Player[0].money == 0:
        advance_sequence(Player)

    return 

#Function to advance the round of play
#
#Inputs: player vector, team vector
def advance_round(Player, Team):

    tlock = 0 #total number of locked players
    #count number of locked players
    for player in Player:
        if player.lock != -1:
            tlock += 1
    
    #if not everyone confirmed their choice display corresponding error message and return
    if tlock < len(Player):
        print('Todos os jogadores têm de confirmar a sua escolha antes de avançar.')
        return
    
    #if everybody confirmed their choice advance the round
    Wteam = get_results() #vector for the winning teams
    update_results(Wteam, Player, Team) #upate the results
    
    return


