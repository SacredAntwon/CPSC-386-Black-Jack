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

"""This module is a meant to be the game file to run our
    the rules for our game."""

from .cards import Deck
from .player import Player, Dealer
from time import sleep
from random import randrange
import pickle


class BlackJackGame:
    def __init__(self):
        self._deck = Deck()
        for i in range(3):
            self._deck.merge(self._deck)
        self._game_is_not_over = True
        self.timeToShuffle = False

    def createDeck(self):
        """This module is a meant to shuffle, cut and
        insert a cut card in the deck."""
        self._deck.shuffle(10)
        self._deck.cut()
        cutCard = randrange(335, 355)
        self._deck.insert(cutCard)

    def to_file(self, pickle_file, players):
        """Write the list players to the file pickle_file."""
        pickle_file = "players.pckl"
        with open(pickle_file, "wb") as file_handle:
            pickle.dump(players, file_handle, pickle.HIGHEST_PROTOCOL)

    def from_file(self, pickle_file):
        """Read the contents of pickle_file"""
        try:
            with open(pickle_file, "rb") as file_handle:
                players = pickle.load(file_handle)
            return players
        except EOFError:
            return list()

    def valueCard(self, currentCard):
        """This module is a meant to get a int value
        from the rank of the card."""
        if currentCard == "Ace" or "King" or "Queen" or "Jack":
            return {"Ace": 11, "King": 10, "Queen": 10, "Jack": 10}.get(
                currentCard, currentCard
            )

    def hit(self, cp, current_player_index):
        """This module is a meant to give the player a card
        to be read."""
        currentCard = self._deck.deal()
        cutCheck = self.checkCutCard(currentCard[0])
        if cutCheck is False:
            cp._cards.append(currentCard[0])
            if current_player_index == (self.num_players):
                print("The Dealer Got: ", currentCard[0])
            else:
                print("Player {} Got: ".format(cp._name), currentCard[0])
            sleep(1)
            current_player_index = (current_player_index + 1) % len(
                self._players
            )
        else:
            print("CUT CARD REACHED. SHUFFLE WILL HAPPEN AFTER THE GAME")
            self.hit(cp, current_player_index)

    def splithit(self, cp, current_player_index):
        """This module is a meant to give the player a card
        to be read for a split hand."""
        currentCard = self._deck.deal()
        cutCheck = self.checkCutCard(currentCard[0])
        if cutCheck is False:
            cp._splitdeck.append(currentCard[0])
            print("Player {} Got: ".format(cp._name), currentCard[0])
            sleep(1)
        else:
            print("CUT CARD REACHED. SHUFFLE WILL HAPPEN AFTER THE GAME")
            self.hit(cp, current_player_index)

    def checkCutCard(self, currentCard):
        """This module is a meant to check if there is a cut
        card in the current hand."""
        if currentCard == "CutCard":
            self.timeToShuffle = True
            return True
        else:
            return False

    def sumOfCards(self, cp):
        """This module is a meant to find the sum of a players
        set of cards."""
        sum = 0
        numberOfAces = 0
        for i in cp._cards:
            card_val = self.valueCard(i.rank)
            sum += int(card_val)
            if int(card_val) == 11:
                numberOfAces += 1
        while sum > 21:
            if numberOfAces >= 1:
                sum -= 10
                numberOfAces -= 1
            else:
                break
        return sum

    def sumOfSplitCards(self, cp):
        """This module is a meant to find the sum of a players
        set of cards on a split hand."""
        sum = 0
        numberOfAces = 0
        for i in cp._splitdeck:
            card_val = self.valueCard(i.rank)
            sum += int(card_val)
            if int(card_val) == 11:
                numberOfAces += 1
        while sum > 21:
            if numberOfAces >= 1:
                sum -= 10
                numberOfAces -= 1
            else:
                break
        return sum

    def initialHandout(self, current_player_index, count):
        """This module is a meant give players and the dealer
        each a card in order."""
        print("\n")
        while len(self._players[self.num_players]._cards) != 2:
            cp = self._players[current_player_index]
            currentCard = self._deck.deal()
            cutCheck = self.checkCutCard(currentCard[0])
            if cutCheck is False:
                cp._cards.append(currentCard[0])
                if current_player_index == (self.num_players):
                    if count == 0:
                        print("The Dealer Got: ", currentCard[0])
                        print("\n")
                        count += 1
                        sleep(1)
                    else:
                        print("The Dealer Hides The Second Card\n")
                else:
                    print("Player {} Got: ".format(cp._name), currentCard[0])
                    sleep(1)
                current_player_index = (current_player_index + 1) % len(
                    self._players
                )
            else:
                print("CUT CARD REACHED. SHUFFLE WILL HAPPEN AFTER THE GAME")
                self.initialHandout(current_player_index, count)

        sleep(1)

    # THIS IS FOR THE WAGER
    def getWager(self):
        """This module is a meant to get the amount
        a player wants to bet."""
        for i in self._players:
            sleep(1)
            if i._name != "Skynet":
                print("\nPlayer: ", i._name)
                if i._balance == 0:
                    print(
                        "Your balance is 0. Another $10,000 will be"
                        " added to your balance."
                    )
                    i._balance = 10000
                print("Current Balance: ", i._balance)
                wager = int(input("How much would you like to wager? "))
                while wager > i._balance or wager < 1:
                    print("Invalid Wager")
                    wager = int(input("How much would you like to wager? "))
                i._wager = wager
                i._balance -= wager
                print("NEW BALANCE: ", i._balance)

    def resetCards(self):
        """This module is a meant to reset the players
        set of cards."""
        for i in self._players:
            i._cards = []

    def insurance(self, cp):
        """This module is a meant to check if a player
        wants insurance."""
        print("\nPlayer: ", cp._name)
        insuranceInput = input(
            "Would you like " "insurance? ('y' for yes, 'n' for no): "
        )

        if insuranceInput == "y":
            if cp._balance == 0:
                print("NOT ENOUGH TO COVER INSURANCE")
            else:
                insuranceWager = int(
                    input(
                        "Enter the amount you would like to wager for insurance: "
                    )
                )

                while insuranceWager > cp._balance:
                    print(
                        "The wager you inputed is more than your"
                        " balance could cover. Try Again!"
                    )
                    insuranceWager = int(
                        input(
                            "Enter the amount you"
                            " would like to wager for insurance: "
                        )
                    )

                cp._balance -= insuranceWager
                cp._insuranceWager = insuranceWager

    def run(self):
        """This module is our main run loop that will call
        our functions and follow the rules."""
        self.num_players = int(input("How many players? [1-4] "))
        while self.num_players > 4 or self.num_players < 1:
            print("Invalid Amount of Players. Try Again!")
            self.num_players = int(input("How many players? [1-4] "))
        self._players = []

        for i in range(self.num_players):
            name = input("What is your name: ")
            cards = []
            self._players.append(Player(name, cards))
        cards = []
        self._players.append(Dealer(cards))
        self.player_list = self.from_file("players.pckl")
        for i in self.player_list:
            for k in self._players:
                if i._name != "Skynet":
                    if i._name == k._name:
                        k._balance = i._balance

        self.getWager()
        self.createDeck()
        self.initialHandout(0, 0)

        current_player_index = 0

        dealer_end = True
        while self._game_is_not_over:
            current_player_index = 0

            # INSURANCE
            dealer = self._players[self.num_players]
            dealerFirst = self.valueCard(dealer._cards[0].rank)
            if dealerFirst == 10 or dealerFirst == 11:
                print("INSURANCE")
                for i in self._players:
                    if i._name != "Skynet":
                        self.insurance(i)

            # LOOP TO DEAL CARDS TO PLAYERS
            while dealer_end:
                sleep(1)
                cp = self._players[current_player_index]
                print("\nIt is {}'s turn".format(cp._name))
                total = self.sumOfCards(cp)
                print("CURRENT TOTAL", total)
                if total != 21:
                    if int(self.valueCard(cp._cards[0].rank)) == int(
                        self.valueCard(cp._cards[1].rank)
                    ):
                        splitOption = input(
                            "Would you like to split"
                            " ('y' for yes, 'n' for no): "
                        )
                        if splitOption == "y":
                            if cp._balance >= cp._wager:
                                cp._balance -= cp._wager
                                cp._splitdeck.append(cp._cards.pop(1))
                                cp._splitwager = cp._wager
                                cp._alreadySplit = True
                                print("Dealing card to first hand")
                                self.hit(cp, current_player_index)
                                print("Dealing card to second hand")
                                self.splithit(cp, current_player_index)

                                print("FIRST HAND")
                                total = self.sumOfCards(cp)
                                print("TOTAL", total)
                            else:
                                print("NOT ENOUGH TO SPLIT")

                    player_response = input(
                        "Would you like to hit, stand or "
                        "double down? ('h' for hit, 's' for stand, "
                        "'d' for double down): "
                    )
                    # THIS IS THE DOUBLE DOWN
                    if player_response == "d" and cp._balance >= cp._wager:
                        cp._balance -= cp._wager
                        cp._wager = cp._wager * 2
                        print("NEW WAGER: ", cp._wager)
                        self.hit(cp, current_player_index)
                        total = self.sumOfCards(cp)
                        print("TOTAL", total)
                        if total > 21:
                            cp._bust = True
                            print("BUST, NEXT PLAYER")

                    elif player_response == "d" and cp._balance < cp._wager:
                        print("NOT ENOUGH TO DOUBLE DOWN")
                        player_response = input(
                            "Would you like to hit or stand"
                            "? ('h' for hit, 's' for stand): "
                        )

                    # THIS IS THE HIT
                    while player_response == "h":
                        self.hit(cp, current_player_index)
                        total = self.sumOfCards(cp)
                        print("TOTAL", total)
                        if total > 21:
                            cp._bust = True
                            print("BUST, NEXT PLAYER")
                            break

                        player_response = input(
                            "Would you like to hit again? "
                            "('h' for hit, 's' for stand): "
                        )

                    cp._total = total
                    # THIS WILL RUN IF A PLAYER SPLITS
                    if cp._alreadySplit is True:
                        print("SECOND HAND")
                        total = self.sumOfSplitCards(cp)
                        print("TOTAL", total)
                        player_response = input(
                            "Would you like to hit, stand "
                            "or double down? ('h' for hit, 's' for stand, "
                            "'d' for double down): "
                        )
                        # THIS IS THE DOUBLE DOWN
                        if (
                            player_response == "d"
                            and cp._balance >= cp._splitwager
                        ):
                            cp._balance -= cp._splitwager
                            cp._splitwager = cp._splitwager * 2
                            print("NEW WAGER: ", cp._splitwager)
                            self.splithit(cp, current_player_index)
                            total = self.sumOfSplitCards(cp)
                            print("TOTAL", total)
                            if total > 21:
                                cp._splitbust = True
                                print("BUST, NEXT PLAYER")

                        elif (
                            player_response == "d"
                            and cp._balance < cp._insuranceWager
                        ):
                            print("NOT ENOUGH TO DOUBLE DOWN")
                            player_response = input(
                                "Would you like to hit or "
                                "stand? ('h' for hit, 's' for stand): "
                            )

                        # THIS IS THE HIT
                        while player_response == "h":
                            self.splithit(cp, current_player_index)
                            total = self.sumOfSplitCards(cp)
                            print("TOTAL", total)
                            if total > 21:
                                cp._bust = True
                                print("BUST, NEXT PLAYER")
                                break

                            player_response = input(
                                "Would you like to hit "
                                "again? ('h' for hit, 's' for stand): "
                            )
                        cp._splittotal = total

                else:
                    print("PLAYER GOT A BLACKJACK")
                    cp._blackjack = True
                    cp._total = total
                current_player_index = (current_player_index + 1) % len(
                    self._players
                )
                if current_player_index == len(self._players) - 1:
                    print("\nDealers turn")
                    break

            # THE DEALERS TURN TO SHOW CARD AND CHECK IF THEY NEED TO HIT
            sleep(1)
            print("Dealer Reveals: ", self._players[self.num_players]._cards[1])
            total = self.sumOfCards(self._players[self.num_players])
            print("TOTAL", total)

            # CHECK IF ALL PLAYERS BUSTED
            countBust = 0
            for i in self._players:
                if i._name != "Skynet":
                    if i._bust is True:
                        countBust += 1

            if total != 21:
                if countBust != self.num_players:
                    while total < 17:
                        self.hit(
                            self._players[self.num_players], self.num_players
                        )
                        total = self.sumOfCards(self._players[self.num_players])
                        print("TOTAL", total)
                        if total > 21:
                            self._players[self.num_players]._bust = True
                            print("DEALER BUSTS")
                            break
            else:
                print("DEALER GOT A BLACKJACK")
                self._players[self.num_players]._blackjack = True
            self._players[self.num_players]._total = total

            # PRINTS THE WINNERS AND LOSERS, THEN RESETS VALUES
            for i in self._players:
                sleep(1)
                if i._name != "Skynet":
                    print("\nPlayer {}".format(i._name))
                    if i._bust is True:
                        print("Busted and Lost")
                    elif (
                        self._players[self.num_players]._total > i._total
                        and self._players[self.num_players]._bust is False
                    ):
                        print("Lost")
                    elif self._players[self.num_players]._total == i._total:
                        print("Push")
                        i._balance += i._wager
                    else:
                        print("Won")
                        i._balance += 2 * i._wager

                    if i._alreadySplit is True:
                        print("SPLIT CARDS")
                        if i._splitbust is True:
                            print("Busted and Lost")
                        elif (
                            self._players[self.num_players]._total
                            > i._splittotal
                            and self._players[self.num_players]._bust is False
                        ):
                            print("Lost")
                        elif (
                            self._players[self.num_players]._total
                            is i._splittotal
                        ):
                            print("Push")
                            i._balance += i._splitwager
                        else:
                            print("Won")
                            i._balance += 2 * i._splitwager

                    if self._players[self.num_players]._blackjack is True:
                        if i._insuranceWager > 0:
                            print("You Won Insurance Wager")
                            i._balance += 2 * i._insuranceWager
                    else:
                        if i._insuranceWager > 0:
                            print("You Lost Insurance Wager")

                    print("NEW BALANCE: ", i._balance)

                i._bust = False
                i._total = 0
                i._wager = 0
                i._blackjack = False
                i._insuranceWager = 0
                i._splitdeck = []
                i._alreadySplit = False
                i._splitbust = False
                i._splitwager = 0
                i._splittotal = 0

            sleep(2)
            # ASK PLAYERS IF THEY WANT TO PLAY AGAIN
            playAgain = input(
                "\nWould all of you like to play again? "
                "('y' for yes, 'n' for no): "
            )
            if playAgain != "y":
                print("\nThank you for playing!")
                update_player_list = self._players
                list_of_name = []
                for k in self._players:
                    list_of_name.append(k._name)
                for i in self.player_list:
                    if i._name not in list_of_name:
                        update_player_list.append(i)
                self.to_file("players.pckl", update_player_list)
                print("Saved Player Data")
                self._game_is_not_over = False
                break
            sleep(2)

            print("\n\nNEW GAME\n\n")
            if self.timeToShuffle is True:
                self._deck = Deck()
                for i in range(3):
                    self._deck.merge(self._deck)
                self.createDeck()
                print("CREATED A NEW SHUFFLED DECK\n")
                self.timeToShuffle = False

            self.resetCards()
            self.getWager()
            self.initialHandout(0, 0)
