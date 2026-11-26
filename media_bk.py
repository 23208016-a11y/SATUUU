#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEDIA PEMBELAJARAN INTERAKTIF - BERPIKIR KOMPUTASIONAL
Informatika Kelas IX - Bab 1
Cara menjalankan:  python media_bk.py   (Python 3.8+, hanya memakai tkinter bawaan)
"""
import tkinter as tk, random, math, re, heapq

BG, CARD, CARD2, CV = '#16123A', '#2A2468', "#4F42DF", '#1E1950'
CY, PK, YE, GR, W, MU, DK = '#22D3EE', '#FF5CA8', '#FFD93D', '#4ADE80', '#FFFFFF', '#C9C5F5', '#4A4390'
FN = 'Trebuchet MS'

# ===================== LOGIKA MURNI (bisa diuji tanpa tampilan) =====================
class Bit:
    def __init__(s, v): s.v = int(v) & 1
    def __and__(s, o): return Bit(s.v & o.v)
    def __or__(s, o): return Bit(s.v | o.v)
    def __xor__(s, o): return Bit(s.v ^ o.v)
    def __invert__(s): return Bit(1 - s.v)

def hitung(expr, a, b):
    e = expr.strip().lower()
    if not e: raise ValueError('Ekspresi masih kosong.')
    if re.sub(r'and|or|xor|not|[ab01()]|\s', '', e):
        raise ValueError('Pakai: A, B, 0, 1, AND, OR, XOR, NOT, dan tanda kurung.')
    peta = {'and': '&', 'or': '|', 'xor': '^', 'not': '~', 'a': 'A', 'b': 'B', '0': 'F', '1': 'T', '(': '(', ')': ')'}
    kode = ' '.join(peta[t] for t in re.findall(r'and|or|xor|not|[ab01()]', e))
    try:
        return eval(kode, {'__builtins__': {}}, {'A': Bit(a), 'B': Bit(b), 'T': Bit(1), 'F': Bit(0)}).v
    except Exception:
        raise ValueError('Susunan ekspresi belum benar.')

def dijkstra(g, src, dst):
    dist = {n: math.inf for n in g}; dist[src] = 0; prev = {}; ev = []; done = set(); pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u in done: continue
        done.add(u); rel = []
        for v, w in g[u]:
            if v not in done and d + w < dist[v]:
                dist[v] = d + w; prev[v] = u; rel.append((v, dist[v])); heapq.heappush(pq, (dist[v], v))
        ev.append((u, d, rel))
        if u == dst: break
    path = [dst]
    while path[-1] != src: path.append(prev[path[-1]])
    return ev, path[::-1], dist[dst]

# ===================== DATA MATERI =====================
INTRO = """
# Apa itu Berpikir Komputasional?
Cara menyelesaikan masalah dengan langkah yang rapi dan terstruktur, sehingga dapat dikerjakan oleh manusia maupun komputer.
## Bukan berarti...
- harus pintar coding atau selalu memegang komputer
## Tetapi...
- melatih cara berpikir yang teliti, runtut, dan kreatif
- dapat dipakai di PR, organisasi, bahkan saat memasak
## Mengapa penting?
- masalah rumit menjadi mudah dikerjakan
- hasilnya bisa dicek dan diulang orang lain
- menjadi dasar pembuatan aplikasi, game, dan kecerdasan buatan (AI)
# Contoh: Google Maps
Saat mencari rute ke sekolah, aplikasi memecah perjalanan menjadi ruas jalan, mengenali pola jam macet, mengambil data penting saja (jalan dan jarak), lalu menyusun langkah: lurus, belok kiri, belok kanan.
# Alur umum (lihat animasi di kanan)
Pahami masalah, pecah, cari pola, ambil yang penting, susun langkah, lalu uji dan perbaiki.
!! Catatan: urutan pilar dapat berubah sesuai masalahnya.
# Tujuan Pembelajaran
- Mengenal dan menyelesaikan masalah yang memakai Tree dan Graf
- Memahami logika (AND, OR, NOT, XOR) dan menemukan pola
- Menyelesaikan soal algoritma, menyajikannya dalam kalimat dan flowchart
"""
PIL = [
"""# Dekomposisi
Memecah masalah besar menjadi bagian-bagian kecil yang lebih mudah dikerjakan.
## Contoh: Pensi sekolah
- Acara: urutan penampil dan pembawa acara
- Dana: sponsor dan penjualan tiket
- Publikasi: poster dan media sosial
- Perlengkapan: panggung dan sound system
## Manfaat
- pekerjaan bisa dibagi ke teman
- bagian yang salah mudah ditemukan dan diperbaiki
++ Di komputer: program besar dibagi menjadi fungsi atau modul kecil.""",
"""# Abstraksi
Menyaring informasi: mengambil yang penting dan mengabaikan detail yang tidak dibutuhkan.
## Contoh: Kartu pelajar
- Dipakai: nama, NIS, kelas, foto
- Diabaikan: warna sepatu, hobi, tinggi badan
## Contoh lain
- Peta MRT hanya menampilkan stasiun dan jalur, bukan gedung
- Ikon baterai mewakili sisa daya tanpa menampilkan isi rangkaiannya
++ Di komputer: variabel dan fungsi menyembunyikan detail yang rumit.""",
"""# Pengenalan Pola
Mencari kesamaan atau hal yang berulang agar masalah baru dapat diselesaikan dengan cara lama.
## Contoh
- Deret 2, 4, 6, 8 selalu bertambah 2, maka berikutnya 10 dan 12
- Jadwal piket berulang tiap minggu
- Soal pecahan memakai cara yang sama, hanya angkanya berbeda
## Manfaat
- tidak perlu memikirkan ulang dari nol
- aturan umum (rumus) menghemat banyak langkah
++ Di komputer: pola yang berulang ditulis sebagai perulangan.""",
"""# Algoritma
Urutan langkah yang jelas dan berurutan untuk menyelesaikan masalah.
## Contoh: Cuci tangan
- Basahi tangan, sabuni 20 detik, bilas, lalu keringkan
## Perhatikan
- Jika urutan terbalik, hasilnya tidak benar
- Setiap langkah harus jelas dan bisa dikerjakan
!! Algoritma yang baik: ada input, proses, output, dan ada akhirnya.
++ Di komputer: algoritma ditulis menjadi program."""]
TREE_TXT = """
# Apa itu Tree (Pohon)?
Struktur data yang tersusun bertingkat, seperti pohon keluarga atau folder di laptop.
## Istilah penting
!! Root: node paling atas, hanya satu
- Node: kotak berisi data
- Edge: garis penghubung antar node
- Parent: node tepat di atas suatu node
- Child: node tepat di bawah suatu node
- Sibling: node bersaudara (satu parent)
++ Leaf: node paling bawah, tidak punya child
- Level: tingkat node; root berada di level 0
- Subtree: satu cabang beserta seluruh turunannya
## Ciri Tree
- hanya ada satu root
- tidak ada lingkaran (tidak ada jalur yang kembali)
- jika ada n node maka ada n - 1 edge
## Contoh nyata
- struktur folder dan file, silsilah keluarga
- struktur organisasi sekolah (gambar di kanan)
- menu bertingkat pada aplikasi
## Menelusuri Tree (Preorder)
Kunjungi root dulu, lalu cabang paling kiri sampai habis, kemudian cabang berikutnya. Tekan tombol Telusuri untuk melihatnya.
## Coba sendiri
Klik tiap node di gambar. Ada berapa leaf? Siapa parent Guru IPA? Di level berapa Asisten Lab?
"""
GRAF_TXT = """
# Apa itu Graf?
Kumpulan simpul (node) yang dihubungkan oleh sisi (edge). Susunannya bebas, tidak harus bertingkat.
## Istilah penting
- Simpul: titik, misalnya tempat atau orang
- Sisi: garis hubungan antar simpul
!! Derajat: jumlah sisi pada satu simpul
- Bobot: angka pada sisi (jarak, waktu, biaya)
- Jalur: urutan simpul yang dilalui
## Fakta menarik
++ Jumlah semua derajat = 2 x jumlah sisi (tiap sisi dihitung dari dua ujungnya)
## Beda Tree dan Graf
- Tree punya root dan tanpa lingkaran
- Graf boleh membentuk lingkaran dan tidak punya root
- Tree sebenarnya adalah graf khusus
## Contoh nyata
- pertemanan di media sosial
- peta jalan dan rute bus
- jaringan komputer dan internet
## Mencari rute terpendek
Algoritma (Dijkstra) selalu mengambil simpul dengan jarak sementara terkecil, lalu memperbarui jarak tetangganya. Tekan tombol Cari Rute dan amati urutannya!
## Coba sendiri
Ada berapa sisi? Berapa derajat Warung? Adakah rute lain yang lebih pendek dari 5 km?
"""
LOG_TXT = """
# Logika Boolean
Hanya ada dua nilai: Benar (1) atau Salah (0).
## Operator dasar
!! AND: hasil 1 hanya jika dua-duanya 1
Contoh: boleh main HP jika PR selesai DAN sudah makan.
!! OR: hasil 0 hanya jika dua-duanya 0
Contoh: ke sekolah naik motor ATAU jalan kaki.
!! NOT: membalik nilai
Contoh: NOT hujan = tidak hujan.
!! XOR: hasil 1 jika kedua nilai BERBEDA
Contoh: ketua kelas hanya satu, Ani ATAU Budi, bukan keduanya.
## Tabel kebenaran
Daftar semua kemungkinan nilai masukan beserta hasilnya. Dua masukan (A dan B) menghasilkan 4 baris.
## Urutan pengerjaan
Tanda kurung, lalu NOT, lalu AND, lalu XOR, terakhir OR.
## Contoh: A = 1 dan B = 0
- A AND NOT B = 1 AND 1 = 1
- NOT (A OR B) = NOT 1 = 0
- (A AND B) OR NOT B = 0 OR 1 = 1
## Pola yang bisa ditemukan
++ AND bernilai 1 hanya pada satu baris (1,1)
++ OR bernilai 0 hanya pada satu baris (0,0)
++ XOR bernilai 1 jika A dan B berbeda
## Penerapan
- pencarian "kucing AND hitam"
- syarat lomba: kelas IX AND nilai >= 75
- percabangan JIKA pada program
## Coba sendiri
Ubah A dan B dengan tombol, lalu ketik ekspresimu dan buat tabel kebenarannya.
"""
ALGO_TXT = """
# Apa itu Algoritma?
Langkah-langkah yang jelas, berurutan, dan berhingga untuk menyelesaikan masalah.
## Ciri algoritma yang baik
- ada input (bahan awal), proses, dan output (hasil)
- setiap langkah jelas dan dapat dikerjakan
- urutannya benar dan ada akhirnya
## Cara menyajikan
- Kalimat: langkah ditulis berurutan
- Flowchart: diagram dengan simbol dan panah
- Pseudocode: mirip kode, tetapi memakai bahasa sehari-hari
## Simbol flowchart
- Oval: mulai atau selesai
- Jajar genjang: input atau output
- Persegi: proses
- Belah ketupat: keputusan (ya atau tidak)
- Anak panah: arah alur
## 3 struktur algoritma
!! Urutan: langkah dikerjakan satu per satu
!! Percabangan: JIKA hujan MAKA bawa payung, JIKA TIDAK pakai topi
!! Perulangan: ULANGI 5 kali: lompat
## Contoh 1: Ganjil atau Genap
Masukkan N. Jika N habis dibagi 2 maka cetak GENAP, jika tidak cetak GANJIL.
## Contoh 2: Mencari nilai terbesar
mulai
  terbesar = data pertama
  ulangi untuk setiap data berikutnya:
    jika data > terbesar maka terbesar = data
  tampilkan terbesar
