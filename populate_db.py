import os
import django
from datetime import date, datetime

# Setup Django Environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tokobuku.settings')
django.setup()

from store.models import Person, Staff, Manager, Author, Category, Publisher, Book, Sale, BookOrder

def populate():
    print("Memulai pengisian data dummy (Database Seeding)...")
    
    # 1. Bersihkan data lama agar bersih
    BookOrder.objects.all().delete()
    Sale.objects.all().delete()
    Book.objects.all().delete()
    Publisher.objects.all().delete()
    Category.objects.all().delete()
    Author.objects.all().delete()
    Manager.objects.all().delete()
    Staff.objects.all().delete()
    Person.objects.all().delete()

    print("Data lama berhasil dihapus.")

    # 2. Membuat Data Person (Orang)
    # Staf
    p1 = Person.objects.create(fname="Budi", lname="Santoso", phone_num="08123456789", email="budi@tokobuku.com", password="password123")
    p2 = Person.objects.create(fname="Siti", lname="Aminah", phone_num="08234567890", email="siti@tokobuku.com", password="password123")
    p3 = Person.objects.create(fname="Rian", lname="Hidayat", phone_num="08345678901", email="rian@tokobuku.com", password="password123")
    
    # Manajer
    p4 = Person.objects.create(fname="Dewi", lname="Lestari", phone_num="08456789012", email="dewi.mgr@tokobuku.com", password="password123")
    
    # Pelanggan
    p5 = Person.objects.create(fname="Andi", lname="Pratama", phone_num="08567890123", email="andi.pratama@gmail.com", password="password123")
    p6 = Person.objects.create(fname="Rina", lname="Amalia", phone_num="08678901234", email="rina.amalia@gmail.com", password="password123")
    p7 = Person.objects.create(fname="Fahmi", lname="Idris", phone_num="08789012345", email="fahmi.idris@gmail.com", password="password123")

    print(f"Berhasil membuat {Person.objects.count()} orang.")

    # 3. Membuat Data Staff (Staf)
    s1 = Staff.objects.create(person=p1, role="Kasir Senior", weekly_hours=40.00, certification_status="Certified Professional Cashier")
    s2 = Staff.objects.create(person=p2, role="Kasir Junior", weekly_hours=32.50, certification_status="In Progress")
    s3 = Staff.objects.create(person=p3, role="Staf Gudang", weekly_hours=38.00, certification_status="")

    print(f"Berhasil membuat {Staff.objects.count()} staf.")

    # 4. Membuat Data Manager (Manajer)
    m1 = Manager.objects.create(person=p4, bonus_level="LEVEL_A", department="Operasional Utama", office_location="Lantai 2, Ruang M-01", hired_date=date(2023, 1, 15))

    print(f"Berhasil membuat {Manager.objects.count()} manajer.")

    # 5. Membuat Data Author (Penulis)
    a1 = Author.objects.create(name="Andrea Hirata")
    a2 = Author.objects.create(name="Tere Liye")
    a3 = Author.objects.create(name="Pramoedya Ananta Toer")
    a4 = Author.objects.create(name="Dee Lestari")
    a5 = Author.objects.create(name="Robert T. Kiyosaki")

    print(f"Berhasil membuat {Author.objects.count()} penulis.")

    # 6. Membuat Data Category (Kategori)
    cat1 = Category.objects.create(name="Fiksi & Sastra")
    cat2 = Category.objects.create(name="Pengembangan Diri")
    cat3 = Category.objects.create(name="Sains & Matematika")
    cat4 = Category.objects.create(name="Ekonomi & Bisnis")
    cat5 = Category.objects.create(name="Komputer & Teknologi")

    print(f"Berhasil membuat {Category.objects.count()} kategori.")

    # 7. Membuat Data Publisher (Penerbit)
    pub1 = Publisher.objects.create(name="Gramedia Pustaka Utama", address="Jl. Palmerah Barat No. 29, Jakarta", phone_num="02153650110")
    pub2 = Publisher.objects.create(name="Bentang Pustaka", address="Jl. Plemburan No. 21, Yogyakarta", phone_num="0274889988")
    pub3 = Publisher.objects.create(name="Mizan Publishing", address="Jl. Cinambo No. 135, Bandung", phone_num="0227834310")

    print(f"Berhasil membuat {Publisher.objects.count()} penerbit.")

    # 8. Membuat Data Book (Buku)
    # Catatan: Sengaja membuat beberapa buku dengan stok di bawah min_quantity untuk melihat warning "Stok Kritis"
    b1 = Book.objects.create(
        isbn="9789791227025",
        title="Laskar Pelangi",
        author=a1,
        publisher=pub2,
        category=cat1,
        publication_year=2005,
        selling_price=85000.00,
        min_quantity=10,
        page_count=529,
        stock_quantity=15  # Stok aman (15 > 10)
    )

    b2 = Book.objects.create(
        isbn="9786020332949",
        title="Hujan",
        author=a2,
        publisher=pub1,
        category=cat1,
        publication_year=2016,
        selling_price=95000.00,
        min_quantity=8,
        page_count=320,
        stock_quantity=3  # Stok Kritis (3 <= 8)
    )

    b3 = Book.objects.create(
        isbn="9789799731235",
        title="Bumi Manusia",
        author=a3,
        publisher=pub3,
        category=cat1,
        publication_year=1980,
        selling_price=120000.00,
        min_quantity=5,
        page_count=535,
        stock_quantity=2  # Stok Kritis (2 <= 5)
    )

    b4 = Book.objects.create(
        isbn="9789793780146",
        title="Filosofi Teras",
        author=a4, # Asumsi saja
        publisher=pub1,
        category=cat2,
        publication_year=2018,
        selling_price=79000.00,
        min_quantity=15,
        page_count=320,
        stock_quantity=20  # Stok aman (20 > 15)
    )

    b5 = Book.objects.create(
        isbn="9780446677455",
        title="Rich Dad Poor Dad",
        author=a5,
        publisher=pub1,
        category=cat4,
        publication_year=1997,
        selling_price=68000.00,
        min_quantity=10,
        page_count=336,
        stock_quantity=8  # Stok Kritis (8 <= 10)
    )

    print(f"Berhasil membuat {Book.objects.count()} buku.")

    # 9. Membuat Data Sale (Transaksi Penjualan)
    # Method save() otomatis menghitung total_amount (quantity * unit_price)
    s_tr1 = Sale.objects.create(staff=s1, book=b1, quantity=3, unit_price=85000.00)
    s_tr2 = Sale.objects.create(staff=s2, book=b2, quantity=5, unit_price=95000.00)
    s_tr3 = Sale.objects.create(staff=s1, book=b4, quantity=2, unit_price=79000.00)
    s_tr4 = Sale.objects.create(staff=s2, book=b1, quantity=1, unit_price=85000.00)

    print(f"Berhasil membuat {Sale.objects.count()} transaksi penjualan.")

    # 10. Membuat Data BookOrder (Pemesanan Buku Pelanggan)
    # Method save() otomatis menghitung total_price (quantity * book.selling_price)
    o1 = BookOrder.objects.create(customer=p5, processed_by_staff=s1, book=b1, quantity=2, status="Pending")
    o2 = BookOrder.objects.create(customer=p6, processed_by_staff=s2, book=b3, quantity=1, status="Completed")
    o3 = BookOrder.objects.create(customer=p7, processed_by_staff=s1, book=b5, quantity=5, status="Pending")

    print(f"Berhasil membuat {BookOrder.objects.count()} pemesanan buku.")
    
    print("\nDATABASE SEEDING BERHASIL DISELESAIKAN!")
    print("Sekarang Anda bisa menjalankan server dan menguji langsung!")

if __name__ == '__main__':
    populate()
