import streamlit as st
import random

# --- Inisialisasi CSS Kustom untuk Background dan Tabel ---
# Warna pastel untuk tabel
PASTEL_COLORS = [
    "#D0E7F5", # Light Blue
    "#F5D0E7", # Light Pink
    "#E7F5D0", # Light Green
    "#F5E7D0", # Light Orange/Peach
    "#D0F5E7", # Light Teal
]

# CSS kustom untuk mengubah background aplikasi dan gaya tabel
custom_css = f"""
<style>
    /* Mengubah warna latar belakang seluruh halaman Streamlit */
    body {{
        background-color: #F4EBD3; /* Warna krem pastel yang diminta */
        color: #333333; /* Warna teks default agar kontras */
    }}
    .stApp {{
        background-color: #F4EBD3; /* Juga untuk container utama Streamlit */
    }}

    /* Gaya untuk tabel perkalian */
    .multiplication-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        font-family: 'Inter', sans-serif; /* Menggunakan font Inter */
        border-radius: 10px; /* Sudut membulat */
        overflow: hidden; /* Penting untuk radius pada collapse table */
    }}
    .multiplication-table th, .multiplication-table td {{
        padding: 12px 15px;
        text-align: center;
        border: 1px solid #e0e0e0; /* Border tipis antar sel */
        border-radius: 8px; /* Sudut membulat pada sel */
    }}
    .multiplication-table th {{
        background-color: #AEC6CF; /* Header warna biru muda */
        color: white;
        font-weight: bold;
    }}
    /* Warna striping untuk baris tabel */
    .multiplication-table tr:nth-child(odd) {{
        background-color: {PASTEL_COLORS[0]};
    }}
    .multiplication-table tr:nth-child(even) {{
        background-color: {PASTEL_COLORS[1]};
    }}
    /* Lebih banyak warna pastel untuk setiap baris */
    .multiplication-table tr:nth-child(3n+0) {{ background-color: {PASTEL_COLORS[2]}; }}
    .multiplication-table tr:nth-child(3n+1) {{ background-color: {PASTEL_COLORS[3]}; }}
    .multiplication-table tr:nth-child(3n+2) {{ background-color: {PASTEL_COLORS[4]}; }}

    /* Gaya untuk elemen-elemen Streamlit lainnya agar serasi */
    .stButton>button {{
        background-color: #C0D6E4; /* Warna tombol yang serasi */
        color: #333333;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: #AEC6CF;
        color: white;
        transform: translateY(-2px);
        box-shadow: 4px 4px 10px rgba(0,0,0,0.3);
    }}
    .stRadio > label, .stSlider > label, .stNumberInput > label, .stTextInput > label, .stSelectbox > label {{
        color: #555555;
        font-weight: 500;
    }}
    .stTextInput>div>div>input {{
        border-radius: 8px;
        border: 1px solid #B0B0B0;
        padding: 8px;
    }}
    .stSuccess {{
        background-color: #D4EDDA; /* Hijau soft */
        color: #155724;
        border-radius: 8px;
        padding: 10px;
    }}
    .stError {{
        background-color: #F8D7DA; /* Merah soft */
        color: #721C24;
        border-radius: 8px;
        padding: 10px;
    }}
    .stWarning {{
        background-color: #FFF3CD; /* Kuning soft */
        color: #856404;
        border-radius: 8px;
        padding: 10px;
    }}
</style>
"""

# Konfigurasi halaman Streamlit dan injeksi CSS kustom
st.set_page_config(layout="centered", page_title="Latihan Matematika 🌷")
st.markdown(custom_css, unsafe_allow_html=True)

# --- Fungsi untuk menghasilkan soal matematika ---
def generate_question(operation, num_range):
    num1 = random.randint(1, num_range)
    num2 = random.randint(1, num_range)

    # Logika khusus untuk pembagian agar hasilnya bulat dan pembagi tidak nol
    if operation == "Pembagian":
        # Pastikan num1 adalah kelipatan num2 dan num2 tidak nol
        # Jika num2 = 0, set ke 1 agar tidak ada pembagian dengan nol
        if num2 == 0:
            num2 = 1
        while num1 % num2 != 0:
            num1 = random.randint(1, num_range)
            num2 = random.randint(1, num_range)
            if num2 == 0: # Pastikan num2 tidak nol, ulangi jika perlu
                num2 = 1

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

# --- Fungsi untuk membuat tabel perkalian (sekarang menghasilkan HTML) ---
def buat_tabel_perkalian(angka):
    tabel_html = '<table class="multiplication-table">'
    tabel_html += '<thead><tr><th>Faktor</th><th>Hasil</th></tr></thead>'
    tabel_html += '<tbody>'
    for i in range(1, 11):
        # Menggunakan inline style untuk warna baris, meskipun CSS global lebih baik
        # Namun, untuk warna striping yang lebih dinamis, CSS di atas sudah cukup
        tabel_html += f'<tr><td>{angka} x {i}</td><td>{angka * i}</td></tr>'
    tabel_html += '</tbody></table>'
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

    # Tampilkan tabel perkalian menggunakan HTML kustom
    st.markdown(buat_tabel_perkalian(int(angka_perkalian)), unsafe_allow_html=True)

st.markdown("---")
st.info("Dibuat oleh fitry dengan Cinta❤️ untuk adik saya!")

