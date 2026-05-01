import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

class GenerationEngine:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("❌ GROQ_API_KEY tidak ditemukan di .env")
            
        self.llm = ChatGroq(
            api_key=api_key,
            model="llama-3.3-70b-versatile",
            temperature=0
        )

    def get_doc_grader(self):
        doc_grader_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "Anda adalah penilai relevansi konteks. Tugas Anda HANYA menentukan apakah potongan dokumen (konteks) "
             "mengandung informasi yang cukup untuk menjawab pertanyaan.\n\n"
             "CARA MENILAI:\n"
             "- Baca pertanyaan, lalu cari apakah konteks memuat kata kunci, angka, prosedur, atau data yang secara "
             "  langsung berkaitan dengan pertanyaan tersebut.\n"
             "- Jika YA → konteks ini berguna sebagai referensi jawaban → jawab 'yes'.\n"
             "- Jika konteks hanya menyinggung topik secara umum tanpa isi yang menjawab → jawab 'no'.\n"
             "- Jika konteks SAMA SEKALI tidak berkaitan → jawab 'no'.\n\n"
             "Jawab HANYA dengan satu kata: 'yes' atau 'no'. Tanpa penjelasan."),
            ("human", 
             "Konteks:\n{context}\n\n"
             "Pertanyaan: {question}\n\n"
             "Apakah konteks ini relevan untuk menjawab pertanyaan?")
        ])
        return doc_grader_prompt | self.llm | StrOutputParser()

    def get_rewriter(self):
        rewriter_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "Anda adalah asisten pencarian dokumen stunting. Tugas Anda memperbaiki pertanyaan pengguna agar "
             "lebih mudah dicocokkan dengan dokumen melalui pencarian semantik (vector similarity).\n\n"
             "INSTRUKSI:\n"
             "1. PERBAIKI TYPO dan ejaan yang salah (contoh: 'brat badan' → 'berat badan').\n"
             "2. PERJELAS maksud pertanyaan jika ambigu, tanpa mengubah topik utamanya.\n"
             "3. TAMBAHKAN 1-2 sinonim atau istilah medis yang relevan di akhir kalimat jika membantu "
             "   pencarian (contoh: tambahkan 'gizi buruk', 'antropometri', 'pertumbuhan balita' jika sesuai).\n"
             "4. JANGAN ubah struktur pertanyaan secara besar-besaran — pertahankan kata kunci asli pengguna.\n"
             "5. JANGAN beri penjelasan. Keluarkan HANYA teks pertanyaan yang sudah diperbaiki."),
            ("human", 
             "Pertanyaan asli: {question}")
        ])
        return rewriter_prompt | self.llm | StrOutputParser()

    def get_generator(self):
        generate_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "Anda adalah asisten informasi pencegahan stunting yang informatif dan terpercaya.\n\n"
             "PANDUAN MENJAWAB:\n"
             "1. GUNAKAN KONTEKS SEBAGAI DASAR: Semua jawaban harus berpijak pada informasi di Konteks Referensi.\n"
             "2. BOLEH ELABORASI RINGAN: Anda boleh menyusun ulang, merangkum, atau menjelaskan isi konteks "
             "   dengan bahasa yang lebih mudah dipahami — selama maknanya tidak berubah dan tidak bertentangan "
             "   dengan konteks.\n"
             "3. FORMAT RAPI: Jika ada data berupa daftar atau angka, susun dalam tabel Markdown jika memungkinkan.\n"
             "4. DATA TIDAK LENGKAP: Jika data di konteks terpotong, sajikan apa adanya dan tambahkan catatan: "
             "   '*Catatan: Data mungkin tidak lengkap karena keterbatasan referensi.*'\n"
             "5. JIKA KONTEKS TIDAK MEMUAT INFORMASI: Jawab dengan jujur: "
             "   'Maaf, informasi tersebut belum tersedia dalam dokumen referensi kami.'\n"
             "6. JANGAN mengarang angka, statistik, atau prosedur medis yang tidak ada di konteks.\n\n"
             "Konteks Referensi:\n{context}"),
            ("human", "{question}")
        ])
        return generate_prompt | self.llm | StrOutputParser()

    def get_answer_grader(self):
        answer_grader_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "Anda adalah validator jawaban. Tugas Anda menilai apakah jawaban AI sudah menjawab pertanyaan "
             "pengguna dengan baik, berdasarkan konteks yang tersedia.\n\n"
             "Kriteria LULUS ('yes'):\n"
             "- Jawaban secara langsung menjawab apa yang ditanyakan pengguna.\n"
             "- Isi jawaban konsisten dan tidak bertentangan dengan konteks (boleh elaborasi, "
             "  asal tidak menyimpang).\n"
             "- AI jujur menyatakan data tidak ada jika memang tidak tersedia di konteks.\n\n"
             "Kriteria GAGAL ('no'):\n"
             "- Jawaban tidak menjawab pertanyaan sama sekali atau melenceng dari topik.\n"
             "- Jawaban mengandung fakta/angka yang bertentangan langsung dengan konteks.\n"
             "- Jawaban menghindari pertanyaan tanpa alasan yang jelas.\n\n"
             "Jawab HANYA dengan satu kata: 'yes' atau 'no'. Tanpa penjelasan."),
            ("human", 
             "Pertanyaan pengguna: {question}\n\n"
             "Konteks Referensi:\n{context}\n\n"
             "Jawaban AI:\n{answer}\n\n"
             "Apakah jawaban ini sudah menjawab pertanyaan pengguna?")
        ])
        return answer_grader_prompt | self.llm | StrOutputParser()