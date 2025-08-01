#extracted.py
import os
import re
import torch
from pathlib import Path
from unidecode import unidecode
from transformers import AutoProcessor, VisionEncoderDecoderModel
from PIL import Image
from pdf2image import convert_from_path
import pdfplumber
from datetime import datetime

#Direktori kerja
DATA_DIR = Path("bps_publikasi_brs") #data di dalam folder yang foldernya sama ada di dalam folder project
EXTRACTED_DIR = Path("extracted")
EXTRACTED_DIR.mkdir(exist_ok=True)

#Load model Nougat
device = "cuda" if torch.cuda.is_available() else "cpu"
model = VisionEncoderDecoderModel.from_pretrained("facebook/nougat-base").to(device)
processor = AutoProcessor.from_pretrained("facebook/nougat-base")

#Fungsi pembersihan teks
def clean_text(text):
    text = unidecode(text)
    text = re.sub(r"Badan Pusat Statistik.*\n", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Statistik.*[0-9]{4}", "", text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r"Halaman\s+\d+", "", text)
    return text.strip()


def extract_with_nougat(pdf_path, page_number):
    img = convert_from_path(pdf_path, dpi=200, first_page=page_number, last_page=page_number)[0]
    pixel_values = processor(images=img, return_tensors="pt").pixel_values.to(device)
    generated_ids = model.generate(pixel_values, max_new_tokens=2048)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

def is_complex_page(text):
    text_clean = text.strip()
    if len(text_clean) < 100:  # teks terlalu sedikit
        return True
    if not re.search(r'[A-Za-z]', text_clean):  # tidak ada huruf alfabet
        return True
    digits_ratio = sum(c.isdigit() for c in text_clean) / max(len(text_clean), 1)
    if digits_ratio > 0.6:  # halaman didominasi angka (tabel)
        return True
    return False

def extract_hybrid(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            current_time = datetime.now().strftime("%H:%M:%S")
            text = page.extract_text() or ""

            # Hybrid: tentukan metode
            if is_complex_page(text):
                print(f" [{current_time}] Fallback Nougat halaman {i+1}/{total_pages}")
                try:
                    text_nougat = extract_with_nougat(pdf_path, i+1)
                    full_text += text_nougat + "\n\n"
                except Exception as e:
                    print(f"Nougat gagal di halaman {i+1}: {e}")
            else:
                print(f" [{current_time}] Ekstraksi Tradisional halaman {i+1}/{total_pages}")
                full_text += text.strip() + "\n\n"
    return clean_text(full_text)

for file_path in Path(DATA_DIR).glob("*.pdf"):
    print(f"Memproses dokumen: {file_path.name}")
    try:
        extracted_text = extract_hybrid(str(file_path))
        if extracted_text.strip():
            output_path = EXTRACTED_DIR / f"{file_path.stem}.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(extracted_text)
            print(f"Tersimpan: {output_path}")
        else:
            print(f"Tidak ada teks yang diekstrak: {file_path.name}")
    except Exception as e:
        print(f"Gagal memproses {file_path.name}: {e}")

print("Semua dokumen selesai diproses dengan mode HYBRID.")
