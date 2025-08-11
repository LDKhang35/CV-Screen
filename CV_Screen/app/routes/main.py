import os
from flask import Blueprint, json, render_template, request, current_app
from werkzeug.utils import secure_filename
from app import db
from app.models import JobDescription, Candidate, CVDetail
from app.utils.extract_llm import extract_cv_info
from app.utils.llm_client import classify_cv_vs_jd
from app.utils.cv_parser import extract_text_from_file
from app.utils.save_to_db import save_screening_result

main_bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@main_bp.route('/results', methods=['GET', 'POST'])
def screen_cv():
    # 1. Nhận dữ liệu JD
    jd_file = request.files.get('jd_file')
    jd_data = {}

    if jd_file and allowed_file(jd_file.filename):
        jd_text = jd_file.read().decode('utf-8-sig', errors='ignore')
        jd_data = {
            'position': 'Từ file',
            'description': jd_text,
            'requirements': '',
            'benefits': '',
            'other': ''
        }
    else:
        jd_data = {
            'position': request.form.get('job_title', ''),
            'description': request.form.get('description', ''),
            'requirements': request.form.get('requirements', ''),
            'benefits': request.form.get('benefits', ''),
            'other': request.form.get('other', '')
        }

    # Lưu JD vào DB
    jd = JobDescription(**jd_data)
    db.session.add(jd)
    db.session.commit()

    jd_id = jd.id
    full_jd_text = f"{jd.description}\n{jd.requirements}\n{jd.benefits}\n{jd.other}"

    # 2. Nhận và lưu file CV
    cv_files = request.files.getlist('cv_files')
    upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_dir, exist_ok=True)

    results = []

    for file in cv_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_dir, filename)
            file.save(file_path)

            # 3. Trích xuất thông tin bằng LLM
            cv_json = extract_cv_info(file_path)

            # 4. Trích xuất nội dung text thô từ file CV
            raw_cv_text = extract_text_from_file(file_path)

            # 5. Đánh giá CV so với JD bằng LLM
            label, comment, score = classify_cv_vs_jd(raw_cv_text, full_jd_text)

            # 6. Lưu kết quả vào DB
            json_path = os.path.join("data", "processed", filename.rsplit('.', 1)[0] + ".json")
            save_screening_result(
                cv_data=cv_json,
                jd_id=jd_id,
                matching_score=score,
                classification=label,
                feedback=comment,
                file_name=filename,
                original_pdf_path=file_path,
                extracted_json_path=json_path
            )

            # 7. Thêm vào danh sách kết quả
            results.append({
                "file_name" : filename,
                "name": cv_json.get('full_name', 'Không rõ'),
                "similarity": score,
                "skills": ", ".join(cv_json.get('skills', [])) if isinstance(cv_json.get('skills'), list) else cv_json.get('skills', ''),
                "assessment": comment,
                "file_name": filename,
                "details": cv_json,
                "classification": label
            })

    # ✅ Sắp xếp kết quả theo điểm phù hợp giảm dần
    results.sort(key=lambda x: x["similarity"], reverse=True)

    return render_template("results.html", results=results)
