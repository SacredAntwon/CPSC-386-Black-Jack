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


"""This module is a meant to be the card file to create a deck of cards
that will be used in our blackjack game."""

from collections import namedtuple
from random import shuffle, randrange
from math import floor

Card = namedtuple("Card", ["rank", "suit"])


def stringify_card(card):
    """This module is a meant to turn our cards into a string
    to be read."""
    return "{} of {}".format(card.rank, card.suit)


Card.__str__ = stringify_card


class Deck:
    """This module is a meant to be our Deck class which has
    has functions to create the deck."""

    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "Jack Queen King".split()
    suits = "Clubs Hearts Spades Diamonds".split()

    def __init__(self):
        self._cards = [
            Card(rank, suit) for suit in self.suits for rank in self.ranks
        ]

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)

    def insert(self, cutCard):
        """This module is used to insert a cut card into the deck
        to be found later."""
        self._cards.insert(cutCard, "CutCard")

    def shuffle(self, number=1):
        """This module will be called to shuffle the deck."""
        for _ in range(number):
            shuffle(self._cards)

    def cut(self):
        """This module will be called to cut the deck."""
        p = floor(len(self._cards) * 0.2)
        half = (len(self._cards) // 2) + randrange(-p, p)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def deal(self, n=1):
        """This module will deal the card by taking from the deck
        and return the value to be added lader to the player."""
        return [self._cards.pop(0) for _ in range(n)]

    def merge(self, other_deck):
        """This module will combine multiple decks of card into
        one single deck."""
        self._cards = self._cards + other_deck._cards

    def __str__(self):
        return "\n".join(map(str, self._cards))
