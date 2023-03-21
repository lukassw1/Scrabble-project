import os


ASCII_DECODE = 64   # A - 65 -> 1


def make_words(file, dic):
    """stworzenie słownika słów na podstawie pliku txt"""
    words = {}
    with open(file) as data:
        for line in data:
            word = line.strip()
            words[word] = count_points(word, dic)
    return words


def int_input(min, max):
    """ funkcja prosząca gracza o wpisanie inta do skutku
        min: int - minimalna wartosc inputa
        max: int - mkasymalna wartosc inputa

        return: int - wartosc wybrana przez gracza"""
    choice = "wrong"
    while choice.isdigit() is False:
        choice = input("Napisz opcje którą wybierasz: ")
        if choice.isdigit() is False:
            print("Wprowadzono niepoprawną wartość")
        else:
            if int(choice) < min or int(choice) > max:
                print("Wprowadzono niepoprawną wartość")
                choice = "wrong"
            else:
                return int(choice)


def count_points(word, dic):
    """ zliczanie punktów za dane słowo
        word: string - dane słowo
        dic: dictionary - słownik z punktami za litere

        return: int - suma punktow za slowo
    """
    sum = 0
    for letter in word:
        letter_point = dic[letter]
        sum += letter_point
    return sum


def chceck_word(word, kit):
    """ Funkcja sprawdza czy słowo można stworzyć z liter,
        które gracz ma przy sobie
        word: string - dane słowo
        kit: list of strings - litery gracza

        return: bool"""
    backup_kit = []
    for item in kit:
        backup_kit.append(item)
    for letter in word:
        if letter in backup_kit:
            backup_kit.remove(letter)
        else:
            return False
    return True


def other_letter(word1, word2):
    """funkcja dostaje dwa wyrazy gdzie pierwszy zawiera się w drugim
    zwraca liste liter którymi się różnią"""
    word1 = list(word1)
    word2 = list(word2)
    for letter in word1:
        word2.remove(letter)
    return word2


def extension(player, board, words):
    """ Dołożenie jednej lub kilku płytek na początku
        lub na końcu słowa już znajdującego się na planszy,
        albo też zarówno na początku, jak i na końcu takiego słowa"""
    options = []
    points = []
    kind = []
    positions = []
    words_on_board = board.words_on_board
    for item in words_on_board:
        if len(item[0]) < 5:
            place = item[1]
            my_word = item[0]
            if str(place[0]).isdigit():
                """napis pionowy"""
                column = place[0]
                line = place[1]
                line = ord(line) - ASCII_DECODE
                for word in words:
                    if my_word in word:
                        other_letters = other_letter(my_word, word)
                        if chceck_word(other_letters, player.letters):
                            if my_word == word:
                                continue
                            try:
                                index = word.index(my_word)
                                new_place = (column, chr(line - index + ASCII_DECODE))
                                board.try_add_word(word, new_place)
                                x = board.check_board(word, new_place, words)
                                if len(x) > 1:
                                    new_po = 0
                                    new_ki = "przedłużenie+"
                                    for added in x:
                                        new_po += words[added]
                                else:
                                    new_po = words[word]
                                    new_ki = "przedłużenie"
                                options.append(word)
                                points.append(new_po)
                                kind.append(new_ki)
                                positions.append(new_place)
                            except ValueError:
                                continue
            else:
                """napis poziomy"""
                column = place[1]
                line = place[0]
                line = ord(line) - ASCII_DECODE
                for word in words:
                    if my_word in word:
                        other_letters = other_letter(my_word, word)
                        if chceck_word(other_letters, player.letters):
                            if my_word == word:
                                continue
                            try:
                                index = word.index(my_word)
                                new_place = (chr(line+ASCII_DECODE), (column - index))
                                board.try_add_word(word, new_place)
                                x = board.check_board(word, new_place, words)
                                if len(x) > 1:
                                    new_po = 0
                                    new_ki = "przedłużenie+"
                                    for added in x:
                                        new_po += words[added]
                                else:
                                    new_po = words[word]
                                    new_ki = "przedłużenie"
                                options.append(word)
                                points.append(new_po)
                                kind.append(new_ki)
                                positions.append(new_place)
                            except ValueError:
                                continue
    chooser = list(zip(options, points, kind, positions))
    return chooser


