from django.db import models
from django.core.exceptions import ValidationError

class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=45, verbose_name="Nama Depan")
    lname = models.CharField(max_length=45, verbose_name="Nama Belakang")
    phone_num = models.CharField(max_length=11, blank=True, null=True, verbose_name="No. Telepon")
    email = models.EmailField(max_length=45, unique=True, verbose_name="Email")
    password = models.CharField(max_length=45, verbose_name="Password")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")

    def __str__(self):
        return f"{self.fname} {self.lname}"

    class Meta:
        verbose_name = "Orang"
        verbose_name_plural = "Daftar Orang"


class Staff(models.Model):
    # Relasi OneToOne dengan Person, bertindak sebagai primary key
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True, db_column='person_id', related_name='staff')
    role = models.CharField(max_length=30, verbose_name="Peran/Jabatan")
    weekly_hours = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Jam Kerja Mingguan")
    certification_status = models.CharField(max_length=45, blank=True, null=True, verbose_name="Status Sertifikasi")

    def __str__(self):
        return f"{self.person.fname} {self.person.lname} ({self.role})"

    class Meta:
        verbose_name = "Staf"
        verbose_name_plural = "Daftar Staf"


class Manager(models.Model):
    # Relasi OneToOne dengan Person, bertindak sebagai primary key
    person = models.OneToOneField(Person, on_delete=models.CASCADE, primary_key=True, db_column='person_id', related_name='manager')
    bonus_level = models.CharField(max_length=10, verbose_name="Level Bonus")
    department = models.CharField(max_length=45, verbose_name="Departemen")
    office_location = models.CharField(max_length=100, verbose_name="Lokasi Kantor")
    hired_date = models.DateField(verbose_name="Tanggal Diterima Kerja")

    def __str__(self):
        return f"Manager: {self.person.fname} {self.person.lname} - {self.department}"

    class Meta:
        verbose_name = "Manajer"
        verbose_name_plural = "Daftar Manajer"


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, verbose_name="Nama Penulis")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Penulis"
        verbose_name_plural = "Daftar Penulis"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, verbose_name="Nama Kategori")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Daftar Kategori"


class Publisher(models.Model):
    publisher_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, verbose_name="Nama Penerbit")
    address = models.CharField(max_length=45, blank=True, null=True, verbose_name="Alamat")
    phone_num = models.CharField(max_length=11, blank=True, null=True, verbose_name="No. Telepon")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Penerbit"
        verbose_name_plural = "Daftar Penerbit"


class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True, verbose_name="ISBN")
    title = models.CharField(max_length=45, verbose_name="Judul Buku")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, db_column='author_id', related_name='books', verbose_name="Penulis")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, db_column='publisher_id', related_name='books', verbose_name="Penerbit")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id', related_name='books', verbose_name="Kategori")
    publication_year = models.IntegerField(verbose_name="Tahun Terbit")
    selling_price = models.FloatField(verbose_name="Harga Jual")
    min_quantity = models.IntegerField(verbose_name="Stok Minimum")
    page_count = models.IntegerField(verbose_name="Jumlah Halaman")
    
    # Kolom stock_quantity ditambahkan agar dashboard dapat membandingkan stok aktif dengan min_quantity
    stock_quantity = models.IntegerField(default=0, verbose_name="Stok Saat Ini")

    @property
    def is_stock_critical(self):
        return self.stock_quantity <= self.min_quantity

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Buku"
        verbose_name_plural = "Daftar Buku"


class Sale(models.Model):
    sale_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, db_column='staff_id', related_name='sales', verbose_name="Staf Penjual")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='isbn', related_name='sales', verbose_name="Buku")
    sale_time = models.DateTimeField(auto_now_add=True, verbose_name="Waktu Penjualan")
    quantity = models.IntegerField(verbose_name="Jumlah")
    unit_price = models.FloatField(verbose_name="Harga Satuan")
    total_amount = models.FloatField(blank=True, verbose_name="Total Pendapatan")

    def clean(self):
        # Validasi stok buku jika melakukan penjualan baru
        if not self.pk and self.book.stock_quantity < self.quantity:
            raise ValidationError(f"Stok buku '{self.book.title}' tidak mencukupi untuk penjualan ini! Stok tersedia: {self.book.stock_quantity}")

    def save(self, *args, **kwargs):
        # Kalkulasi otomatis Total Amount
        self.total_amount = self.quantity * self.unit_price
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Potong stok buku jika transaksi baru berhasil disimpan
        if is_new:
            self.book.stock_quantity -= self.quantity
            self.book.save()

    def __str__(self):
        return f"Penjualan #{self.sale_id} - {self.book.title} ({self.quantity})"

    class Meta:
        verbose_name = "Penjualan"
        verbose_name_plural = "Daftar Penjualan"


class BookOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Person, on_delete=models.CASCADE, db_column='customer_id', related_name='orders', verbose_name="Pelanggan")
    processed_by_staff = models.ForeignKey(Staff, on_delete=models.CASCADE, db_column='processed_by_staff_id', related_name='processed_orders', verbose_name="Staf Pemroses", blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, db_column='isbn', related_name='orders', verbose_name="Buku")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Pemesanan")
    quantity = models.IntegerField(verbose_name="Jumlah")
    total_price = models.FloatField(blank=True, verbose_name="Total Harga")
    status = models.CharField(max_length=20, default='Pending', verbose_name="Status")

    def save(self, *args, **kwargs):
        # Kalkulasi otomatis Total Price — selalu di-update setiap kali disimpan
        self.total_price = self.quantity * self.book.selling_price

        is_new = self.pk is None

        if not is_new:
            # Ambil status lama sebelum disimpan untuk deteksi perubahan status
            try:
                old = BookOrder.objects.get(pk=self.pk)
                status_changed_to_completed = (
                    old.status.lower() != 'completed' and
                    self.status.lower() == 'completed'
                )
            except BookOrder.DoesNotExist:
                status_changed_to_completed = False
        else:
            status_changed_to_completed = False

        super().save(*args, **kwargs)

        # Jika status baru berubah ke Completed → tambahkan stok buku (restocking)
        if status_changed_to_completed:
            self.book.stock_quantity += self.quantity
            self.book.save(update_fields=['stock_quantity'])

    def __str__(self):
        return f"Order #{self.order_id} - {self.book.title} ({self.status})"

    class Meta:
        verbose_name = "Pemesanan Buku"
        verbose_name_plural = "Daftar Pemesanan Buku"
