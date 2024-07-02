import random
discard = []
multi = 1
total_damage = 0
""" CLASSES """

class player:

    def __init__(self, name: str, hp: int, maxhp: int, hand: list):
        self.hp = hp
        self.maxhp = maxhp
        self.hand = hand
        self.name = name
        self.healthbar = healthbar(self)
        
    def drawcard(self):
        damage = random.randint(1,12)
        colour = random.randint(1,4)
        return([colour, damage])
    
    def startcard(self):
        global discard
        colour, damage = self.drawcard()
        while damage > 9:
            colour, damage = self.drawcard()
        discard = [colour, damage]
        self.discardpile(discard)

    def discardpile(self, card):
        colour, damage = self.cardname(card)
        print("Discard Pile: {} {}".format(colour, damage))
        print()

    def cardname(self, x):
        
        if x[0] == 1:
            colour = "Red"
        elif x[0] == 2:
            colour = "Blue"
        elif x[0] == 3:
            colour = "Green"
        else:
            colour = "Yellow"

        if x[1] == 10:
            damage = "x2"
        elif x[1] == 11:
            damage = "+2"
        elif x[1] == 12:
            colour = "Wild"
            damage = "Card"
        else:
            damage = x[1]

        return(colour, damage)
        
    def showhand(self) -> None:
        print("{}'s hand:".format(self.name))
        count = 0
        for x in (self.hand):
            count += 1
            colour, damage = self.cardname(x)               
            print("{}: {} {}".format(count, colour, damage))
        print("")

    def usable(self):
        global discard
        use_array = []
        for x in (self.hand):
            if x[0] == discard[0] or x[1] == discard[1] or discard[1] == 12 or x[1] == 12: 
                use_array.append(x)
                
        return use_array

    def showgamestate(self, enemy) -> None:
        global discard
        enemy.healthbar.display()
        print()
        enemy.showhand()
        print()
        self.healthbar.display()
            
    def turn(self) -> None:
        global total_damage
        total_damage = 0
        global discard
        print("{}'s turn:".format(self.name))
        print()
        use_array = self.usable()
        
        if len(self.hand) == 0:
            print("You are out of cards!")
            print("You draw seven new cards!")
            
            for x in range(7):
                self.hand.append(self.drawcard())
                
            use_array = self.usable()
        
        if len(use_array) == 0:
            print("You have no playable cards!")
            while len(use_array) == 0:
                print("You draw one card!")
                    
                newcard = (self.drawcard())
                self.hand.append(newcard)
                colour, damage = self.cardname(newcard)
                print("You drew {} {}.".format(colour, damage))
                print()
                    
                use_array = self.usable()
                
                    
        while len(use_array) > 0:
            self.showhand()
            self.discardpile(discard)
            choose = input("Choose action - Play card(P) / Check(C) / End turn(E): ")
            print()
            
            if choose.upper() == 'P':
                print("Usable Cards: ")
                
                count = 0
                for x in use_array:
                    count += 1
                    colour, damage = self.cardname(x)
                    print("{}: {} {}".format(count, colour, damage))
                print()

                action = input("Input the number of the card you want to play: ")
                while True:
                    if action.isdigit() == False or action == '':
                        action = input("Invalid action. Please input a number from 1 to {}: ".format(count))
                    elif int(action)-1 >= count or int(action)-1 < 0:
                        action = input("Invalid action. Please input a number from 1 to {}: ".format(count))
                    else:
                        break
                action = int(action)-1
                
                card.playcard(self, use_array, action)
                
                discard = (use_array[action])
                self.discardpile(discard)
                
                self.hand.remove(use_array[action])
                
                if len(use_array) == 0:
                    self.hand.append(self.drawcard())

                use_array = self.usable()

            elif choose.upper() == 'C':
                if self.name == "Player 1":
                    self.showgamestate(B)
                else:
                    self.showgamestate(A)
                
            elif choose.upper() == 'E':
                print("You end your turn and draw two cards!")
                
                newcard = (self.drawcard())
                self.hand.append(newcard)
                colour, damage = self.cardname(newcard)
                print("You drew {} {}.".format(colour, damage))
                
                newcard = (self.drawcard())
                self.hand.append(newcard)
                colour, damage = self.cardname(newcard)
                print("You drew {} {}.".format(colour, damage))
                print()
                
                break
            else:
                continue
            print()

        print("You have run out of actions")
        print("Your turn is over.")
        print()
        print("You dealt {} damage in total".format(total_damage))


