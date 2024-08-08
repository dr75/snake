import sys, tty, termios, fcntl, os, time
import shutil
import select

def term_width():
    return shutil.get_terminal_size((80, 20)).columns

def term_height():
    return shutil.get_terminal_size((80, 20)).lines

def clear_screen():
    print(chr(27) + "[2J")

def print_at(x, y, text, clear=False):
    if clear:
        space = " " * term_width()
        sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, 0, space))
    sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
    sys.stdout.flush()

def wait_key(timeout_ms=1000):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    ch = ''
    try:
        tty.setraw(sys.stdin.fileno())
        ready, _, _ = select.select([sys.stdin], [], [], timeout_ms / 1000.0)
        if ready:
            ch = sys.stdin.read(1)
            if ch == '\x1b':  # ESC key
                # Set to non-blocking
                fl = fcntl.fcntl(fd, fcntl.F_GETFL)
                fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
                ch2 = sys.stdin.read(2)  # Attempt to read arrow keys or other escape sequences
                ch += ch2
                # Reset to blocking
                fcntl.fcntl(fd, fcntl.F_SETFL, fl)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
