from classes import Board, Bot, Player, Kit
from functions import make_words


def test_try_add_word_incorrect_coordinates():
    board1 = Board()
    try:
        board1.try_add_word("słowo", ("Z", 18))
    except ValueError:
        return
    return


def test_try_add_word_other_letter():
    board1 = Board()
    board1.add_word("przyklad", ("H", 8))
    try:
        board1.try_add_word("słowo", ("H", 8))
    except ValueError:
        return
    return


def test_check_player_word():
    board1 = Board()
    player1 = Player("gracz1")
    player1.letters = ["h", "o", "j"]
    board1.add_word("hoj", ("H", 8))
    player1.letters = ["h", "o"]
    abc = board1.check_player_word("ho", (9, "G"))
    assert abc == (1, "h")


def test_check_board_one_word():
    kit1 = Kit()
    words1 = make_words("slowa.txt", kit1.dic)
    board1 = Board()
    player1 = Player("gracz1")
    player1.letters = ["h", "o", "j"]
    board1.add_word("hoj", ("H", 8))
    player1.letters = ["h", "o"]
    abc = board1.check_board("ho", (9, "G"), words1)
    assert abc == ["ho"]


def test_check_board_few_words():
    kit1 = Kit()
    words1 = make_words("slowa.txt", kit1.dic)
    board1 = Board()
    player1 = Player("gracz1")
    player1.letters = ["a", "h", "o", "j"]
    board1.add_word("ahoj", ("H", 8))
    player1.letters = ["h", "o"]
    abc = board1.check_board("oh", ("G", 9), words1)
    assert abc == ["oh", "oh", "ho"]


def test_current_words():
    board1 = Board()
    board1.add_word("ahoj", ("H", 8))
    board1.add_word("oh", ("G", 9))
    abc = board1.current_words()
    assert abc == ["oh", "ahoj", "oh", "ho"]


def test_kit_init():
    kit1 = Kit()
    assert len(kit1.bag) == 98
    assert len(kit1.dic) == 34


def test_kit_add_letters():
    player1 = Player("przykład")
    kit1 = Kit()
    kit1.add_letters(10, player1.letters)
    assert len(kit1.bag) == 88
    assert len(kit1.dic) == 34
    assert len(player1.letters) == 10


def test_player():
    player1 = Player("przykład")
    player1.set_name("jan")
    player1.add_points(50)
    player1.add_letter("l")
    assert player1.name == "jan"
    assert player1.points == 50
    assert player1.letters == ["l"]


def test_bot():
    bot1 = Bot("przykład")
    bot1.set_name("bot jan")
    bot1.add_points(50)
    bot1.add_letter("l")
    assert bot1.name == "bot jan"
    assert bot1.points == 50
    assert bot1.letters == ["l"]


def test_bot_first_move():
    kit1 = Kit()
    words1 = make_words("slowa.txt", kit1.dic)
    board1 = Board()
    bot1 = Bot("przykład")
    bot1.set_name("bot jan")
    bot1.add_points(50)
    bot1.letters = ["a", "t", "e", "s", "t"]
    bot1.first_move(board1, kit1, words1)
    assert bot1.name == "bot jan"
    assert bot1.points == 57