class card:
    def __init__(self, colour: str, damage: int):
        self.colour = colour
        self.damage = damage

    def damage(self, target, damage: int) -> None:
        global total_damage
        global multi
        target.hp -= damage*multi
        print()
        
        if multi > 1:
            print("You dealt {} damage! (x{})".format(damage*multi, multi))
        else:
            print("You dealt {} damage!".format(damage*multi))
                  
        total_damage += (damage*multi)
        target.hp = max(target.hp, 0)

    def playcard(self, use_array, action) -> None:
        global multi
        damage = use_array[action][1]
        if damage < 10:
            if self.name == "Player 1":
                card.damage(A, B, (use_array[action])[1])
                B.healthbar.display()
                print()
            else:
                card.damage(B, A, (use_array[action])[1])
                A.healthbar.display()
                print()
            multi = 1
            
        elif damage == 10:
            multi *= 2
            print("Current Multiplier: x{}".format(multi))

        elif damage == 11:
            print()
            print("You draw two cards!")
            
            if self.name == "Player 1":
                newcard = (self.drawcard())
                A.hand.append(newcard)
                colour, damage = self.cardname(newcard)
                print("You drew {} {}.".format(colour, damage))
                
                newcard = (self.drawcard())
                A.hand.append(newcard)
                colour, damage = self.cardname(newcard)
                print("You drew {} {}.".format(colour, damage))

                print()
            else:
                newcard = (self.drawcard())
                B.hand.append(newcard)
                colour, damage = self.cardname(newcard)
                print("You drew {} {}.".format(colour, damage))
                
                newcard = (self.drawcard())
                B.hand.append(newcard)
                colour, damage = self.cardname(newcard)
                print("You drew {} {}.".format(colour, damage))

                print()
                
            print("Current Multiplier: x{}".format(multi))
        else:
            print("Current Multiplier: x{}".format(multi))

class healthbar:
    full = "■"
    empty = "□"
    barrier = "|"
    
    def __init__(self, entity, length: int = 20) -> None:
        self.entity = entity
        self.length = length
        self.maxvalue = entity.maxhp
        self.currentvalue = entity.hp
    
    def update(self) -> None:
        self.currentvalue = self.entity.hp

    def display(self) -> None:
        self.update()
        fullbars = round(self.currentvalue / self.maxvalue * self.length)
        emptybars = self.length - fullbars
        
        print("{}'s health: {}/{}".format(self.entity.name, self.entity.hp, self.entity.maxhp))
        print("{}{}{}{}".format(self.barrier, self.full*fullbars, self.empty*emptybars, self.barrier))

