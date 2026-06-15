import os
import django
import re
import hashlib

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tokobuku.settings')
django.setup()

from store.models import Book, Author, Publisher, Category

# Raw tab-separated data from the user
raw_data = """1	Bumi Manusia	Pramoedya Ananta Toer	Lentera Dipantara	9789799731234	1980	145,000	Diadaptasi menjadi Film (2019)
2	Laskar Pelangi	Andrea Hirata	Bentang Pustaka	9789791227032	2005	89,000	International Best Seller, Film (2008)
3	Ronggeng Dukuh Paruk	Ahmad Tohari	Gramedia Pustaka Utama	9789792277289	1982	105,000	Diadaptasi menjadi film Sang Penari
4	Sitti Nurbaya: Kasih Tak Sampai	Marah Rusli	Balai Pustaka	9789794071679	1922	65,000	Sastra klasik legendaris era Balai Pustaka
5	Cantik Itu Luka	Eka Kurniawan	Gramedia Pustaka Utama	9786020312583	2002	125,000	Pemenang World Readers' Award 2016
6	Madilog	Tan Malaka	Narasi	9789791683937	1943	95,000	Karya magnum opus filsafat Indonesia
7	Habis Gelap Terbitlah Terang	R.A. Kartini	Balai Pustaka	9789794070207	1911	55,000	Kumpulan surat emansipasi perempuan
8	Catatan Seorang Demonstran	Soe Hok Gie	LP3ES	9789798015793	1983	90,000	Buku harian asli, dasar Film Gie (2005)
9	Negeri 5 Menara	Ahmad Fuadi	Gramedia Pustaka Utama	9789792248197	2009	88,000	Diadaptasi menjadi Film layar lebar (2012)
10	Perahu Kertas	Dee Lestari	Bentang Pustaka	9789791227780	2009	99,000	Diadaptasi menjadi Film 2 bagian (2012)
11	Salah Asuhan	Abdoel Moeis	Balai Pustaka	9789794070627	1928	58,000	Diangkat menjadi film klasik tahun 1972
12	Azab dan Sengsara	Merari Siregar	Balai Pustaka	9789794070009	1920	48,000	Novel modern pertama berbahasa Indonesia
13	Tenggelamnya Kapal Van der Wijck	Buya Hamka	Gema Insani	9786022501916	1938	70,000	Sastra roman Islam terbesar, Film (2013)
14	Di Bawah Lindungan Ka'bah	Buya Hamka	Gema Insani	9786022501909	1938	50,000	Ditulis tahun 1938, dua kali difilmkan
15	Layar Terkembang	Sutan Takdir Alisjahbana	Balai Pustaka	9789794070498	1936	55,000	Karya utama era Pujangga Baru
16	Belenggu	Armijn Pane	Balai Pustaka	9789794070214	1940	55,000	Novel psikologis pertama Indonesia
17	Ateis	Achdiat K. Mihardja	Balai Pustaka	9789794071853	1949	65,000	Meraih Penghargaan Pemerintah RI (1969)
18	Student Hidjo	Mas Marco K.	Yayasan Aksara Indonesia	9789799542823	1918	55,000	Pelopor sastra pergerakan pra-kemerdekaan
19	Hikayat Kadiroen	Semaoen	Sega Arsy	9786028635196	1920	48,000	Ditulis oleh tokoh pergerakan kiri (1920)
20	Kalau Tak Untung	Selasih	Balai Pustaka	9789794070900	1933	48,000	Novel pertama oleh penulis perempuan
21	Sukreni Gadis Bali	I Gusti Nyoman P. T.	Balai Pustaka	9789794070719	1936	50,000	Mengangkat hukum karma dalam kultur Bali
22	Katak Hendak Jadi Lembu	Nur Sutan Iskandar	Balai Pustaka	9789794070580	1935	55,000	Sindiran tajam terhadap feodalisme priyayi
23	Sengsara Membawa Nikmat	Tulis Sutan Sati	Balai Pustaka	9789794070634	1929	60,000	Diadaptasi menjadi serial legendaris TVRI
24	Gadis Pantai	Pramoedya Ananta Toer	Lentera Dipantara	9789799731227	1987	85,000	Kisah tragis paksaan menjadi selir priyayi
25	Bukan Pasar Malam	Pramoedya Ananta Toer	Lentera Dipantara	9789799731210	1951	55,000	Novel pendek reflektif mengenai kematian
26	Anak Semua Bangsa	Pramoedya Ananta Toer	Lentera Dipantara	9789799731241	1980	130,000	Buku kedua Tetralogi Buru
27	Jejak Langkah	Pramoedya Ananta Toer	Lentera Dipantara	9789799731258	1985	140,000	Buku ketiga Tetralogi Buru
28	Rumah Kaca	Pramoedya Ananta Toer	Lentera Dipantara	9789799731265	1988	135,000	Buku penutup Tetralogi Buru
29	Saman	Ayu Utami	Kepustakaan Populer Gramedia	9789799023179	1998	68,000	Pemenang Sayembara Novel DKJ 1998
30	Larung	Ayu Utami	Kepustakaan Populer Gramedia	9789799100146	2001	70,000	Sekuel dari novel gerakan bawah tanah Saman
31	Sang Penari	Ahmad Tohari	Gramedia Pustaka Utama	9789792277289	1982	105,000	Edisi omnibus bersatu dari trilogi Ronggeng
32	Amba	Laksmi Pamuntjak	Gramedia Pustaka Utama	9789792288001	2012	100,000	Pemenang LiBeraturpreis Jerman 2016
33	Pulang	Leila S. Chudori	Kepustakaan Populer Gramedia	978979105158	2012	90,000	Pemenang Khatulistiwa Literary Award 2013
34	Laut Bercerita	Leila S. Chudori	Kepustakaan Populer Gramedia	9786024246938	2017	110,000	Mega Best Seller, bertema aktivis '98
35	Lelaki Harimau	Eka Kurniawan	Gramedia Pustaka Utama	9786020305882	2004	80,000	Nominasi Man Booker International Prize
36	Seperti Dendam, Rindu Harus Dibayar Tuntas	Eka Kurniawan	Gramedia Pustaka Utama	9786020304199	2014	88,000	Filmnya menang Golden Leopard di Locarno
37	Burung-Burung Manyar	Y.B. Mangunwijaya	Gramedia Pustaka Utama	9789792210088	1981	90,000	Menang Penghargaan Sastra Asia Tenggara 1983
38	Sri Sumarah	Umar Kayam	Pustaka Utama Grafiti	9789794441091	1975	60,000	Memotret karakter keteguhan wanita Jawa
39	Para Priyayi	Umar Kayam	Gramedia Pustaka Utama	9789792241518	1992	90,000	Pemenang Hadiah Yayasan Buku Utama Depdikbud
40	Jalan Tak Ada Ujung	Mochtar Lubis	Yayasan Pustaka Obor	9789794611081	1952	60,000	Meraih penghargaan sastra BMKN 1952
41	Senja di Jakarta	Mochtar Lubis	Yayasan Pustaka Obor	9789794611180	1963	70,000	Novel Indonesia pertama terbit dalam Bhs Inggris
42	Olenka	Budi Darma	Balai Pustaka	9789794072812	1983	68,000	Pemenang Hadiah Pertama Sayembara Novel DKJ
43	Orang-Orang Bloomington	Budi Darma	Noura Books	9232422117	1980	85,000	Diterbitkan internasional oleh Penguin Classics
44	Pada Sebuah Kapal	Nh. Dini	Gramedia Pustaka Utama	9786020334202	1973	85,000	Karya pilar feminisme sastra Indonesia
45	Namaku Hiroko	Nh. Dini	Gramedia Pustaka Utama	9786020331614	1977	70,000	Novel trans-kultural berlatar kota Jepang
46	Telegram	Putu Wijaya	Pustaka Firdaus	978979410140	1973	50,000	Novel eksperimental bercorak surealisme
47	Khotbah di Atas Danau	Kuntowijoyo	Basabasi	9786026651815	1976	68,000	Eksplorasi sufistik manusia modern
48	Ca-Bau-Kan	Remy Sylado	Kepustakaan Populer Gramedia	9789799100061	1999	98,000	Diadaptasi menjadi film layar lebar (2002)
49	Gadis Kretek	Ratih Kumala	Gramedia Pustaka Utama	9789792281439	2012	95,000	Diadaptasi menjadi Serial Orisinal Netflix
50	Raden Mandasia Si Pencuri Daging Sapi	Yusi Avianto Pareanom	Banana	9789791079525	2016	105,000	Pemenang Kusala Sastra Khatulistiwa 2016
51	Sang Pemimpi	Andrea Hirata	Bentang Pustaka	9789791227094	2006	84,000	Buku kedua tetralogi Laskar Pelangi, Film (2009)
52	Edensor	Andrea Hirata	Bentang Pustaka	9789791227025	2007	84,000	Nominasi Khatulistiwa Literary Award
53	Maryamah Karpov	Andrea Hirata	Bentang Pustaka	9789791227452	2008	94,000	Buku penutup kisah perjuangan masa muda Ikal
54	Ranah 3 Warna	Ahmad Fuadi	Gramedia Pustaka Utama	9789792258448	2011	89,000	Sekuel Negeri 5 Menara, diadaptasi ke Film
55	Rantau 1 Muara	Ahmad Fuadi	Gramedia Pustaka Utama	9786020300375	2013	89,000	Seri penutup trilogi dunia kerja internasional
56	Ayat-Ayat Cinta	Habiburrahman El S.	Republika	9789793210452	2004	89,000	Pelopor kebangkitan fiksi islami modern
57	Ketika Cinta Bertasbih	Habiburrahman El S.	Republika	9789791102148	2007	95,000	Sukses diadaptasi menjadi film layar lebar
58	Hafalan Shalat Delisa	Tere Liye	Republika	9786232791657	2005	69,000	Kisah paska Tsunami Aceh 2004, Film (2011)
59	Moga Bunda Disayang Allah	Tere Liye	Republika	9786232791671	2005	79,000	Kisah perjuangan disabilitas, Film (2013)
60	Daun Yang Jatuh Tak Pernah Membenci Angin	Tere Liye	Gramedia Pustaka Utama	9786020331607	2010	69,000	Novel melankolis romantis cetak ulang masif
61	Bumi	Tere Liye	Gramedia Pustaka Utama	9786020332956	2014	99,000	Seri fantasi Dunia Paralel paling sukses
62	Pulang	Tere Liye	SabakGrip	9786239767303	2015	89,000	Novel aksi petualangan shadow economy
63	5 cm	Donny Dhirgantoro	Grasindo	9789797524944	2005	88,000	Filmnya memicu tren pendakian gunung masif
64	Supernova: Ksatria, Puteri, & Bintang Jatuh	Dee Lestari	Bentang Pustaka	9786022912446	2001	89,000	Dobrakan fiksi sains kontemporer, Film (2014)
65	Madre	Dee Lestari	Bentang Pustaka	9786028811422	2011	68,000	Kumpulan fiksi pendek, Adaptasi Film (2013)
66	Filosofi Kopi	Dee Lestari	Bentang Pustaka	9786022913535	2006	69,000	Sukses memicu tren kedai kopi modern & Film
67	Aroma Karsa	Dee Lestari	Bentang Pustaka	9786022914631	2018	135,000	Pemenang Book of the Year IKAPI Awards 2018
68	Critical Eleven	Ika Natassa	Gramedia Pustaka Utama	9786020318622	2015	95,000	Pelopor novel genre Metropop, Film (2017)
69	The Architecture of Love	Ika Natassa	Gramedia Pustaka Utama	9786020329260	2016	99,000	Berlatar kota New York, Sukses difilmkan
70	Sabtu Bersama Bapak	Adhitya Mulya	Bukune	9786022201847	2014	75,000	Novel keluarga populer, Adaptasi Serial TV
71	Di Bawah Bendera Revolusi	Soekarno	Yayasan Bung Karno	N/A (Edisi Khusus)	1959	450,000	Kompilasi tulisan/pidato asli Bung Karno
72	Demokrasi Kita	Mohammad Hatta	Sega Arsy	9786028635332	1960	48,000	Esai politik kritis dari sang Proklamator
73	Mohammad Hatta: Memoir	Mohammad Hatta	Kompas	9789797096670	1979	135,000	Rekam jejak sejarah jujur Bung Hatta
74	Dari Penjara ke Penjara	Tan Malaka	Narasi	9789791684347	1948	115,000	Otobiografi perjuangan yang sangat legendaris
75	Massa Actie	Tan Malaka	Narasi	9789791684125	1926	55,000	Pamflet politik inspirasi pledoi Bung Karno
76	Manusia Indonesia	Mochtar Lubis	Yayasan Pustaka Obor	9789794611487	1977	48,000	Membedah ciri-ciri sifat miring bangsa
77	Perubahan Sosial di Yogyakarta	Selo Soemardjan	Komunitas Bambu	9786029402124	1962	100,000	Rujukan sosiologi klasik sistem kemasyarakatan
78	Kebudayaan Mentalitas & Pembangunan	Koentjaraningrat	Gramedia Pustaka Utama	9789792224535	1974	70,000	Buku wajib studi antropologi di Indonesia
79	Islam, Kemodernan, & Keindonesiaan	Nurcholish Madjid	Mizan	9789794335345	1987	89,000	Pemikiran pembaharuan Islam inklusif Cak Nur
80	Catatan Pinggir (Jilid 1)	Goenawan Mohamad	Tempo / Grafiti	9789795113942	1982	95,000	Kumpulan esai humaniora dari Majalah Tempo
81	Aku Ini Binatang Jalang	Chairil Anwar	Gramedia Pustaka Utama	9789792218718	1986	68,000	Kompilasi lengkap puisi pelopor Angkatan '45
82	Deru Campur Debu	Chairil Anwar	Dian Rakyat	9789795230236	1949	45,000	Kumpulan puisi orisinal cetakan tahun 1949
83	Hujan Bulan Juni	Sapardi Djoko Damono	Gramedia Pustaka Utama	9786020318431	1994	65,000	Diadaptasi jadi Novel, Musikalisasi, & Film
84	Melipat Jarak	Sapardi Djoko Damono	Gramedia Pustaka Utama	9786020331621	2015	58,000	Kumpulan puisi pilihan kurun waktu 1998-2015
85	Tirani dan Benteng	Taufiq Ismail	Yayasan Indonesia	N/A (Edisi Sastra)	1966	55,000	Kumpulan puisi aksi demonstrasi mahasiswa '66
86	Nyanyian Akar Rumput	Wiji Thukul	Gramedia Pustaka Utama	9786020301419	2014	65,000	Puisi perlawanan dari penyair rakyat
87	Sepotong Senja untuk Pacarku	Seno Gumira A.	Gramedia Pustaka Utama	9786020324838	2002	75,000	Kumpulan cerpen romantis-surealis paling ikonik
88	Saksi Mata	Seno Gumira A.	Bentang Pustaka	9786022912521	1994	65,000	Menang Dinny O'Hearn Prize Australia 1997
89	Sebuah Pertanyaan untuk Cinta	Seno Gumira A.	Gramedia Pustaka Utama	9786020325170	2016	68,000	Kompilasi cerpen urban potret psikologi kota
90	Godlob	Danarto	Divapress	9786023916023	1974	58,000	Cerpen eksperimental bercorak sufisme magis
91	Tanpa Tanda Jasa	Sartono Kartodirdjo	Gitanyali	978979863416	1992	70,000	Otobiografi bapak sejarah modern Indonesia
92	Pemberontakan Petani Banten 1888	Sartono Kartodirdjo	Komunitas Bambu	9786029402001	1966	120,000	Disertasi induk penulisan sejarah Indonesia
93	Nusa Jawa: Silang Budaya	Denys Lombard	Gramedia Pustaka Utama	9789796054527	1996	330,000	Edisi kajian komprehensif sejarah total Jawa
94	Indonesia Poenja Cerita	@InfoHistori	Bentang Pustaka	9786028811774	2011	58,000	Buku ringkas sejarah populer generasi muda
95	Guritan Kesunyian	Sitor Situmorang	Pustaka Jaya	9789794193303	2002	50,000	Karya kumpulan puisi sastrawan Angkatan '45
96	Sang Guru	Gerson Poyk	Divapress	9786023913077	1971	55,000	Novel kritis nasib dan idealisme guru pelosok
97	Laporan dari Banaran	T.B. Simatupang	Sinar Harapan	9789794160411	1960	70,000	Memoar militer otentik taktik perang gerilya
98	Kuantar ke Gerbang	Ramadhan K.H.	Kompas	9789797098179	1981	80,000	Biografi kisah Inggit Garnasih & Bung Karno
99	Catatan Subversif	Mochtar Lubis	Yayasan Pustaka Obor	9789794618783	1980	70,000	Catatan harian berkala saat ditahan rezim
100	Kamus Umum Bahasa Indonesia	W.J.S. P.	Balai Pustaka	9789794073307	1952	165,000	Kamus legendaris rujukan leksikografi awal"""

