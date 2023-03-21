from functions import other_letter, count_points, chceck_word, parallel
from functions import make_words, extension, right_angel
from classes import Kit, Board, Player


basic_kit = Kit()


def test_make_words():
    ans = {'slowo': 6, 'slowa': 6, 'slowu': 8}
    assert make_words("test_slowa.txt", basic_kit.dic) == ans


def test_count_points():
    word = "góruj"
    assert count_points(word, basic_kit.dic) == 15


def test_count_points2():
    word = "potok"
    assert count_points(word, basic_kit.dic) == 8


def test_check_word_true():
    word = "potok"
    kit1 = ["p", "t", "o", "o", "k"]
    assert chceck_word(word, kit1) is True


def test_check_word_false():
    word = "prom"
    kit1 = ["p", "t", "o", "m", "k"]
    assert chceck_word(word, kit1) is False


def test_check_word_false2():
    word = "aaa"
    kit1 = ["a", "a", "o", "m", "k"]
    assert chceck_word(word, kit1) is False


def test_other_letter():
    word1 = "abc"
    word2 = "abcde"
    assert other_letter(word1, word2) == ["d", "e"]


def test_extension_1():
    words1 = make_words("slowa.txt", basic_kit.dic)
    board1 = Board()
    player1 = Player("gracz1")
    player1.letters = ["h", "o", "j"]
    board1.add_word("hoj", ("H", 8))
    player1.letters = ["a"]
    abc = extension(player1, board1, words1)
    x = "przedłużenie"
    ans = [('ahoj', 8, x, ('H', 7)), ('hoja', 8, x, ('H', 8))]
    assert abc == ans


def test_extension_2_plus():
    words1 = make_words("slowa.txt", basic_kit.dic)
    board1 = Board()
    player1 = Player("gracz1")
    player1.letters = ["h", "o", "j"]
    board1.add_word("hoj", ("H", 8))
    board1.add_word("cyk", (11, "E"))
    player1.letters = ["a"]
    abc = extension(player1, board1, words1)
    one = ('ahoj', 8, 'przedłużenie', ('H', 7))
    two = ('hoja', 15, 'przedłużenie+', ('H', 8))
    three = ('cyka', 15, 'przedłużenie+', (11, 'E'))
    assert abc == [one, two, three]


def test_right_angle_horizontally():
    words1 = make_words("slowa.txt", basic_kit.dic)
    board1 = Board()
    player1 = Player("gracz1")
    player1.letters = ["h", "o", "j"]
    board1.add_word("hoj", ("H", 8))
    player1.letters = ["a", "k"]
    board1.print()
    abc = right_angel(player1, board1, words1)
    ans = []
    ans.append(('ha', 4, 'kąt prosty', (8, 'H')))
    ans.append(('hak', 6, 'kąt prosty', (8, 'H')))
    ans.append(('ko', 3, 'kąt prosty', (9, 'G')))
    ans.append(('ok', 3, 'kąt prosty', (9, 'H')))
    ans.append(('oka', 4, 'kąt prosty', (9, 'H')))
    ans.append(('aj', 4, 'kąt prosty', (10, 'G')))
    ans.append(('ja', 4, 'kąt prosty', (10, 'H')))
    ans.append(('jak', 6, 'kąt prosty', (10, 'H')))
    assert abc == ans


def test_right_angle_uprigth():
    words1 = make_words("slowa.txt", basic_kit.dic)
    board1 = Board()
    player1 = Player("gracz1")
    player1.letters = ["h", "o", "j"]
    board1.add_word("hoj", (8, "H"))
    player1.letters = ["k"]
    abc = right_angel(player1, board1, words1)
    x = "kąt prosty"
    assert abc == [('ko', 3, x, ('I', 7)), ('ok', 3, x, ('I', 8))]


def test_right_angle_plus_h():
    words1 = make_words("slowa.txt", basic_kit.dic)
    board1 = Board()
    player1 = Player("gracz1")
    board1.add_word("honda", ("H", 8))
    board1.add_word("fach", ("L", 9))
    player1.letters = ["o", "p", "c", "e"]
    board1.print()
    abc = right_angel(player1, board1, words1)
    for item in abc:
        if item[3] == "kąt prosty+":
            assert item == ('hopce', 21, 'kąt prosty+', (8, 'H'))


def test_parallel():
    words1 = make_words("slowa.txt", basic_kit.dic)
    board1 = Board()
    player1 = Player("gracz1")
    player1.letters = ["h", "o", "j"]
    board1.add_word("hoj", ("H", 8))
    player1.letters = ["h", "a"]
    ans = []
    ans.append(('ha', 8, 'parallel', ('I', 7)))
    ans.append(('ha', 12, 'parallel', ('G', 9)))
    ans.append(('ha', 12, 'parallel', ('I', 9)))
    assert parallel(player1, board1, words1) == ans
