from math import factorial as f
import math


pascal = [[1], [1, 1]]

def get_prob(k, i):
    # get probability of this variant
    '''
    global pascal
    while k > len(pascal) - 1:
        last_line = pascal[-1]
        new_line = [1]
        for j in range(len(last_line)-1):
            new_line.append(last_line[j] + last_line[j+1])
        new_line.append(1)    
        pascal.append(new_line)
    return pascal[k][i] / (2**k)
    '''
    if k < i:
        return 1
    else:
        return f(k)/(f(i)*f(k-i)*(2**k))


def errors(line):
    L, n, p, k = map(float, line.strip().split())
    L, n, k = int(L), int(n), int(k)
    ans = 0
    alig_vars = n*k - n + 1
    for i in range(alig_vars):
        prob = get_prob(alig_vars-1, i)
        covered = min(L, n+i)
        uncovered = max(0, L - covered)
        coverage = (n*k)/covered
        min_cov = math.floor(coverage)
        max_cov = min_cov + 1
        min_cov_part = max_cov - coverage
        max_cov_part = coverage - min_cov
        if coverage <= 2:
            covered_error = max_cov_part * covered * (p*2) + min_cov_part * covered * p
        elif coverage <= 3:
            covered_error = max_cov_part * covered * (p*3) + min_cov_part * covered * (p*2)
        else:
            covered_error = max_cov_part * covered * (p*max_cov) + min_cov_part * covered * (p*min_cov)
        uncovered_error = uncovered * 0.75
        ans += prob * (covered_error + uncovered_error)
    return ans

fname = '1_test'
inp = open(fname + '.txt', 'r')
out = open(fname + '_output.txt', 'w')

t = int(inp.readline().strip())

for i in range(t):
    line = inp.readline()
    ans = errors(line)

    out.write(str(ans) + '\n')
    print('###', ans)

inp.close()
out.close()















