import streamlit as st
from modules.nomor import generate_nomor
from modules.database import simpan_data, load_data
from datetime import date, timedelta
import os
import pandas as pd
import re
from jinja2 import Environment, FileSystemLoader
import base64
from docxtpl import DocxTemplate, InlineImage
import tempfile
from docx.shared import Mm

# Konfigurasi halaman
st.set_page_config(
    page_title="E-Surat Perpanjangan Izin Operasional",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏛️"
)

# Inisialisasi session state
if "confirm_generate" not in st.session_state:
    st.session_state.confirm_generate = False
if "menu" not in st.session_state:
    st.session_state.menu = "Dashboard"

# CSS Modern Pemerintah
st.markdown("""
<style>
/* ===========================================
    GLOBAL STYLES - TEMA PEMERINTAH RESMI
============================================= */
:root {
    --primary-color: #0d47a1;
    --primary-dark: #003087;
    --secondary-color: #1976d2;
    --accent-color: #ffc107;
    --success-color: #2e7d32;
    --danger-color: #d32f2f;
    --warning-color: #ed6c02;
    --text-primary: #212121;
    --text-secondary: #757575;
    --bg-primary: #f8f9fa;
    --bg-secondary: #ffffff;
    --border-color: #e0e0e0;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}

options = {
    'margin-top': '2cm',
    'margin-bottom': '1cm',
    'margin-left': '3cm',
    'margin-right': '3cm',
}            

body {
    margin: 0;
    padding-left: 3cm;
    padding-right: 3cm;
    padding-top: 2cm;
    padding-bottom: 1cm;
}            

/* Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
}

/* Main Container */
.block-container {
    padding-top: 2rem;
    max-width: 1400px;
    margin: 0 auto;
}

/* ===========================================
    HEADER & LOGO
============================================= */
.header-container {
    background: var(--bg-secondary);
    border-bottom: 4px solid var(--primary-color);
    box-shadow: var(--shadow-md);
    padding: 1.5rem 2rem;
    margin-bottom: 2rem;
    border-radius: 0 0 20px 20px;
}

.gov-header {
    display: flex;
    align-items: center;
    gap: 1.5rem;
}

.gov-logo {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 2rem;
    font-weight: 700;
    box-shadow: var(--shadow-lg);
}

.header-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    line-height: 1.2;
}

.header-subtitle {
    color: var(--text-secondary);
    font-size: 1.1rem;
    font-weight: 500;
    margin: 0.25rem 0 0 0;
}

/* ===========================================
    SIDEBAR PEMERINTAH
============================================= */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--primary-color) 0%, var(--primary-dark) 100%);
    padding-top: 2rem;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    background: rgba(255,255,255,0.1);
    border: 2px solid rgba(255,255,255,0.2);
    color: white;
    padding: 1rem 1.5rem;
    margin-bottom: 0.75rem;
    border-radius: 12px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
    text-align: left;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.2);
    border-color: rgba(255,255,255,0.4);
    transform: translateX(8px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

section[data-testid="stSidebar"] .stButton > button:focus {
    background: rgba(255,255,255,0.25);
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(255,193,7,0.3);
}

/* Sidebar Info */
.sidebar-info {
    background: rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}

.sidebar-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.sidebar-subtitle {
    color: rgba(255,255,255,0.9);
    font-size: 1rem;
    font-weight: 500;
}

/* ===========================================
    STATISTIC CARDS
============================================= */
.stat-card {
    background: var(--bg-secondary);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid var(--border-color);
    box-shadow: var(--shadow-md);
    transition: all 0.3s ease;
    height: 100%;
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
}

.stat-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
}

.stat-icon {
    width: 64px;
    height: 64px;
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-md);
}

.stat-primary { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; }
.stat-success { background: linear-gradient(135deg, var(--success-color), #4caf50); color: white; }
.stat-warning { background: linear-gradient(135deg, var(--warning-color), #ff9800); color: white; }

.stat-title {
    font-size: 0.95rem;
    color: var(--text-secondary);
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stat-value {
    font-size: 3rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 0;
    line-height: 1;
}

/* ===========================================
    FORM ELEMENTS
============================================= */
.form-section {
    background: var(--bg-secondary);
    padding: 2.5rem;
    border-radius: 24px;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border-color);
    margin-bottom: 2rem;
}

.section-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 1.5rem;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid var(--primary-color);
    display: inline-block;
}

.form-row {
    background: #f8fafc;
    padding: 1.5rem;
    border-radius: 16px;
    border-left: 5px solid var(--primary-color);
    margin-bottom: 1.5rem;
}

/* Input styling */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > select {
    border: 2px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    background: white !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus,
.stSelectbox > div > div > select:focus {
    border-color: var(--primary-color) !important;
    box-shadow: 0 0 0 3px rgba(13,71,161,0.1) !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: white !important;
    border: none !important;
    padding: 1rem 2.5rem !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    box-shadow: var(--shadow-md) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg) !important;
    background: linear-gradient(135deg, var(--secondary-color), var(--primary-dark)) !important;
}

.btn-success {
    background: linear-gradient(135deg, var(--success-color), #4caf50) !important;
}

.btn-danger {
    background: linear-gradient(135deg, var(--danger-color), #f44336) !important;
}

/* ===========================================
    TABLE & DATA
============================================= */
[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: var(--shadow-sm) !important;
}

table {
    border-radius: 12px !important;
    overflow: hidden !important;
}

/* Archive cards */
.archive-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
    transition: all 0.3s ease;
}

.archive-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

/* Status badges */
.status-badge {
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 700;
    text-transform: uppercase;
}

.badge-primary { background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; }
.badge-success { background: linear-gradient(135deg, var(--success-color), #4caf50); color: white; }

/* Success message */
.success-message {
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    border: 1px solid #c3e6cb;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    box-shadow: var(--shadow-md);
}

.info-message {
    background: linear-gradient(135deg, #d1ecf1, #bee5eb);
    border: 1px solid #bee5eb;
    border-radius: 16px;
    padding: 1.5rem;
    border-left: 5px solid var(--primary-color);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    padding: 1rem 2rem !important;
    border-radius: 12px 12px 0 0 !important;
    font-weight: 600 !important;
}

/* Responsive */
@media (max-width: 768px) {
    .header-title { font-size: 1.8rem !important; }
    .stat-value { font-size: 2.2rem !important; }
    .form-section { padding: 1.5rem !important; }
}
</style>
""", unsafe_allow_html=True)

