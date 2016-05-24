# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
game_end = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


card_no = 0

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_list = []	# create Hand object

    def __str__(self):
        # return a string representation of a hand
        card_string = ""
        for i in range(len(self.hand_list)):
            card_string += self.hand_list[i].suit
            card_string += self.hand_list[i].rank
            card_string += " "
        return card_string

    def add_card(self, card):
        self.hand_list.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        self.hand_value = 0
        hand_has_ace = 0
        for card in self.hand_list:
            self.hand_value += int(VALUES[card.rank])
            if int(VALUES[card.rank]) == 1:
                hand_has_ace += 1
        if  hand_has_ace >= 2 or hand_has_ace == 0:        
            return self.hand_value
        else:
            if self.hand_value + 10 <=21:
                return self.hand_value + 10
            else:
                return self.hand_value
            
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.hand_list:
            card.draw(canvas,pos)
            pos[0] = pos[0] + CARD_SIZE[0] + 10
 
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.deck = []
        for i in range(4):
            for j in range(13):
                card = Card(SUITS[i], RANKS[j])
                self.deck.append(card)

    def shuffle(self):
        # shuffle the deck 
        # use random.shuffle()
        random.shuffle(self.deck)
        

    def deal_card(self):
        # deal a card object from the deck
        global card_no
        dealed_card = self.deck[card_no]
        card_no += 1
        return dealed_card
    
    def __str__(self):
        # return a string representing the deck
        deck_string = "Deck contains"
        for i in range(len(self.deck)):
            deck_string += str(self.deck[i])
            deck_string += " "
        return deck_string	


#define event handlers for buttons
def deal():
    global outcome, in_play, card_no, deck,player_hand, dealer_hand
    global game_end, score,message
    outcome = ""
    if in_play:
        outcome = "You lose.New Game started."
        score -= 1
        #game_end = 0
        print outcome, score
   
    #new game starts
   
    message = "Hit or Stand ?"
    game_end = 0
    in_play = 1
    #outcome = ""
    deck = Deck()
    player_hand = Hand()
    dealer_hand = Hand()
    deck.shuffle()
    
    card_no = 0
    print deck
    for i in range(2):
       player_hand.add_card(deck.deal_card())
       dealer_hand.add_card(deck.deal_card())
      
    print "player hand", player_hand
    print "dealer hand", dealer_hand
    in_play = True
    
    print "player value",player_hand.get_value()
    print "delaer value",dealer_hand.get_value()

def hit():
    # replace with your code below
    global in_play, score, outcome, game_end, message
    # if the hand is in play, hit the player
    #outcome=""
    if not game_end:
        if in_play and player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            message = "Hit or Stand ?"
        print "player hand", player_hand
        
        # if busted, assign a message to outcome, update in_play and score
        if in_play and player_hand.get_value() > 21:
            in_play = False
            outcome = "You went bust and lose!"
            message = "New Deal?"
            score -= 1
            game_end = 1
            print outcome, score
            return
        if not in_play:
            dealer_hand.add_card(deck.deal_card())
            print "dealer hand:", dealer_hand
            if dealer_hand.get_value() > 21:
                outcome = "Dealer busted, you win."
                message = "New Deal?"
                score += 1
                game_end = 1
                print outcome, score
                return
            elif player_hand.get_value() <= dealer_hand.get_value():
                outcome = "You lose."
                message = "New Deal?"
                score -= 1
                game_end = 1
                print outcome, score
                return
        
def stand():
   
    global in_play, score, outcome, game_end,message
    in_play = 0
    if not game_end:
        if  player_hand.get_value() <= dealer_hand.get_value():
            outcome = "You lose. Dealer wins."
            message = "New Deal?"
            score -= 1
            game_end = 1
            print outcome, score,player_hand.get_value()
            return
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        if player_hand.get_value() > 21:
            print outcome
            game_end = 1
            return
        else:
            if dealer_hand.get_value() >= player_hand.get_value() and dealer_hand.get_value() >= 17:
                outcome = "You Lose."
                message = "New Deal?"
                score =- 1
                game_end = 1
                print outcome, score
                return
            while dealer_hand.get_value() < 17:
                hit()
        if  player_hand.get_value() > dealer_hand.get_value():
            outcome = "You win."
            message = "New Deal?"
            score += 1
            game_end = 1
            print outcome, score
            return
    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome
    #card = Card("S", "A")
    #card.draw(canvas, [300, 300])
    canvas.draw_text("Blackjack",[230,50], 35, "Red")
    canvas.draw_text("Dealer",[50,100],25, "Black")
    dealer_hand.draw(canvas,[50,150])
    canvas.draw_text("Player",[50,300],25, "Black")
    player_hand.draw(canvas,[50,350])
    canvas.draw_text(outcome,[250,100],25,"Black")
    canvas.draw_text(message,[250,300],25,"Black")
    #print in_play
    if in_play:
       canvas.draw_image(card_back,[36, 48], [72, 96],[86,198],[72,96] )
    score_str = "Your Score:" + str(score)
    canvas.draw_text(score_str, [400,50], 25, "Blue")
#initialization objects


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


