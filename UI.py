import initialize as ini
import enum as en
import UIcommands as UIc

#List of possible user interface commands given by the user
class UICommand(en.Enum):

    startGame = en.auto() #start game
    advanceRound = en.auto() #advance to next round
    saveGame = en.auto()

    selectPlayer = en.auto() #select player
    betTeam = en.auto() #select team to bet in
    confirmTeam = en.auto() #confirm team choice

    joker2 = en.auto()
    joker3 = en.auto()

    terminate = en.auto() #exit the program

    ukCommand = en.auto() #unknown command

#Function to transform a string given by the user to its corresponding command
#
#Inputs: user input
#
#Outputs: corresponding command
def string_to_command(comcand):
    
    if comcand == 'start':
        return UICommand.startGame
    
    if comcand =='confirm':
        return UICommand.confirmTeam
    
    if comcand == 'next':
        return UICommand.advanceRound
    
    if comcand == 'joker2':
        return UICommand.joker2

    if comcand == 'joker3':
        return UICommand.joker3
    
    if comcand == 'save':
        return UICommand.saveGame

    if comcand == 'exit':
        return UICommand.terminate
    
    return UICommand.ukCommand


#Function that defines the behaviour of the user interface depending on the input given by the user
def UIstart():

    command = UICommand.ukCommand #default to unkown command
    startok = 0 #signal to mark that the game as started
    action = 0 #action control variable
    round = 1 #current round

    while command != UICommand.terminate:

        command = UICommand.ukCommand #reset command (if this isnt done same command would repeat)
        userinput = input().split(' ') #divide user input to analyse 
        comcand = '' #command candidate

        #Iterate through every element of the userinput until a valid command is found
        i = 0 #counter for words in user input
        while (command == UICommand.ukCommand and i < len(userinput)):
            
            comcand = ini.fstc(comcand + userinput[i]) #format string (no spaces all lower)
            command = string_to_command(comcand) #get possible command from comcand

            i += 1
        #get extra arguments if user input has not ended
        extra = [''] #default value (if there is no extra) to avoid crashes
        if i < len(userinput):
            extra = userinput[i:]
        
        # ------------------------------------------Execute correct command----------------------------------------------------

        # Start game------------------------------------------------------------------
        if command == UICommand.startGame and not startok:

            Team, Player = UIc.start_game()
            activeplayer = Player[0]
            UIc.print_teams(activeplayer, Team)
            startok = 1 #game has started
        elif command == UICommand.startGame:
            print('O jogo já começou!')
            UIc.print_teams(activeplayer, Team)
        #------------------------------------------------------------------------------

        # Save game---------------------------------------------------------------
        if command == UICommand.saveGame and startok:
            UIc.save_game(Player)
        elif command == UICommand.saveGame:
            command = UICommand.ukCommand
        #------------------------------------------------------------------------

        # Confirm bet---------------------------------------------
        if command == UICommand.confirmTeam and startok:
            UIc.confirm_bet(activeplayer, Team)
        elif command == UICommand.confirmTeam:
            command = UICommand.ukCommand
        
        #----------------------------------------------------------------

        # Advance round--------------------------------------------------------------------
        if command == UICommand.advanceRound and startok:
            UIc.advance_round(Player, Team)
            UIc.print_teams(activeplayer, Team)
        elif command == UICommand.advanceRound:
            command = UICommand.ukCommand
        #-----------------------------------------------------------------------------

        # Jokers-----------------------------------------------------------------------------
        if command == UICommand.joker2 and startok:
            UIc.joker(2,activeplayer)
            UIc.print_teams(activeplayer, Team)
        
        elif command == UICommand.joker3 and startok:
            UIc.joker(3,activeplayer)
            UIc.print_teams(activeplayer, Team)

        elif command == UICommand.joker2 or command == UICommand.joker3:
            command = UICommand.ukCommand
        #---------------------------------------------------------------------------------

        # Change active player----------------------------------------------------------
        if command == UICommand.ukCommand and startok == 1: #if commmand is unknown check if it is the name of any player

            activeplayer, action = UIc.check_players(comcand, activeplayer, Player, Team)
            if action == 1:
                command = UICommand.selectPlayer
                action = 0
        #--------------------------------------------------------------------------------------

        # Bet on team----------------------------------------------------------
        if command == UICommand.ukCommand and startok == 1: #if command is unknown check if it is the name of any team
            
            action = UIc.check_teams(comcand, activeplayer, Team)
            if action == 1:
                command = UICommand.betTeam
                action = 0
        #-----------------------------------------------------------------------------------
        
        # Default unknown-----------------------------------------------------------------
        if command == UICommand.ukCommand:
            print('Unknown command.')
        #---------------------------------------------------------------------------------

    return


