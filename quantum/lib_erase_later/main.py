import getopt
import sys
import time
from datetime import datetime

import program as prog
import quantum.send_email as se


def check_args(argv):
    try:
        opts, args = getopt.getopt(argv, "e")
    except getopt.GetoptError:
        print("Wrong argument: USAGE: '[filename].py -e' OR '[filename].py'")
        sys.exit()
    if not opts:
        print("Email option OFF")
        t = time.time()
        main()
        print(f"Time:{time.time()-t} s.")
    else:
        print("Email option ON")
        t = time.time()
        main()
        now = datetime.now()
        se.SendMail(MESSAGE=f"{now} - Time:{time.time()-t} s.")


def main():
    prog.arahama_ql_mod()


if __name__ == "__main__":
    check_args(sys.argv[1:])
