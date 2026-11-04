"""
Simulasi "Panggung yang Disunting" (GCFest 2026) - versi 1.0, 2 November 2026
Penulis: Labib Althaf. Semua angka di naskah wajib diambil dari berkas keluaran skrip ini.

Pertanyaan: berapa persen pengguna yang melihat "rata-rata hidup" di feed-nya lebih baik
daripada hidupnya sendiri, bila (a) struktur jaringan nyata, (b) jangkauan akun populer,
dan (c) kurasi momen terbaik bekerja bersama? Dan apakah perbandingan setara
("sorotan dibanding sorotan") memulihkan proporsi ke sekitar 50%?

Asumsi (ditulis terbuka, diuji sensitivitasnya):
 A1 Kesejahteraan harian x_it = mu_i + e_it; mu_i ~ N(0,1) antarindividu, e_it ~ N(0,1) harian.
 A2 Korelasi popularitas-kesejahteraan rho in {0; 0,1; 0,2} (Bollen dkk. 2017 melaporkan akun
    populer cenderung lebih bahagia, besarnya tidak dikalibrasi -> diuji).
 A3 Kurasi: setiap orang mengunggah p bagian hari terbaiknya, p in {100%, 50%, 20%, 10%}.
 A4 Feed "kronologis": setiap unggahan teman tampil sekali.
    Feed "keterlibatan": bobot tampil sebanding derajat (jumlah teman) pengunggah.
 A5 Penilaian diri memakai seluruh hari sendiri (orang tahu hari buruknya sendiri).
 Pembanding setara: penilaian diri hanya memakai p bagian hari terbaik sendiri.
"""
import json, sys, hashlib
import numpy as np, networkx as nx

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
T = 60
SEEDS = list(range(1, 11))
RHOS = [0.0, 0.1, 0.2]
PS = [1.0, 0.5, 0.2, 0.1]
FEEDS = ["kronologis", "keterlibatan"]

def load_networks():
    fb_path = "data/facebook_combined.txt"
    sha = hashlib.sha256(open(fb_path, "rb").read()).hexdigest()
    G_fb = nx.read_edgelist(fb_path, nodetype=int)
    G_fb = nx.convert_node_labels_to_integers(G_fb)
    n = G_fb.number_of_nodes()
    m = round(G_fb.number_of_edges() / n)
    G_ba = nx.barabasi_albert_graph(n, m, seed=2026)
    return {"facebook_snap": (G_fb, sha), "sintetis_BA": (G_ba, None)}

def csr(G):
    n = G.number_of_nodes()
    A = nx.to_scipy_sparse_array(G, nodelist=range(n), format="csr", dtype=float)
    deg = np.asarray(A.sum(axis=1)).ravel()
    return A, deg

def run(A, deg, rho, p, feed, seed):
    rng = np.random.default_rng(seed)
    n = len(deg)
    z = np.log(deg); z = (z - z.mean()) / z.std()
    mu = rho * z + np.sqrt(1 - rho**2) * rng.normal(0, 1, n)
    life = mu[:, None] + rng.normal(0, 1, (n, T))
    k = max(1, int(round(p * T)))
    top = np.sort(life, axis=1)[:, -k:]          # hari terbaik yang diunggah
    post_mean = top.mean(axis=1)
    w_src = np.full(n, float(k)) if feed == "kronologis" else k * deg
    num = A @ (w_src * post_mean)
    den = A @ w_src
    feed_mean = num / den
    own_all = life.mean(axis=1)
    own_top = post_mean
    gap = feed_mean - own_all
    return {
        "pct_merasa_di_bawah": float(np.mean(own_all < feed_mean) * 100),
        "pct_di_bawah_bila_setara": float(np.mean(own_top < feed_mean) * 100),
        "median_selisih_SD": float(np.median(gap)),
    }

def main():
    nets = load_networks()
    rows, meta = [], {}
    for name, (G, sha) in nets.items():
        A, deg = csr(G)
        nbr_mean_deg = (A @ deg) / deg
        meta[name] = {
            "simpul": G.number_of_nodes(), "sisi": G.number_of_edges(),
            "rerata_derajat": float(deg.mean()), "sha256": sha,
            "pct_teman_lebih_populer": float(np.mean(nbr_mean_deg > deg) * 100),
            "pct_teman_sama_populer": float(np.mean(nbr_mean_deg == deg) * 100),
        }
        for rho in RHOS:
            for p in PS:
                for feed in FEEDS:
                    res = [run(A, deg, rho, p, feed, s) for s in SEEDS]
                    row = {"jaringan": name, "rho": rho, "porsi_unggah": p, "feed": feed}
                    for key in res[0]:
                        v = np.array([r[key] for r in res])
                        row[key + "_mean"] = round(float(v.mean()), 2)
                        row[key + "_min"] = round(float(v.min()), 2)
                        row[key + "_max"] = round(float(v.max()), 2)
                    rows.append(row)
    import csv
    with open(f"{OUT}/hasil_simulasi.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        wr.writeheader(); wr.writerows(rows)
    with open(f"{OUT}/meta_jaringan.json", "w") as f:
        json.dump({"T_hari": T, "seeds": SEEDS, "jaringan": meta}, f, indent=2)
    print(json.dumps(meta, indent=2))

if __name__ == "__main__":
    main()
