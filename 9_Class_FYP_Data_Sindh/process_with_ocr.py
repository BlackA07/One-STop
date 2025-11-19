import os
import sqlite3
import fitz  # This is PyMuPDF
import easyocr
import time

# --- Configuration ---
DATABASE_FILE = 'knowledge.db'
BASE_FOLDER = '9_Class_FYP_Data_Sindh' # This is correct
CATEGORIES = ['9_Class_Books', '9_Class_Notes'] # We will check these names

# Load EasyOCR (this will run only once)
print("Loading EasyOCR... This might take a moment the first time...")
reader = easyocr.Reader(['en']) # English language
print("OCR model loaded. Starting processing...")

def process_file_with_ocr(file_path, category, subject):
    """
    Opens a PDF file, extracts text from each page using OCR,
    and saves it to the database.
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    try:
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

        if len(full_document_text.strip()) > 10:
            cursor.execute(
                "INSERT INTO knowledge (category, subject, source_file, text_chunk) VALUES (?, ?, ?, ?)",
                (category, subject, os.path.basename(file_path), full_document_text.strip())
            )
            conn.commit()
            print(f"    - SUCCESS: Full text for file saved to database.")
        else:
            print(f"    - WARNING: No text found in this file.")
            
    except Exception as e:
        print(f"    - !!! FAILED to process {file_path}. Error: {e}")
    
    finally:
        conn.close()

# --- Main Program ---
if __name__ == '__main__':
    start_time = time.time()
    files_processed = 0
    
    print(f"Starting processing... Folder: '{BASE_FOLDER}'")

    # --- NEW DEBUGGING STEP ---
    # We will print the folders found in the base directory
    is_first_loop = True
    # --- END NEW DEBUGGING STEP ---

    for root, dirs, files in os.walk(BASE_FOLDER):
        
        # --- NEW DEBUGGING STEP ---
        # This will run only once, at the start
        if is_first_loop:
            print(f"\n--- DEBUGGING ---")
            print(f"Base folder ('.') contains these directories: {dirs}")
            print(f"Script is set to look for: {CATEGORIES}")
            print(f"--- END DEBUGGING ---\n")
            is_first_loop = False
        # --- END NEW DEBUGGING STEP ---

        for file in files:
            # Only process .pdf files (case-insensitive)
            if file.lower().endswith('.pdf'):
                
                file_path = os.path.join(root, file)
                
                try:
                    relative_path = os.path.relpath(file_path, BASE_FOLDER)
                    parts = relative_path.split(os.sep)
                    
                    if len(parts) > 1: # Make sure it's inside a subfolder
                        category = parts[0] # e.g., '9_Class_Books'
                        subject = parts[1]  # e.g., 'biology'
                        
                        # Check if the found category is in our list
                        if category in CATEGORIES:
                            print(f"\n-> Processing file: {relative_path}")
                            process_file_with_ocr(file_path, category, subject)
                            files_processed += 1
                
                except Exception as e:
                    print(f"    - ERROR: Could not parse file path {file_path}: {e}")

    end_time = time.time()
    print("\n--- PROCESSING COMPLETE ---")
    print(f"Total PDF files processed with OCR: {files_processed}")
    print(f"Total time taken: {(end_time - start_time) / 60:.2f} minutes")