def clean_isbn(isbn, title):
    # Bersihkan karakter non-alphanumeric
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', isbn)
    if len(cleaned) < 10 or cleaned.lower() == 'na':
        # Generate mock ISBN menggunakan MD5 hash dari judul
        cleaned = "MOCK" + hashlib.md5(title.encode('utf-8')).hexdigest()[:9].upper()
    return cleaned[:13]

def run_import():
    print("Memulai proses impor data buku dari teks...")
    lines = raw_data.strip().split('\n')
    
    # Kategori default dan kategori sosial/sejarah
    cat_fiksi, _ = Category.objects.get_or_create(name="Fiksi & Sastra")
    cat_sosial, _ = Category.objects.get_or_create(name="Sosial & Politik")
    cat_sejarah, _ = Category.objects.get_or_create(name="Sejarah")
    
    # Kata kunci untuk mengelompokkan kategori secara otomatis
    sejarah_keywords = ['sejarah', 'perjuangan', 'revolusi', 'memoar', 'otobiografi', 'biografi', 'catatan', 'kamus']
    sosial_keywords = ['filsafat', 'politik', 'sosial', 'antropologi', 'sosiologi', 'kebudayaan', 'mentalitas', 'demokrasi']
    
    imported_count = 0
    used_isbns = set(Book.objects.values_list('isbn', flat=True))
    
    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) < 7:
            continue
        
        # Mapping kolom:
        # 0: No, 1: Judul Buku, 2: Penulis, 3: Penerbit Utama, 4: ISBN, 5: Tahun Terbit, 6: Harga Jual, 7: Detail
        title = parts[1].strip()
        author_name = parts[2].strip()
        publisher_name = parts[3].strip()
        raw_isbn = parts[4].strip()
        
        try:
            pub_year = int(parts[5].strip())
        except ValueError:
            pub_year = 2000
            
        try:
            selling_price = float(parts[6].strip().replace(',', ''))
        except ValueError:
            selling_price = 75000.0
            
        detail = parts[7].strip() if len(parts) > 7 else ""
        
        # 1. Pastikan Author terdaftar
        author, _ = Author.objects.get_or_create(name=author_name)
        
        # 2. Pastikan Publisher terdaftar
        publisher, _ = Publisher.objects.get_or_create(
            name=publisher_name,
            defaults={
                'address': 'Alamat Default Penerbit',
                'phone_num': '0210000000'
            }
        )
        
        # 3. Klasifikasi Kategori secara cerdas
        check_text = (title + " " + detail).lower()
        if any(kw in check_text for kw in sejarah_keywords):
            category = cat_sejarah
        elif any(kw in check_text for kw in sosial_keywords):
            category = cat_sosial
        else:
            category = cat_fiksi
            
        # 4. Amankan ISBN yang unik
        isbn = clean_isbn(raw_isbn, title)
        
        if isbn in used_isbns:
            # Jika duplikat, buat modifikasi mock ISBN agar tidak error primary key
            h = hashlib.md5((title + raw_isbn).encode('utf-8')).hexdigest()[:9].upper()
            isbn = "MOCK" + h
            counter = 1
            original_mock = isbn
            while isbn in used_isbns:
                isbn = original_mock[:10] + f"{counter:03d}"
                counter += 1
                
        used_isbns.add(isbn)
        
        # 5. Nilai stok acak agar dashboard bervariasi (beberapa di bawah min_quantity)
        # Kami menggunakan min_quantity = 5.
        # Jika digit terakhir ISBN ganjil, set stok = 2 (Kritis). Jika genap, set stok = 15 (Aman).
        min_qty = 5
        last_char = isbn[-1]
        if last_char.isdigit() and int(last_char) % 2 != 0:
            stock_qty = 2  # Stok kritis
        else:
            stock_qty = 15 # Stok aman
            
        # 6. Simpan Buku ke Database
        # Gunakan update_or_create agar data ter-update jika dijalankan ulang
        book, created = Book.objects.update_or_create(
            isbn=isbn,
            defaults={
                'title': title,
                'author': author,
                'publisher': publisher,
                'category': category,
                'publication_year': pub_year,
                'selling_price': selling_price,
                'min_quantity': min_qty,
                'page_count': 250, # Nilai default halaman
                'stock_quantity': stock_qty
            }
        )
        imported_count += 1
        
    print(f"Berhasil mengimpor {imported_count} buku ke database.")

if __name__ == '__main__':
    run_import()
