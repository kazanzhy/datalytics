import re
import random

def to_cigar(string):
    ans = ''
    last = ''
    count = 1
    for ch in string:
        if ch == last:
            count += 1
        else:
            ans += str(count) + last
            last = ch
            count = 1
    ans += str(count) + ch
    return ans[1:]

def consensus(seqs):
    cons = ''
    l = len(seqs[0])
    t = [{'A': 0, 'T': 0, 'G': 0, 'C': 0} for i in range(l)]
    for seq in seqs:
        for i in range(l):
            ch = seq[i]
            t[i][ch] += 1
    for nuc in t:
        cons += list(nuc.keys())[list(nuc.values()).index(max(nuc.values()))]
    return cons

def ed_dis(A, B):
    n, m = len(A), len(B)
    D = [[0 for j in range(n+1)] for i in range(m+1)]
    cigar = ''
    #for i in range(m+1): D[i][0] = i
    #for j in range(n+1): D[0][j] = j
    for i in range(1, m+1):
        for j in range(1, n+1):
            D[i][j] = min(D[i-1][j]+1, D[i][j-1]+1, D[i-1][j-1] + int(A[j-1]!=B[i-1]))
    # 'M', 'X', 'I' and 'D' – match, mismatch, insertion, and deletion
    while True:
        prev = min(D[i][j-1], D[i-1][j], D[i-1][j-1])
        if prev == D[i-1][j-1]:
            if A[j-1] == B[i-1]:
                cigar = 'M' + cigar
            else:
                cigar = 'X' + cigar            
            i, j = i-1, j-1
        elif prev == D[i][j-1]:
            j = j-1
            cigar = 'D' + cigar
        elif prev == D[i-1][j]:
            i = i-1
            cigar = 'I' + cigar
        if i == 0 or j == 0:
            break
    return (D[-1][-1], cigar, j)

def alignment(A, B, errors):
    n, m = len(A), len(B)
    indexes = []
    i = 0
    while i < (n-m-d):
        dist, cigar, shift = ed_dis(A[i:i+m+d], B)
        if dist <= errors:
            indexes.append((i+shift, cigar, dist))
            #print(A[i+shift:i+shift+m])
            #print(B)
            #print(cigar)
            #print(shift)
            i += m
        else:
            i += 1
    return indexes



fname = '7'
inp = open(fname + '.txt', 'r')
out = open(fname + '_output.txt', 'w')

n, l, d = map(int, inp.readline().strip().split())
E = inp.readline().strip().upper()
'''
for i in range(len(E)-l):
    print(i, len(E)-l)
    motif = E[i:i+l]
    aligns = alignment(E, motif, d)
    if len(aligns) >= n:
        break
'''
'''
print('##')

motif = consensus(motifs)
print(motif)
aligns = alignment(E, motif, d)
'''
motif = 'AACTGGGTTCGGGGAGCCCTGGGCGGGGCAGCTGTTGGGGGG'

aligns = alignment(E, motif, d)


out.write(motif + '\n')
for i in range(n):
    i, cigar, dist = aligns[i]
    out.write(str(i+1) + ' ' + to_cigar(cigar) + '\n')
    print(i+1, to_cigar(cigar))



inp.close()
out.close()















