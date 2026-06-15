from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.db.models import Q, Sum
from django.http import JsonResponse

from .models import Book, Sale, BookOrder, Staff, Category, Manager, Person
from .forms import SaleForm, BookOrderCreateForm, BookOrderUpdateForm

class BookListView(ListView):
    model = Book
    template_name = 'store/dashboard.html'
    context_object_name = 'books'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Ambil parameter pencarian dan filter
        query = self.request.GET.get('q')
        category_id = self.request.GET.get('category')
        
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(isbn__icontains=query) |
                Q(author__name__icontains=query)
            )
            
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset.select_related('author', 'category').order_by('title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Kirim daftar kategori untuk filter dropdown
        context['categories'] = Category.objects.all().order_by('name')
        context['selected_category'] = self.request.GET.get('category', '')
        context['query'] = self.request.GET.get('q', '')
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'store/book_detail.html'
    context_object_name = 'book'

    def get_queryset(self):
        # Optimasi query dengan select_related untuk relasi Author & Publisher
        return super().get_queryset().select_related('author', 'publisher', 'category')


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'store/sales_form.html'
    success_url = reverse_lazy('report_business')  # Redirect ke Laporan Bisnis setelah sukses

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Form Penjualan Langsung (Sales Form)"
        return context


class BookOrderCreateView(CreateView):
    model = BookOrder
    form_class = BookOrderCreateForm
    template_name = 'store/order_form.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        messages.success(self.request, f"✅ Order berhasil dibuat dengan status Pending!")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Buat Order Buku Baru"
        return context


class BookOrderListView(ListView):
    model = BookOrder
    template_name = 'store/order_list.html'
    context_object_name = 'orders'
    ordering = ['-order_date']

    def get_queryset(self):
        qs = super().get_queryset().select_related('customer', 'book', 'processed_by_staff__person')
        status = self.request.GET.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status', '')
        context['status_choices'] = [
            ('', 'Semua Status'),
            ('Pending', '⏳ Pending'),
            ('Processed', '🔄 Diproses'),
            ('Completed', '✅ Selesai'),
            ('Cancelled', '❌ Dibatalkan'),
        ]
        return context


class BookOrderUpdateView(UpdateView):
    model = BookOrder
    form_class = BookOrderUpdateForm
    template_name = 'store/order_update.html'
    success_url = reverse_lazy('order_list')

    def form_valid(self, form):
        old = BookOrder.objects.get(pk=self.object.pk)
        response = super().form_valid(form)
        new_status = self.object.status
        if old.status != new_status:
            messages.success(self.request, f"✅ Status order #{self.object.order_id} diperbarui menjadi '{new_status}'.")
        return response


class BusinessReportView(TemplateView):
    template_name = 'store/report_business.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Total Pendapatan (Sum of TOTAL_AMOUNT dari SALES)
        total_revenue = Sale.objects.aggregate(total=Sum('total_amount'))['total']
        context['total_revenue'] = total_revenue if total_revenue is not None else 0.0
        
        # 2. Daftar 5 Buku Terlaris
        context['top_books'] = Book.objects.annotate(
            total_sold=Sum('sales__quantity')
        ).filter(total_sold__gt=0).order_by('-total_sold')[:5]

        # 3. Jumlah pesanan buku berdasarkan status
        context['pending_orders'] = BookOrder.objects.filter(status='Pending').count()
        context['completed_orders'] = BookOrder.objects.filter(status='Completed').count()

        return context


class StaffReportView(TemplateView):
    template_name = 'store/report_staff.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Daftar STAFF aktif beserta jam kerja mingguan
        context['staff_list'] = Staff.objects.select_related('person').all().order_by('-weekly_hours')
        
        # 2. Daftar MANAGER beserta departemen dan info penugasan
        context['manager_list'] = Manager.objects.select_related('person').all().order_by('department')

        return context


# API View sederhana untuk mengambil harga buku (otomatisasi JavaScript pada Sales Form)
def get_book_price(request, isbn):
    book = get_object_or_404(Book, pk=isbn)
    return JsonResponse({
        'selling_price': book.selling_price,
        'stock_quantity': book.stock_quantity
    })


# API View untuk pencarian pelanggan (Customer Autocomplete pada Order Form)
def search_person(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        persons = Person.objects.filter(
            Q(fname__icontains=query) |
            Q(lname__icontains=query) |
            Q(email__icontains=query)
        )[:10]
        results = [
            {
                'id': p.person_id,
                'name': f"{p.fname} {p.lname}",
                'email': p.email,
            }
            for p in persons
        ]
    return JsonResponse({'results': results})

