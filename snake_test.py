import time
from terminal import print_at, wait_key, clear_screen, term_height

class Board:
    def __init__(self) -> None:
        self.max_y = term_height()
        self.count = 0
        self.pos = (0, 0)
        self.direction = (0, 0)
        self.speed = 2    # chars per second
        self.last_update = time.time()

    def go_up(self):
        self.direction = (0, -1)
        self.message(f"up {self.count}")

    def go_down(self):
        self.direction = (0, 1)
        self.message(f"down {self.count}")

    def go_left(self):
        self.direction = (-1, 0)
        self.message(f"left {self.count}")

    def go_right(self):
        self.direction = (1, 0)
        self.message(f"right {self.count}")

    def message(self, msg):
        print_at(0, self.max_y, f"> {msg}", clear=True)

    def delete_pos(self):
        print_at(self.pos[0], self.pos[1], ' ', clear=False)

    def update_pos(self):
        t = time.time()
        dt = t - self.last_update
        if dt < 1/self.speed:
            return
        
        s = int(self.speed * dt)
        dt = dt - s/self.speed
        self.last_update = t - dt

        self.delete_pos()
        self.pos = (self.pos[0] + self.direction[0] * s * 2, self.pos[1] + self.direction[1] * s)
        print_at(self.pos[0], self.pos[1], 'X', clear=False)

    def handle_key(self, k):
        self.count+=1

        self.update_pos()

        if k=='\x1b[A':
            self.go_up()
        elif k=='\x1b[B':
            self.go_down()
        elif k=='\x1b[C':
            self.go_right()
        elif k=='\x1b[D':
            self.go_left()
        else:
            self.message(f"unknown key: {k}")


def main():
    board = Board()
    clear_screen()

    while(1):
        k = wait_key(100)

        # end on 'q' or ESC
        if k == 'q' or k == '\x1b':
            break

        # handle other keys
        board.handle_key(k)

    print_at(0, board.max_y, "> good bye...", clear=True)
    time.sleep(0.2)


if __name__=='__main__':
    main()
