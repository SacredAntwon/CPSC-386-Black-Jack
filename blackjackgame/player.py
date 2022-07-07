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


"""This module is a meant to be the plaher file to hold our
player information."""

from .cards import Deck


class Player:
    """This module is a meant to hold our player information."""

    def __init__(self, name, cards):
        self._name = name
        self._cards = cards
        self._balance = 10000
        self._bust = False
        self._total = 0
        self._wager = 0
        self._insuranceWager = 0
        self._blackjack = False
        self._splitdeck = []
        self._alreadySplit = False
        self._splitbust = False
        self._splitwager = 0
        self._splittotal = 0


class Dealer:
    """This module is a meant to hold our dealer information."""

    def __init__(self, cards):
        self._name = "Skynet"
        self._cards = cards
        self._bust = False
        self._total = 0
        self._blackjack = False
