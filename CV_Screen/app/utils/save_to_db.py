from app import db
from app.models import Candidate, CVDetail

def save_screening_result(cv_data, jd_id, matching_score, classification, feedback, file_name, original_pdf_path, extracted_json_path):
    candidate = Candidate(
        full_name=cv_data.get("full_name", "Không rõ"),
        file_name=file_name,
        matching_score=matching_score,
        classification=classification,
        feedback=feedback,
        jd_id=jd_id,
        original_pdf_path=original_pdf_path,
        extracted_json_path=extracted_json_path
    )
    db.session.add(candidate)
    db.session.flush()

    # ✅ Chuyển list/dict sang chuỗi
    skills = cv_data.get("skills", [])
    if isinstance(skills, list):
        skills = ", ".join(skills)

    certifications = cv_data.get("certifications", [])
    if isinstance(certifications, list):
        certifications = ", ".join(certifications)

    experience = cv_data.get("experience", "")
    if isinstance(experience, list) or isinstance(experience, dict):
        import json
        experience = json.dumps(experience, ensure_ascii=False)

    cv_detail = CVDetail(
        candidate_id=candidate.id,
        full_name=cv_data.get("full_name", ""),
        applied_position=cv_data.get("applied_position", ""),
        gender=cv_data.get("gender", ""),
        dob=cv_data.get("dob", ""),
        email=cv_data.get("email", ""),
        address=cv_data.get("address", ""),
        phone=cv_data.get("phone", ""),
        skills=skills,
        experience=experience,
        university=cv_data.get("university", ""),
        major=cv_data.get("major", ""),
        gpa=cv_data.get("gpa", ""),
        certifications=certifications
    )
    db.session.add(cv_detail)
    db.session.commit()
