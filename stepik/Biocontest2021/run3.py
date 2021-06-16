import numpy as np
import sys
sys.setrecursionlimit(1000000)

file = '3'
fi = open(f'Diagnosis/test{file}')
fo = open(f'Diagnosis/test{file}_out', 'w')
hpo_num = int(fi.readline())
hpo_par = [None, *map(lambda x: int(x)-1, fi.readline().strip().split())]
hpo_val = list(map(int, fi.readline().strip().split()))

diseases_num = int(fi.readline())
diseases = []
for dn in range(diseases_num):
    diseases.append(list(map(lambda x: int(x)-1, fi.readline().strip().split())))
    
patients_num = int(fi.readline())
patients = []
for dn in range(patients_num):
    patients.append(list(map(lambda x: int(x)-1, fi.readline().strip().split())))
    
hpo = []
for i in range(hpo_num):
    hpo.append({'idx': i, 'val': hpo_val[i], 'par': hpo_par[i], 'route': [], 'childs': []})

# Add childs for DFS
for chld, par in enumerate(hpo_par[1:], 1):
    hpo[par]['childs'].append(chld)

def dfs_root(v, route):
    route.append(v)
    hpo[v]['route'] = route.copy()
    for child in hpo[v]['childs']:
        dfs_root(child, route.copy())
dfs_root(0, [])

lca_vals = np.zeros((hpo_num, hpo_num))
for i in range(hpo_num):
    for j in range(hpo_num):
        lca = max(set(hpo[i]['route']) & set(hpo[j]['route']))
        lca_vals[i,j] = hpo_val[lca]
        
for pi, patient in enumerate(patients):
    disease_scores = []
    for di, disease in enumerate(diseases):
        score = lca_val[patient][:,disease].max(axis=0).sum()
        disease_scores.append([di, score])
    d_max = max(disease_scores, key=lambda x: x[1])
    fo.write(f'{d_max[0] + 1}\n')
    print(pi+1, patients_num, end='\r')
    
fi.close()
fo.close()