# Data
tanggal_obj = date.today()
bulan_indo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
def format_indo(tgl):
    bulan = [
        "Januari","Februari","Maret","April","Mei","Juni",
        "Juli","Agustus","September","Oktober","November","Desember"
    ]
    return f"{tgl.day} {bulan[tgl.month-1]} {tgl.year}"


FILE_DB = r"database/surat.xlsx"
df = pd.read_excel(FILE_DB) if os.path.exists(FILE_DB) else pd.DataFrame()

def generate_docx(data):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(base_dir, "templates", "template.docx")

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template tidak ditemukan: {template_path}")

        doc = DocxTemplate(template_path)

        logo_path = os.path.join(base_dir, "logo.jpg")
        if os.path.exists(logo_path):
            data["logo"] = InlineImage(doc, logo_path, width=Mm(25))

        doc.render(data)

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc.save(tmp.name)

        with open(tmp.name, "rb") as f:
            return f.read()

# HEADER
st.markdown("""
<div class="header-container">
    <div class="gov-header">
        <div class="gov-logo">🏛️</div>
        <div>
            <h1 class="header-title">E-SURAT</h1>
            <p class="header-subtitle">Sistem Perpanjangan Izin Operasional Lembaga Kesejahteraan Sosial</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div class="sidebar-info">
        <h2 class="sidebar-title">📋 E-SURAT</h2>
        <p class="sidebar-subtitle">Perpanjangan Izin Operasional</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("📊 Dashboard", key="dashboard_btn"):
        st.session_state.menu = "Dashboard"
    if st.button("📝 Buat Surat", key="buat_surat_btn"):
        st.session_state.menu = "Buat Surat"

# Konten Utama
menu = st.session_state.menu

# ============ DASHBOARD ==============================
if menu == "Dashboard":
    st.markdown('<h2 style="color: var(--primary-color); font-weight: 700; margin-bottom: 2rem;">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # --- PERBAIKAN LOGIKA TANGGAL ---
    if not df.empty:
        # Pastikan kolom tanggal adalah tipe datetime
        df["tanggal_dt"] = pd.to_datetime(df["tanggal"], errors='coerce')
        
        now = date.today()
        # Hitung Hari Ini (berdasarkan objek tanggal, bukan string)
        hari_ini = len(df[df["tanggal_dt"].dt.date == now])
        
        # Hitung Bulan Ini
        bulan_ini = len(df[(df["tanggal_dt"].dt.month == now.month) & 
                           (df["tanggal_dt"].dt.year == now.year)])
        total = len(df)
    else:
        hari_ini = 0
        bulan_ini = 0
        total = 0

    # Pastikan kolom jenis_lks ada untuk tampilan tabel
    if "jenis_lks" not in df.columns:
        df["jenis_lks"] = "-"

    # --- STAT CARDS ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon stat-primary">📄</div>
            <h3 class="stat-title">Total Surat</h3>
            <h2 class="stat-value">{total:,}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon stat-success">📅</div>
            <h3 class="stat-title">Hari Ini</h3>
            <h2 class="stat-value">{hari_ini}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon stat-warning">📈</div>
            <h3 class="stat-title">Bulan Ini</h3>
            <h2 class="stat-value">{bulan_ini}</h2>
        </div>
        """, unsafe_allow_html=True)

        
    # Tabel Terbaru
    if not df.empty:
        st.markdown('<h3 style="color: var(--text-primary); margin-bottom: 1.5rem;">📋 Surat Terbaru</h3>', unsafe_allow_html=True)
        df_tampil = df.tail(5).reset_index(drop=True)
        df_tampil.insert(0, "No", df_tampil.index + 1)

        st.dataframe(df_tampil[['No', 'nomor', 'nama', 'jenis_lks', 'tanggal']], use_container_width=True)
        
        # Arsip
        st.markdown('<h3 style="color: var(--text-primary); margin: 2rem 0 1.5rem 0;">📦 Arsip Surat</h3>', unsafe_allow_html=True)
        
        for i, row in df.iterrows():
            file_path = row.get("file_path")

            if pd.isna(file_path):
                file_path = ""

            col1, col2 = st.columns([4,1])

            with col1:
                st.markdown(f"""
                <div class="archive-card">
                    <strong style="font-size: 1.2rem; color: var(--primary-color);">{row.get("nomor", "-")}</strong><br>
                    <span style="color: var(--text-secondary);">{row.get("nama", "-")}</span><br>
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">
                        Jenis LKS: <b>{row.get("jenis_lks", "-")}</b>
                    </span>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if isinstance(file_path, str) and file_path.strip() != "" and os.path.exists(file_path):
                    with open(file_path, "rb") as f:
                        st.download_button("⬇️", f, file_name=os.path.basename(file_path), key=f"d{i}")

                if st.button("🗑️", key=f"h{i}"):
                    if isinstance(file_path, str) and file_path.strip() != "" and os.path.exists(file_path):
                        os.remove(file_path)
                    df = df.drop(i).reset_index(drop=True)
                    df.to_excel(FILE_DB, index=False)
                    st.rerun()
    
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: var(--text-secondary);">
            <h2 style="font-size: 2rem; margin-bottom: 1rem;">📭</h2>
            <p>Belum ada data surat</p>
        </div>
        """, unsafe_allow_html=True)
