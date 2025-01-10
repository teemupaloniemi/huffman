#!/usr/bin/python3
import sys
import math
from functools import reduce
from huffman import *

ENCCHARSET = " abcdefghijklmnopqrstuvwxyz"
DECCHARSET = "01"
USAGE = f"""
usage:
     codes 
     dec <string to decode>
     enc <string to encode>

Example:
    >enc kissa istuu puussa
     10100011001010101010110001001010111011010110101001100111010110101010101010110

    >dec 10100011001010101010110001001010111011010110101001100111010110101010101010110
     kissa istuu puussa

    >codes
     _->00       
     a->0110     
     b->010000   
     ... 
     y->101001   
     z->1111000011

Please use only items from these charsets:

encoding: {ENCCHARSET} 
decoding: {DECCHARSET}
"""

# Letter propabilities from 
# Lecture 4: 
#     Entropy and Data Compression (III): Shannon's Source Coding Theorem, Symbol Codes
#     video: https://youtu.be/eHGqNvkL4n4?t=390
LETTERS = { 
    " ":19.28,
    "a":5.75,	
    "b":1.28,	
    "c":2.63,	
    "d":2.85,	
    "e":9.13,	
    "f":1.73,	
    "g":1.33,	
    "h":3.13,	
    "i":5.99,	
    "j":0.06,	
    "k":0.84,	
    "l":3.35,	
    "m":2.35,	
    "n":5.96,	
    "o":6.89,	
    "p":1.92,	
    "q":0.08,	
    "r":5.08,	
    "s":5.67,	
    "t":7.06,	
    "u":3.34,	
    "v":0.69,	
    "w":1.19,	
    "x":0.73,	
    "y":1.64,	
    "z":0.07
}

def entropy(X):
    def f(x, y):
        return x if y == 0 else y * math.log2(1/y) + x
    return reduce(f, X, 0)

def clean(ss, cc):
    for si in ss:
        if si not in cc:
            ss = ss.replace(si, "")
    return ss

def get_input(last):
    user    = input(">").lower().split(" ")
    action  = user[0].strip()
    message = " ".join(user[1:]).strip()
    if message == "last":
        message = last
    return action, message

def dispatch(action, message, c, h):
    if action == "enc":
        m = clean(message, ENCCHARSET)
        if len(m) == 0:
            print("no encodable message found, check charset!")
            return m
        e = encode(m, c, LETTERS)  
        print(f"ENCODED MESSAGE: {e}\nLENGTH: {len(e)}\nSHANNON OPTIMAL LENGTH: {h*len(m)}") 
        return e
    elif action == "dec":
        m = clean(message, DECCHARSET)
        if len(m) == 0:
            print("no decodable message found, check charset!")
            return m
        d = decode(m, c, LETTERS)
        print(f"DECODED MESSAGE: {d}\nLENGTH: {len(d)}") 
        return d
    elif action == "codes":
        for idx, ci in enumerate(c):
            print(f"{list(LETTERS.keys())[idx]:1s}->{ci:9s}")
    else:
        print(USAGE)
    return None

def main():
    p = list(LETTERS.values())
    h = entropy([pi/100.0 for pi in p])
    c = build_codewords(p)
    last = None
    while(1):
        action, message = get_input(last) 
        last = dispatch(action, message, c, h) 
           
if __name__ == "__main__":
    print(USAGE)
    main()

