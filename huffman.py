GRAPH = False
def build_codewords(p):
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
    return codewords(p, tree([], sorted(p), len(p)))

def encode(s, c, l):
   coded = []
   for letter in s:
       encoding = c[list(l.keys()).index(letter)]
       coded.append(encoding)
   return "".join(coded)

def decode(es, c, l):
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
            let = list(l.keys())[idx]
            s += let
            code = ""
    return s 