def tutorial():
    
    print("Welcome to UNO Battle!")
    print("If you aren't already familiar with UNO, this game is played with cards that each have their own colour and number")
    print("At the start of their turn, each player draws 7 cards. This is their 'hand'")
    print("There is a 'discard pile', where all the cards you play will go.")
    print("Whenever you play a card, it MUST match the card on the top of the discard pile in either colour or number.")
    print("If none of your cards match the card on top of the discard pile, you have to draw cards until you get a card that does match.")
    print("The objective of UNO is to use up all your cards.")
    print("However, there are a few key differences between UNO and UNO Battle.")
    print()
    input("Press enter to continue.")
    print()
    print("Firstly, in UNO Battle, the objective of the game is to defeat your opponent.")
    print("Each player has 100 health points, and when their health reaches 0, they lose.")
    print("Whenever you play a card, your opponent will receive damage equal to the number on the card")
    print("For example, a Blue card with the number 5 on it wil reduce your enemy's health by 5 points")
    print("However, the rules of the discard pile still apply, and you can only play certain cards")
    print()
    input("Press enter to continue.")
    print()
    print("Secondly, you can play an unlimited number of cards from your hand, until your hand is empty.")
    print("When you play a card, it goes on top of the discard pile, and the next card you play has to match it")
    print("However, since you can play as many cards as you want, if you are careful and have the right cards,")
    print("you can keep playing cards until your hand is empty!")
    print("Therefore, you should try to chain together as many cards as possible, to deal the most amount of damage")
    print()
    input("Press enter to continue.")
    print()
    print("However, you can also end your turn prematurely, which will allow you to immediately receive two cards!")
    print("Furthermore, if you end a turn with no cards, you will draw 7 cards at the start of the next turn!")
    print("By planning carefully, you will be able to get a large number of cards, which you can use to defeat your opponent!")
    print()
    input("Press enter to continue.")
    print()
    print("Lastly, if you are familiar with UNO, you probably know about action cards and wild cards!")
    print("We have those in UNO Battle too!")
    print("However, our cards are slightly different.")
    print("There is the x2 card, which will multiply the next damage-dealing card's damage by 2!")
    print("Notably, the x2 multiplier can stack, which means that playing another x2 card on top of the last one will multiply damage by 4!")
    print("And if you play yet another x2 card, it will multiply by 8!")
    print("With enough x2 cards, you can deal DEVASTATING amounts of damage.")
    print()
    input("Press enter to continue.")
    print()
    print("We also have the +2 card, which unlike its UNO counterpart, will allow YOU to immediately draw 2 cards.")
    print("This can be used to give you more options for cards to play.")
    print()
    input("Press enter to continue.")
    print()
    print("Last but not least, the wild card!")
    print("While the last 2 special cards have colours assigned to them, this card can be played no matter what.")
    print("It is considered to match with all other cards in this game.")
    print("This card is especially useful when you have no cards that match with the discard pile.")
    print("It can also be used to chain together cards that don't match, by using it as a middleman.")
    print()
    input("Press enter to continue.")
    print()
    print("To end off with, here's some useful information: ")
    print("The player who goes first is decided by a coin flip.")
    print("Players decide between themselves who is player 1 and player 2, and player 1 will enter heads or tails.")
    print()
    input("Press enter to continue.")
    print()
    print("Players' hands are not hidden from each other. This is partially due to the nature of Python,")
    print("but also gives players the option to strategize around your opponent's cards.")
    print()
    input("Press enter to continue.")
    print()
    print("During a player's turn, they have 3 possible actions. Play a card, Check, or End their turn.")
    print("If you play cards until you can no longer play any more cards, your turn will end automatically")
    print()
    input("Press enter to continue.")
    print()
    print("The 'Check' option can be used by players to check their opponents health and hand, as well as their own health")
    print("The player's hand and the card on top of the discard pile will always be shown to the players before they select their action")
    print()
    input("Press enter to continue.")
    print()
    print("That marks the end of this tutorial! Hopefully it wasn't too lengthy and you were able to understand all of it.")
    print("Take your time to learn how to play this game, and have fun!")
    print("Now, the game will begin,")
    print()
    input("Press enter to continue.")
    
            
""" MAIN """
while True:
    tutor = input("Would you like to read the tutorial? [Y/N]: ")
    if tutor.upper() == "Y":
        tutorial()
        break
    elif tutor.upper() == "N":
        break


A = player(name="Player 1", hp=100, maxhp=100, hand=[])
B = player(name="Player 2", hp=100, maxhp=100, hand=[])

for x in range(7):
    A.hand.append(A.drawcard())
    B.hand.append(B.drawcard())

A.showhand()
B.showhand()
A.startcard()


A_coin = input("Player 1, enter heads or tails to decide who starts: ")
while A_coin.upper() != 'HEADS' and A_coin.upper() != 'TAILS':
    A_coin = input("Player 1, enter heads or tails to decide who starts: ")
if A_coin.upper() == 'HEADS':
    coin = 1
elif A_coin.upper() == 'TAILS':
    coin = 2
if random.randint(1,2) == coin:
    print()
    print("The coin landed on {}!".format(A_coin.lower()))
    print("Player 1 starts first.")
    print()
    print("=================================")
    print()
    while A.hp != 0 and B.hp != 0:
        A.turn()
        print()
        print("=================================")
        print()

        if B.hp > 0:
            B.turn()
            print()
            print("=================================")
            print()
else:
    if A_coin.upper() == 'TAILS':
        B_coin = 'heads'
    else:
        B_coin = 'tails'
    print("The coin landed on {}!".format(B_coin.lower()))
    print("Player 2 starts first.")
    print()
    print("=================================")
    print()
    
    while A.hp > 0 and B.hp > 0:
        B.turn()
        print()
        print("=================================")
        print()

        if A.hp > 0:
            A.turn()
            print()
            print("=================================")
            print()

if A.hp > 0:
    print(" - Player 1 Wins! - ")
else:
    print(" - Player 2 Wins! - ")
