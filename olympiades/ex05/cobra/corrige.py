#!/bin/python3
import hashlib

hash_to_crack = hashlib.md5("cobra".encode()).hexdigest()
alphabet = "abcdefghijklmnopqrstuvwxyz"

def convert_to_base_26(n: int) -> str:
    res = ""
    while n > 0:
        res = alphabet[n % 26] + res
        n //= 26
    return res

for i in range(1000000000):
    psw = convert_to_base_26(i)
    hashed = hashlib.md5(psw.encode()).hexdigest()
    if hashed == hash_to_crack:
        print(f"Password found: {psw}")
        break
