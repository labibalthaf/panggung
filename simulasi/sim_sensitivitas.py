"""Uji sensitivitas tambahan (v1.1, 2 Nov 2026): (a) proporsi varians antarindividu (ICC),
(b) bias menilai diri lebih baik (pergeseran penilaian diri sebesar delta SD antarindividu).
Jaringan ego-Facebook SNAP, rho = 0, feed kronologis, seed 1-10."""
import csv, numpy as np, networkx as nx
T=60; SEEDS=range(1,11)
G=nx.convert_node_labels_to_integers(nx.read_edgelist("data/facebook_combined.txt",nodetype=int))
n=G.number_of_nodes(); A=nx.to_scipy_sparse_array(G,nodelist=range(n),format="csr",dtype=float)
def run(icc,p,delta,seed):
    rng=np.random.default_rng(seed)
    mu=rng.normal(0,1,n); se=np.sqrt((1-icc)/icc)
    life=mu[:,None]+rng.normal(0,1,(n,T))*se
    k=max(1,int(round(p*T))); top=np.sort(life,axis=1)[:,-k:].mean(axis=1)
    feed=(A@top)/(A@np.ones(n))
    own=life.mean(axis=1)+delta
    return float(np.mean(own<feed)*100)
rows=[]
for icc in [0.75,0.5,0.26]:
    for p in [0.5,0.2,0.1]:
        v=np.array([run(icc,p,0.0,s) for s in SEEDS]); rows.append(dict(uji="ICC",icc=icc,porsi=p,delta=0,mean=round(v.mean(),2),min=round(v.min(),2),max=round(v.max(),2)))
for d in [0.25,0.5]:
    for p in [0.5,0.2,0.1]:
        v=np.array([run(0.5,p,d,s) for s in SEEDS]); rows.append(dict(uji="bias_diri",icc=0.5,porsi=p,delta=d,mean=round(v.mean(),2),min=round(v.min(),2),max=round(v.max(),2)))
for icc in [0.75]:
    for d in [0.25,0.5]:
        for p in [0.5,0.2,0.1]:
            v=np.array([run(icc,p,d,s) for s in SEEDS]); rows.append(dict(uji="gabungan",icc=icc,porsi=p,delta=d,mean=round(v.mean(),2),min=round(v.min(),2),max=round(v.max(),2)))
with open("out/hasil_sensitivitas.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows: print(r)
