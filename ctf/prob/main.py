import help
import sys
import prob
import os

def choice():
    clear1=0
    clear2=0
    while 1:
        if clear1 * clear2:
            os.system("/bin/sh")
            sys.exit(0)
        if clear1:
            print("1. Encryption (solved)")
        else:
            print("1. Encryption")
        if clear2:
            print("2. Decryption (solved)")
        else:
            print("2. Decryption")
        print("3. Help")
        try:
            main_choice=int(input("> "))
        except:
            sys.exit(0)
        if main_choice == 3:
            help.help()
        elif main_choice == 1:
            for i in range(100):
                prob.encryption()
            clear1=1
        elif main_choice == 2:
            for i in range(100):
                prob.decryption()
            clear2=1
        else:
            sys.exit(0)

if __name__ == "__main__":
    help.banner()
    choice()