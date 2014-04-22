"""
Created on Sun Apr 13 10:53:32 2014

@author: V SHETTY

Description:
Basic Black Jack game for Insight Data Engineering Programming Challenge
Starter code: http://bit.ly/1iHXhBr
Only 2 players including the dealer.
One deck of 52 cards used.
Cards have the following values:
Cards 2 - 10 -> face value
Card  Ace -> 11 or 1
Cards J, Q, K -> 10
Dealer randomly selects 2 cards for the player and for himself
Player adds the value of the 2 cards
If the value is 21, then it is a blackjack/natural and the player is ..
.. declared winner automatically.
If the player has a total value of <21 he can choose:
  a) Hit (request new card) until he is happy with his choice of cards
  b) Stand(stop taking any more cards)
If the player chooses to Stand, it is the turn of the dealer to play
The dealer counts the value of his 2 cards:
If the value is 21, then it is a blackjack/natural and the dealer is ..
.. declared winner automatically.
If the dealer's score is greater than the player's but does not exceed 21 ..
.. then the dealer wins
If the scores are equal then it is a draw
If the player or the dealer scores over 21 then it is declared a Bust ...
.. i.e. busted player loses and if both bust there is no winner
If the dealer's value is less than the player's, then he should hit ...
.. until his total value is greater than or equal to 17. 
If the dealer's value is >= 17, he must take the Stand and the winner ...
... declared based on who has the total value closest to 21

Simple example of a game:
            Player    |  Dealer |
(Hand 1)|    2,J      |    5,9  |"Players total value = 12.Dealer's value = 14"
(Hand 2)|    2,J,7    |    5,9  |"Player chooses to Hit, new total = 19"
(Hand 3)|    2,J,7    |   5,9,3 |"Player chooses to Stand. Dealer's value is.."
                                 " less than 17. Dealer takes a hit and his .."
                                 "  .. new card has a value =3"
(Result)      19      |     18  |"Player's value is closer to 21 and hence .. "
                                 " .. is declared winner"
"""


from random import choice as rc

def total(hand):
    """Calculates the total in hand including when 'Aces' are also present"""
    
    aces = hand.count(11)
    tot = sum(hand)
    # Since the ace can be 11 or 1, if you have gone over 21 
    if tot > BLACK_JACK and aces > 0:
        while aces > 0 and tot > BLACK_JACK:
        # Switch ace from 11 to 1
            tot -= 10
            aces -= 1
    return tot

def make_bet():
    """If the player chooses to play a hand, new balance is calculated"""
    global totalChipsHand, chipsHand, chipsBalance
    if chipsBalance == 0:
        print "Available balance cannot be zero. Reinitialising balance to 100"
        chipsBalance = CHIPS_INITIAL
    else:
        print "-->Chip Balance: %d<--" % (chipsBalance)
    while True:
        try:
            chipsHand = input("How many chips would player like to use from"
            " %d:" % (chipsBalance)) 
            if isinstance(chipsHand,int):                
                if chipsHand <= chipsBalance and chipsHand > 0:
                    chipsBalance -= chipsHand
                    break
                else:
                    print ("Cannot pick an amount > available balance of %d " 
                    "or <= 0" % (chipsBalance))
            else:
                print ("Error: Input restricted to integer values only. " 
                "Try again.")
        except:
            print ("Error: Input restricted to integer values only. " 
            "Try again.")
    totalChipsHand += chipsHand

# Initialise the constants
BLACK_JACK = 21
CHIPS_INITIAL = 100
FORCE_STAND = 17
BLACK_JACK_MULTIPLIER = 1.5
DEFAULT_VALUE = 0

# Assume only a single deck of cards to choose from
suit = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
deck = 4 * suit

dWin = 0 # dealer win counter
pWin = 0 # player win counter
chipsBalance = CHIPS_INITIAL

