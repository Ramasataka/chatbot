from rag_core import StuntingRAG

def main():
    print("Mempersiapkan Sistem RAG Stunting (CLI)...")
    rag = StuntingRAG()
    
    print("\n--- Sistem Siap (Ketik 'exit' untuk keluar) ---")
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() == 'exit':
            break
            
        print("Chatbot sedang berpikir dan mengevaluasi data secara mendalam...\n")
        
        # Jalankan RAG TANPA history
        response = rag.run(user_input)
        
        final_answer = response["answer"]
        
        print("\n" + "="*50)
        print("=== JAWABAN CHATBOT ===")
        print(final_answer)
        print("="*50 + "\n")
        
        print("=== SUMBER REFERENSI YANG DIGUNAKAN ===")
        if response["context"] and isinstance(response["context"], list):
            for i, doc in enumerate(response["context"]):
                sumber = doc.metadata.get("sumber", "Tidak diketahui")
                print(f"{i+1}. File: {sumber}")
        else:
            print("- Tidak ada referensi spesifik dari dokumen.")

if __name__ == "__main__":
    main()