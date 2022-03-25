import sys

def help():
    print("* each category contains 100 probs *")
    print("Encryption example: if your problem is...")
    print("187\n296\n345")
    print("then your hash value is sha1(\"[0, 3, 6, 7, 8, 5, 2, 1, 4]\") == 6fc102fa063e2ecf81c8e42751381357b3deb16b\n")
    print("Decryption example: if your problem is...")
    print("6fc102fa063e2ecf81c8e42751381357b3deb16b")
    print("then write down the pattern like this: ")
    print("187\n296\n345\n")
    sys.exit(0)

def banner():
    print("===== Welcome to Devleo's android forensics prob =====")