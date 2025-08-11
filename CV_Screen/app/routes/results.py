from flask import Blueprint, render_template
from app.models import Candidate, CVDetail
from app import db

results_bp = Blueprint('results', __name__)

@results_bp.route('/results')
def show_results():
    candidates = Candidate.query.order_by(Candidate.match_score.desc()).all()

    # Lấy chi tiết CV tương ứng theo từng candidate_id
    candidate_details = {}
    for c in candidates:
        detail = CVDetail.query.filter_by(candidate_id=c.id).first()
        if detail:
            candidate_details[c.id] = detail

    return render_template("results.html", candidates=candidates, candidate_details=candidate_details)
