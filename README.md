# Panggung yang Disunting

Simulator psikoedukasi untuk Sesi 1 "Sadari": berapa banyak akun yang merasa hidupnya di bawah rata-rata *feed* ketika setiap orang hanya mengunggah hari terbaiknya, pada jaringan pertemanan nyata (set data ego-Facebook SNAP, 4.039 akun, 88.234 pertemanan; McAuley & Leskovec, 2012).

- `index.html`: simulator web (berjalan di peramban, tanpa server, tanpa mengumpulkan data pribadi).
- `simulasi/sim_panggung.py`: simulasi utama (10 seed, ρ = 0; 0,1; 0,2, *feed* kronologis dan keterlibatan, jaringan nyata dan sintetis).
- `simulasi/sim_sensitivitas.py`: uji sensitivitas ICC dan bias menilai diri lebih baik.
- `hasil/`: berkas keluaran yang dipakai di esai.

Data jaringan diunduh dari https://snap.stanford.edu/data/ego-Facebook.html dan disimpan sebagai `data/facebook_combined.txt` sebelum skrip dijalankan.

Kesejahteraan harian dalam simulasi adalah data sintetis. Simulator menunjukkan mekanisme, bukan prevalensi pada mahasiswa.

Labib Althaf, Program Studi Informatika, Universitas Negeri Padang, 2026.