while True:
    playerBusted = False
    dealerBusted = False 
    totalDealer = DEFAULT_VALUE
    totalPlayer = DEFAULT_VALUE
    totalChipsHand = DEFAULT_VALUE
    chipsHand = DEFAULT_VALUE + 1
    player = []
    print "-------------------------------------------------------------------"
    make_bet()
    #Card 1
    pickedCard = rc(deck)
    deck.remove(pickedCard)
    player.append(pickedCard)
    #Card 2 
    pickedCard = rc(deck)
    deck.remove(pickedCard)
    player.append(pickedCard)
    
    totalPlayer = total(player)

    if totalPlayer == BLACK_JACK:
        print "Player has a Black Jack, wins automatically!"
        print "Player's cards are %s" % (player)
        chipsBalance += BLACK_JACK_MULTIPLIER * totalChipsHand
        pWin += 1
    else:
        while True:
            # loop for the player's play ...
            totalPlayer = total(player)
            print "Player's cards: %s, Total value: %d" % (player, totalPlayer)
            if totalPlayer > BLACK_JACK:
                print "-->The Player is busted!<--"
                playerBusted = True
                break
            elif totalPlayer == BLACK_JACK:
                print "-->Player has got a Black Jack!<--"
                break
            else:
                hs = raw_input("Hit('h') or Stand('Enter'): ").lower()
                if 'h' in hs:
                    pickedCard = rc(deck)
                    deck.remove(pickedCard)
                    player.append(pickedCard)
                    make_bet()
                else:
                    break                
        if playerBusted == True:
            print "-->The dealer wins automatically!<--"
            dWin += 1
        else:
            while True:
                # loop for the dealer play ...
                dealer = []
                # draw 2 cards for the Dealer to start:
                #Card 1
                pickedCard = rc(deck)
                deck.remove(pickedCard)
                dealer.append(pickedCard)
                #Card 2 
                pickedCard = rc(deck)
                deck.remove(pickedCard)
                dealer.append(pickedCard)
                
                totalDealer = total(dealer)
                print "Dealer's inital pick of cards is %s " % (dealer)
                
                while True:
                    if totalDealer < FORCE_STAND: # Dealer Hits when < 17
                        print "Dealer picks another card from the deck"
                        pickedCard = rc(deck)
                        deck.remove(pickedCard)
                        dealer.append(pickedCard)
                        totalDealer = total(dealer)
                        print "The dealer has %s, Total value: %d" \
                        % (dealer, totalDealer)
                    else:
                        break
                print "Dealer's final pick: %s, Total value: %d" \
                % (dealer, totalDealer)
                print "Player's final pick: %s, Total value: %d" \
                % (player, totalPlayer)
                if totalDealer > BLACK_JACK:
                    print "--> The dealer is busted!<--"
                    dealerBusted = True
                    break
                elif totalDealer == BLACK_JACK:
                    print "-->Dealer has a Black Jack!!<--"
                    break
                elif totalDealer >= FORCE_STAND:
                    break
                
            # Figure out the final result
            if playerBusted == True and dealerBusted == True:
                print "-->Both Player & Dealer BUSTED! No winners!<--"
            elif playerBusted == True and dealerBusted == False:
                print "-->The dealer wins!<--"
                dWin += 1
            elif playerBusted == False and dealerBusted == True:
                if totalPlayer == BLACK_JACK:
                    print "-->Player wins with a Black Jack<--"
                    chipsBalance += BLACK_JACK_MULTIPLIER * totalChipsHand
                else:
                    print "-->The player wins!<--"
                    chipsBalance += totalChipsHand
                pWin += 1
            else:
                if totalDealer > totalPlayer:
                    print "-->The dealer wins!<--"
                    dWin += 1
                elif totalDealer == totalPlayer:
                    print "-->It's a draw!<--"
                    chipsBalance += totalChipsHand
                else: 
                    if totalPlayer > totalDealer:
                        if totalPlayer == BLACK_JACK:
                            print "-->Player wins with a Black Jack<--"
                            chipsBalance += BLACK_JACK_MULTIPLIER * totalChipsHand
                        else:
                            print "-->The player wins!<--"
                            chipsBalance += totalChipsHand
                    pWin += 1
            
    print "Wins, Player = %d \t Dealer = %d" % (pWin, dWin)
    print "-->Available Chip Balance: %d<--" % (chipsBalance) 
    status = raw_input("Press Enter or 'q' to Quit: ").lower()
    if 'q' in status:
        break
print "\n------------End of Black Jack---------------"
