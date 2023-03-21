from classes import Player, Board, Kit, Bot
from functions import int_input, count_points, make_words, clear
import time
from random import choice


class Game:
    def __init__(self):
        self.players = []
        self.kit1 = Kit()
        self.board1 = Board()
        self.correct_words = make_words("slowa.txt", self.kit1.dic)
        self.amount_of_rounds = 0
        self.index = 0
        self.amount_of_pl = 0

    def allocation_of_letters(self):
        """ funkcja na rozpoczęciu gry rozdaje każdemu
        zawodnikowi po 7 liter"""
        for player in self.players:
            self.kit1.add_letters(7, player.letters)

    def who_starts(self):
        """ funkcja sprwadzająca kto zaczyna według
        zasady podaanej na stronie pfs (gracz który
        wylosuje litere najbliższą początkowi alfabetu zaczyna"""
        print("\nLosowanie kto zaczyna:\n")
        scores = []
        for player in self.players:
            letter = choice(self.kit1.bag)
            player_score = self.kit1.bag.index(letter)
            scores.append(player_score)
            print(f"{player.name}: {letter}\n")
        mini = min(scores)
        if scores.count(mini) > 1:
            print("\nNie da się wyłonić zwycięzcy\n")
            return self.who_starts()
        else:
            result = scores.index(mini)
            print(f"\nZaczyna {self.players[result].name}")
            return result

    def set_game(self):
        print("Wybierz ilość graczy (2 - 4) a następnie podaj ich nazwy")
        self.amount_of_pl = int_input(2, 4)
        print("Aby sterował komputer nazwa musi zawierać ciąg znaków: 'bot'")
        for i in range(self.amount_of_pl):
            name = input(f"Podaj nazwę gracza nr {i+1}: ")
            x = ""
            if len(name) >= 3:
                x = name[:3]
            if "bot" == x.lower():
                player = Bot(name)
            else:
                player = Player(name)
            self.players.append(player)
        self.players = self.players[:self.amount_of_pl]
        self.index = self.who_starts()
        self.allocation_of_letters()
        time.sleep(10)

    def run_game(self):
        while True:
            if self.end_conditions():
                break
            print(f"Ruch gracza {self.players[self.index].name}: ")
            print(f"Punkty gracza: {self.players[self.index].points}")
            print(f"Litery gracza: {self.players[self.index].show_letters(self.kit1)}")
            self.players[self.index].show_words()
            self.board1.print()
            if len(self.board1.words_on_board) != 0:
                self.players[self.index].move(self.board1, self.kit1, self.correct_words)
            else:
                self.players[self.index].first_move(self.board1, self.kit1, self.correct_words)
            time.sleep(10)
            clear()
            self.index += 1
            self.index = self.index % self.amount_of_pl
        self.end()

    def end_conditions(self):
        """warunke skoczenia gry 1"""
        if self.kit1.skipped == 2 * self.amount_of_pl:
            return True
        "warunek skonczenia gry 2"
        if len(self.kit1.bag) == 0:
            for player in self.players:
                if player.name != "" and len(player.letters) == 0:
                    return True
        return False

    def end(self):
        """funckja na podstawie zasad gry optymalizuje zdobyte punkty"""
        kits = []
        for player in self.players:
            kits.append(player.letters)
        for j in range(len(kits)):
            kit = kits[j]
            player = self.players[j]
            if kit == []:
                for cur_kit in kits:
                    for letter in cur_kit:
                        player.points += count_points(letter, self.kit1.dic)
            else:
                for letter in kit:
                    player.points -= count_points(letter, self.kit1.dic)
        """ekran końcowy"""
        print("Koniec gry")
        self.board1.print()
        for player in self.players:
            if player.name != "":
                print(f"{player.name} zdobyte punkty: {player.points}")
                player.show_words()


if __name__ == "__main__":
    game = Game()
    game.set_game()
    clear()
    game.run_game()
