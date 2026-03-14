from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from ..models import Profile, Project, Skill, Experience, Admin, PageView
from ..extensions import csrf, limiter
from sqlalchemy import func
from datetime import datetime, timedelta

api_bp = Blueprint("api", __name__)

# Exempt the entire API blueprint from CSRF (uses JWT / JSON, not form posts)
csrf.exempt(api_bp)


@api_bp.route("/profile", methods=["GET"])
def get_profile():
    profile = Profile.query.first()
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify({
        "name": profile.name,
        "title": profile.title,
        "tagline": profile.tagline,
        "bio": profile.bio,
        "email": profile.email,
        "phone": profile.phone,
        "location": profile.location,
        "profile_image": profile.profile_image,
    })


@api_bp.route("/projects", methods=["GET"])
def get_projects():
    projects = Project.query.order_by(Project.id.desc()).all()
    return jsonify([{
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "github": p.github,
        "demo": p.demo,
        "image": p.image,
    } for p in projects])


@api_bp.route("/skills", methods=["GET"])
def get_skills():
    skills = Skill.query.all()
    return jsonify([{"id": s.id, "name": s.name} for s in skills])


@api_bp.route("/experience", methods=["GET"])
def get_experience():
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    return jsonify([{
        "id": e.id,
        "role": e.role,
        "company": e.company,
        "company_url": e.company_url,
        "location": e.location,
        "start_date": e.start_date,
        "end_date": e.end_date,
        "description": e.description,
    } for e in experiences])


@api_bp.route("/visitor-stats", methods=["GET"])
def get_visitor_stats():
    """Get public visitor statistics."""
    total_visitors = PageView.query.count()
    today = datetime.utcnow().date()
    today_visitors = PageView.query.filter(
        func.date(PageView.created_at) == today
    ).count()
    unique_countries = PageView.query.with_entities(
        PageView.country
    ).distinct().count()

    return jsonify({
        "total": total_visitors,
        "today": today_visitors,
        "countries": unique_countries,
    })


@api_bp.route("/auth/login", methods=["POST"])
@limiter.limit("5 per minute")
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON body"}), 400

    username = data.get("username", "")
    password = data.get("password", "")

    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        token = create_access_token(identity=str(admin.id))
        return jsonify({"access_token": token})

    return jsonify({"error": "Invalid credentials"}), 401
