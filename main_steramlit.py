import streamlit as st
from rag_core import StuntingRAG

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Chatbot Stunting - Gizi Anak",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. CUSTOM CSS — Dark mode, warm red-orange accent
# ==========================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&family=Lora:wght@600&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif !important;
}

.stApp {
    background: #0f0f0f !important;
}
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 740px !important;
    background: transparent !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* --- Brand header --- */
.brand-header {
    background: linear-gradient(135deg, #c62828 0%, #e64a19 55%, #f57c00 100%);
    border-radius: 18px;
    padding: 24px 28px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(230, 74, 25, 0.35);
}
.brand-header::before {
    content: '';
    position: absolute;
    top: -35px; right: -35px;
    width: 160px; height: 160px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
}
.brand-header::after {
    content: '';
    position: absolute;
    bottom: -45px; left: 25px;
    width: 120px; height: 120px;
    background: rgba(255,255,255,0.04);
    border-radius: 50%;
}
.brand-title {
    color: #fff !important;
    font-size: 1.5rem !important;
    font-weight: 800 !important;
    margin: 0 0 4px 0 !important;
    line-height: 1.2 !important;
}
.brand-subtitle {
    color: rgba(255,255,255,0.90) !important;
    font-size: 0.85rem !important;
    margin: 0 !important;
    font-weight: 600 !important;
}

/* --- Greeting bar --- */
.greeting-bar {
    background: #1e1e1e;
    border-radius: 13px;
    padding: 13px 18px;
    margin-bottom: 14px;
    border: 1px solid rgba(230, 74, 25, 0.25);
    display: flex;
    align-items: center;
    gap: 12px;
}
.greet-name { font-weight: 800; color: #ff7043; font-size: 0.95rem; }
.greet-sub  { font-size: 0.80rem; color: #bba090; }

/* --- Notice --- */
.stAlert {
    background: #1e1210 !important;
    border-left: 4px solid #e64a19 !important;
    border-radius: 10px !important;
    color: #ffccb0 !important;
    font-size: 0.86rem !important;
}

/* --- Disclaimer box --- */
.disclaimer-box {
    background: #1a0e08;
    border: 1.5px solid rgba(230, 74, 25, 0.40);
    border-radius: 12px;
    padding: 13px 17px;
    margin-bottom: 14px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
}
.disclaimer-icon {
    font-size: 1.1rem;
    flex-shrink: 0;
    margin-top: 1px;
}
.disclaimer-text {
    color: #ffb39a !important;
    font-size: 0.82rem !important;
    line-height: 1.65 !important;
    margin: 0 !important;
}
.disclaimer-text strong {
    color: #ff7043 !important;
}

/* --- Suggest label --- */
.suggest-label {
    font-size: 0.73rem;
    color: #a07060;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 9px;
    display: block;
}

/* --- All buttons (example + primary) --- */
.stButton > button {
    background: #1e1e1e !important;
    border: 1.5px solid rgba(230, 74, 25, 0.35) !important;
    border-radius: 11px !important;
    color: #ffb39a !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.83rem !important;
    font-weight: 700 !important;
    padding: 10px 14px !important;
    text-align: left !important;
    transition: all 0.18s !important;
    white-space: normal !important;
    height: auto !important;
    min-height: 48px !important;
    line-height: 1.4 !important;
}
.stButton > button:hover {
    background: #2a1508 !important;
    border-color: #e64a19 !important;
    color: #ffe0d0 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(230, 74, 25, 0.22) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #c62828, #e64a19, #f57c00) !important;
    border: none !important;
    color: #fff !important;
    font-size: 0.92rem !important;
    padding: 11px 24px !important;
    text-align: center !important;
    box-shadow: 0 4px 18px rgba(230, 74, 25, 0.40) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #b71c1c, #d84315, #ef6c00) !important;
    box-shadow: 0 6px 24px rgba(230, 74, 25, 0.50) !important;
    transform: translateY(-1px) !important;
    color: #fff !important;
}

/* --- Text input --- */
.stTextInput > div > div > input {
    background: #1e1e1e !important;
    border: 1.5px solid rgba(230, 74, 25, 0.30) !important;
    border-radius: 11px !important;
    color: #f5d8cc !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.93rem !important;
    padding: 11px 15px !important;
}
.stTextInput > div > div > input::placeholder { color: #7a5a50 !important; }
.stTextInput > div > div > input:focus {
    border-color: #e64a19 !important;
    box-shadow: 0 0 0 3px rgba(230, 74, 25, 0.14) !important;
}
label[data-testid="stWidgetLabel"] {
    color: #c49a88 !important;
    font-size: 0.84rem !important;
}

/* --- Login card --- */
.login-card {
    background: #161616;
    border: 1px solid rgba(230, 74, 25, 0.20);
    border-radius: 18px;
    padding: 36px 36px 30px;
    text-align: center;
    margin-top: 10px;
    box-shadow: 0 4px 40px rgba(0,0,0,0.50);
}
.login-card h2 {
    font-family: 'Lora', serif !important;
    color: #ff7043 !important;
    font-size: 1.45rem !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
}
.login-card p {
    color: #c9a898 !important;
    font-size: 0.90rem !important;
    line-height: 1.65 !important;
    margin-bottom: 22px !important;
}

/* --- Divider --- */
.section-divider {
    border: none;
    border-top: 1.5px dashed rgba(230, 74, 25, 0.18);
    margin: 16px 0 18px;
}

/* --- Chat messages --- */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 4px 0 !important;
}
[data-testid="stChatMessageContent"] p {
    color: #f0ddd5 !important;
    line-height: 1.80 !important;
}
[data-testid="stChatMessageContent"] strong { color: #ffb39a !important; }
[data-testid="stChatMessageContent"] li { color: #f0ddd5 !important; }
[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3 {
    color: #ffb39a !important;
}

/* --- Chat input --- */
[data-testid="stChatInput"] > div {
    background: #1e1e1e !important;
    border: 1.5px solid rgba(230, 74, 25, 0.28) !important;
    border-radius: 14px !important;
    box-shadow: 0 2px 14px rgba(0,0,0,0.30) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #f5d8cc !important;
    font-family: 'Nunito', sans-serif !important;
    font-size: 0.92rem !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #7a5a50 !important; }

/* --- Reference box --- */
.ref-box {
    background: #1a0e08;
    border: 1px solid rgba(230, 74, 25, 0.22);
    border-radius: 10px;
    padding: 12px 16px;
    margin-top: 12px;
}
.ref-title {
    font-weight: 800;
    color: #ff8a65;
    font-size: 0.71rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 5px;
}
.ref-item {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 4px 0;
    border-bottom: 1px solid rgba(230, 74, 25, 0.10);
}
.ref-item:last-child { border-bottom: none; }
.ref-num {
    background: #e64a19;
    color: #fff;
    border-radius: 50%;
    width: 18px; height: 18px;
    font-size: 0.68rem; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0; margin-top: 1px;
}
.ref-name { color: #c9a090; font-weight: 600; font-size: 0.82rem; line-height: 1.4; }

/* --- Spinner --- */
.stSpinner > div { border-top-color: #e64a19 !important; }

/* --- Footer --- */
.app-footer {
    text-align: center;
    color: #7a5a50;
    font-size: 0.74rem;
    padding: 10px 0 4px;
    line-height: 1.7;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# 3. SOURCE NAME MAPPING
# ==========================================
SOURCE_MAP = {
    "1000_HPK.md":
        "Buku 1000 HPK",
    "2294-Pahami dan Cegah Stunting.md":
        "Buku Pahami dan Cegah Stunting",
    "Buku Stunting.md":
        "Buku Stunting",
    "BUKU-REFERENSI-STUDY-GUIDE-STUNTING_2018.md":
        "Study Guide - Stunting dan Upaya Pencegahannya",
    "buku-saku-kader-pintar-cegah-stunting.md":
        "Buku Saku Kader Pintar Cegah Stunting",
    "KeluargaBebasStunting.md":
        "Buku Keluarga Bebas Stunting",
    "MELANGKAH-MAJU-INISIATIF-LOKAL-DALAM-MENURUNKAN-STUNTING-DI-INDONESIA.md":
        "Melangkah Maju: Inisiatif Lokal dalam Menurunkan Stunting",
    "Modul Pencegahan Stunting.md - EBOOK":
        "Modul Pencegahan Stunting (Ebook)",
    "PEDOMAN PENCEGAHAN DAN TATALAKSANA GIZI BURUK PADA BALITA.md":
        "Pedoman Pencegahan Gizi Buruk pada Balita",
    "PGS Ibu Hamil dan Ibu Menyusui - Merge-1.md":
        "Pedoman Gizi Seimbang Ibu Hamil dan Menyusui",
    "V5 Buku KIA Revisi 2024 Final.md":
        "Buku KIA Revisi 2024",
}

def get_display_source(filename: str) -> str:
    return SOURCE_MAP.get(filename, filename)


# ==========================================
# 4. HELPER — render_refs
# ==========================================
def render_refs(sources: list):
    """Render a styled reference box."""
    if not sources:
        st.markdown("""
        <div class="ref-box">
          <div class="ref-title">Sumber Referensi</div>
          <div style="color:#c49a88;font-size:0.83rem;">Tidak ada referensi spesifik dari dokumen.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    items_html = "".join([
        f'<div class="ref-item">'
        f'<div class="ref-num">{i + 1}</div>'
        f'<div class="ref-name">{get_display_source(src)}</div>'
        f'</div>'
        for i, src in enumerate(sources)
    ])
    st.markdown(f"""
    <div class="ref-box">
      <div class="ref-title">Sumber Referensi</div>
      {items_html}
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# 5. RAG ENGINE (cached)
# ==========================================
@st.cache_resource
def get_rag_engine():
    return StuntingRAG()

rag = get_rag_engine()


# ==========================================
# 6. SESSION STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "show_empty_warning" not in st.session_state:
    st.session_state.show_empty_warning = False


# ==========================================
# 7. BRAND HEADER
# ==========================================
st.markdown("""
<div class="brand-header">
  <p class="brand-title">Chatbot Pencegahan Stunting</p>
  <p class="brand-subtitle">Informasi gizi anak dan ibu berbasis buku referensi terpercaya</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# 8. LOGIN SCREEN
# ==========================================
def show_login():
    st.markdown("""
    <div class="login-card">
      <h2>Selamat Datang</h2>
      <p>
        Sebelum memulai konsultasi mengenai
        <strong style="color:#ff7043;">gizi anak</strong> dan
        <strong style="color:#ff7043;">pencegahan stunting</strong>,
        silakan perkenalkan diri Anda terlebih dahulu.
      </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=False):
        name_input = st.text_input(
            "Nama Anda",
            placeholder="Contoh: Bu Sari, Pak Budi, Kader Posyandu...",
        )
        submitted = st.form_submit_button(
            "Mulai Konsultasi",
            type="primary",
            use_container_width=True,
        )
        if submitted:
            if name_input.strip() == "":
                st.error("Mohon isi nama Anda sebelum melanjutkan.")
            else:
                st.session_state.user_name = name_input.strip()
                st.rerun()

    st.markdown("""
    <div style="text-align:center;color:#a07060;font-size:0.78rem;margin-top:16px;line-height:1.8;">
      Data Anda tidak dibagikan ke pihak mana pun &nbsp;&middot;&nbsp;
      Berbasis 11 buku referensi nasional
    </div>
    """, unsafe_allow_html=True)


if st.session_state.user_name is None:
    show_login()
    st.stop()


# ==========================================
# 9. MAIN CHAT UI
# ==========================================
first_name = st.session_state.user_name.split()[0]

# Greeting bar
st.markdown(f"""
<div class="greeting-bar">
  <div>
    <div class="greet-name">Halo, {st.session_state.user_name}!</div>
    <div class="greet-sub">Silakan tanyakan apa pun seputar gizi dan stunting anak.</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
<div class="disclaimer-box">
  <div class="disclaimer-icon">⚕️</div>
  <p class="disclaimer-text">
    <strong>Disclaimer:</strong> Informasi yang diberikan chatbot ini bersifat edukatif dan
    <strong>bukan pengganti diagnosis atau saran medis profesional</strong>.
    Selalu konsultasikan kondisi anak dan kehamilan Anda kepada
    <strong>dokter, bidan, atau tenaga kesehatan</strong> terdekat untuk penanganan yang tepat.
  </p>
</div>
""", unsafe_allow_html=True)

st.info("Chatbot ini beroperasi **tanpa memori antar percakapan**. "
        "Berikan pertanyaan yang lengkap dan spesifik untuk hasil terbaik.")

# ==========================================
# EXAMPLE QUESTIONS
# Hanya tampil jika belum ada riwayat chat
# dan tidak ada pending_query
# ==========================================
show_examples = (
    len(st.session_state.messages) == 0
    and "pending_query" not in st.session_state
)

if show_examples:
    st.markdown('<span class="suggest-label">Coba tanyakan</span>', unsafe_allow_html=True)

    examples = [
        "Makanan bergizi untuk anak balita",
        "Makanan bergizi untuk ibu hamil",
        "Cara mengecek apakah anak stunting",
        "Apa itu 1000 HPK?",
    ]
    cols = st.columns(2)
    for i, label in enumerate(examples):
        with cols[i % 2]:
            if st.button(label, key=f"ex_{i}", use_container_width=True):
                # Simpan ke pending_query, rerun agar tombol hilang dan flow masuk ke bawah
                st.session_state.pending_query = label
                st.rerun()

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# --- Render existing chat history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("refs") is not None:
            render_refs(msg["refs"])

# --- Resolve final query: ambil dari chat_input ATAU pending_query ---
# PENTING: chat_input harus selalu dipanggil agar Streamlit tidak error,
# lalu pending_query (dari tombol contoh) akan menimpanya jika ada.
chat_input_value = st.chat_input(f"Ketik pertanyaan Anda, {first_name}...")

# Ambil pending_query (dari tombol contoh) — prioritas di atas chat_input
if "pending_query" in st.session_state:
    user_input = st.session_state.pop("pending_query")
else:
    user_input = chat_input_value

# Frasa yang menandakan jawaban "tidak ditemukan" di dokumen
NO_INFO_PHRASES = [
    "belum tersedia dalam dokumen referensi",
    "tidak tersedia dalam dokumen referensi",
    "tidak ditemukan dalam dokumen",
    "belum ada dalam dokumen",
    "informasi tersebut belum tersedia",
    "tidak ada informasi",
]

def is_no_info_answer(text: str) -> bool:
    # Jawaban panjang (>300 karakter) berarti ada info tambahan → tetap render refs
    if len(text.strip()) > 300:
        return False
    lowered = text.lower()
    return any(phrase in lowered for phrase in NO_INFO_PHRASES)

# --- Peringatan input kosong ---
if user_input is not None and user_input.strip() == "":
    st.session_state.show_empty_warning = True
    user_input = None
else:
    st.session_state.show_empty_warning = False

if st.session_state.show_empty_warning:
    st.warning("Pertanyaan tidak boleh kosong. Silakan ketik pertanyaan Anda terlebih dahulu.")

# --- Process and respond ---
if user_input and user_input.strip():

    # Tampilkan pesan user
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Tampilkan respons asisten dengan spinner di dalam chat bubble
    with st.chat_message("assistant"):
        with st.spinner("Mencari informasi terbaik untuk Anda..."):
            response = rag.run(user_input, user_name=st.session_state.user_name)

        final_answer = response["answer"]
        referensi_docs = response.get("context", [])

        st.markdown(final_answer)

        # Jika jawaban adalah "tidak ditemukan", tidak tampilkan ref-box
        if not is_no_info_answer(final_answer):
            seen = set()
            unique_sources = []
            if referensi_docs and isinstance(referensi_docs, list):
                for doc in referensi_docs:
                    src = doc.metadata.get("sumber", "Tidak diketahui")
                    if src not in seen:
                        seen.add(src)
                        unique_sources.append(src)
            render_refs(unique_sources)
        else:
            unique_sources = []

    st.session_state.messages.append({
        "role": "assistant",
        "content": final_answer,
        "refs": unique_sources if not is_no_info_answer(final_answer) else None,
    })

# --- Footer ---
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div class="app-footer">
  Berdasarkan 11 buku referensi nasional &nbsp;&middot;&nbsp;
  Bukan pengganti konsultasi dokter / bidan
</div>
""", unsafe_allow_html=True)