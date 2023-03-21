from random import choice
from copy import deepcopy
import functions


class MissingLettersError(Exception):
    def __init__(self):
        super().__init__("Brak liter na utworzenie wyrazu")


class SeparateWordError(Exception):
    def __init__(self):
        super().__init__("Wyraz musi łączyć się z innym na mapie")


class Board():
    def __init__(self):
        """stworzenie nowej planszy"""
        self.board = []
        self.words_on_board = []
        for i in range(15):
            line = 15 * [" "]
            self.board.append(line)

    def add_letter(self, line, column, letter):
        "dodanie litery na plansze"
        if line > 15 or line < 1 or column > 15 or column < 1:
            raise ValueError("Złe współrzędne")
        elif self.board[line-1][column-1] == " ":
            self.board[line-1][column-1] = letter
        elif self.board[line-1][column-1] == letter:
            pass
        else:
            raise ValueError("Na tym miejscu stoi inna litera")

    def add_word(self, newword, place):
        "dodanie całego wyrazu"
        if str(place[0]).isdigit():
            """wyraz pionowy"""
            column = place[0]
            line = place[1]
            line = ord(line) - functions.ASCII_DECODE
            index = 0
            self.words_on_board.append((newword, place))
            for letter in newword:
                self.add_letter(line+index, column, letter)
                index += 1
        else:
            "wyraz poziomy"
            column = place[1]
            line = place[0]
            line = ord(line) - functions.ASCII_DECODE
            index = 0
            self.words_on_board.append((newword, place))
            for letter in newword:
                self.add_letter(line, column+index, letter)
                index += 1

    def try_add_letter(self, line, column, letter):
        "sprawdzenie czy lietere mozna dodac"
        if line > 15 or line < 1 or column > 15 or column < 1:
            raise ValueError("Złe współrzędne")
        elif self.board[line-1][column-1] == " ":
            pass
        elif self.board[line-1][column-1] == letter:
            pass
        else:
            raise ValueError("Na tym miejscu stoi inna litera")

    def try_add_word(self, newword, place):
        "sprawdzenie czy wyraz mozna dodac"
        if str(place[0]).isdigit():
            """wyraz pionowy"""
            column = place[0]
            line = place[1]
            line = ord(line) - functions.ASCII_DECODE
            index = 0
            for letter in newword:
                self.try_add_letter(line+index, column, letter)
                index += 1
        else:
            "wyraz poziomy"
            column = place[1]
            line = place[0]
            line = ord(line) - functions.ASCII_DECODE
            index = 0
            for letter in newword:
                self.try_add_letter(line, column+index, letter)
                index += 1

    def check_player_letter(self, line, column, letter):
        """ sprawdza czy litere mozna dodac i czy łączy się
            z literami na tablicy """
        if line > 15 or line < 1 or column > 15 or column < 1:
            raise ValueError("Złe współrzędne")
        elif self.board[line-1][column-1] == " ":
            return False
        elif self.board[line-1][column-1] == letter:
            return True
        else:
            raise ValueError("Na tym miejscu stoi inna litera")

    def check_player_word(self, newword, place):
        """ sprawdza czy wyraz mozna dodac oraz czy
            łączy się z wyrazami na tablicy

            return: common letters - (int, str)"""
        common_letters = 0
        needed_letters = ""
        if str(place[0]).isdigit():
            """wyraz pionowy"""
            column = place[0]
            line = place[1]
            line = ord(line) - functions.ASCII_DECODE
            index = 0
            for letter in newword:
                if self.check_player_letter(line+index, column, letter):
                    common_letters += 1
                else:
                    needed_letters += letter
                index += 1
        else:
            "wyraz poziomy"
            column = place[1]
            line = place[0]
            line = ord(line) - functions.ASCII_DECODE
            index = 0
            for letter in newword:
                if self.check_player_letter(line, column+index, letter):
                    common_letters += 1
                else:
                    needed_letters += letter
                index += 1
        return (common_letters, needed_letters)

    def print(self):
        """wyświetlenie obecnego stanu planszy"""
        print("    |", end="")
        for i in range(15):
            if i < 9:
                print(f" {i+1} |", end="")
            else:
                print(f" {i+1}|", end="")
        print("\n", end="")
        number = 0
        for line in self.board:
            print(f"{chr(65+number)}   |", end="")
            for item in line:
                print(f" {item} |", end="")
            print("\n", end="")
            number += 1

    def check_board(self, newword, place, correct_words):
        """sprawdza czy stan gry bedzie prawidłowy po dodaniu wyrazu
        i jakie ewentulane zmiany wprowadza
        jeżeli nie to wyskakuje valueerror,
        jeśli tak to zwraca liste nowych wyrazów
        return: list of new words / Error"""
        copied_board = deepcopy(self)
        potetial_new_words = []
        old_words = copied_board.current_words()
        copied_board.add_word(newword, place)
        words = copied_board.current_words()
        for word in words:
            if word not in correct_words:
                raise ValueError
            else:
                if word in old_words:
                    old_words.remove(word)
                else:
                    potetial_new_words.append(word)
        return potetial_new_words

    def current_words(self):
        """zwraca wszytskie slowa na danej planszy"""
        copied_board = deepcopy(self)
        words = []
        for line in copied_board.board:
            word = ""
            for item in line:
                word = word + item
            word = word.strip()
            word = word.split(" ")
            words.extend(word)
        for i in range(15):
            word = ""
            for line in copied_board.board:
                word = word + line[i]
            word = word.strip()
            word = word.split(" ")
            words.extend(word)
        backup_words = deepcopy(words)
        for word in backup_words:
            if len(word) <= 1:
                words.remove(word)
        return words


