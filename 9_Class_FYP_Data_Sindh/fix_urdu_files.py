import os
import sqlite3
import fitz  # PyMuPDF
import easyocr
import time

# --- Configuration ---
DATABASE_FILE = 'knowledge.db'
BASE_FOLDER = '9_Class_FYP_Data_Sindh' # Aapka main data folder

# --- ZAROORI: Yahan un files ka path likhen jin mein Urdu hai ---
FILES_TO_REPROCESS = [
    # Paths ab relative hain aur "/" istemal kar rahe hain
    '9_Class_Books/Urdu_Book_9_part1.pdf',
    '9_Class_Books/Urdu_Book_9_part2.pdf',
    '9_Class_Books/Urdu_Book_9_part3.pdf',
    '9_Class_Books/Urdu_Book_9_part4.pdf',
    '9_Class_Books/Urdu_Book_9_part5.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_1_Part1.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_1_Part2.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_2.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_3_A.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_3_B.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_3_C_part1.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_3_c_part2.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_3_D.pdf',
    '9_Class_Books/Islamiat_Book_Chapter_4.pdf',
    '9_Class_Notes/9th URDU Chapter 1 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 2 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 3 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 4 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 5 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 6 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 7 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 8 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 9 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 10 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 11 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 12 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 13 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 14 Sindh Board Notes(1).pdf',
    '9_Class_Notes/9th URDU Chapter 16 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 17 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 18 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 19 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 20 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 21 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 22 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 23 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 24 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 25 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 26 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 28 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 29 Sindh Board Notes.pdf',
    '9_Class_Notes/9th URDU Chapter 30 Sindh Board Notes.pdf',
    '9_Class_Notes/9th-Class-Islamiat-Unique-Notes-New-Syllabus-Chapter-1.pdf',
    '9_Class_Notes/9th-Class-Islamiat-Unique-Notes-New-Syllabus-Chapter-2.pdf',
    '9_Class_Notes/9th-Class-Islamiat-Unique-Notes-New-Syllabus-Chapter-3.pdf',
    '9_Class_Notes/9th-Class-Islamiat-Unique-Notes-New-Syllabus-Chapter-4.pdf',
    '9_Class_Notes/9th-Class-Islamiat-Unique-Notes-New-Syllabus-Chapter-5.pdf',
    '9_Class_Notes/9th-Class-Islamiat-Unique-Notes-New-Syllabus-Chapter-6.pdf',
    '9_Class_Notes/9th-Class-Islamiat-Unique-Notes-New-Syllabus-Chapter-7.pdf',
]
# -----------------------------------------------------------------

# Load EasyOCR (BILINGUAL MODEL)
print("Loading BILINGUAL (En+Ur) OCR model... Ismein time lagega...")
reader = easyocr.Reader(['en', 'ur']) 
print("Bilingual model loaded. Targeting specific files...")

def re_process_file(file_path, category, subject):
    """
    File ko dobara OCR karta hai (Urdu+English) aur database mein update karta hai.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    file_name = os.path.basename(file_path)

    try:
        # --- Step 1: Purana (English-only) data DELETE karen ---
        print(f"    - Deleting old (English-only) entry for: {file_name}")
        cursor.execute("DELETE FROM knowledge WHERE source_file = ?", (file_name,))
        conn.commit()

        # --- Step 2: Naya (Urdu+English) data OCR karen ---
        print(f"    - Re-processing with (En+Ur) OCR...")
        doc = fitz.open(file_path)
        full_document_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap(dpi=150) 
            img_bytes = pix.tobytes("png")
            
            results = reader.readtext(img_bytes)
            
            for (bbox, text, prob) in results:
                full_document_text += text + " "
            print(f"    - Page {page_num + 1} read...")

        # --- Step 3: Naya data database mein INSERT karen ---
        if len(full_document_text.strip()) > 10:
            cursor.execute(
                "INSERT INTO knowledge (category, subject, source_file, text_chunk) VALUES (?, ?, ?, ?)",
                (category, subject, file_name, full_document_text.strip())
            )
            conn.commit()
            print(f"    - SUCCESS: New (En+Ur) data for {file_name} saved.")
        else:
            print(f"    - WARNING: No text found in {file_name}.")
            
    except Exception as e:
        print(f"    - !!! FAILED to process {file_name}. Error: {e}")
    
    finally:
        conn.close()

# --- Main Program ---
if __name__ == '__main__':
    start_time = time.time()
    
    print(f"Starting targeted re-processing for {len(FILES_TO_REPROCESS)} files...")

    for relative_path in FILES_TO_REPROCESS:
        full_path = os.path.join(BASE_FOLDER, relative_path)
        
        if os.path.exists(full_path):
            try:
                # --- YEH LINE FIX HO GAYI HAI ---
                parts = relative_path.split('/') # Hum '/' par split kar rahe hain
                # --- FIX ENDS ---
                
                category = parts[0]
                subject = parts[1]
                
                print(f"\n-> Targeting file: {relative_path}")
                re_process_file(full_path, category, subject)
                
            except Exception as e:
                print(f"    - ERROR: Could not parse path {relative_path}: {e}")
        else:
            print(f"\n-> SKIPPING: File not found at {full_path}")
            print(f"   (Script looked for: {full_path})") # Debug line

    end_time = time.time()
    print("\n--- TARGETED PROCESSING COMPLETE ---")
    print(f"Total files re-processed: {len(FILES_TO_REPROCESS)}")
    print(f"Total time taken: {(end_time - start_time) / 60:.2f} minutes")