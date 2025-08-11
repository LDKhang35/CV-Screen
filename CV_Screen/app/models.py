from app import db

class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(255), nullable=False)
    requirements = db.Column(db.Text)
    description = db.Column(db.Text)
    benefits = db.Column(db.Text)
    other = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

class Candidate(db.Model):
    __tablename__ = 'candidates'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(255))
    file_name = db.Column(db.Text)
    matching_score = db.Column(db.Integer)
    classification = db.Column(db.String(50))  # 'Phù hợp', 'Cân nhắc', 'Không phù hợp'
    feedback = db.Column(db.Text)
    jd_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    original_pdf_path = db.Column(db.Text)
    extracted_json_path = db.Column(db.Text)


class CVDetail(db.Model):
    __tablename__ = 'cv_details'
    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidates.id'))
    full_name = db.Column(db.String(255))
    applied_position = db.Column(db.String(255))
    gender = db.Column(db.String(50))
    dob = db.Column(db.String(50))
    email = db.Column(db.String(255))
    address = db.Column(db.Text)
    phone = db.Column(db.String(50))
    skills = db.Column(db.Text)
    experience = db.Column(db.Text)
    university = db.Column(db.String(255))
    major = db.Column(db.String(255))
    gpa = db.Column(db.String(50))
    certifications = db.Column(db.Text)

