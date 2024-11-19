# perintah di Python untuk memuat modul SQLite3, yaitu library bawaan Python yang digunakan untuk bekerja dengan database SQLite.
import sqlite3
#membangun antarmuka grafis (GUI), termasuk elemen seperti label, tombol, dan lain-lain.
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    #Membuat database SQLite dan tabel 'nilai_siswa' jika belum ada.
    conn = sqlite3.connect('nilai_siswa.db') # Membuat atau membuka database SQLite
    cursor = conn.cursor()  # Membuat objek cursor untuk menjalankan perintah SQL
    # Perintah SQL untuk membuat tabel jika belum ada
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama_siswa TEXT, 
            biologi INTEGER, 
            fisika INTEGER, 
            inggris INTEGER, 
            prediksi_fakultas TEXT 
        )
    ''')
    conn.commit()  # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi database

# Fungsi untuk mengambil semua data dari tabel
def fetch_data():
    #Mengambil semua data dari tabel 'nilai_siswa'
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database
    cursor = conn.cursor()  # Membuat objek cursor
    cursor.execute("SELECT * FROM nilai_siswa") # Perintah SQL untuk mengambil semua data
    rows = cursor.fetchall()  # Mengambil hasil query
    conn.close() # Menutup koneksi database
    return rows # Mengembalikan data dalam bentuk list

# Fungsi untuk menyimpan data baru ke tabel
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    #Menyimpan data baru ke tabel 'nilai_siswa'
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database
    cursor = conn.cursor() # Membuat objek cursor
    #untuk menjalankan perintah SQL pada database
    # Menggunakan parameter untuk menghindari SQL injection
    #Tanda ? digunakan sebagai placeholder untuk mencegah SQL Injection, lalu diisi dengan data dari parameter.
    cursor.execute(''' 
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi)) 
    conn.commit() # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi database

# Fungsi untuk memperbarui data yang ada di tabel
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    #Memperbarui data pada tabel 'nilai_siswa' berdasarkan ID.
    conn = sqlite3.connect('nilai_siswa.db') # Membuka koneksi ke database
    cursor = conn.cursor() # Membuat objek cursor
    cursor.execute(''' ## Perintah SQL untuk memperbarui data berdasarkan ID
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    ''', (nama, biologi, fisika, inggris, prediksi, record_id)) # Parameter data yang akan diperbarui
    conn.commit()  # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi database

# Fungsi untuk menghapus data dari tabel
def delete_database(record_id):
    #Menghapus data dari tabel 'nilai_siswa' berdasarkan ID
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    # Perintah SQL untuk menghapus data berdasarkan ID
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,)) 
    conn.commit() # Menyimpan perubahan ke database
    conn.close() # Menutup koneksi database

# Fungsi untuk menentukan prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    #Menghitung prediksi fakultas berdasarkan nilai tertinggi
    if biologi > fisika and biologi > inggris: # Jika nilai biologi paling tinggi
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris: # Jika nilai fisika paling tinggi
        return "Teknik"
    elif inggris > biologi and inggris > fisika: # Jika nilai inggris paling tinggi
        return "Bahasa"
    else: # Jika tidak ada nilai yang dominan
        return "Tidak Diketahui"

# Fungsi untuk menambah data baru
def submit():
    #Menambah data baru ke tabel dan memperbarui tabel di GUI.
    try:
        nama = nama_var.get() # Mengambil nilai dari input 'Nama Siswa'
        biologi = int(biologi_var.get()) # Mengambil nilai dari input 'Nilai Biologi'
        fisika = int(fisika_var.get()) # Mengambil nilai dari input 'Nilai Fisika'
        inggris = int(inggris_var.get()) # Mengambil nilai dari input 'Nilai Inggris'

        if not nama: # Validasi nama tidak boleh kosong
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris) # Menghitung prediksi fakultas
        save_to_database(nama, biologi, fisika, inggris, prediksi) # Menyimpan data ke database

        # Menampilkan pesan sukses
        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")  
        clear_inputs() # Membersihkan input
        populate_table() # Memperbarui tabel di GUI
    except ValueError as e: # Menangani kesalahan input
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data yang dipilih
def update():
    #Memperbarui data yang dipilih di tabel.
    try:
        if not selected_record_id.get(): # Validasi jika tidak ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get()) # Mengambil ID data yang dipilih
        nama = nama_var.get() # Mengambil nilai dari input 'Nama Siswa'
        biologi = int(biologi_var.get()) # Mengambil nilai dari input 'Nilai Biologi'
        fisika = int(fisika_var.get()) # Mengambil nilai dari input 'Nilai Fisika'
        inggris = int(inggris_var.get()) # Mengambil nilai dari input 'Nilai Inggris'

        if not nama:  # Validasi nama tidak boleh kosong
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris) # Menghitung prediksi fakultas
        update_database(record_id, nama, biologi, fisika, inggris, prediksi) # Memperbarui data di database

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!") # Menampilkan pesan sukses
        clear_inputs() # Membersihkan input
        populate_table() # Memperbarui tabel di GUI
    except ValueError as e: # Menangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data yang dipilih
