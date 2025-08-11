import os
import json
import time
from pathlib import Path
from app.utils.cv_parser import extract_text_from_file
from app.utils.llm_client import extract_cv_info_with_llm

RAW_CV_DIR = Path("data/raw")
PROCESSED_CV_DIR = Path("data/processed")
PROCESSED_CV_DIR.mkdir(parents=True, exist_ok=True)

def extract_cv_info(file_path):
    """
    Hàm trích xuất thông tin từ 1 file CV (PDF hoặc DOCX) và lưu ra file JSON
    Trả về dữ liệu đã trích xuất (dict)
    """
    try:
        # Trích xuất văn bản từ CV
        cv_text = extract_text_from_file(file_path)

        # Gọi LLM để trích xuất thông tin
        extracted_data = extract_cv_info_with_llm(cv_text)

        # Lưu kết quả ra file JSON
        json_path = PROCESSED_CV_DIR / f"{Path(file_path).stem}.json"
        with open(json_path, "w", encoding="utf-8-sig") as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=2)

        return extracted_data

    except Exception as e:
        raise RuntimeError(f"❌ Error processing {file_path}: {e}")


def extract_all_cv_to_json():
    """
    Chạy cho toàn bộ file trong thư mục raw → processed
    """
    files = [f for f in RAW_CV_DIR.iterdir() if f.suffix.lower() in ['.pdf', '.docx']]
    print(f"\n[INFO] Found {len(files)} CVs to process in '{RAW_CV_DIR}'\n")

    for idx, file_path in enumerate(files):
        try:
            print(f"[{idx+1}/{len(files)}] Processing: {file_path.name}")
            extract_cv_info(file_path)
            print(" ✅ Done.\n")
            time.sleep(1.5)  # tránh gọi API quá nhanh
        except Exception as e:
            print(f" ❌ Failed: {e}\n")

if __name__ == "__main__":
    extract_all_cv_to_json()
