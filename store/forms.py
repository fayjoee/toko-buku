from django import forms
from .models import Sale, BookOrder

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['staff', 'book', 'quantity', 'unit_price']
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-select'}),
            'book': forms.Select(attrs={'class': 'form-select', 'id': 'id_book'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Jumlah', 'min': 1, 'id': 'id_quantity'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan Harga Satuan', 'step': 'any', 'id': 'id_unit_price'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Placeholder or custom labeling
        self.fields['staff'].empty_label = "-- Pilih Staf Penjual --"
        self.fields['book'].empty_label = "-- Pilih Buku --"


class BookOrderCreateForm(forms.ModelForm):
    """Form untuk membuat order baru. Status otomatis = Pending, tidak perlu diisi."""
    class Meta:
        model = BookOrder
        fields = ['customer', 'processed_by_staff', 'book', 'quantity']
        widgets = {
            'customer':           forms.Select(attrs={'class': 'form-select', 'id': 'id_customer'}),
            'processed_by_staff': forms.Select(attrs={'class': 'form-select'}),
            'book':               forms.Select(attrs={'class': 'form-select', 'id': 'id_book'}),
            'quantity':           forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Masukkan jumlah pesanan',
                'min': 1,
                'id': 'id_quantity',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].empty_label           = "-- Pilih Pelanggan --"
        self.fields['processed_by_staff'].empty_label = "-- Pilih Staf Pemroses (Opsional) --"
        self.fields['processed_by_staff'].required    = False
        self.fields['book'].empty_label               = "-- Pilih Buku --"

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.status = 'Pending'   # Selalu Pending saat order pertama dibuat
        if commit:
            instance.save()
        return instance


class BookOrderUpdateForm(forms.ModelForm):
    """Form untuk mengupdate status order yang sudah ada."""
    class Meta:
        model = BookOrder
        fields = ['status', 'processed_by_staff']
        widgets = {
            'status': forms.Select(
                choices=[
                    ('Pending',   '⏳ Pending — Menunggu diproses'),
                    ('Processed', '🔄 Diproses — Sedang disiapkan'),
                    ('Completed', '✅ Selesai — Stok buku otomatis bertambah'),
                    ('Cancelled', '❌ Dibatalkan'),
                ],
                attrs={'class': 'form-select fw-semibold'},
            ),
            'processed_by_staff': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['processed_by_staff'].empty_label = "-- Pilih Staf Pemroses --"
        self.fields['processed_by_staff'].required    = False


# Alias agar views lama tidak rusak
BookOrderForm = BookOrderCreateForm

