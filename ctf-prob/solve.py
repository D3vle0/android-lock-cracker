# !/usr/bin/python3
import hashlib
import sqlite3
import json
import os
from pwn import *
from dotenv import load_dotenv

p=remote("", )
p.sendlineafter("> ", "1")
for prob in range(100): ## encryption prob
    tmp=""
    path=[]
    for i in range(3):
        tmp+=p.recvline().decode()
    for i in tmp:
        if i != "\n":
            path.append(int(i))
    queue=[]
    for i in range(9):
        queue.append(path.index(i+1))
    p.sendlineafter("> ", hashlib.sha1(str(queue).encode()).hexdigest())
p.sendlineafter("> ", "2")
load_dotenv(verbose=True)
RAINBOWTABLE_PATH = os.getenv('RAINBOWTABLE_PATH')
conn = sqlite3.connect(RAINBOWTABLE_PATH)
cur = conn.cursor()
for prob in range(100): ## decryption prob
    hash = p.recvline().decode()[:-1]
    cur.execute(f"SELECT pattern FROM RainbowTable WHERE hash = '{hash}'")
    rows = cur.fetchall()
    for row in rows:
        queue=json.loads(row[0])
    path=[0]*9
    for i in range(9):
        path[queue[i]]=i+1
    correct_answer = ""
    for i in range(9):
        if (i+1)%3:
            correct_answer += str(path[i])
        else:
            correct_answer += str(path[i]) + "\n"
    correct_answer = correct_answer[:-1]
    for i in range(3):
        p.sendlineafter("> ", correct_answer.split("\n")[i])
p.interactive()