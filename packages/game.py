from .player import Player
import random
import keyboard
import time

class Game:
    players = []
    player_turn = 0

    started = False

    MAX_PLAYERS = 10
    DICES_NUMBER = 6

    points_sum = 0
    last_dices_rest = 0


    def showRules(self):
        print("Règles\n\n") 


    def showMenu(self):
        print("A game by p2sias")
        print("Bienvenue dans le jeu du 5000 !\na) Voir les règles\nb) Jouer")
        while True:
            choice = input("Votre choix (a/b) : ")
            
            if choice == "a":
                self.showRules
            elif choice == "b":
                self.initGame()
            else:
                print("[INFO] Erreur de saisie")
                continue
            break
    
    def inputFilter(self, string):
        """
            Replace space by void in inputs

            string : input string
        """
        res = input(string)
        res = res.replace(" ", "")
        return res
    
    def dropDices(self, number):
        """
            Roll a amount of dices

            number : amount of dices
        """
        dices = []
        
        # because i use the last_rest_dices variable in param, if there is no rest, i roll 6 dices
        if number == 0:
           number = self.DICES_NUMBER

        # add the results of dices roll in a array of dices
        for i in range(number):
            dices.append(random.randint(1, 6))

        # return the dices
        return dices
    
    def seeScore(self):
        """
            Obviously, print the score
        """
        print("\n"*600)
        print("\n_____SCORES____")
        print("Cagnotte: " + str(self.points_sum)+"\n")
        for player in self.players:
            print(player.pseudo + " : " + str(player.score()))
        print("_______________\n")

    

    def displayDices(self, dices):
        """
            Display dices with delay and 1, 5 are marked by a '-'
        """
        print(self.pseudoTag() + "Voici vos dés : \n")
        for dice in dices:
            if dice == 1 or dice == 5:
                dice = str(dice) + "-"
            print(dice)
            time.sleep(0.500)
    
    def checkPoints(self, dices):
        """
            Check all dices an return the score
        """
        points_to_add = 0
        dices_rest = 0

        last_three = 0

        #for dice in dices.sort():
            #if dices.count(dice) == 3 and dice != last_three:
                


        for dice in dices:
            if dice == 1:
                points_to_add += 100
            elif dice == 5:
                points_to_add += 50
            else:
                dices_rest += 1

        self.last_dices_rest = dices_rest

        return points_to_add
    
    def nextTurn(self):
        """
            Go to next turn when i press SPACE
        """
        # return to the first player when last player played
        try:
            self.players[self.player_turn + 1]
            self.player_turn += 1
            print("Appuyez sur ESPACE pour passer au tour de " + self.players[self.player_turn].pseudo)

        except IndexError:
            self.player_turn = 0
            print("Appuyez sur ESPACE pour passer au tour de " + self.players[self.player_turn].pseudo)

        keyboard.wait('space')



    def pseudoTag(self):
        """
            Generate a pseudo Tag like '[pseudo] blablabla...'
        """
        pseudo = self.players[self.player_turn].pseudo
        return "["+pseudo+"] "
        
    def playTurn(self):
        """
            Play a turn of one player
        """

        self.seeScore()

        # redrop variable is True when a player want to reroll the dices
        redrop = False

        print("C'est au tour de " + self.players[self.player_turn].pseudo + '\n')
        
        
        while True:
            # If there is dices in rest and not redrop, it mean that a new turn is beginning, so the next player can roll the rest dices and maybe keep the points or roll from 0 
            if self.last_dices_rest > 0 and not redrop:
                while True:
                    keep_last_dices = self.inputFilter(self.pseudoTag() + "Voulez-vous rejouer le(s) " + str(self.last_dices_rest) + " dé(s) précédants ? " + str(self.points_sum) + " points en jeu (o/n)")

                    if keep_last_dices == "o":
                        break
                    elif keep_last_dices == "n":
                        # The player want to make a new roll 
                        self.points_sum = 0
                        self.last_dices_rest = 0
                        break
                    else:
                        print("Erreur de saisie")
                        continue
            redrop = False

            # Get the rolled dices
            dices = self.dropDices(self.last_dices_rest)

            # Display the dices
            self.displayDices(dices)

            # Check the score
            points = self.checkPoints(dices)
            
            self.points_sum += points

            # If player won points
            if points > 0:
                # Display somes informations
                print(self.pseudoTag()+"+ "+str(points)+" points en cagnotte")
                print(self.pseudoTag()+" Cagnotte: " + str(self.points_sum) + " | Dés restants : " + str(self.last_dices_rest)+ "\n")
                if self.last_dices_rest == 0:
                    print(self.pseudoTag() + "Bravo, c'est un sans faute !\n")
                
                # Ask for reroll
                while True:
                    choice = self.inputFilter(self.pseudoTag() +
                                   "Voulez-vous relancer ? (o/n) : ")
                    if choice == "n":
                        # If not, the player win the current points and the next player may use his rest dices and points
                        self.players[self.player_turn].addPoints(self.points_sum)
                        break
                    elif choice == "o":
                        # If yes, the current player reroll with the rest dices
                        redrop = True
                        break
                    else:
                        print("Erreur de saisie")
                        continue
            # If player not won points
            else:
                self.points_sum = 0
                self.last_dices_rest = 0
                print(self.pseudoTag() + "Vous n'avez gagné aucun points")
                self.nextTurn()
                break
            
            # If a player get 5000, end the game
            if self.players[self.player_turn].score() >= 5000:
                self.started = False
            
            if redrop == True:
                continue
            else:
                self.nextTurn()
                break
                

    def initGame(self):
        """
            Get informations like :
                * Amount of players
                * Pseudo of players
        """
        player_count = ""
        while True:
            player_count = input("Combien de joueurs ? : ")

            try:
                int(player_count)

            except ValueError:
                print("[INFO] Erreur de saisie !")
                continue
            
            player_count = int(player_count)

            if (player_count > self.MAX_PLAYERS):
                print("[INFO] 6 joueurs maxi !")
                continue
            else:
                break
        
        for i in range(player_count):
            

            while True:
                exist = False
                pseudo = str(input("Pseudo du joueur " + str(i + 1) + " : "))
                for player in self.players:
                    if player.pseudo == pseudo:
                        print("[INFO] Ce pseudo est déjà utilisé !")
                        exist = True
                        break
                if exist:
                    continue
                else:
                    break
                
            
            # Create a New player instance
            new_player = Player(pseudo)

            # Add the instance to the player list
            self.players.append(new_player)
        
        # Start the game
        self.started = True
        

        
    