def delete():
    #Menghapus data yang dipilih di tabel.
    try:
        if not selected_record_id.get(): # Validasi jika tidak ada data yang dipilih
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil ID data yang dipilih
        delete_database(record_id) # Menghapus data dari database
        messagebox.showinfo("Sukses", "Data berhasil dihapus!") # Menampilkan pesan sukses
        clear_inputs() # Membersihkan input
        populate_table() # Memperbarui tabel di GUI
    except ValueError as e: # Memperbarui tabel di GUI
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk membersihkan input
def clear_inputs():
    #Menghapus semua input di form.
    nama_var.set("") # Mengosongkan input 'Nama Siswa'
    biologi_var.set("") # Mengosongkan input 'Nilai Biologi'
    fisika_var.set("") # Mengosongkan input 'Nilai Fisika'
    inggris_var.set("") # Mengosongkan input 'Nilai Inggris'
    selected_record_id.set("") # Mengosongkan ID data yang dipilih

#fungsi yang bertugas untuk mengisi atau memperbarui data yang ditampilkan pada tabel
def populate_table():
    for row in tree.get_children(): #Mengambil semua baris di tabel.
        tree.delete(row) # Menghapus semua data yang saat ini ada di tabel.
    for row in fetch_data(): #Mengambil data dari database SQLite.
        tree.insert('', 'end', values=row)  # Menambahkan data dari database ke tabel.

#fungsi yang digunakan untuk mengisi input form di antarmuka pengguna dengan data dari baris yang dipilih di dalam tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0] # Mengambil baris yang dipilih
        selected_row = tree.item(selected_item)['values'] # Mengambil data dari baris yang dipilih

        selected_record_id.set(selected_row[0]) # Menampilkan ID record
        nama_var.set(selected_row[1]) # Menampilkan Nama Siswa
        biologi_var.set(selected_row[2]) # Menampilkan Nilai Biologi
        fisika_var.set(selected_row[3]) # Menampilkan Nilai Fisika
        inggris_var.set(selected_row[4])  # Menampilkan Nilai Inggris
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!") # Jika tidak ada data yang dipilih

# Inisialisasi database
create_database() 

# Membuat GUI dengan tkinter
root = Tk()  #Membuat jendela utama aplikasi
root.title("Prediksi Fakultas Siswa") # Menambahkan judul pada jendela

# Variabel tkinter
#StringVar() → Membuat variabel yang dapat terhubung dengan widget di Tkinter, digunakan untuk mengontrol inputan dari pengguna.
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Untuk menyimpan ID record yang dipilih

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5) #Membuat label untuk nama siswa
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5) # Input untuk Nama

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5) # Membuat label untuk Nilai Biologi
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5) # Input untuk Nilai Biologi

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5) # Membuat label untuk Nilai Fisika
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5) # Input untuk Nilai Fisika

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5) # Membuat label untuk Nilai Inggris
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5) # Input untuk Nilai Inggris

Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10) # Tombol untuk menambah data
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10) # Tombol untuk memperbarui data
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10) # Tombol untuk menghapus data

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas") # Menentukan kolom untuk tabel
tree = ttk.Treeview(root, columns=columns, show='headings') # Membuat tabel untuk menampilkan data

# Mengatur posisi isi tabel di tengah
for col in columns:
    tree.heading(col, text=col.capitalize())  # Menambahkan heading untuk setiap kolom
    tree.column(col, anchor='center') # Menyusun kolom di tengah

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10) # Menempatkan tabel pada layout

tree.bind('<ButtonRelease-1>', fill_inputs_from_table) # Menambahkan event listener untuk memilih data dari tabel

#Memanggil fungsi populate_table untuk memperbarui data yang ditampilkan di tabel berdasarkan data terbaru yang ada di database.
populate_table() 

root.mainloop() #Menjalankan aplikasi Tkinter
