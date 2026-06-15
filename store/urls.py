from django.urls import path
from . import views

urlpatterns = [
    # 1. Halaman Dashboard Katalog Utama
    path('', views.BookListView.as_view(), name='book_list'),
    
    # 2. Halaman Detail Buku
    path('book/<str:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    
    # 3. Halaman Form Penjualan Langsung
    path('sales/add/', views.SaleCreateView.as_view(), name='sale_add'),
    
    # 4. Halaman Form Pemesanan Buku
    path('order/add/', views.BookOrderCreateView.as_view(), name='order_add'),
    
    # 5. Halaman Laporan Bisnis
    path('reports/business/', views.BusinessReportView.as_view(), name='report_business'),
    
    # 6. Halaman Laporan Staf
    path('reports/staff/', views.StaffReportView.as_view(), name='report_staff'),
    
    # Endpoint Helper: Mengambil harga & stok buku secara dinamis via JavaScript
    path('api/book-price/<str:isbn>/', views.get_book_price, name='get_book_price'),
    
    # Endpoint Helper: Pencarian pelanggan untuk fitur autocomplete Customer
    path('api/search-person/', views.search_person, name='search_person'),
]
