import streamlit as st
import random

# Konfigurasi halaman Streamlit
st.set_page_config(layout="centered", page_title="Latihan Matematika Asyik!")

# --- Fungsi untuk menghasilkan soal matematika ---
def generate_question(operation, num_range):
    num1 = random.randint(1, num_range)
    num2 = random.randint(1, num_range)

    # Logika khusus untuk pembagian agar hasilnya bulat dan pembagi tidak nol
    if operation == "Pembagian":
        # Pastikan num1 adalah kelipatan num2 dan num2 tidak nol
        while num2 == 0 or num1 % num2 != 0:
            num1 = random.randint(1, num_range)
            num2 = random.randint(1, num_range)
            if num2 == 0: # Pastikan num2 tidak nol, ulangi jika perlu
                num2 = random.randint(1, num_range)


    question = ""
    answer = 0
    if operation == "Penjumlahan":
        question = f"{num1} + {num2} ="
        answer = num1 + num2
    elif operation == "Pengurangan":
        # Pastikan hasil tidak negatif untuk memudahkan adik Anda di awal
        if num1 < num2:
            num1, num2 = num2, num1 # Tukar angka agar hasilnya positif
        question = f"{num1} - {num2} ="
        answer = num1 - num2
    elif operation == "Perkalian":
        question = f"{num1} x {num2} ="
        answer = num1 * num2
    elif operation == "Pembagian":
        question = f"{num1} : {num2} ="
        answer = num1 // num2 # Menggunakan integer division untuk hasil bulat
    return question, answer

# --- Fungsi untuk membuat tabel perkalian ---
def buat_tabel_perkalian(angka):
    tabel_html = f"## Tabel Perkalian {angka}\n\n"
    # Menggunakan format markdown untuk tabel yang lebih rapi
    tabel_html += "| Faktor | Hasil |\n"
    tabel_html += "|:------:|:-----:|\n"
    for i in range(1, 11):
        tabel_html += f"| {angka} x {i} | {angka * i} |\n"
    return tabel_html

# --- Inisialisasi session state untuk menyimpan data antar sesi ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""
if 'operation_selected' not in st.session_state:
    st.session_state.operation_selected = "Penjumlahan"
if 'number_range' not in st.session_state:
    st.session_state.number_range = 10
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = "" # Untuk menyimpan jawaban pengguna

# --- Bagian utama aplikasi Streamlit ---
st.title("Latihan Matematika Asyik!")
st.write("Ayo latihan berhitung dan hafalkan tabel perkalian!")

# Pilihan antara soal latihan dan tabel perkalian
pilihan_tampilan = st.selectbox(
    "Pilih Tampilan:",
    ("Soal Latihan", "Tabel Perkalian"),
    key='pilihan_tampilan_selector'
)

# --- Tampilan Soal Latihan ---
if pilihan_tampilan == "Soal Latihan":
    st.markdown("---")
    st.subheader("Latihan Soal Matematika")

    # Pilihan operasi matematika
    operation = st.radio(
        "Pilih Operasi:",
        ("Penjumlahan", "Pengurangan", "Perkalian", "Pembagian"),
        key='operation_selector'
    )

    # Slider untuk menentukan rentang angka soal
    num_range = st.slider(
        "Rentang Angka Soal (contoh: 1 sampai 10):",
        min_value=5, max_value=100, value=st.session_state.number_range, step=5,
        key='range_slider'
    )

    # Logika untuk menghasilkan soal baru jika operasi atau rentang angka berubah
    if (operation != st.session_state.operation_selected or
        num_range != st.session_state.number_range or
        not st.session_state.current_question): # Hasilkan soal pertama kali
        st.session_state.operation_selected = operation
        st.session_state.number_range = num_range
        st.session_state.current_question, st.session_state.correct_answer = generate_question(operation, num_range)
        st.session_state.user_answer = "" # Reset kolom jawaban

    # Tombol untuk mendapatkan soal baru secara manual
    if st.button("Soal Baru", key='new_question_btn'):
        st.session_state.current_question, st.session_state.correct_answer = generate_question(operation, num_range)
        st.session_state.user_answer = "" # Reset kolom jawaban


    # Tampilkan soal
    st.write(f"## Berapakah {st.session_state.current_question}")

    # Kolom input untuk jawaban pengguna
    user_answer = st.text_input("Jawab di sini:", value=st.session_state.user_answer, key='answer_input')

    # Tombol untuk memeriksa jawaban
    if st.button("Cek Jawaban", key='check_answer_btn'):
        try:
            if int(user_answer) == st.session_state.correct_answer:
                st.success("Benar! Hebat! 🎉")
                st.session_state.score += 1
                st.session_state.user_answer = "" # Clear input setelah jawaban benar
                # Langsung beri soal baru setelah jawaban benar
                st.session_state.current_question, st.session_state.correct_answer = generate_question(operation, num_range)
                st.rerun() # Refresh aplikasi untuk menampilkan soal baru
            else:
                st.error("Salah, coba lagi ya. 🤔")
                st.session_state.user_answer = user_answer # Pertahankan jawaban yang salah
        except ValueError:
            st.warning("Mohon masukkan angka yang valid.")
            st.session_state.user_answer = user_answer # Pertahankan input tidak valid


    st.markdown("---")

    # Tampilkan skor
    st.write(f"### Skor Anda: {st.session_state.score} 💪")

    # Tombol reset skor
    if st.button("Reset Skor", key='reset_score_btn'):
        st.session_state.score = 0
        st.success("Skor telah direset!")
        st.rerun() # Refresh aplikasi setelah reset skor

# --- Tampilan Tabel Perkalian ---
elif pilihan_tampilan == "Tabel Perkalian":
    st.markdown("---")
    st.subheader("Hafalkan Tabel Perkalian")

    # Input angka untuk tabel perkalian
    angka_perkalian = st.number_input(
        "Masukkan angka untuk melihat tabel perkalian:",
        min_value=1, max_value=20, value=2, step=1,
        key='angka_tabel_perkalian'
    )

    # Tampilkan tabel perkalian
    st.markdown(buat_tabel_perkalian(int(angka_perkalian)))

st.markdown("---")
st.info("Dibuat dengan ❤️ dari Fitry untuk Laila & Laili")