# ================= BUAT SURAT =================
elif menu == "Buat Surat":
    st.title("📝 Buat Surat")

    nomor = generate_nomor()
    st.info(f"📄 Nomor Surat: {nomor}")

    # ================= DATA LEMBAGA =================
    with st.container():
        st.subheader("🏢 Data Lembaga")

        col1, col2 = st.columns(2)

        with col1:
            nama = st.text_input("Nama Lembaga")
            npwp = st.text_input("NPWP")

        with col2:
            alamat = st.text_area("Alamat")

    # ================= AKTA =================
    with st.container():
        st.subheader("📜 Data Akta Notaris")

        col1, col2 = st.columns(2)

        with col1:
            notaris_pendirian = st.text_input("Notaris Pendirian")
            nomor_akte_pendirian = st.text_input("Nomor/Tanggal Akta Pendirian")

        with col2:
            notaris_perubahan = st.text_input("Notaris Perubahan Terakhir")
            nomor_akte_perubahan = st.text_input("Nomor/Tanggal Perubahan")

    # ================= STP =================
    with st.container():
        st.subheader("📑 Data STP Sebelumnya")

        col1, col2 = st.columns(2)

        with col1:
            stp_tanggal = st.text_input("Tanggal STP Terakhir")

        with col2:
            stp_nomor = st.text_input("Nomor STP Terakhir")

    # ================= STATUS =================
    with st.container():
        st.subheader("🌍 Status & Wilayah")

        col1, col2 = st.columns(2)

        with col1:
            status = st.selectbox("Status Organisasi", ["Pusat", "Cabang"])

        with col2:
            lingkup = st.selectbox("Lingkup Wilayah Kerja", ["Provinsi", "Kabupaten"])
    
    # =============== JENIS LKS ==============
    with st.container():
        st.subheader("Jenis LKS")
        jenis_lks = st.selectbox("Jenis LKS", ["Anak", "Lansia", "Psikotik"])
    # ================= USAHA =================
    with st.container():
        st.subheader("💼 Kegiatan Usaha")

        usaha_jalan = st.text_area("Usaha Kesejahteraan Sosial yang Sedang Dilaksanakan")
        usaha_rencana = st.text_area("Rencana Usaha Kesejahteraan Sosial")

    # ================= MASA BERLAKU =================
    masa = tanggal_obj.replace(year=tanggal_obj.year + 3) - timedelta(days=1)


    def format_tanggal(tgl):
        return f"{tgl.day} {bulan_indo[tgl.month-1]} {tgl.year}"

    tanggal_awal = format_tanggal(tanggal_obj)
    tanggal_akhir = format_tanggal(masa)

    hasil = f"3 Tahun mulai tanggal {tanggal_awal} s/d {tanggal_akhir}"

    st.success(f"⏳ Masa Berlaku: {hasil}")

    # ================= DASAR =================
    st.subheader("📌 Dasar")

    # ===== AREA 1: INSTRUMEN =====
    with st.container():
        st.markdown("### 📄 Instrumen")

        col1, col2 = st.columns(2)

        with col1:
            dasar_tanggal = st.text_input("Tanggal")

        with col2:
            dasar_nomor = st.text_input("Nomor")

    # ===== AREA 2: KETERANGAN =====
    with st.container():
        st.markdown("### 📝 Surat Permohonan Lembaga")

        col1, col2 = st.columns(2)

        with col1:
            tanggal_permohonan = st.text_area("Tanggal")

        with col2:
            nomor_permohonan = st.text_area("nomor")

        tanggal = tanggal_awal
    # ================= GENERATE SURAT (REFACED) =================
        # 1. Tombol Submit (Masuk ke mode konfirmasi)
        if st.button("🚀 Generate Surat"):
            # Simpan semua data input ke session_state
            st.session_state.data_temp = {
                "nomor": nomor, "nama": nama, "npwp": npwp, "alamat": alamat,
                "notaris_pendirian": notaris_pendirian, "nomor_akte_pendirian": nomor_akte_pendirian,
                "notaris_perubahan": notaris_perubahan, "nomor_akte_perubahan": nomor_akte_perubahan,
                "stp_tanggal": stp_tanggal, "stp_nomor": stp_nomor,
                "status": status, "lingkup": lingkup,
                "usaha_jalan": usaha_jalan, "usaha_rencana": usaha_rencana,
                "dasar_tanggal": dasar_tanggal, "dasar_nomor": dasar_nomor,
                "tanggal_permohonan": tanggal_permohonan, "nomor_permohonan": nomor_permohonan,
                "tanggal": tanggal, "jenis_lks": jenis_lks,
                "tanggal_ttd": format_indo(tanggal_obj),
                "masa": hasil,
            }
            st.session_state.confirm_generate = True
            st.rerun()

        # 2. Blok Konfirmasi (Hanya muncul jika tombol di atas ditekan)
        if st.session_state.get("confirm_generate", False):
            st.warning("⚠️ Periksa kembali data di bawah sebelum memproses:")
            
            # Tampilkan Ringkasan Data (Opsional tapi sangat disarankan untuk UX)
            data = st.session_state.data_temp
            st.info(f"Lembaga: **{data.get('nama')}** | Nomor: **{data.get('nomor')}**")
            
            col1, col2 = st.columns(2)
            
            # ===== LANJUT =====
            with col1:
                if st.button("✅ Lanjut Generate"):
                    try:
                        # Bersihkan NaN/None sebelum diproses
                        for k, v in data.items():
                            if pd.isna(v): data[k] = ""

                        docx_bytes = generate_docx(data)

                        # Sanitasi nama file
                        safe_nama = re.sub(r'[^\w\s-]', '', data.get("nama", "")).strip().replace(" ", "_")
                        safe_nomor = re.sub(r'[^\w\-\.]', '_', data.get("nomor", ""))
                        os.makedirs("surat", exist_ok=True)
                        file_path = f"surat/{safe_nama}_{safe_nomor}.docx"

                        with open(file_path, "wb") as f:
                            f.write(docx_bytes)

                        data["file_path"] = file_path
                        simpan_data(data)

                        st.success("✅ Surat berhasil dibuat!")
                        st.download_button("📄 Download Word", docx_bytes, file_name=os.path.basename(file_path))

                        # Reset state setelah sukses
                        st.session_state.confirm_generate = False
                        st.session_state.data_temp = {}
                        
                    except Exception as e:
                        st.error("❌ Gagal membuat surat")
                        st.exception(e)

            # ===== EDIT =====
            with col2:
                if st.button("✏️ Edit Data"):
                    st.session_state.confirm_generate = False
                    # Tidak perlu hapus data_temp agar user bisa edit tanpa isi ulang dari nol
                    st.rerun()
