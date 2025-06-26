import streamlit as st
import random

# Judul Aplikasi
st.set_page_config(page_title="Latihan Matematika Dasar", layout="centered")
st.title("🎮 Latihan Operasi Matematika Dasar")

# Menu Navigasi
menu = st.sidebar.selectbox("Pilih Menu", [
    "Penjumlahan",
    "Pengurangan",
    "Perkalian",
    "Pembagian",
    "📘 Tabel Perkalian"
])

# Fungsi: Membuat soal dan memeriksa jawaban
def latihan_operasi(op):
    a = random.randint(1, 10)
    b = random.randint(1, 10)

    if op == "Penjumlahan":
        jawaban_benar = a + b
        simbol = "+"
    elif op == "Pengurangan":
        # Supaya tidak negatif
        a, b = max(a, b), min(a, b)
        jawaban_benar = a - b
        simbol = "-"
    elif op == "Perkalian":
        jawaban_benar = a * b
        simbol = "×"
    elif op == "Pembagian":
        # Pastikan pembagian bulat
        jawaban_benar = a
        b = random.randint(1, 10)
        a = a * b
        simbol = "÷"

    st.subheader(f"{a} {simbol} {b} = ?")
    jawaban = st.number_input("Masukkan Jawaban Anda:", step=1, format="%d")

    if st.button("Periksa Jawaban"):
        if jawaban == jawaban_benar:
            st.success("✅ Benar!")
        else:
            st.error(f"❌ Salah. Jawaban yang benar: {jawaban_benar}")

# Halaman Tabel Perkalian
def tampilkan_tabel_perkalian():
    angka = st.selectbox("Pilih angka dasar:", list(range(1, 11)))
    st.subheader(f"Tabel Perkalian {angka}")
    for i in range(1, 11):
        st.write(f"{i} × {angka} = {i * angka}")

# Logika Pemilihan Menu
if menu in ["Penjumlahan", "Pengurangan", "Perkalian", "Pembagian"]:
    latihan_operasi(menu)
elif menu == "📘 Tabel Perkalian":
    tampilkan_tabel_perkalian()
