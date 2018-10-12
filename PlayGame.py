# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 13:37:11 2018

"""

from random import randint

listDeck=[]
######################################################################
# Construct the representation of a given card using special unicode
# characters for hearts, diamonds, clubs, and spades.
def displayCard(c):
    suits = {'spades':'\u2660', 'hearts':'\u2661', 'diamonds':'\u2662', 'clubs':'\u2663'}
    return(''.join( [ str(c[0]), suits[c[1]] ] ))


    
#simpleShuffle(D) takes a deck, D, and modifies it to scramble the
# order of the cards.This is the Fisher-Yates-Knuth algorithm.
#
# simpleShuffle(D) takes as input list of elements. It should step
# through the list, at each point exchanging the current element with
# an element chosen at random from the remainder of the list
# (including the present element). In other words, if we are
# considering the 3rd element of a 10 element list (0-indexed as
# usual), we select an index between 3 and 9, inclusive, and exchange
# list[3] with list[0] before advancing to the 4th element of the list
# and repeating the process.
#
# simpleShuffle(D) should return the permuted deck.
def simpleShuffle(D):
    result = []
    while D:
        p = randint(0, len(D)-1)
        result.append(D[p])
        D.pop(p)
    return result


######################################################################
# createDeck() produces a new, cannonically ordered, |S|*N card
# deck. A deck is implemented as a list of cards: each card is a
# tuple, (v, s), where 0 < v < N is the value of the card and s is the
# suit of the card. So, for example:
#
# >>> createDeck(1)
# [(1, 'spades'), (1, 'hearts'), (1, 'clubs'), (1, 'diamonds')]
# >>> createDeck(2)
# [(1, 'spades'), (2, 'spades'), (1, 'hearts'), (2, 'hearts'), (1, 'clubs'), (2, 'clubs'), (1, 'diamonds'), (2, 'diamonds')]
# >>> createDeck()
# [(1, 'spades'), (2, 'spades'), (3, 'spades'), ... (12, 'diamonds'), (13, 'diamonds')]
#
# where the second example above has been edited for clarity. Note
# that the default, N=13, is to produce a standard 52 card deck having
# the standard four suits specified in the function signature.
def createDeck(N=13, S=('spades', 'hearts', 'clubs', 'diamonds')):
    for j in S:
        for i in range(1,N+1):
            listDeck.append((i,j))
    return listDeck


######################################################################
# A game is represented as a dictionary with keys:
#   stacks = list of player stacks, where each stack is a list of cards
#   table = list of cards currently on table (initially [])
#   next = index of player next to play (0 or 1, initially 0)
#   debt = penalty cards owed by next player (initially 0)
#
# newGame() should first create a new shuffled deck using createDeck()
# and simpleShuffle().  It should then return a dictionary describing
# the initial state of the current game, where the shuffled deck has
# been evenly divided amongst the players. So, for example (linefeed
# added for clarity):
#
# >>> newGame(2, S=('spades, 'hearts'))
# { 'table':[], 'next':0, 'debt':0,
#   'stacks':[[(2, 'spades'), (1, 'hearts')], [(2, 'hearts'), (1, 'spades')]]}
#
# Note the division of the shuffled deck into two equal stacks, one
# for player 0 and one for player 1.
def newGame(N=13, S=('spades', 'hearts', 'clubs', 'diamonds')):
    dict={}
    stacks=[]
    D=createDeck(N,S)
    listShu=simpleShuffle(D)
    stack1=listShu[0:][::2]
    stack2=listShu[1:][::2]
    stacks.append(stack1)
    stacks.append(stack2)
    dict['table']=[]
    dict['next']=0
    dict['debt']=0
    dict['stacks']=stacks
    return dict


def penalty_value_of(card):
    values = {"11":1,"12":2,"13":3,"1":4}
    return values[card]

######################################################################
# describeGame(G) takes a game description G (a dictionary of the type
# produced by newGame()) and returns a string that, when printed,
# describes the state of the game. 
#
# >>> G = newGame(2, S=('spades, 'hearts'))
# >>> describeGame(G)
# 'Player:0 Stacks:[2, 2] Table:0 Debt:0'
#
# The string or description returned is quite terse; it will still be
# useful in helping you debug how the game is progressing. It tells
# you who the next player to play is, what the sizes of the individual
# player stacks are, the number of cards on the table, and any debt
# that is due from the next player to play.
def describeGame(G):
    stack=[]
    player=G['next']
    for i in G['stacks'][player]:
        stack.append(i[0])
    table=len(G['table'])
    debt=G['debt']
    return ("Player:{} Stacks:{} Table:{} Debt:{}".format(player,stack,table,debt))

######################################################################
# current(G) should take a game description G (a dictionary of the
# type produced by newGame()) and return the index of the player who
# is currently playing (indicated by the G['next'] value).
def current(G):
    return G['next']

# opponent(G) should take a game description G (a dictionary of the
# type produced by newGame()) and return the index of the player who
# is not currently playing 
def opponent(G):
    describeGame(G)
    player=G['next']
    if player==0:
        return 1
    else:
        return 0

# advancePlayer(G) should take a game description G (a dictionary of the
# type produced by newGame()) and modify G so as to "flip" the next
# player field. So if the next player was player 0, it should now
# become player 1 and vice versa (hint: make use of the opponent(G)
# function just implemented).
def advancePlayer(G):
    next=opponent(G)
    G['next']=next
    return G
    

def play(G=newGame()):
    # Use turn to keep track of number of rounds played.
    turn = 0
    #Calculate the number of cards in each player's hand
    a=len(G['stacks'][0])
    b=len(G['stacks'][1])
    
    # Continue iterating until next player to move has an empty stack(
    #No cards in hand).
    while a>0 and b>0: 
        ## Show the state of play.
        print("Turn {}: {}".format(turn, describeGame(G)))
        
        #Who is the next player?
        next=G['next']
        
        # Make a move. First, check to see if a debt is due. If so,
        # pay it.
        
        #Current player debt
        if G['debt']!=0:
            #How much is the debt?
            debt=G['debt']
            
            #Pay off debt
            for i in range(1,debt+1):
                
                #Determine the number of cards in the current player's hand
                l=len(G['stacks'][next])
                if l!=0:
                    #If there is a card in hand, pay one
                    card=G['stacks'][next][0][0]
                    print("Turn {}: Player {} is paying a debt.".format(turn, current(G)))
                    
                    #Put the card that the player paid on the table
                    G['table'].append(G['stacks'][next][0])
                    
                    #Remove the paid card from the stack
                    G['stacks'][next]=G['stacks'][next][1:]
                    
                    #Recalculate the number of cards in each player's hand
                    a=len(G['stacks'][0])
                    b=len(G['stacks'][1])
                    
                    #Determine if the card is J, Q, K, A
                    if card in [11,12,13,1]:
                        #Calculate debt based on J, Q, K, A
                        card_1=str(card)
                        G['debt']=penalty_value_of(card_1)
                        
                        #Advance to next player.
                        advancePlayer(G)
                        break
                else:#No cards in hand
                    #Recalculate the number of cards in each player's hand
                    a=len(G['stacks'][0])
                    b=len(G['stacks'][1])
                    break
            #Cycle completed(Debt pay off)
            
            G['debt']=0
            #Advance to next player.And give the card on the table to another player.
            if(next==0):
                G['next']=1
                G['stacks'][1]=G['stacks'][1]+G['table']
            else:
                G['next']=0
                G['stacks'][0]=G['stacks'][0]+G['table']
            #At this time, the number of cards on the table is 0.
            G['table']=[]
        else:#No debt
            #No debt, take out a card
            card_num=G['stacks'][next][0][0]
            
            #Describe the card
            card_num_flower=list(G['stacks'][next][0])
            print("Turn {}: Player {} is using {}".format(turn, current(G),displayCard(card_num_flower)))
            
            #Put the cards that are taken out on the table
            G['table'].append(G['stacks'][next][0])
            #Remove the paid card from the stack
            G['stacks'][next]=G['stacks'][next][1:]
            
            a=len(G['stacks'][0])
            b=len(G['stacks'][1])

            if card_num in [11,12,13,1]:
                card_1=str(card_num)
                G['debt']=penalty_value_of(card_1)
                advancePlayer(G)
            else:
                advancePlayer(G)
        turn = turn + 1
    ##Advance to next player.
    G=advancePlayer(G)
    print("Player {} wins in {} turns.".format(opponent(G), turn))
    return(G)
    
def main():
    play()
    
if __name__ == "__main__":
    main()


