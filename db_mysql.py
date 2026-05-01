import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"❌ Error Koneksi Database: {err}")
        return None


def save_chat_to_db(user_name, question, answer, duration):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Query disesuaikan untuk 4 variabel
            sql = "INSERT INTO chat_logs (nama_user, pertanyaan_user, jawaban_llm, durasi_detik) VALUES (%s, %s, %s, %s)"
            val = (user_name, question, answer, duration)
            cursor.execute(sql, val)
            conn.commit()
            print(f"   -> 💾 Berhasil menyimpan log ({duration} detik) ke MySQL.")
        except mysql.connector.Error as err:
            print(f"   -> ❌ Gagal menyimpan ke database: {err}")
        finally:
            cursor.close()
            conn.close()