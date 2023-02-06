import signal
from random import randint
from os import system, name
from getch import getch

class Game:
    def __init__(self):
        print("**********WELCOME TO TETRIS GAME**********")
        print("\n\n GAMEPLAY\n---------\na: move left\nd: move right\ns: takes stone to the bottom of its column\nr: rotate\np: pause\nq: quit\n\n")
        input("PRESS ENTER TO START\n")
        self.different_stones = [
            [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
            [[0, 1, 0], [1, 1, 0], [0, 1, 0]],
            [[1, 1, 0], [0, 1, 0], [0, 1, 0]],
            [[1, 1, 0], [1, 1, 0], [0, 0, 0]],
            [[1, 0, 0], [1, 1, 0], [0, 1, 0]],
            [[0, 1, 0], [1, 1, 0], [1, 0, 0]],
        ]

        self.map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        self.move = "y"
        self.status1 = True
        self.status2 = True
        self.coordinator()

    def coordinator(self):
        while self.status1:
            self.stones_coordinate_vertical = [[0, 1, 2], [4]]
            self.stones_coordinate_horizontal = [[1], [3, 4, 5]]
            self.new_stone()
            self.put_new_stone()
            while self.status2:
                self.get_move()
                self.play_move()
            self.delete_row()
            self.status2 = True
            self.is_it_finished()

    def is_it_finished(self):
        i = 3
        for j in range(9):
            if self.map[i][j] == 1:
                print("\n\n\t\t\t\tGAME OVER")
                self.status1 = False

    def new_stone(self):

        self.stone = self.different_stones[randint(0, 5)]

        for i in range(randint(0, 3)):
            self.rotate()

    def rotate(self):
        # 1 2 3
        # 4 5 6
        # 7 8 9
        rotated = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        # 7 4 1
        # 8 5 2
        # 9 6 3

        for i in [2, 1, 0]:
            for j in [0, 1, 2]:
                rotated[j][2-i] = self.stone[i][j]

        self.stone = rotated

    def put_new_stone(self):
        a = self.stones_coordinate_vertical[1][0]
        b = self.stones_coordinate_horizontal[0][0]

        for i, k in zip([b-1, b, b+1], [0, 1, 2]):
            for j, l in zip([a-1, a, a+1], [0, 1, 2]):
                self.map[i][j] = self.stone[k][l]

    def get_move(self):

        def alarm_handler(signum, frame):
            raise TimeoutError

        def input_with_timeout(prompt, timeout):
            # set signal handler
            signal.signal(signal.SIGALRM, alarm_handler)
            signal.alarm(timeout)  # produce SIGALRM in `timeout` seconds

            try:
                return getch()
            finally:
                signal.alarm(0)  # cancel alarm

        prompt = "x"
        try:
            answer = input_with_timeout(prompt, 1)
        except TimeoutError:
            self.move = "b"

        else:
            print('Got %r' % answer)
            self.move = answer

    def play_move(self):

        if self.move == "s":
            self.joker_down()
            self.status2 = False

        elif self.move == "a" and ( (self.stones_coordinate_vertical[1][0] > 1) or
                                   (
                                   (self.map[self.stones_coordinate_vertical[0][0]][0] == 0) and
                                   (self.map[self.stones_coordinate_vertical[0][1]][0] == 0) and
                                   (self.map[self.stones_coordinate_vertical[0][2]][0] == 0)
                                    ) ):

            # checking
            flag = 1
            for i in self.stones_coordinate_vertical[0]:

                j = self.stones_coordinate_vertical[1][0] - 1

                while self.map[i][j] == 0 and j < self.stones_coordinate_vertical[1][0] + 2:
                    j += 1

                if self.map[i][j-1] == 1:
                    flag = 0
                    break

            # moving
            if flag:

                # detail
                irregular = 0
                for i in self.stones_coordinate_vertical[0]:
                    try:
                        if self.map[i][self.stones_coordinate_vertical[1][0] - 1] == 1 and \
                                self.map[i][self.stones_coordinate_vertical[1][0] - 2] == 1:
                            irregular = 1
                    except IndexError:
                        pass

                k = self.stones_coordinate_vertical[1][0]
                for i in self.stones_coordinate_vertical[0]:
                    for j in [k-1, k, k+1]:
                        if self.map[i][j] == 1:
                            self.map[i][j-1] = self.map[i][j]
                            self.map[i][j] = 0

                if irregular == 0:
                    self.stones_coordinate_vertical[1][0] -= 1
                    self.stones_coordinate_horizontal[1][0] -= 1
                    self.stones_coordinate_horizontal[1][1] -= 1
                    self.stones_coordinate_horizontal[1][2] -= 1

        elif self.move == "d" and ( (self.stones_coordinate_vertical[1][0] < 7) or
                                   (
                                   (self.map[self.stones_coordinate_vertical[0][0]][8] == 0) and
                                   (self.map[self.stones_coordinate_vertical[0][1]][8] == 0) and
                                   (self.map[self.stones_coordinate_vertical[0][2]][8] == 0)
                                    ) ):

            # checking
            flag = 1
            for i in self.stones_coordinate_vertical[0]:

                j = self.stones_coordinate_vertical[1][0] + 1

                while self.map[i][j] == 0 and j > self.stones_coordinate_vertical[1][0] - 2:
                    j -= 1

                if self.map[i][j+1] == 1:
                    flag = 0
                    break

            # moving
            if flag:

                # detail
                irregular = 0
                for i in self.stones_coordinate_vertical[0]:

                    try:
                        if self.map[i][self.stones_coordinate_vertical[1][0] + 1] == 0 and \
                                self.map[i][self.stones_coordinate_vertical[1][0] + 2] == 1:
                            irregular = 1

                    except IndexError:
                        pass
                if self.stones_coordinate_horizontal[1][2] == 8:
                    irregular = 1

                k = self.stones_coordinate_vertical[1][0]
                for i in self.stones_coordinate_vertical[0]:
                    for j in [k+1, k, k-1]:
                        if self.map[i][j] == 1:
                            self.map[i][j+1] = self.map[i][j]
                            self.map[i][j] = 0

                if irregular == 0:
                    self.stones_coordinate_vertical[1][0] += 1
                    self.stones_coordinate_horizontal[1][0] += 1
                    self.stones_coordinate_horizontal[1][1] += 1
                    self.stones_coordinate_horizontal[1][2] += 1

        elif self.move == "r":
            self.rotate()
            self.put_new_stone()

        elif self.move == "q":
            self.move = input("Do you want to quit? Enter 'q' to quit.\n")
            if self.move == "q":
                self.status1 = False
                self.status2 = False

        elif self.move == "p":
            input("Press enter to end pause")

        if self.status2:

            flag = 1
            for j in self.stones_coordinate_horizontal[1]:
                i = self.stones_coordinate_horizontal[0][0] + 1

                try:
                    if self.map[i+2][j] == 1:
                        self.joker_down()
                        self.status2 = False
                        flag = 0
                        break

                except IndexError:
                    self.joker_down()
                    self.status2 = False
                    flag = 0
                    break

                while self.map[i][j] == 0 and i > self.stones_coordinate_horizontal[0][0] - 2:
                    i -= 1
                if self.map[i+1][j] == 1:
                    flag = 0
                    self.status2 = False

            if flag:
                for j in self.stones_coordinate_horizontal[1]:
                    a = self.stones_coordinate_horizontal[0][0]
                    for i in [a+1, a, a-1]:
                        self.map[i+1][j] = self.map[i][j]
                        self.map[i][j] = 0

                self.stones_coordinate_horizontal[0][0] += 1
                self.stones_coordinate_vertical[0][0] += 1
                self.stones_coordinate_vertical[0][1] += 1
                self.stones_coordinate_vertical[0][2] += 1

        self.clear_output()
        self.output()

    def joker_down(self):
        # find 1 in square
        the_ones = []
        all_ones = []
        for j in self.stones_coordinate_horizontal[1]:
            one_time = 1
            for i in reversed(self.stones_coordinate_vertical[0]):
                if self.map[i][j] == 1:
                    if one_time:
                        the_ones.append([i, j])
                        one_time = 0
                    all_ones.append([i, j])

        minn = 20
        for k in range(len(the_ones)):
            l = 1
            while the_ones[k][0] + l < 16 and self.map[the_ones[k][0] + l][the_ones[k][1]] == 0:
                l += 1
            l -= 1
            if minn > l:
                minn = l

        for k in range(len(all_ones)):
            self.map[all_ones[k][0] + minn][all_ones[k][1]] = 1
            self.map[all_ones[k][0]][all_ones[k][1]] = 0

    def delete_row(self):
        for max_delete in range(3):
            for i in reversed(range(16)):
                for j in range(9):
                    if self.map[i][j] == 0:
                        break
                    if j == 8:
                        self.scroll_down(i)

    def scroll_down(self, row):

        for i in reversed(range(row)):
            for j in range(9):
                self.map[i+1][j] = self.map[i][j]
        i = 0
        for j in range(9):
            self.map[i][j] = 0

    def clear_output(self):

        print("\n"*10)
        system('cls' if name == 'nt' else 'clear')
        #system('clear')

    def output(self):

        try:
            import emoji
            for i in range(16):
                print("\t"*8, end="")
                for j in range(9):
                    if i < 3:
                        print(emoji.emojize(":red_square:") if self.map[i][j] == 0 else emoji.emojize(
                            ":white_square_button:"), end="")

                    elif i == 3:
                        print(emoji.emojize(":red_triangle_pointed_down:") if self.map[i][j] == 0 else emoji.emojize(
                            ":white_square_button:"), end="")
                    else:
                        print(emoji.emojize(":black_square_button:") if self.map[i][j] == 0 else emoji.emojize(":white_square_button:"), end="")
                print()

        except ModuleNotFoundError:
            for i in range(16):
                print("\t\t\t\t", *self.map[i])

Tetris = Game()