def right_angel(player, board, words):
    """ Ułożenie słowa pod kątem prostym do słowa
        znajdującego się na planszy. Nowe słowo
        musi wykorzystywać jedną z liter słowa
        leżącego na planszy."""
    options = []
    points = []
    kind = []
    positions = []
    for item in board.words_on_board:
        word = item[0]
        place = item[1]
        if str(place[0]).isdigit():
            """napis pionowy -> napis poziomy"""
            column = place[0]
            line = place[1]
            line = ord(line)
            for letter in word:
                player.letters.append(letter)
                for word in words:
                    if chceck_word(word, player.letters) and letter in word:
                        try:
                            current_column = column - word.find(letter)
                            new_place = (chr(line), current_column)
                            board.try_add_word(word, new_place)
                            x = board.check_board(word, new_place, words)
                            if len(x) > 1:
                                new_po = 0
                                new_ki = "kąt prosty+"
                                for added in x:
                                    new_po += words[added]
                            else:
                                new_po = words[word]
                                new_ki = "kąt prosty"
                            options.append(word)
                            points.append(new_po)
                            kind.append(new_ki)
                            positions.append(new_place)
                        except ValueError:
                            continue
                line += 1
                player.letters.remove(letter)
        else:
            """napis poziomy -> napis pionowy"""
            column = place[1]
            line = place[0]
            line = ord(line)
            for letter in word:
                player.letters.append(letter)
                for word in words:
                    if chceck_word(word, player.letters) and letter in word:
                        try:
                            current_line = line - word.find(letter)
                            new_place = (column, chr(current_line))
                            board.try_add_word(word, new_place)
                            x = board.check_board(word, new_place, words)
                            if len(x) > 1:
                                new_po = 0
                                new_ki = "kąt prosty+"
                                for added in x:
                                    new_po += words[added]
                            else:
                                new_po = words[word]
                                new_ki = "kąt prosty"
                            options.append(word)
                            points.append(new_po)
                            kind.append(new_ki)
                            positions.append(new_place)
                        except ValueError:
                            continue
                column += 1
                player.letters.remove(letter)
    chooser = list(zip(options, points, kind, positions))
    return chooser


def parallel(player, board, words):
    """ Ułożenie całego słowa równolegle do słowa
        już istniejącego w taki sposób, by stykające
        się płytki także tworzyły całe słowa."""
    options = []
    points = []
    kind = []
    positions = []
    possibilities = []
    for word in words:
        if chceck_word(word, player.letters):
            possibilities.append(word)
    for item in board.words_on_board:
        word = item[0]
        place = item[1]
        if str(place[0]).isdigit():
            """napis pionowy -> napis pionowy"""
            column = place[0]
            line = place[1]
            for poss in possibilities:
                c_line = ord(line) - len(poss) + 1
                for i in range(len(poss)+2):
                    try:
                        new_place = (column + 1, chr(c_line))
                        board.try_add_word(poss, new_place)
                        x = board.check_board(poss, new_place, words)
                        new_po = 0
                        for element in x:
                            new_po += words[element]
                        new_ki = "parallel"
                        options.append(poss)
                        points.append(new_po)
                        kind.append(new_ki)
                        positions.append(new_place)
                    except ValueError:
                        pass
                    try:
                        # z drugiej strony wyrazu
                        new_place = (column - 1, chr(c_line))
                        board.try_add_word(poss, new_place)
                        x = board.check_board(poss, new_place, words)
                        new_po = 0
                        for element in x:
                            new_po += words[element]
                        new_ki = "parallel"
                        options.append(poss)
                        points.append(new_po)
                        kind.append(new_ki)
                        positions.append(new_place)
                    except ValueError:
                        c_line += 1
                        continue
                    c_line += 1
        else:
            "napis poziomy -> napis poziomy"
            column = place[1]
            line = place[0]
            line = ord(line)
            for poss in possibilities:
                c_column = column - len(poss) + 1
                for i in range(len(poss)+2):
                    try:
                        new_place = (chr(line - 1), c_column)
                        board.try_add_word(poss, new_place)
                        x = board.check_board(poss, new_place, words)
                        new_po = 0
                        for element in x:
                            new_po += words[element]
                        new_ki = "parallel"
                        options.append(poss)
                        points.append(new_po)
                        kind.append(new_ki)
                        positions.append(new_place)
                    except ValueError:
                        pass
                    try:
                        # z drugiej strony wyrazu
                        new_place = (chr(line + 1), c_column)
                        board.try_add_word(poss, new_place)
                        x = board.check_board(poss, new_place, words)
                        new_po = 0
                        for element in x:
                            new_po += words[element]
                        new_ki = "parallel"
                        options.append(poss)
                        points.append(new_po)
                        kind.append(new_ki)
                        positions.append(new_place)
                    except ValueError:
                        c_column += 1
                        continue
                    c_column += 1
    chooser = list(zip(options, points, kind, positions))
    return chooser


def line_input():
    """ funkcja do skutku pyta gracza o podanie wiersza,
        gdzie ma się zacząć jego słowo akceptuje tylko litery
        A-O
        return: line - str"""
    line = input("Podaj wiersz, w którym twój wyraz ma się zaczynać(A-O): ")
    if line.isdigit():
        print("Wprowadzono niepoprawne dane.")
        return line_input()
    else:
        if len(line) > 1 or len(line) == 0:
            print("Wprowadzoną niepoprawne dane.")
            return line_input()
        if ord(line) >= 65 and ord(line) <= 79:
            return line
        else:
            print("Wprowadzono niepoprawne dane.")
            return line_input()


def clear():
    os.system('clear')
