import sys, tty, termios, fcntl, os, time
import shutil

def term_width():
    return shutil.get_terminal_size((80, 20)).columns


def term_height():
    return shutil.get_terminal_size((80, 20)).lines


def clear_screen():
    print(chr(27) + "[2J")


def print_at(x, y, text, clear = False):
    if clear:
        space = " " * term_width()
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, 0, space))
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()


def wait_key():
    ch = 0
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        while(1):
            # read one char blocking
            ch = sys.stdin.read(1)

            # When we got ESC, try to read the next chars without blocking:
            # If the key ESC was pressed, there are no more chars to read and 
            # the next read will return an empty string.
            if ch == '\x1b':
                # set to non-blocking
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

                # read
                ch2 = sys.stdin.read(2)

                # try to read, if nothing there, sleep a bit
                # TODO: there must be some better way to handle the ESC key
                if len(ch2) == 0:
                    time.sleep(0.001)
                    ch2 = sys.stdin.read(2)

                if len(ch2) == 0:
                    # once again to be sure (usually we only get here if ESC was pressed)
                    time.sleep(0.005)
                    ch2 = sys.stdin.read(2)

                ch = ch + ch2

                # set to blocking
                fcntl.fcntl(fd, fcntl.F_SETFL, fl)
            if ch != '':
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
