import time
from terminal import print_at, wait_key, clear_screen, term_height

max_y = term_height()
count = 0

def go_up():
    print_at(1, max_y, f"> up    {count}", clear=True)


def go_down():
    print_at(1, max_y, f"> down  {count}", clear=True)


def go_left():
    print_at(1, max_y, f"> left  {count}", clear=True)


def go_right():
    print_at(1, max_y, f"> right {count}", clear=True)


def handle_key(k):
    global count
    count+=1

    if k=='\x1b[A':
        go_up()
    elif k=='\x1b[B':
        go_down()
    elif k=='\x1b[C':
        go_right()
    elif k=='\x1b[D':
        go_left()
    else:
        print_at(0, max_y, f"> {k}", clear=True)



def main():
    clear_screen()

    for i in range(0,10):
        print_at(i+10, i+10, '  -- hello --  ')

    while(1):
        k = wait_key()

        # end on 'q' or ESC
        if k == 'q' or k == '\x1b':
            break

        # handle other keys
        handle_key(k)

    print_at(0, max_y, "> good bye...", clear=True)
    time.sleep(0.2)


if __name__=='__main__':
    main()
