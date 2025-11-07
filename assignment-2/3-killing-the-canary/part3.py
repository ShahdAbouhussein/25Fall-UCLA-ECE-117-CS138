#!/usr/bin/env python3
import re
from pwn import *

exe = ELF("./killing-the-canary")

r = process([exe.path])
# gdb.attach(r)

r.recvuntil(b"What's your name? ")
r.sendline(b"xxx") #Add your code here

val = r.recvuntil(b"What's your message? ")
# log.info(val)
canary = int(re.match(b"Hello, ([0-9]+)\n!.*", val).groups()[0])
log.info(f"Canary: {canary:x}")

win = exe.symbols['print_flag']
# log.info(hex(win))

payload = # Add your payload here
r.sendline(payload)

r.recvline()
r.interactive()