class Kit():
    def __init__(self):
        """stworzenie nowego zestawu liter"""
        self.skipped = 0
        self.bag = []
        self.dic = {}
        with open("zestaw.txt") as data:
            for line in data:
                line = line.strip()
                line = line.split("/")
                occurences = int(line[0])
                points = int(line[1])
                letter = str(line[2])
                letter = letter.strip()
                self.bag.extend(occurences * [letter])
                self.dic[letter] = points

    def add_letters(self, amount, target):
        """ funkcja dodaje litery do zestawu gracza i usuwa z zestawu do gry"""
        if len(self.bag) == 0:
            self.skipped += 1
        elif amount > len(self.bag):
            for i in range(len(self.bag)):
                letter = choice(self.bag)
                self.bag.remove(letter)
                target.append(letter)
        else:
            for i in range(amount):
                letter = choice(self.bag)
                self.bag.remove(letter)
                target.append(letter)


class Player():
    def __init__(self, name):
        "stworzenie nowej postaci"
        self.name = name
        self.letters = []
        self.points = 0
        self.words_created = {}

    def set_name(self, newname):
        self.name = newname

    def add_points(self, value):
        "dodanie punktów postaci"
        self.points += value

    def add_letter(self, letter):
        "dodanie litery do zestawu postaci"
        self.letters.append(letter)

    def add_word(self, word, points):
        "dodanie wyrazu i uzyskanych dzięki niemu punktów"
        self.words_created[word] = points

    def show_letters(self, kit: Kit):
        msg = "["
        for letter in self.letters:
            msg += f"'{letter}' ({kit.dic[letter]}), "
        return msg

    def show_words(self):
        "wyświetlenie utworzonych słów przez gracza"
        ret = f"Słowa stworzone przez {self.name}:\n["
        for move in self.words_created:
            ret += f" - {move}: {self.words_created[move]}\n"
        ret += "]"
        print(ret)

    def change_letters(self, kit: Kit):
        "ruch polegający na wymianie liter"
        numbers = []
        index = 1
        for letter in self.letters:
            print(f"{index}. {letter}")
            index += 1
        print("Wypisuj pojedynczo indeksy liter które chcesz wymienić")
        print("Aby zakończyć napisz 0")
        while True:
            number = functions.int_input(0, len(self.letters))
            if number == 0:
                break
            else:
                numbers.append(number)
        numbers = list(set(numbers))
        dropped_out = []
        if len(numbers) == 0:
            return functions.skip(kit)
        for number in numbers:
            dropped_out.append(self.letters[number-1])
        for number in dropped_out:
            self.letters.remove(number)
        kit.add_letters(len(numbers), self.letters)
        for number in dropped_out:
            kit.bag.append(number)
        print(f"\nTwoje nowe litery: {self.letters}\n")

    def skip(self, kit: Kit):
        """ dodaje 1 do ilości pominiętych kolejek z rzędu
            ruch polegającu na przeczekaniu"""
        kit.skipped += 1

    def first_move(self, board: Board, kit: Kit, words: dict):
        """pierwszy ruch w grze gracza"""
        print("Jaki jest twój plan na tę rundę?")
        print("1 - wymienić litery\n2 - stworzyć słowo\n3 - pomiń ruch")
        move_type = functions.int_input(1, 3)
        if move_type == 1:
            return self.change_letters(kit)
        if move_type == 2:
            word = input("Podaj wyraz jaki chcesz dodać: ")
            if word in words and functions.chceck_word(word, self.letters):
                print("Twój wyraz jest: 1 - pionowy, 2 - poziomy")
                composition = functions.int_input(1, 2)
                print("Podaj kolumne, w której twój wyraz ma się zaczynać")
                column = functions.int_input(1, 15)
                line = functions.line_input()
                if composition == 1:
                    place = (column, line)
                    if column != 8:
                        print("\nSłowo musi znajdować się na środku planszy\n")
                        return self.first_move(board, kit, words)
                    else:
                        x = line
                        if ord(x) - functions.ASCII_DECODE + len(word) - 1 >= 8 and ord(x) - functions.ASCII_DECODE < 9:
                            board.add_word(word, place)
                            self.add_points(words[word])
                            self.add_word(word, words[word])
                            for letter in word:
                                self.letters.remove(letter)
                            kit.add_letters(len(word), self.letters)
                        else:
                            print("\nSłowo musi być na środku planszy\n")
                            return self.first_move(board, kit, words)
                else:
                    place = (line, column)
                    if line != "H":
                        print("\nSłowo musi znajdować się na środku planszy\n")
                        return self.first_move(board, kit, words)
                    else:
                        if column + len(word) - 1 >= 8 and column < 9:
                            board.add_word(word, place)
                            self.add_points(words[word])
                            self.add_word(word, words[word])
                            for letter in word:
                                self.letters.remove(letter)
                            kit.add_letters(len(word), self.letters)
                        else:
                            print("\nSłowo musi być na środku planszy\n")
                            return self.first_move(board, kit, words)
                msg = f"\nDodałeś słowo {word},"
                print(f"{msg} które zdobyło {words[word]} punktów\n")
                board.print()
            else:
                if functions.chceck_word(word, self.letters):
                    print("\nPodane słowo nie istnieje\n")
                else:
                    print("\nNie posiadasz nizbędnych liter\n")
                return self.first_move(board, kit, words)
        if move_type == 3:
            return self.skip(kit)

    def move(self, board: Board, kit: Kit, words: dict):
        """ Ruch gracza"""
        print("Jaki jest twój plan na tę rundę?")
        print("1 - wymienić litery\n2 - stworzyć słowo\n3 - pomiń ruch")
        move_type = functions.int_input(1, 3)
        if move_type == 1:
            return self.change_letters(kit)
        if move_type == 2:
            word = input("Podaj wyraz jaki chcesz dodać: ")
            if word in words:
                print("Twój wyraz jest: 1 - pionowy, 2 - poziomy")
                composition = functions.int_input(1, 2)
                print("Podaj kolumne, w której twój wyraz ma się zaczynać")
                column = functions.int_input(1, 15)
                line = functions.line_input()
                if composition == 1:
                    place = (column, line)
                else:
                    place = (line, column)
                try:
                    cl = board.check_player_word(word, place)
                    needed_letters = cl[1]
                    cl = cl[0]      # common letters
                    if not functions.chceck_word(needed_letters, self.letters):
                        raise MissingLettersError
                    new_words = board.check_board(word, place, words)
                    if len(new_words) == 1 and cl == 0:
                        raise SeparateWordError
                    if len(new_words) == 0 or cl == len(word):
                        raise SeparateWordError
                    points = 0
                    for element in new_words:
                        points += words[element]
                    board.add_word(word, place)
                    self.points += points
                    self.add_word(word, points)
                    msg = f"\nDodałeś słowo {word},"
                    print(f"{msg} które zdobyło {points} punktów\n")
                    board.print()
                    for letter in word:
                        if letter in self.letters:
                            self.letters.remove(letter)
                    kit.add_letters(7-len(self.letters), self.letters)
                    kit.skipped = 0
                except MissingLettersError:
                    print("\nNie posiadasz niezbędnych niezbędnych liter\n")
                    return self.move(board, kit, words)
                except SeparateWordError:
                    print("\nWyraz musi łączyć się z innym na mapie\n")
                    return self.move(board, kit, words)
            else:
                print("\nPodane słowo nie isnieje\n")
                return self.move(board, kit, words)
        if move_type == 3:
            return self.skip(kit)


