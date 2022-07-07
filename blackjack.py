#!/usr/bin/env python3
# Anthony Maida
# CPSC 386-04
# 2022-03-31
# amaida@csu.fullerton.edu
# @SacredAntwon
#
# Lab 00-03
#
# This is a blackjack game that has many rules to follow in order to make
# everything flow. Goal is to get as close to 21 without going over.
#


"""This module is a meant to be the main file to run our
    blackjack game."""

from time import sleep
from blackjackgame import game


if __name__ == "__main__":
    DELAY = 0.5
    print("Welcome to Blackjack!")
    sleep(DELAY)
    print("Goal is to get to 21 or close without going over.")
    sleep(DELAY)
    print(
        "There will be splitting and insurance"
        " offered to players if suitable."
    )
    sleep(DELAY)
    print("There will be hitting, standing and double down.")
    sleep(DELAY)
    print(
        "The double down and splitting will make"
        " sure your balance covers it before going through."
    )
    sleep(DELAY)
    print(
        "Once a players balance reaches 0, the next game cycle will"
        " give the player another $10,000 to play with."
    )
    sleep(DELAY)
    print("Dealer will keep hitting till it reaches at least 17.")
    sleep(DELAY)
    print("If all players bust, the dealer could stand on the first two cards.")
    sleep(DELAY)
    print(
        "The players information will save once a prompt asks users"
        " to continue the game and you respond with 'n'."
    )
    sleep(DELAY)
    input("Press ENTER to continue.\n")

    GAME = game.BlackJackGame()
    GAME.run()
