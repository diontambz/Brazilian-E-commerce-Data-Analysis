# 🎈 E-Commerce Public Dataset

## Dashboard via Streamlit : 
https://brazilian-e-commerce-analysis.streamlit.app/

![Screenshot 2025-03-11 163057](https://github.com/user-attachments/assets/03ccfa29-f4de-4cdd-a8c9-a60e2a62f83b)
![Screenshot 2025-03-11 163107](https://github.com/user-attachments/assets/3c140754-fb80-4f48-9b0b-6e92e3e1fad6)
![Screenshot 2025-03-11 163236](https://github.com/user-attachments/assets/e866563f-d2b8-4319-a409-75ed9a067487)
![Screenshot 2025-03-11 164459](https://github.com/user-attachments/assets/2485ea2c-1d84-4b4b-ba7f-5d41ce49c512)
![Screenshot 2025-03-11 163035](https://github.com/user-attachments/assets/e65edb69-3026-4f5a-9f4d-5e3cc328badd)


Proyek ini menganalisis dataset publik e-commerce dari Brasil untuk mendapatkan wawasan bisnis yang berharga. Analisis berfokus pada pemahaman pola penjualan produk, tren pendapatan, distribusi pelanggan, dan preferensi pembayaran untuk membantu mengoptimalkan strategi bisnis.

## Pertanyaan Bisnis

Analisis ini bertujuan untuk menjawab pertanyaan bisnis utama berikut:

1. Kategori produk apa saja yang paling banyak terjual?
2. Berapa jumlah pendapatan per tahun?
3. Bagaimana distribusi pelanggan di berbagai negara bagian?
4. Metode pembayaran apa yang paling sering digunakan?

## Dataset

Analisis menggunakan beberapa dataset terkait:

- `customers_dataset.csv` - Informasi pelanggan
- `geolocation_dataset.csv` - Data lokasi geografis
- `order_items_dataset.csv` - Detail item pesanan
- `order_payments_dataset.csv` - Informasi pembayaran
- `order_reviews_dataset.csv` - Ulasan pelanggan
- `orders_dataset.csv` - Informasi pesanan
- `product_category_name_translation.csv` - Terjemahan kategori produk
- `products_dataset.csv` - Detail produk
- `sellers_dataset.csv` - Informasi penjual

## Alat & Pustaka yang Digunakan

- Python 3
- Google Colab
- Pandas - Manipulasi dan analisis data
- NumPy - Perhitungan numerik
- Matplotlib - Visualisasi data
- Seaborn - Visualisasi data statistik

## Dataset

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Temuan Utama :

### Kategori Produk

- Kategori "bed_bath_table" memiliki penjualan tertinggi, menunjukkan minat pelanggan yang kuat pada barang-barang rumah tangga dan kamar mandi.
- Produk perabotan rumah dan dekorasi termasuk di antara kategori yang paling populer.

### Tren Pendapatan

- Tahun 2018 menunjukkan pendapatan tertinggi, menunjukkan pertumbuhan positif dari tahun-tahun sebelumnya.
- Tren pendapatan menunjukkan pengembangan bisnis yang sukses dan peningkatan akuisisi pelanggan.

### Distribusi Pelanggan

- Sebagian besar pelanggan terkonsentrasi di tiga negara bagian: SP (São Paulo), RJ (Rio de Janeiro), dan MG (Minas Gerais).
- Distribusi ini selaras dengan pusat populasi Brasil, dengan São Paulo sebagai negara bagian yang paling padat penduduknya.
- Ada peluang untuk ekspansi pasar di negara bagian yang penetrasinya lebih rendah.

### Preferensi Pembayaran

- Kartu kredit adalah metode pembayaran yang dominan, diikuti oleh "boleto" (sistem pembayaran khas Brasil) dan voucher.
- Prevalensi metode pembayaran non-tunai menunjukkan adopsi teknologi finansial yang tinggi di antara pengguna platform.

## Kesimpulan

Analisis ini memberikan wawasan berharga yang dapat menginformasikan strategi bisnis:

- Fokuskan upaya pemasaran pada produk perabotan rumah, khususnya barang-barang tempat tidur dan kamar mandi
- Manfaatkan tren pertumbuhan yang diamati pada tahun 2018 untuk mengembangkan strategi penjualan di masa depan
- Targetkan kampanye pemasaran di tiga negara bagian dengan konsentrasi pelanggan tertinggi
- Terus mengoptimalkan pembayaran kartu kredit sambil memastikan dukungan untuk metode pembayaran alternatif

## Pekerjaan di Masa Depan

Analisis tambahan dapat mengeksplorasi:

- Tren musiman dalam popularitas kategori produk
- Segmentasi pelanggan berdasarkan perilaku pembelian
- Korelasi antara metode pembayaran dan nilai pesanan
- Dampak ulasan pada penjualan di masa depan





[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

### How to run it on your own machine

1. Setup virtual environment
   ```
   python -m venv yourvirtualenv_name
   .\yourvirtualenv_name\Scripts\activate
   ```
   
2. Install Streamlit
   ```
   pip install streamlit babel
   ```
4. Install the requirements

   ```
   $ pip install -r requirements.txt
   ```

5. Run the app

   ```
   $ streamlit run dashboard.py
   ```
