#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 21:05:49 2020

@author: thomasmusieracki
"""
import random

money = 100

#Making a Game of Chance
#flipping_coin function ist supossed to simulate a flipping coin action
def flipping_coin(Bet, Player_call):
    coin_value = ""
    if Bet <= money:
        if Player_call != "Heads" and Player_call != "Tails":
            print("Please return call Heads or Tails")
            return 0
        else:
            print("You are playing flipping_coin 8)")
            num = random.randint(1, 2)
            print("You choosed " + Player_call)
            print("Coin Flipped")
        if num == 1:
         coin_value += "Heads"
        else:
         coin_value += "Tails"
        print(coin_value)
        if Player_call == coin_value:
            print("You won!" + "Your Bet has dobled!")
            return Bet
        else:
            print("You lose!" + "Your Bet was discounted!")
            lost_bet = -(Bet)
            return lost_bet
            return "Won"
    else:
        print("You dont have enough money to play flipping_coin")
        return 0

money += flipping_coin(10, "Heads")
print("Your money is: " + str(money))
    
#Cho-Han function
def Cho_Han(Bet, Player_call):
    if Bet <= money:
        if Player_call != "Even" and Player_call != "Odd":
            print("Please return Even or Odd.")
            return 0
        else:
            print("You are playing Cho-Han 8)")
            print("You choosed: " + Player_call)
            num = random.randint(1, 6)
            print("First Dice: " + str(num))
            num2 = random.randint(1, 6)
            print("Second Dice: " + str(num2))
            print("The Sum is: " + str(num + num2))
            Result = ""
        if (num + num2)%2 == 0:
            print("Even")
            Result += "Even"
        else:
            print("Odd")
            Result += "Odd"
        if Player_call == Result:
            print("You won!" + "Your Bet has dobled")
            return Bet
        else:
            print("You Lose! Your Bet was discounted!")
            lost_bet = -(Bet)
            return lost_bet
    else:
        print("You dont have enough money to play Cho-Han")
        return 0
money += Cho_Han(29,"Even")
print("Your money is: " + str(money))


# 2 Players Picking a Card

def High_Card(Bet):
    Random_Card = random.randint(1, 13)
    Random_Card2 = random.randint(1, 13)
    if Random_Card > Random_Card2:
        print(Random_Card)
        print(Random_Card2)
        print("You Won!")
    elif Random_Card == Random_Card2:
        print("Its a tie")
    else:
        print(Random_Card)
        print(Random_Card2)
        print("You lose!")
        
# 2 Players Picking a Card aprimorate

def High_Card2(Bet):
    if Bet <= money:
        print("You are playing High_Card 8)")
        Cards = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13]
        Random_Card = random.choice(Cards)
        print("You picked a card! " + str(Random_Card))
        del Cards[Random_Card]
        Random_Card2 = random.choice(Cards)
        print("Player 2 picked a card! " + str(Random_Card2))
        if Random_Card > Random_Card2:
            print("You won!")
            return Bet
        elif Random_Card == Random_Card2:
            print("Its a Tie")
            return Bet
        else:
            print("You lose!")
            lost_bet =-(Bet)
            return lost_bet
    else:
        print("You dont have enough money to play High-Card")
        return 0
money += High_Card2(30)
print("Your money is :" + str(money))
        
#Roulette game
def Roullete_game(Bet, call):
    all_calls = [i for i in range(37)] + ["Even", "Odd"]
    if Bet <= money:
        if call not in all_calls:
            print("Please choose a valid call")
            return 0
        else:
            roullete_list = [00] + list(range(0, 37))
            print(list(roullete_list))
            num = random.randint(1, len(roullete_list))
            num2 = ""
            print(num)
            if num%2 == 0:
                print("Even")
                num2 += "Even"
            else:
                print("Odd")
                num2 += "Odd"
            if call == num:
                print("You Won!")
                return Bet
            elif call == "Even" and num%2 == 0:
                print("You Won!")
                return Bet
            elif call == "Odd" and num%2 == 1:
                print("You Won!")
                return Bet
            else:
                print("You Lose!")
                return -(Bet)
    else:
        print("You dont have enough money")
        return 0
money += Roullete_game(20,0)
print("Your money is: " + str(money))
        