class Bot(Player):
    def first_move(self, board: Board, kit: Kit, words: dict):
        """pierwszy ruch w grze bota"""
        options = []
        points = []
        for word in words:
            if functions.chceck_word(word, self.letters):
                word_points = words[word]
                options.append(word)
                points.append(word_points)
        chooser = list(sorted(list(zip(options, points)), key=lambda x: x[1]))
        chooser.reverse()
        if len(chooser) == 0:
            return self.skip(kit)
        chosen = chooser[0]
        word = chosen[0]
        points = chosen[1]
        self.add_points(points)
        self.add_word(word, points)
        positions = []
        index = 8
        for i in range(len(word)):
            positions.append((8, chr(65+index-1)))
            positions.append((chr(72), index))
            index -= 1
        position = choice(positions)
        board.add_word(word, position)
        print(f"\nBot dodał słowo {word}, które zdobyło {points} punktów\n")
        board.print()
        for letter in word:
            self.letters.remove(letter)
        kit.add_letters(len(word), self.letters)

    def move(self, board: Board, kit: Kit, words: dict):
        """ruch bota"""
        chooser = []
        chooser.extend(functions.extension(self, board, words))
        chooser.extend(functions.right_angel(self, board, words))
        chooser.extend(functions.parallel(self, board, words))
        chooser = list(sorted(chooser, key=lambda x: x[1]))
        chooser.reverse()
        if len(chooser) == 0:
            return self.skip(kit)
        if len(chooser) > 20:
            chooser = chooser[:20]
        pick = chooser[0]
        word = pick[0]
        points = pick[1]
        position = pick[3]
        board.add_word(word, position)
        msg = f"\nBot dodał słowo {word},"
        print(f"{msg} które zdobyło {words[word]} punktów\n")
        board.print()
        self.add_points(points)
        self.add_word(word, points)
        for letter in word:
            if letter in self.letters:
                self.letters.remove(letter)
        kit.add_letters(7-len(self.letters), self.letters)
        kit.skipped = 0
