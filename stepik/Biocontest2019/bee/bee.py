import re

def bee_population_f(line):
    n1, a, b = map(float, line.strip().split())
    n_prev, n_next = 0, n1
    # Make 1kk iterations
    for j in range(1000000):
        n_prev = n_next
        n_next =a*n_prev - b*(n_prev**2)
        # If next is too small or negative
        if n_next < 0.0001:
            n_next = 0
            break
        # If next is too high 
        if n_next > 1000000000:
            n_next = -1
            break
        # If change too small
        if abs(n_next - n_prev) < 0.0001:
            break
    n_next = round(n_next, 4)
    return n_next

def bee_population_s(line):
    n1, a, b = map(float, line.strip().split())
    if b == 0 and a > 1:
        return -1
    elif b == 0 and a <= 1:
        return 0
    if (a-1)/b < 0:
        ni = 0
    else:
        ni = (a-1)/b
    return ni


inp = open('bee_tests.txt', 'r')
out = open('output.txt', 'w')

t = int(inp.readline().strip())

for i in range(t):
    line = inp.readline()
    #ans = bee_population_f(line)
    ans = bee_population_s(line)

    out.write(str(ans) + '\n')
    print(ans)

inp.close()
out.close()















