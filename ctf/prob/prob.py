import sqlite3
import random
import hashlib
import sys

def encryption():
    queue=random.sample(range(9), 9)
    path=[0]*9
    for i in range(9):
        path[queue[i]]=i+1
    for i in range(9):
        if (i+1)%3:
            print(path[i], end="")
        else:
            print(path[i])
    hash_str = "[" + ", ".join(map(str, queue)) + "]"
    hash_str = hash_str.encode()
    a=input("> ")
    if a == hashlib.sha1(hash_str).hexdigest():
        return
    else:
        sys.exit(0)

def decryption():
    conn = sqlite3.connect("GestureRainbowTable.db")
    cur = conn.cursor()
    queue=random.sample(range(9), 9)
    cur.execute(f"SELECT hash FROM RainbowTable WHERE pattern = '{queue}'")
    rows = cur.fetchall()
    for row in rows:
        print(row[0])
    path=[0]*9
    for i in range(9):
        path[queue[i]]=i+1
    correct_answer = ""
    for i in range(9):
        if (i+1)%3:
            correct_answer += str(path[i])
        else:
            correct_answer += str(path[i]) + "\n"
    answer1=input("> ")
    answer2=input("> ")
    answer3=input("> ")
    if answer1 == correct_answer.split("\n")[0] and answer2 == correct_answer.split("\n")[1] and answer3 == correct_answer.split("\n")[2]:
        return
    else:
        sys.exit(0)