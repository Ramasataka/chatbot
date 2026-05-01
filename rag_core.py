import time
from vectorDatabase import VectorDatabase
from retrieval import StuntingRetriever
from generation import GenerationEngine
from db_mysql import save_chat_to_db

class StuntingRAG:
    def __init__(self):
        db = VectorDatabase().load_db()
        self.retriever = StuntingRetriever(db).get_retriever()

        engine = GenerationEngine()
        self.doc_grader  = engine.get_doc_grader()
        self.rewriter    = engine.get_rewriter()
        self.generator   = engine.get_generator()
        self.ans_grader  = engine.get_answer_grader()

    def run(self, question: str, user_name: str = "Anonim", max_retries: int = 2):
        start_time       = time.time()
        current_question = question

        for attempt in range(max_retries + 1):
            print(f"\n[🔄 Iterasi {attempt + 1}] Memproses Query: '{current_question}'")

            # ── Retrieval ──────────────────────────────────────────────
            docs    = self.retriever.invoke(current_question)
            context = "\n\n".join([d.page_content for d in docs])
            print(f"   -> Konteks ditemukan ({len(docs)} dokumen)")

            # ── Document grading ───────────────────────────────────────
            print("   -> 🔎 Evaluasi relevansi dokumen...")
            doc_grade = self.doc_grader.invoke(
                {"context": context, "question": current_question}
            ).strip().lower()
            print(f"   -> Hasil Grading Dokumen: {doc_grade}")

            if "no" in doc_grade:
                print("   -> ❌ Dokumen TIDAK RELEVAN.")
                if attempt < max_retries:
                    print("   -> ✍️ Query Rewrite...")
                    current_question = self.rewriter.invoke({"question": current_question})
                    print(f"   -> Pertanyaan Baru: '{current_question}'")
                    continue
                else:
                    final_answer = (
                        "Maaf, informasi tidak ditemukan meskipun telah dilakukan "
                        "pencarian mendalam. Silakan coba pertanyaan yang lebih spesifik."
                    )
                    duration = round(time.time() - start_time, 2)
                    save_chat_to_db(user_name, question, final_answer, duration)
                    return {"answer": final_answer, "context": []}

            # ── Generation ─────────────────────────────────────────────
            print("   -> ✅ Dokumen RELEVAN. Menghasilkan jawaban...")
            answer = self.generator.invoke(
                {"context": context, "question": current_question}
            )
            print(f"   -> Jawaban: '{str(answer)[:120]}...'")

            # ── Answer grading ─────────────────────────────────────────
            # FIX: prompt ans_grader expects 'context' — always include it.
            print("   -> ⚖️ Validasi jawaban...")
            ans_grade = self.ans_grader.invoke(
                {"question": current_question, "answer": answer, "context": context}
            ).strip().lower()
            print(f"   -> Hasil Validasi: {ans_grade}")

            if "yes" in ans_grade:
                print("   -> 🎯 Jawaban Valid!")
                duration = round(time.time() - start_time, 2)
                save_chat_to_db(user_name, question, answer, duration)
                return {"answer": answer, "context": docs}
            else:
                print("   -> ⚠️ Jawaban belum optimal.")
                if attempt < max_retries:
                    print("   -> ✍️ Query Rewrite untuk menggali lebih dalam...")
                    current_question = self.rewriter.invoke({"question": current_question})
                    continue
                else:
                    duration = round(time.time() - start_time, 2)
                    save_chat_to_db(user_name, question, answer, duration)
                    return {"answer": answer, "context": docs}