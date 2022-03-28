
import sys,tty,termios

def print_at(x, y, text):
     sys.stdout.write("\x1b7\x1b[%d;%df%s\x1b8" % (y, x, text))
     sys.stdout.flush()

class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


def get_ch():
        inkey = _Getch()
        while(1):
                k=inkey()
                if k!='':break
        if k=='\x1b[A':
                print_at(0, 20, " >>> up    <<< ")
        elif k=='\x1b[B':
                print_at(0, 20, " >>> down  <<< ")
        elif k=='\x1b[C':
                print_at(0, 20, " >>> right <<< ")
        elif k=='\x1b[D':
                print_at(0, 20, " >>> left  <<< ")
        else:
                print("not an arrow key!")


def main():
    for i in range(0,10):
      print_at(i+10, i+10, '  -- hello --  ')

    for i in range(0,20):
      get_ch()


if __name__=='__main__':
        main()