selesai
## Tips menyusun algoritma
- pahami input dan output dulu
- pecah dengan dekomposisi
- uji dengan contoh sederhana, lalu perbaiki
"""
END_TXT = """
# Rangkuman
!! 4 Pilar: dekomposisi, abstraksi, pengenalan pola, dan algoritma
!! Tree: bertingkat (root, parent, child, leaf), n node punya n - 1 edge
!! Graf: simpul dan sisi, boleh berbobot; jumlah derajat = 2 x jumlah sisi
!! Logika: AND, OR, NOT, XOR dengan 1 = benar dan 0 = salah
!! Algoritma: input, proses, output; berupa urutan, percabangan, dan perulangan
# Refleksi
- Bagian mana yang paling mudah bagimu?
- Bagian mana yang masih membingungkan?
- Di mana kamu bisa memakai berpikir komputasional minggu ini?
# Tantangan
Pilih satu masalah (jadwal belajar atau rute berangkat sekolah), pecah dengan dekomposisi, tentukan data pentingnya, lalu tulis algoritma dan flowchart-nya.
++ Hebat! Kamu sudah menyelesaikan seluruh materi.
"""
QUIZ = [
("Cara menyelesaikan masalah dengan langkah rapi dan terstruktur seperti komputer disebut...", "Berpikir komputasional", ["Berpikir kritis", "Mengetik cepat", "Mengunduh data"], "Berpikir komputasional memecahkan masalah secara terstruktur."),
("Membagi masalah besar menjadi bagian-bagian kecil disebut...", "Dekomposisi", ["Abstraksi", "Algoritma", "Pengenalan pola"], "Dekomposisi = memecah masalah, seperti pensi dibagi menjadi acara, dana, publikasi."),
("Pada kartu pelajar, data yang diabaikan menurut abstraksi adalah...", "Warna sepatu", ["Nama", "NIS", "Foto"], "Abstraksi mengambil yang penting dan membuang detail yang tidak perlu."),
("Deret 2, 4, 6, 8 dilanjutkan dengan 10 karena menemukan...", "Pola tambah 2", ["Pola kali 2", "Pola acak", "Pola kurang 2"], "Setiap angka bertambah 2."),
("Langkah jelas dan berurutan untuk menyelesaikan masalah disebut...", "Algoritma", ["Graf", "Tree", "XOR"], "Algoritma = langkah jelas dan berurutan."),
("Node paling atas pada Tree disebut...", "Root", ["Leaf", "Edge", "Child"], "Root adalah akar, hanya ada satu."),
("Node paling bawah yang tidak punya child disebut...", "Leaf", ["Root", "Parent", "Edge"], "Leaf = daun."),
("Jika Tree memiliki 8 node, jumlah edge-nya adalah...", "7", ["8", "9", "6"], "Tree dengan n node memiliki n - 1 edge."),
("Jumlah sisi pada satu simpul graf disebut...", "Derajat", ["Bobot", "Level", "Root"], "Derajat = banyaknya sisi pada simpul."),
("Sebuah graf punya 7 sisi. Jumlah seluruh derajatnya adalah...", "14", ["7", "21", "49"], "Jumlah derajat = 2 x jumlah sisi = 14."),
("Rumah-Warung 2, Warung-Pasar 2, Pasar-Sekolah 1, Warung-Sekolah 4 (km). Rute terpendek Rumah ke Sekolah adalah...", "5 km", ["6 km", "7 km", "4 km"], "Rumah-Warung-Pasar-Sekolah = 2 + 2 + 1 = 5 km."),
("Hasil dari 1 AND 0 adalah...", "0", ["1", "Bisa 1 atau 0", "Tidak ada"], "AND hanya 1 jika dua-duanya 1."),
("Hasil dari 1 XOR 1 adalah...", "0", ["1", "Bisa 1 atau 0", "Tidak ada"], "XOR bernilai 1 hanya jika nilainya berbeda."),
("Jika A = 1 dan B = 0, hasil NOT (A OR B) adalah...", "0", ["1", "Bisa 1 atau 0", "Tidak ada"], "A OR B = 1, lalu NOT 1 = 0."),
("Pada flowchart, simbol belah ketupat dipakai untuk...", "Keputusan", ["Mulai/selesai", "Input/output", "Proses"], "Belah ketupat = keputusan (ya/tidak)."),
("Kalimat 'JIKA hujan MAKA bawa payung' adalah struktur...", "Percabangan", ["Urutan", "Perulangan", "Root"], "JIKA...MAKA = percabangan."),
("Dari data 5, 9, 3, 7, nilai terbesar yang ditemukan algoritma adalah...", "9", ["5", "3", "7"], "Algoritma membandingkan satu per satu hingga data terakhir."),
]
TREE = {'kep': ('Kepala Sekolah', 270, 50, None), 'kur': ('Waka Kurikulum', 140, 150, 'kep'), 'sis': ('Waka Kesiswaan', 400, 150, 'kep'),
        'tik': ('Guru TIK', 70, 260, 'kur'), 'ipa': ('Guru IPA', 210, 260, 'kur'), 'osis': ('Pembina OSIS', 340, 260, 'sis'),
        'pram': ('Pembina Pramuka', 470, 260, 'sis'), 'lab': ('Asisten Lab', 210, 365, 'ipa')}
GN = {'Rumah': (80, 240), 'Warung': (240, 130), 'Pasar': (240, 340), 'Sekolah': (455, 240), 'Taman': (430, 55)}
GE = [('Rumah', 'Warung', 2), ('Rumah', 'Pasar', 5), ('Warung', 'Pasar', 2), ('Warung', 'Sekolah', 4), ('Pasar', 'Sekolah', 1), ('Warung', 'Taman', 3), ('Taman', 'Sekolah', 6)]
GRAF = {n: [] for n in GN}
for _a, _b, _w in GE: GRAF[_a].append((_b, _w)); GRAF[_b].append((_a, _w))

def kids(k): return [x for x, v in TREE.items() if v[3] == k]
def level(k): return 0 if TREE[k][3] is None else 1 + level(TREE[k][3])
def pre(k): return [k] + [y for c in kids(k) for y in pre(c)]

# ===================== APLIKASI =====================
class App(tk.Tk):
    def __init__(s):
        super().__init__()
        s.title('Media Interaktif Berpikir Komputasional - Informatika Kelas IX')
        s.geometry('1180x700'); s.minsize(1100, 660); s.configure(bg=BG)
        s.gen = 0
        s.side = tk.Frame(s, bg=CARD, width=200); s.side.pack(side='left', fill='y'); s.side.pack_propagate(False)
        tk.Label(s.side, text='◆ BK Kelas IX', bg=CARD, fg=YE, font=(FN, 16, 'bold')).pack(pady=(20, 12))
        s.pages = [('Beranda', s.p_home), ('Pengantar', s.p_intro), ('4 Pilar', s.p_pilar), ('Tree (Pohon)', s.p_tree), ('Graf', s.p_graf),
                   ('Logika', s.p_logika), ('Algoritma', s.p_algo), ('Kuis', s.p_kuis), ('Rangkuman', s.p_end)]
        s.nb = []
        for i, (t, _) in enumerate(s.pages):
            b = tk.Button(s.side, text='  %d.  %s' % (i, t) if i else '  ▶  ' + t, anchor='w', bd=0, relief='flat', font=(FN, 12, 'bold'), bg=CARD, fg=W,
                          activebackground=PK, activeforeground=W, padx=10, pady=7, cursor='hand2', command=lambda i=i: s.show(i))
            b.pack(fill='x', padx=8, pady=2); s.nb.append(b)
        s.main = tk.Frame(s, bg=BG); s.main.pack(side='left', fill='both', expand=True)
        s.show(0)

    # ---- mesin animasi ----
    def show(s, i):
        s.gen += 1
        for w in s.main.winfo_children(): w.destroy()
        for j, b in enumerate(s.nb): b.config(bg=PK if j == i else CARD)
        s.pages[i][1]()
    def lp(s, ms, fn):
        g = s.gen
        def w():
            if g == s.gen: fn(); s.after(ms, w)
        s.after(ms, w)
    def at(s, ms, fn):
        g = s.gen; s.after(ms, lambda: fn() if g == s.gen else None)
    def anim(s, ms, fn, done=None):
        g = s.gen; n = max(1, ms // 30); i = [0]
        def st():
            if g != s.gen: return
            i[0] += 1; t = min(1, i[0] / n); fn(t * t * (3 - 2 * t))
            if t < 1: s.after(30, st)
            elif done: done()
        st()
    def btn(s, p, text, cmd, bg=PK, fg=W):
        return tk.Button(p, text=text, command=cmd, bg=bg, fg=fg, activebackground=YE, activeforeground=BG, bd=0, relief='flat', font=(FN, 11, 'bold'), padx=12, pady=6, cursor='hand2')

    # ---- kerangka halaman ----
    def split(s, title, sub=''):
        tk.Label(s.main, text=title, bg=BG, fg=YE, font=(FN, 21, 'bold'), anchor='w').pack(fill='x', padx=22, pady=(14, 0))
        tk.Label(s.main, text=sub, bg=BG, fg=MU, font=(FN, 11), anchor='w').pack(fill='x', padx=22)
        body = tk.Frame(s.main, bg=BG); body.pack(fill='both', expand=True, padx=18, pady=8)
        right = tk.Frame(body, bg=BG, width=540); right.pack(side='right', fill='y', padx=(14, 0)); right.pack_propagate(False)
        left = tk.Frame(body, bg=CARD); left.pack(side='left', fill='both', expand=True)
        t = tk.Text(left, width=10, wrap='word', bg=CARD, fg=W, bd=0, font=(FN, 11), padx=14, pady=10, cursor='arrow', spacing1=2, spacing3=3)
        sb = tk.Scrollbar(left, command=t.yview); t.config(yscrollcommand=sb.set); sb.pack(side='right', fill='y'); t.pack(side='left', fill='both', expand=True)
        for tag, kw in {'h': dict(foreground=YE, font=(FN, 14, 'bold'), spacing1=8), 's': dict(foreground=CY, font=(FN, 11, 'bold'), spacing1=6),
                        'k': dict(foreground=PK, font=(FN, 11, 'bold')), 'g': dict(foreground=GR, font=(FN, 11, 'bold'))}.items(): t.tag_config(tag, **kw)
        return t, right
    def write(s, t, md):
        t.config(state='normal'); t.delete('1.0', 'end')
        for ln in md.strip('\n').split('\n'):
            tag = ()
            if ln.startswith('# '): tag, ln = ('h',), ln[2:]
            elif ln.startswith('## '): tag, ln = ('s',), ln[3:]
            elif ln.startswith('!! '): tag, ln = ('k',), ln[3:]
            elif ln.startswith('++ '): tag, ln = ('g',), ln[3:]
            elif ln.startswith('- '): ln = '• ' + ln[2:]
            t.insert('end', ln + '\n', tag)
        t.config(state='disabled'); t.yview_moveto(0)
    def cv(s, r, h=500):
        c = tk.Canvas(r, width=540, height=h, bg=CV, highlightthickness=0); c.pack(); return c
    def arrow(s, c, *pts, col=MU): c.create_line(*pts, fill=col, width=2, arrow='last')

    # ---- 0 BERANDA ----
    def p_home(s):
        c = tk.Canvas(s.main, bg=BG, highlightthickness=0); c.pack(fill='both', expand=True); s.update_idletasks()
        Wd, Ht = max(c.winfo_width(), 900), max(c.winfo_height(), 600)
        dim = ['#0E7490', '#9D2460', '#9A8310', '#2A8A52']
        balls = [[random.randint(60, Wd - 60), random.randint(60, Ht - 60), random.choice([-2.2, -1.5, 1.5, 2.2]), random.choice([-1.8, -1.2, 1.2, 1.8]), random.randint(16, 44), random.choice(dim)] for _ in range(16)]
        ids = [c.create_oval(0, 0, 1, 1, fill=b[5], outline='') for b in balls]
        c.create_text(Wd // 2, Ht // 2 - 150, text='INFORMATIKA • KELAS IX • BAB 1', fill=CY, font=(FN, 14, 'bold'))
        ti = c.create_text(Wd // 2, Ht // 2 - 80, text='', fill=YE, font=(FN, 44, 'bold'))
        c.create_text(Wd // 2, Ht // 2 - 10, text='Yuk, belajar mikir kayak komputer!', fill=W, font=(FN, 20))
        c.create_text(Wd // 2, Ht // 2 + 30, text='Pilih menu di kiri, atau tekan tombol di bawah', fill=MU, font=(FN, 12))
        judul = 'Berpikir Komputasional'
        for k in range(len(judul) + 1): s.at(70 * k, lambda k=k: c.itemconfig(ti, text=judul[:k]))
        b = s.btn(c, 'Mulai Belajar  ▶', lambda: s.show(1)); b.config(font=(FN, 18, 'bold'), padx=24, pady=10)
        c.create_window(Wd // 2, Ht // 2 + 100, window=b)
        tog = [0]
        def pulse(): tog[0] ^= 1; b.config(bg=PK if tog[0] else '#FF8FC4')
        s.lp(500, pulse)
        def move():
            w, h = max(c.winfo_width(), 300), max(c.winfo_height(), 300)
            for bl, i in zip(balls, ids):
                bl[0] += bl[2]; bl[1] += bl[3]
                if bl[0] < bl[4] or bl[0] > w - bl[4]: bl[2] = -bl[2]
                if bl[1] < bl[4] or bl[1] > h - bl[4]: bl[3] = -bl[3]
                c.coords(i, bl[0] - bl[4], bl[1] - bl[4], bl[0] + bl[4], bl[1] + bl[4])
        s.lp(33, move)

    # ---- 1 PENGANTAR ----
    def p_intro(s):
        t, r = s.split('Pengantar Berpikir Komputasional', 'Apa, mengapa, dan bagaimana alurnya'); s.write(t, INTRO); c = s.cv(r, 500)
        st = [('Masalah', 'Cari rute ke sekolah', CY), ('Dekomposisi', 'Pecah menjadi ruas jalan', PK), ('Pola', 'Jam sibuk = macet berulang', YE),
              ('Abstraksi', 'Ambil jalan dan jarak saja', GR), ('Algoritma', 'Lurus, belok kiri, belok kanan', CY), ('Evaluasi', 'Uji dan perbaiki rute', PK)]
        bx = []
        for i, (a, b, col) in enumerate(st):
            y = 14 + i * 82
            rc = c.create_rectangle(50, y, 510, y + 60, fill=CARD, outline=col, width=2)
            c.create_text(70, y + 20, text=a, anchor='w', fill=col, font=(FN, 14, 'bold')); c.create_text(70, y + 42, text=b, anchor='w', fill=MU, font=(FN, 10))
            if i < 5: c.create_text(280, y + 71, text='▼', fill=MU)
            bx.append(rc)
        tok = c.create_oval(14, 28, 36, 50, fill=YE, outline=''); k = [0]
        def tick():
            i = k[0] % 6
            for j, rc in enumerate(bx): c.itemconfig(rc, fill=CARD2 if j == i else CARD, width=4 if j == i else 2)
            y = 14 + i * 82 + 19; c.coords(tok, 14, y, 36, y + 22); k[0] += 1
        tick(); s.lp(1100, tick)

    # ---- 2 PILAR ----
    def p_pilar(s):
        t, r = s.split('4 Pilar Berpikir Komputasional', 'Klik tiap pilar untuk melihat penjelasan dan animasinya')
        bar = tk.Frame(r, bg=BG); bar.pack(fill='x', pady=(0, 6)); c = s.cv(r, 465)
        cols = [CY, PK, YE, GR]; names = ['Dekomposisi', 'Abstraksi', 'Pola', 'Algoritma']; fs = [s.d_dekom, s.d_abs, s.d_pola, s.d_algo]; pb = []
        def pick(i):
            s.gen += 1
            for j, b in enumerate(pb): b.config(bg=cols[j] if j == i else CARD, fg=BG if j == i else W)
            s.write(t, PIL[i]); c.delete('all'); fs[i](c)
        for i, n in enumerate(names):
            b = s.btn(bar, n, lambda i=i: pick(i), CARD); b.pack(side='left', padx=3); pb.append(b)
        pick(0)
    def d_dekom(s, c):
        c.create_text(270, 24, text='Masalah besar: Pensi Sekolah', fill=YE, font=(FN, 14, 'bold'))
        big = c.create_rectangle(155, 180, 385, 280, fill=CY, outline=''); bt = c.create_text(270, 230, text='PENSI SEKOLAH', fill=BG, font=(FN, 15, 'bold'))
        parts = [('Acara', 'urutan penampil', PK), ('Dana', 'sponsor dan tiket', YE), ('Publikasi', 'poster dan medsos', GR), ('Perlengkapan', 'panggung dan sound', CY)]
        tg = [(20, 55), (290, 55), (20, 345), (290, 345)]; its = []
        for a, b, col in parts:
            its.append((c.create_rectangle(0, 0, 1, 1, fill=col, outline='', state='hidden'), c.create_text(0, 0, text=a, fill=BG, font=(FN, 13, 'bold'), state='hidden'), c.create_text(0, 0, text=b, fill=BG, font=(FN, 10), state='hidden')))
        def move(p):
            for (rc, t1, t2), (tx, ty) in zip(its, tg):
                x = 155 + (tx - 155) * p; y = 180 + (ty - 180) * p
                c.coords(rc, x, y, x + 230, y + 100); c.coords(t1, x + 115, y + 38); c.coords(t2, x + 115, y + 66)
        def go():
            c.itemconfig(big, state='hidden'); c.itemconfig(bt, state='hidden')
            for it in its:
                for i in it: c.itemconfig(i, state='normal')
            s.anim(1200, move, lambda: c.create_text(270, 245, text='Dipecah menjadi bagian kecil\nlebih mudah dikerjakan bersama', fill=W, font=(FN, 13, 'bold'), justify='center'))
        s.at(900, go)
    def d_abs(s, c):
        c.create_text(270, 24, text='Kartu Pelajar: data apa yang penting?', fill=YE, font=(FN, 14, 'bold'))
        items = [('Nama', 1), ('NIS', 1), ('Kelas', 1), ('Foto', 1), ('Warna sepatu', 0), ('Hobi', 0), ('Tinggi badan', 0), ('Makanan favorit', 0)]; rows = []
        for i, (n, ok) in enumerate(items):
            y = 50 + i * 46
            rows.append((c.create_rectangle(70, y, 470, y + 38, fill=CARD, outline=DK, width=2), c.create_text(90, y + 19, text=n, anchor='w', fill=W, font=(FN, 13, 'bold')), c.create_text(450, y + 19, text='', anchor='e', font=(FN, 12, 'bold')), ok))
        def res(i):
            rc, tx, st, ok = rows[i]
            if ok: c.itemconfig(rc, fill='#14532D', outline=GR); c.itemconfig(st, text='✔ dipakai', fill=GR)
            else: c.itemconfig(rc, fill=CV, outline=DK); c.itemconfig(tx, fill='#6C67A8'); c.itemconfig(st, text='✘ diabaikan', fill=PK)
        for i in range(8): s.at(600 + i * 600, lambda i=i: res(i))
        s.at(600 + 8 * 600, lambda: c.create_text(270, 438, text='Ambil yang penting, abaikan detail lainnya', fill=GR, font=(FN, 12, 'bold')))
    def d_pola(s, c):
        c.create_text(270, 24, text='Temukan polanya!', fill=YE, font=(FN, 14, 'bold'))
        vals = [2, 4, 6, 8, 10, 12]; bxs = []
        for i, v in enumerate(vals):
            x = 18 + i * 86; rc = c.create_rectangle(x, 90, x + 70, 150, fill=CARD, outline=YE, width=2, state='hidden')
            tx = c.create_text(x + 35, 120, text=str(v) if i < 4 else '?', fill=W, font=(FN, 18, 'bold'), state='hidden'); bxs.append((rc, tx))
            if i: c.create_text(x - 8, 75, text='+2', fill=PK, font=(FN, 11, 'bold'), state='hidden', tags=('pl%d' % i,))
        def show(i): c.itemconfig(bxs[i][0], state='normal'); c.itemconfig(bxs[i][1], state='normal'); c.itemconfig('pl%d' % i, state='normal')
        for i in range(6): s.at(500 + i * 450, lambda i=i: show(i))
        def rev():
            for i in (4, 5): c.itemconfig(bxs[i][0], fill='#14532D', outline=GR); c.itemconfig(bxs[i][1], text=str(vals[i]), fill=GR)
            c.create_text(270, 190, text='Pola: setiap angka ditambah 2', fill=GR, font=(FN, 13, 'bold'))
        s.at(500 + 6 * 450 + 400, rev)
        c.create_text(270, 270, text='Pola berulang dalam kehidupan: jadwal piket', fill=YE, font=(FN, 14, 'bold'))
        hr = ['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab']; dy = []
        for i, h in enumerate(hr):
            x = 18 + i * 86; dy.append(c.create_rectangle(x, 310, x + 70, 360, fill=CARD, outline=CY, width=2)); c.create_text(x + 35, 335, text=h, fill=W, font=(FN, 13, 'bold'))
        k = [0]
        def hl():
            for j, d in enumerate(dy): c.itemconfig(d, fill=PK if j == k[0] % 6 else CARD)
            k[0] += 1
        s.lp(600, hl); c.create_text(270, 400, text='Setiap minggu urutannya sama, jadi cukup dibuat satu kali', fill=MU, font=(FN, 11))
    def d_algo(s, c):
        c.create_text(270, 24, text='Algoritma: Cuci Tangan', fill=YE, font=(FN, 14, 'bold'))
        stp = ['Basahi tangan', 'Sabuni 20 detik', 'Bilas dengan air', 'Keringkan']; bx = []
        for i, n in enumerate(stp):
            y = 60 + i * 90; bx.append((c.create_rectangle(80, y, 460, y + 60, fill=CARD, outline=GR, width=2), c.create_text(100, y + 30, text='%d.  %s' % (i + 1, n), anchor='w', fill=W, font=(FN, 14, 'bold')), c.create_text(440, y + 30, text='', anchor='e', fill=GR, font=(FN, 16, 'bold'))))
            if i < 3: c.create_text(270, y + 75, text='▼', fill=MU)
        tok = c.create_oval(38, 78, 62, 102, fill=YE, outline='')
        def go(i):
            y = 60 + i * 90 + 18; c.coords(tok, 38, y, 62, y + 24); c.itemconfig(bx[i][0], fill='#14532D'); c.itemconfig(bx[i][2], text='✔')
        for i in range(4): s.at(700 + i * 1000, lambda i=i: go(i))
        s.at(700 + 4 * 1000, lambda: c.create_text(270, 440, text='Urutan benar → hasil benar!', fill=GR, font=(FN, 14, 'bold')))
        s.at(700 + 4 * 1000 + 2500, lambda: (c.delete('all'), s.d_algo(c)))

    # ---- 3 TREE ----
    def p_tree(s):
        t, r = s.split('Tree (Pohon)', 'Data bertingkat: root, parent, child, leaf'); s.write(t, TREE_TXT)
        c = s.cv(r, 425)
        info = tk.Label(r, text='Klik salah satu node untuk melihat perannya.', bg=BG, fg=MU, font=(FN, 11), wraplength=530, justify='left', height=3, anchor='nw'); info.pack(fill='x', pady=4)
        bar = tk.Frame(r, bg=BG); bar.pack(fill='x'); lv = [False]
        def draw(vis=(), cur=None):
            c.delete('all')
            for k, (l, x, y, p) in TREE.items():
                if p: c.create_line(TREE[p][1], TREE[p][2] + 17, x, y - 17, fill=MU, width=2)
            for k, (l, x, y, p) in TREE.items():
                col = PK if not p else (GR if not kids(k) else CY)
                if k in vis: col = YE
                tag = 'n_' + k
                c.create_rectangle(x - 62, y - 17, x + 62, y + 17, fill=col, outline=W if k == cur else '', width=3, tags=(tag,))
                c.create_text(x, y, text=l, fill=BG, font=(FN, 10, 'bold'), tags=(tag,))
                if lv[0]: c.create_text(x, y + 27, text='level %d' % level(k), fill=YE, font=(FN, 10, 'bold'))
                c.tag_bind(tag, '<Button-1>', lambda e, k=k: show_info(k))
            for i, (n, col) in enumerate([('root', PK), ('parent', CY), ('leaf', GR), ('dikunjungi', YE)]):
                c.create_rectangle(20 + i * 120, 405, 34 + i * 120, 417, fill=col, outline=''); c.create_text(40 + i * 120, 411, text=n, anchor='w', fill=MU, font=(FN, 10))
        def show_info(k):
            l, x, y, p = TREE[k]; ch = kids(k)
            peran = 'ROOT' if not p else ('LEAF' if not ch else 'PARENT sekaligus CHILD')
            info.config(text='%s  |  Peran: %s  |  Level: %d\nParent: %s\nChild: %s' % (l, peran, level(k), TREE[p][0] if p else '-', ', '.join(TREE[x][0] for x in ch) or '-'), fg=W)
        def tele():
            s.gen += 1; order = pre('kep'); draw()
            for i, k in enumerate(order):
                s.at(700 * (i + 1), lambda i=i, k=k: (draw(order[:i + 1], k), info.config(fg=GR, text='Urutan kunjungan (preorder):\n' + ' → '.join(TREE[x][0] for x in order[:i + 1]))))
        def tlevel(): lv[0] = not lv[0]; draw()
        def reset(): s.gen += 1; draw(); info.config(text='Klik salah satu node untuk melihat perannya.', fg=MU)
        for tx, cm in [('▶ Telusuri (Preorder)', tele), ('Tampilkan Level', tlevel), ('Reset', reset)]: s.btn(bar, tx, cm).pack(side='left', padx=3)
        draw()

    # ---- 4 GRAF ----
    def p_graf(s):
        t, r = s.split('Graf', 'Simpul, sisi, derajat, dan rute terpendek'); s.write(t, GRAF_TXT); c = s.cv(r, 410)
        log = tk.Label(r, text='Tekan "Cari Rute" untuk melihat Rumah menuju Sekolah.', bg=BG, fg=MU, font=(FN, 11), wraplength=530, justify='left', height=4, anchor='nw'); log.pack(fill='x', pady=4)
        bar = tk.Frame(r, bg=BG); bar.pack(fill='x'); S = {}
        def draw(dist=None, vis=(), cur=None, hot=(), path=(), deg=False):
            c.delete('all'); pe = set(zip(path, path[1:])) | set(zip(path[1:], path))
            for a, b, w in GE:
                (x1, y1), (x2, y2) = GN[a], GN[b]; on = (a, b) in pe
                c.create_line(x1, y1, x2, y2, fill=GR if on else (YE if (a, b) in hot or (b, a) in hot else DK), width=6 if on else 3)
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2; c.create_oval(mx - 14, my - 11, mx + 14, my + 11, fill=CV, outline=''); c.create_text(mx, my, text=str(w), fill=YE, font=(FN, 11, 'bold'))
            for n, (x, y) in GN.items():
                col = GR if n in path else (CY if n == cur else (CARD2 if n in vis else CARD))
                c.create_oval(x - 32, y - 32, x + 32, y + 32, fill=col, outline=CY if n in vis else MU, width=2)
                c.create_text(x, y, text=n, fill=BG if col in (GR, CY) else W, font=(FN, 10, 'bold'))
                if dist: c.create_text(x, y + 46, text='jarak: ' + str(dist[n]), fill=YE, font=(FN, 10, 'bold'))
                if deg: c.create_oval(x + 20, y - 44, x + 42, y - 22, fill=PK, outline=''); c.create_text(x + 31, y - 33, text=str(len(GRAF[n])), fill=W, font=(FN, 11, 'bold'))
        def cari():
            s.gen += 1; ev, path, tot = dijkstra(GRAF, 'Rumah', 'Sekolah'); dist = {n: '∞' for n in GN}; dist['Rumah'] = 0; vis = set(); draw(dist, cur='Rumah')
            for i, (u, d, rel) in enumerate(ev):
                def step(u=u, d=d, rel=rel):
                    vis.add(u)
                    for v, nd in rel: dist[v] = nd
                    draw(dist, vis, u, {(u, v) for v, _ in rel})
                    log.config(fg=W, text='Ambil %s (jarak %s km).\n%s' % (u, d, ('Perbarui: ' + ', '.join('%s = %s' % (v, nd) for v, nd in rel)) if rel else 'Tidak ada jarak yang diperbarui.'))
                s.at(1500 * (i + 1), step)
            s.at(1500 * (len(ev) + 1), lambda: (draw(dist, vis, None, (), path), log.config(fg=GR, text='Rute terpendek: ' + ' → '.join(path) + '  =  %s km' % tot)))
        def derajat():
            s.gen += 1; draw(deg=True); log.config(fg=W, text='Derajat: ' + ', '.join('%s %d' % (n, len(GRAF[n])) for n in GN) + '\nJumlah derajat = %d = 2 x %d sisi' % (sum(len(v) for v in GRAF.values()), len(GE)))
        def reset(): s.gen += 1; draw(); log.config(fg=MU, text='Tekan "Cari Rute" untuk melihat Rumah menuju Sekolah.')
        for tx, cm in [('▶ Cari Rute', cari), ('Tampilkan Derajat', derajat), ('Reset', reset)]: s.btn(bar, tx, cm).pack(side='left', padx=3)
        draw()

    # ---- 5 LOGIKA ----
    def p_logika(s):
        t, r = s.split('Logika Boolean', 'Ubah nilai A dan B, lalu amati lampunya'); s.write(t, LOG_TXT)
        st = {'A': 1, 'B': 0}; top = tk.Frame(r, bg=BG); top.pack(fill='x', pady=(0, 4)); c = s.cv(r, 170)
        ba = s.btn(top, '', lambda: tog('A'), CY, BG); bb = s.btn(top, '', lambda: tog('B'), PK, W); ba.pack(side='left', padx=3); bb.pack(side='left', padx=3)
        lamp = []
        for i, n in enumerate(['A AND B', 'A OR B', 'A XOR B', 'NOT A']):
            x = 70 + i * 132; lamp.append((c.create_oval(x - 38, 40, x + 38, 116, fill=DK, outline=MU, width=3), c.create_text(x, 78, text='', fill=BG, font=(FN, 26, 'bold'))))
            c.create_text(x, 140, text=n, fill=W, font=(FN, 12, 'bold'))
        fn = [lambda a, b: a & b, lambda a, b: a | b, lambda a, b: a ^ b, lambda a, b: 1 - a]
        def upd(flash=True):
            ba.config(text='A = %d  (klik)' % st['A']); bb.config(text='B = %d  (klik)' % st['B'])
            for i, ((o, tx), f) in enumerate(zip(lamp, fn)):
                v = f(st['A'], st['B']); x = 70 + i * 132
                c.itemconfig(o, fill=GR if v else '#7A2A52'); c.itemconfig(tx, text=str(v), fill=BG if v else W)
                if flash: s.anim(350, lambda p, o=o, x=x: c.coords(o, x - 38 - 8 * math.sin(math.pi * p), 40 - 8 * math.sin(math.pi * p), x + 38 + 8 * math.sin(math.pi * p), 116 + 8 * math.sin(math.pi * p)))
        def tog(k): st[k] ^= 1; upd()
        ef = tk.Frame(r, bg=BG); ef.pack(fill='x', pady=(8, 2)); tk.Label(ef, text='Ekspresi:', bg=BG, fg=YE, font=(FN, 11, 'bold')).pack(side='left')
        en = tk.Entry(ef, font=(FN, 12), bg=CARD, fg=W, insertbackground=W, bd=0, width=26); en.insert(0, 'A AND NOT B'); en.pack(side='left', padx=6, ipady=4)
        res = tk.Label(r, text='', bg=BG, fg=W, font=(FN, 12, 'bold'), anchor='w', wraplength=530, justify='left'); res.pack(fill='x', pady=2)
        tb = tk.Text(r, width=40, height=7, bg=CARD, fg=W, bd=0, font=('Consolas', 12), padx=12, pady=6); tb.pack(fill='x'); tb.tag_config('1', foreground=GR); tb.tag_config('0', foreground=PK); tb.tag_config('h', foreground=YE)
        def hit():
            try: v = hitung(en.get(), st['A'], st['B']); res.config(fg=GR if v else PK, text='Dengan A = %d, B = %d  →  hasil = %d' % (st['A'], st['B'], v))
            except ValueError as e: res.config(fg=PK, text=str(e))
        def tabel():
            tb.delete('1.0', 'end')
            try: rows = [(a, b, hitung(en.get(), a, b)) for a in (0, 1) for b in (0, 1)]
            except ValueError as e: res.config(fg=PK, text=str(e)); return
            res.config(fg=W, text='Tabel kebenaran: ' + en.get().upper()); tb.insert('end', ' A  B | hasil\n', 'h')
            for a, b, v in rows: tb.insert('end', ' %d  %d |   %d\n' % (a, b, v), str(v))
        s.btn(ef, 'Hitung', hit, GR, BG).pack(side='left', padx=2); s.btn(ef, 'Tabel', tabel).pack(side='left', padx=2)
        upd(False); tabel(); hit()

    # ---- 6 ALGORITMA ----
    def p_algo(s):
        t, r = s.split('Algoritma', 'Flowchart, mencari nilai terbesar, dan 3 struktur'); s.write(t, ALGO_TXT)
        bar = tk.Frame(r, bg=BG); bar.pack(fill='x', pady=(0, 4)); c = s.cv(r, 440)
        log = tk.Label(r, text='', bg=BG, fg=W, font=(FN, 11, 'bold'), wraplength=530, justify='left', height=2, anchor='nw'); log.pack(fill='x')
        ctl = tk.Frame(r, bg=BG); ctl.pack(fill='x'); tabs = []; cols = [CY, YE, GR]
        def demo(i):
            s.gen += 1; c.delete('all'); log.config(text='', fg=W)
            for w in ctl.winfo_children(): w.destroy()
            for j, b in enumerate(tabs): b.config(bg=cols[j] if j == i else CARD, fg=BG if j == i else W)
            [s.a_flow, s.a_max, s.a_struk][i](c, ctl, log)
        for i, n in enumerate(['Flowchart', 'Nilai Terbesar', 'Struktur']):
            b = s.btn(bar, n, lambda i=i: demo(i), CARD); b.pack(side='left', padx=3); tabs.append(b)
        demo(0)
    def a_flow(s, c, ctl, log):
        N = {'mulai': ('o', 270, 34, 'Mulai'), 'input': ('p', 270, 100, 'Input N'), 'dec': ('d', 270, 200, 'N habis\ndibagi 2?'), 'genap': ('r', 125, 320, 'Cetak: GENAP'),
             'ganjil': ('r', 415, 320, 'Cetak: GANJIL'), 'selesai': ('o', 270, 400, 'Selesai')}
        self_ids = {}
        c.create_line(270, 52, 270, 82, fill=MU, width=2, arrow='last'); c.create_line(270, 118, 270, 153, fill=MU, width=2, arrow='last')
        c.create_line(165, 200, 125, 200, 125, 298, fill=MU, width=2, arrow='last'); c.create_line(375, 200, 415, 200, 415, 298, fill=MU, width=2, arrow='last')
        c.create_line(125, 342, 125, 400, 210, 400, fill=MU, width=2, arrow='last'); c.create_line(415, 342, 415, 400, 330, 400, fill=MU, width=2, arrow='last')
        c.create_text(143, 188, text='Ya', fill=GR, font=(FN, 11, 'bold')); c.create_text(397, 188, text='Tidak', fill=PK, font=(FN, 11, 'bold'))
        for k, (sh, x, y, tx) in N.items():
            if sh == 'o': i = c.create_oval(x - 60, y - 18, x + 60, y + 18, fill=CARD, outline=PK, width=3)
            elif sh == 'p': i = c.create_polygon(x - 46, y - 18, x + 74, y - 18, x + 46, y + 18, x - 74, y + 18, fill=CARD, outline=CY, width=3)
            elif sh == 'd': i = c.create_polygon(x, y - 46, x + 105, y, x, y + 46, x - 105, y, fill=CARD, outline=YE, width=3)
            else: i = c.create_rectangle(x - 72, y - 22, x + 72, y + 22, fill=CARD, outline=GR, width=3)
            c.create_text(x, y, text=tx, fill=W, font=(FN, 11, 'bold'), justify='center'); self_ids[k] = i
        tok = c.create_oval(0, 0, 1, 1, fill=YE, outline='', state='hidden')
        tk.Label(ctl, text='N =', bg=BG, fg=YE, font=(FN, 12, 'bold')).pack(side='left'); en = tk.Entry(ctl, width=6, font=(FN, 12), bg=CARD, fg=W, insertbackground=W, bd=0, justify='center'); en.insert(0, '7'); en.pack(side='left', padx=6, ipady=4)
        def run():
            s.gen += 1
            try: n = int(en.get())
            except ValueError: log.config(fg=PK, text='Masukkan bilangan bulat, misalnya 7 atau 12.'); return
            for i in self_ids.values(): c.itemconfig(i, fill=CARD)
            sq = ['mulai', 'input', 'dec', 'genap' if n % 2 == 0 else 'ganjil', 'selesai']; c.itemconfig(tok, state='normal'); log.config(fg=W, text='Menjalankan algoritma dengan N = %d ...' % n)
            def hop(i, prev=None):
                if i >= len(sq): log.config(fg=GR, text='%d %% 2 = %d  →  %d adalah bilangan %s.' % (n, n % 2, n, 'GENAP' if n % 2 == 0 else 'GANJIL')); c.itemconfig(tok, state='hidden'); return
                k = sq[i]; x2, y2 = N[k][1], N[k][2]; x1, y1 = (N[prev][1], N[prev][2]) if prev else (x2, y2 - 40)
                def mv(p): x = x1 + (x2 - x1) * p; y = y1 + (y2 - y1) * p; c.coords(tok, x - 9, y - 9, x + 9, y + 9)
                def arr(): c.itemconfig(self_ids[k], fill='#6B5E00'); s.at(450, lambda: hop(i + 1, k))
                s.anim(600, mv, arr)
            hop(0)
        s.btn(ctl, '▶ Jalankan', run, GR, BG).pack(side='left', padx=4); s.btn(ctl, 'Reset', lambda: (setattr(s, 'gen', s.gen + 1), [c.itemconfig(i, fill=CARD) for i in self_ids.values()], c.itemconfig(tok, state='hidden'), log.config(text=''))).pack(side='left')
    def a_max(s, c, ctl, log):
        def setup():
            s.gen += 1; vals = random.sample(range(10, 100), 7); c.delete('all'); log.config(fg=W, text='Tekan Jalankan untuk mencari nilai terbesar.')
            c.create_text(270, 20, text='Cari nilai terbesar', fill=YE, font=(FN, 14, 'bold')); c.create_line(20, 400, 520, 400, fill=MU, width=2); bars = []
            for i, v in enumerate(vals):
                x = 28 + i * 70; h = v * 3.4
                bars.append((c.create_rectangle(x, 400 - h, x + 52, 400, fill=PK, outline=''), c.create_text(x + 26, 400 - h - 12, text=str(v), fill=W, font=(FN, 12, 'bold')), c.create_text(x + 26, 416, text='data[%d]' % i, fill=MU, font=(FN, 9))))
            mx = c.create_text(270, 50, text='', fill=GR, font=(FN, 12, 'bold')); ev = []; m = 0
            for i in range(1, len(vals)):
                nm = i if vals[i] > vals[m] else m; ev.append((i, m, nm)); m = nm
            def run():
                s.gen += 1; c.itemconfig(mx, text='terbesar sementara = %d' % vals[0])
                for b in bars: c.itemconfig(b[0], fill=PK)
                c.itemconfig(bars[0][0], fill=YE)
                for k, (i, m, nm) in enumerate(ev):
                    def st(i=i, m=m, nm=nm):
                        for j, b in enumerate(bars): c.itemconfig(b[0], fill=YE if j == m else PK)
                        c.itemconfig(bars[i][0], fill=CY)
                        log.config(fg=W, text='Bandingkan data[%d] = %d dengan %d.\n%s' % (i, vals[i], vals[m], 'Lebih besar, jadi terbesar diganti.' if nm != m else 'Tidak lebih besar, terbesar tetap.'))
                        s.at(650, lambda: (c.itemconfig(mx, text='terbesar sementara = %d' % vals[nm]), [c.itemconfig(b[0], fill=YE if j == nm else PK) for j, b in enumerate(bars)]))
                    s.at(1300 * (k + 1), st)
                fin = ev[-1][2]; s.at(1300 * (len(ev) + 1), lambda: (c.itemconfig(bars[fin][0], fill=GR), c.itemconfig(mx, text='HASIL: nilai terbesar = %d' % vals[fin]), log.config(fg=GR, text='Selesai! Nilai terbesar = %d (data[%d]).' % (vals[fin], fin))))
            ctl.pack_forget(); ctl.pack(fill='x')
            for w in ctl.winfo_children(): w.destroy()
            s.btn(ctl, '▶ Jalankan', run, GR, BG).pack(side='left', padx=4); s.btn(ctl, 'Acak Data', setup).pack(side='left', padx=4)
        setup()
    def a_struk(s, c, ctl, log):
        c.create_text(270, 20, text='Percabangan (JIKA ... MAKA ... JIKA TIDAK)', fill=YE, font=(FN, 13, 'bold'))
        dia = c.create_polygon(270, 45, 350, 95, 270, 145, 190, 95, fill=CARD, outline=YE, width=3); c.create_text(270, 95, text='Hujan?', fill=W, font=(FN, 13, 'bold'))
        yes = c.create_rectangle(40, 185, 230, 235, fill=CARD, outline=GR, width=3); c.create_text(135, 210, text='Bawa payung', fill=W, font=(FN, 12, 'bold'))
        no = c.create_rectangle(310, 185, 500, 235, fill=CARD, outline=PK, width=3); c.create_text(405, 210, text='Pakai topi', fill=W, font=(FN, 12, 'bold'))
        c.create_line(190, 95, 135, 95, 135, 183, fill=MU, width=2, arrow='last'); c.create_line(350, 95, 405, 95, 405, 183, fill=MU, width=2, arrow='last')
        c.create_text(165, 85, text='Ya', fill=GR, font=(FN, 11, 'bold')); c.create_text(375, 85, text='Tidak', fill=PK, font=(FN, 11, 'bold'))
        tok = c.create_oval(261, 36, 279, 54, fill=YE, outline='', state='hidden')
        def cab(ya):
            s.gen += 1; c.itemconfig(yes, fill=CARD); c.itemconfig(no, fill=CARD); c.itemconfig(tok, state='normal'); tx = 135 if ya else 405
            def mv(p):
                if p < 0.5: x = 270 + (tx - 270) * (p * 2); y = 45 + 50 * (p * 2)
                else: x = tx; y = 95 + 90 * ((p - 0.5) * 2)
                c.coords(tok, x - 9, y - 9, x + 9, y + 9)
            s.anim(1000, mv, lambda: (c.itemconfig(yes if ya else no, fill='#14532D' if ya else '#7A2A52'), log.config(fg=GR if ya else PK, text='Hujan = %s → %s.' % ('YA' if ya else 'TIDAK', 'bawa payung' if ya else 'pakai topi'))))
        c.create_text(270, 285, text='Perulangan (ULANGI 5 kali: lompat)', fill=YE, font=(FN, 13, 'bold')); ci = []
        for i in range(5): x = 60 + i * 105; ci.append(c.create_oval(x - 26, 330, x + 26, 382, fill=CARD, outline=CY, width=3)); c.create_text(x, 356, text=str(i + 1), fill=W, font=(FN, 14, 'bold'))
        cnt = c.create_text(270, 425, text='', fill=GR, font=(FN, 12, 'bold')); k = [0]
        def lompat():
            i = k[0] % 6
            for j, o in enumerate(ci): c.itemconfig(o, fill=PK if j == i - 1 else CARD)
            c.itemconfig(cnt, text='Lompat ke-%d' % i if i else 'Mulai ulang...'); k[0] += 1
        s.lp(800, lompat)
        s.btn(ctl, 'Hujan: YA', lambda: cab(True), GR, BG).pack(side='left', padx=4); s.btn(ctl, 'Hujan: TIDAK', lambda: cab(False), PK).pack(side='left', padx=4)
        log.config(fg=MU, text='Pilih kondisi hujan untuk melihat cabang yang dijalankan.')

    # ---- 7 KUIS ----
    def p_kuis(s):
        data = []
        for q, ok, wr, ex in random.sample(QUIZ, len(QUIZ)):
            o = [ok] + wr; random.shuffle(o); data.append((q, o, o.index(ok), ex))
        st = {'i': 0, 'sc': 0, 'wrong': [], 'lock': False}
        tk.Label(s.main, text='Kuis Kilat', bg=BG, fg=YE, font=(FN, 21, 'bold'), anchor='w').pack(fill='x', padx=22, pady=(14, 0))
        pb = tk.Canvas(s.main, height=14, bg=CARD, highlightthickness=0); pb.pack(fill='x', padx=22, pady=6); bar = pb.create_rectangle(0, 0, 0, 14, fill=GR, outline='')
        box = tk.Frame(s.main, bg=BG); box.pack(fill='both', expand=True, padx=22)
        def prog(n):
            w = max(pb.winfo_width(), 700); a = pb.coords(bar)[2]; b = w * n / len(data); s.anim(500, lambda p: pb.coords(bar, 0, 0, a + (b - a) * p, 14))
        def load():
            for w in box.winfo_children(): w.destroy()
            if st['i'] >= len(data): return fin()
            q, o, ans, ex = data[st['i']]; st['lock'] = False
            tk.Label(box, text='Soal %d dari %d' % (st['i'] + 1, len(data)), bg=BG, fg=CY, font=(FN, 12, 'bold'), anchor='w').pack(fill='x')
            tk.Label(box, text=q, bg=CARD, fg=W, font=(FN, 15, 'bold'), wraplength=820, justify='left', padx=16, pady=14, anchor='w').pack(fill='x', pady=8)
            bt = []
            for j, tx in enumerate(o):
                b = tk.Button(box, text='%s.  %s' % ('ABCD'[j], tx), anchor='w', bg=CARD2, fg=W, activebackground=CY, activeforeground=BG, bd=0, relief='flat', font=(FN, 13, 'bold'), padx=16, pady=9, cursor='hand2', command=lambda j=j: pick(j)); b.pack(fill='x', pady=3); bt.append(b)
            fb = tk.Label(box, text='', bg=BG, fg=W, font=(FN, 12, 'bold'), wraplength=820, justify='left', anchor='w'); fb.pack(fill='x', pady=6)
            nx = s.btn(box, 'Lanjut ▶', lambda: (st.__setitem__('i', st['i'] + 1), load()), GR, BG)
            def pick(j):
                if st['lock']: return
                st['lock'] = True; ok = j == ans; bt[ans].config(bg=GR, fg=BG); bt[j].config(bg=GR if ok else PK, fg=BG if ok else W)
                if ok: st['sc'] += 1
                else: st['wrong'].append((q, o[ans], ex))
                fb.config(fg=GR if ok else PK, text=('Benar! ' if ok else 'Belum tepat. ') + ex); prog(st['i'] + 1); nx.pack(anchor='e', pady=4)
        def fin():
            n = len(data); sc = st['sc']
            tk.Label(box, text='Kuis Selesai!', bg=BG, fg=YE, font=(FN, 26, 'bold')).pack(pady=(10, 0)); lab = tk.Label(box, text='Skor: 0 / %d' % n, bg=BG, fg=GR, font=(FN, 34, 'bold')); lab.pack()
            s.anim(1200, lambda p: lab.config(text='Skor: %d / %d' % (round(sc * p), n)))
            pct = sc / n; tk.Label(box, text='Luar biasa, kamu hebat!' if pct >= .85 else ('Bagus! Ulangi sedikit lagi.' if pct >= .6 else 'Ayo baca materinya lagi, lalu coba lagi.'), bg=BG, fg=W, font=(FN, 14, 'bold')).pack(pady=4)
            if st['wrong']:
                tk.Label(box, text='Soal yang perlu dipelajari lagi:', bg=BG, fg=CY, font=(FN, 12, 'bold'), anchor='w').pack(fill='x')
                tx = tk.Text(box, height=8, bg=CARD, fg=W, bd=0, font=(FN, 11), wrap='word', padx=10, pady=8); tx.pack(fill='x')
                for q, a, e in st['wrong']: tx.insert('end', '• %s\n   Jawaban: %s. %s\n' % (q, a, e))
                tx.config(state='disabled')
            row = tk.Frame(box, bg=BG); row.pack(pady=8); s.btn(row, 'Ulangi Kuis', lambda: s.show(7)).pack(side='left', padx=4); s.btn(row, 'Ke Rangkuman ▶', lambda: s.show(8), GR, BG).pack(side='left', padx=4)
        load()

    # ---- 8 RANGKUMAN ----
    def p_end(s):
        t, r = s.split('Rangkuman dan Refleksi', 'Selamat, kamu telah menyelesaikan materi!'); s.write(t, END_TXT); c = s.cv(r, 500)
        c.create_text(270, 230, text='SELAMAT!', fill=YE, font=(FN, 40, 'bold')); c.create_text(270, 285, text='Kamu sudah bisa berpikir\nseperti komputer', fill=W, font=(FN, 16), justify='center')
        ps = [[random.randint(0, 540), random.randint(-500, 0), random.uniform(2, 5), random.choice([CY, PK, YE, GR]), random.randint(6, 12)] for _ in range(60)]
        ids = [c.create_rectangle(0, 0, 1, 1, fill=p[3], outline='') for p in ps]
        def fall():
            for p, i in zip(ps, ids):
                p[1] += p[2]
                if p[1] > 510: p[1] = -10; p[0] = random.randint(0, 540)
                c.coords(i, p[0], p[1], p[0] + p[4], p[1] + p[4])
        s.lp(30, fall); s.btn(r, '↺ Kembali ke Beranda', lambda: s.show(0), PK).pack(pady=6)

if __name__ == '__main__':
    App().mainloop()
