#!/usr/bin/python
import sys
import math
from functools import reduce

CHARSET = " abcdefghijklmnopqrstuvwxyz"
GRAPH = False
USAGE = f"""
usage:
     dec <string to decode>
     enc <string to encode>

Example:
    >enc kissa istuu puussa
     10100011001010101010110001001010111011010110101001100111010110101010101010110

    >dec 10100011001010101010110001001010111011010110101001100111010110101010101010110
     kissa istuu puussa

Please use only items from this charset:

{CHARSET}

I try to parse everything else away, but have not accounted for everything."""

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

def codewords(p, t):
    paths = []
    for pi in p:
        path = []
        parent = pi
        for i in range(len(t)):
            if t[i][1] == parent:
                parent = t[i][0]
                path.append("1")
            elif t[i][2] == parent:
                path.append("0")
                parent = t[i][0]
        paths.append("".join(reversed(path)))
    return paths

def tree(t, i, ni):
   if ni == 1:
       return t
   f, s = i[-ni], i[-(ni-1)]
   n = f + s
   t.append([n, s, f])
   i.append(n)
   if GRAPH:
       print(f'{round(s,2)} -> {round(n,2)} [label="1"];')
       print(f'{round(f,2)} -> {round(n,2)} [label="0"];')
   return tree(t, sorted(i), ni-1)

def encodings(p):
   return codewords(p, tree([], sorted(p), len(p)))

def encode(s, c):
   coded = []
   for letter in s:
       encoding = c[list(LETTERS.keys()).index(letter)]
       coded.append(encoding)
   return "".join(coded)

def decode(es, c):
    def inencodings(code):
        for idx, ci in enumerate(c):
            if ci == code:
                return idx, True
        return -1, False
    s = ""
    code = ""
    for letter in es:
        code += letter
        idx, t = inencodings(code)
        if t:
            let = list(LETTERS.keys())[idx]
            s += let
            code = ""
    return s

def entropy(X):
    X_hattu = [x/100.0 for x in X]
    def f(x, y):
        return x if y == 0 else y * math.log2(1/y) + x
    return reduce(f, X_hattu, 0)


def main():
    print(USAGE)
    p = list(LETTERS.values())
    h = entropy(p)
    c = encodings(p)
    if GRAPH:
        return
    last = ""
    while(1):
        user = input(">").lower()
        for char in user:
            if char not in CHARSET:
                user = user.replace(char, "")
        luser = user.split(" ")
        action = luser[0].strip()
        message = " ".join(luser[1:]).strip()
        if message == "last":
            message = last
        if action == "enc":
            e    = encode(message, c)
            last = e
            print(f"\nENTROPY (H) OF THE CHARSET IS {h}.\nTHE LENGTH (N) OF YOUR MESSAGE (X) IS {len(message)}\nACCORDING TO SHANNON THIS SHOULD BE ENCODABLE TO (almost) N times H bits which is {len(message)*h}")
            print(f"\nENCODED MESSAGE: {e}\nLENGTH: {len(e)}")
        elif action == "dec":
            d    = decode(message, c)
            last = d
            print(d)
        else:
            print(USAGE)
        print()

if __name__ == "__main__":
    main()
