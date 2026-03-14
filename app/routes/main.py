import os
from datetime import datetime
from functools import wraps
from flask import (
    Blueprint, render_template, redirect, url_for, request,
    flash, current_app, send_from_directory, session, Response
)
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message as MailMessage
from werkzeug.utils import secure_filename
from sqlalchemy import func
from ..models import (
    Admin, Project, Message, Skill, Experience, Profile, SocialLink,
    CodingProfile, PageView, ResumeDownload, AdminLog,
)
from ..extensions import db, mail, limiter
from config import allowed_file

main = Blueprint("main", __name__)


# ──────────────────────── Helpers ──────────────────────────────────

def _safe_int(value, default=0):
    """Safely convert a value to int."""
    try:
        return int(value or default)
    except (ValueError, TypeError):
        return default


def log_admin_action(action, details=None):
    """Log an admin action."""
    if current_user.is_authenticated:
        log = AdminLog(
            admin_id=current_user.id,
            action=action,
            details=details,
            ip_address=request.remote_addr,
        )
        db.session.add(log)
        db.session.commit()


# ──────────────────────── Context Processor ────────────────────────

@main.app_context_processor
def inject_globals():
    chatbot_enabled = bool(
        current_app.config.get("OPENAI_API_KEY")
        and current_app.config.get("OPENAI_API_KEY") != "your-openai-api-key"
    )
    return {
        "current_year": datetime.utcnow().year,
        "chatbot_enabled": chatbot_enabled,
    }


# ──────────────────────── Public: Home Page ────────────────────────

@main.route("/")
def index():
    from ..analytics import track_page_view
    try:
        track_page_view("/")
    except Exception:
        pass

    profile = Profile.query.first()
    projects = Project.query.order_by(Project.id.desc()).all()
    skills = Skill.query.all()
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    social_links = SocialLink.query.all()
    coding_profiles = CodingProfile.query.all()

    resume_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "resumes", "resume.pdf")
    resume_exists = os.path.exists(resume_path)

    # Extract GitHub username from social links for heatmap
    github_username = None
    if social_links:
        for link in social_links:
            if 'github' in link.url.lower():
                github_username = link.url.rstrip('/').split('/')[-1]
                break

    return render_template(
        "index.html",
        profile=profile,
        projects=projects,
        skills=skills,
        experiences=experiences,
        social_links=social_links,
        coding_profiles=coding_profiles,
        resume_exists=resume_exists,
        github_username=github_username,
    )


# ──────────────────────── Public: Contact Form ─────────────────────

@main.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message_text = request.form.get("message", "").strip()

    if not name or not email or not message_text:
        flash("Please fill in all required fields.", "danger")
        return redirect(url_for("main.index", _anchor="contact"))

    msg = Message(name=name, email=email, subject=subject, message=message_text)
    db.session.add(msg)
    db.session.commit()

    # Try to send email notification
    admin_email = current_app.config.get("ADMIN_EMAIL")
    if admin_email and current_app.config.get("MAIL_USERNAME"):
        try:
            email_msg = MailMessage(
                subject=f"Portfolio Contact: {subject or 'New Message'} from {name}",
                sender=current_app.config["MAIL_DEFAULT_SENDER"],
                recipients=[admin_email],
                body=f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\nMessage:\n{message_text}",
            )
            mail.send(email_msg)
        except Exception as e:
            current_app.logger.error(f"Failed to send email notification: {e}")

    flash("Your message has been sent successfully!", "success")
    return redirect(url_for("main.index", _anchor="contact"))


# ──────────────────────── Public: Resume Download ──────────────────

@main.route("/download-resume")
def download_resume():
    from ..analytics import track_resume_download
    try:
        track_resume_download()
    except Exception:
        pass

    return send_from_directory(
        os.path.join(current_app.config["UPLOAD_FOLDER"], "resumes"),
        "resume.pdf",
        as_attachment=True,
    )


# ──────────────────────── SEO: Sitemap & Robots ───────────────────

@main.route("/sitemap.xml")
def sitemap():
    site_url = current_app.config.get("SITE_URL", request.url_root.rstrip("/"))
    pages = [
        {"loc": site_url + "/", "priority": "1.0"},
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for page in pages:
        xml.append(f'  <url><loc>{page["loc"]}</loc><priority>{page["priority"]}</priority></url>')
    xml.append("</urlset>")
    return Response("\n".join(xml), mimetype="application/xml")


@main.route("/robots.txt")
def robots():
    site_url = current_app.config.get("SITE_URL", request.url_root.rstrip("/"))
    content = f"User-agent: *\nAllow: /\nSitemap: {site_url}/sitemap.xml\n"
    return Response(content, mimetype="text/plain")


# ──────────────────────── Auth: Login / Logout ─────────────────────

@main.route("/admin/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            if admin.is_2fa_enabled and admin.totp_secret:
                session["pending_2fa_admin_id"] = admin.id
                return redirect(url_for("main.verify_2fa"))

            login_user(admin)
            log_admin_action("login")
            flash("Welcome back!", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid credentials.", "danger")
    return render_template("admin_login.html")


@main.route("/verify-2fa", methods=["GET", "POST"])
def verify_2fa():
    admin_id = session.get("pending_2fa_admin_id")
    if not admin_id:
        return redirect(url_for("main.admin_login"))

    if request.method == "POST":
        token = request.form.get("token", "").strip()
        admin = db.session.get(Admin,admin_id)

        if admin and admin.verify_totp(token):
            session.pop("pending_2fa_admin_id", None)
            login_user(admin)
            log_admin_action("login (2FA)")
            flash("Welcome back!", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid 2FA code. Please try again.", "danger")

    return render_template("verify_2fa.html")


@main.route("/admin/logout")
@login_required
def admin_logout():
    log_admin_action("logout")
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))


# ──────────────────────── Admin: Dashboard ─────────────────────────

@main.route("/admin/dashboard")
@login_required
def dashboard():
    profile = Profile.query.first()
    projects = Project.query.order_by(Project.id.desc()).all()
    skills = Skill.query.order_by(Skill.id.desc()).all()
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    messages = Message.query.order_by(Message.id.desc()).all()
    social_links = SocialLink.query.all()

    resume_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "resumes", "resume.pdf")
    resume_exists = os.path.exists(resume_path)

    return render_template(
        "dashboard.html",
        profile=profile,
        projects=projects,
        skills=skills,
        experiences=experiences,
        messages=messages,
        social_links=social_links,
        resume_exists=resume_exists,
    )


# ──────────────────────── Admin: Profile ───────────────────────────

@main.route("/admin/profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    profile = Profile.query.first()
    if not profile:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()

    social_links = SocialLink.query.all()

    if request.method == "POST":
        profile.name = request.form.get("name", "").strip()
        profile.title = request.form.get("title", "").strip()
        profile.tagline = request.form.get("tagline", "").strip()
        profile.bio = request.form.get("bio", "").strip()
        profile.email = request.form.get("email", "").strip()
        profile.phone = request.form.get("phone", "").strip()
        profile.location = request.form.get("location", "").strip()

        image_file = request.files.get("profile_image")
        if image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], "profile_images", filename
            )
            image_file.save(save_path)
            profile.profile_image = filename

        db.session.commit()
        log_admin_action("update_profile")
        flash("Profile updated successfully!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("edit_profile.html", profile=profile, social_links=social_links)


# ──────────────────────── Admin: Social Links ──────────────────────

@main.route("/admin/social/add", methods=["POST"])
@login_required
def add_social():
    name = request.form.get("name", "").strip()
    url = request.form.get("url", "").strip()
    icon = request.form.get("icon", "").strip()

    if name and url:
        link = SocialLink(name=name, url=url, icon=icon)
        db.session.add(link)
        db.session.commit()
        flash("Social link added.", "success")

    return redirect(url_for("main.edit_profile"))


@main.route("/admin/social/delete/<int:id>", methods=["POST"])
@login_required
def delete_social(id):
    link = SocialLink.query.get_or_404(id)
    db.session.delete(link)
    db.session.commit()
    flash("Social link removed.", "success")
    return redirect(url_for("main.edit_profile"))


# ──────────────────────── Admin: Projects ──────────────────────────

@main.route("/admin/add-project", methods=["GET", "POST"])
@login_required
def add_project():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        github = request.form.get("github", "").strip()
        demo = request.form.get("demo", "").strip()

        image_filename = None
        image_file = request.files.get("image")
        if image_file and image_file.filename and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_file.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], "project_images", image_filename)
            )

        project = Project(
            title=title, description=description,
            github=github, demo=demo, image=image_filename,
        )
        db.session.add(project)
        db.session.commit()
        log_admin_action("add_project", f"Added: {title}")
        flash("Project added successfully!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("add_project.html")


@main.route("/admin/import-github", methods=["GET", "POST"])
@login_required
def import_github():
    """Import projects from GitHub."""
    import requests

    github_repos = []
    username = request.form.get("github_username", "").strip()

    if request.method == "POST":
        if not username:
            flash("Please enter a GitHub username.", "danger")
        else:
            try:
                # Fetch repos from GitHub API (public, rate limited to 60 req/hr)
                resp = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", timeout=5)
                if resp.status_code == 200:
                    all_repos = resp.json()
                    if isinstance(all_repos, list):
                        # Get list of repo names already in portfolio
                        existing_titles = {p.title for p in Project.query.all()}

                        # Filter and prepare repos
                        for repo in all_repos:
                            if not repo.get("fork") and repo["name"] not in existing_titles:
                                github_repos.append({
                                    "name": repo["name"],
                                    "description": repo.get("description") or "No description",
                                    "url": repo.get("html_url"),
                                    "language": repo.get("language") or "Unknown"
                                })
                    else:
                        flash(f"GitHub user '{username}' not found.", "danger")
                else:
                    flash(f"GitHub API error: {resp.status_code}", "danger")
            except requests.RequestException as e:
                flash(f"Failed to fetch repositories: {str(e)}", "danger")

    return render_template("import_github.html", github_repos=github_repos, username=username)


@main.route("/admin/import-github-save", methods=["POST"])
@login_required
def import_github_save():
    """Save selected GitHub repos as projects."""
    import requests

    selected = request.form.getlist("selected_repos")
    username = request.form.get("github_username", "").strip()
    count = 0

    if username and selected:
        try:
            resp = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100", timeout=5)
            if resp.status_code == 200:
                repos_by_name = {r["name"]: r for r in resp.json() if isinstance(resp.json(), list)}

                for repo_name in selected:
                    if repo_name in repos_by_name:
                        repo = repos_by_name[repo_name]
                        project = Project(
                            title=repo["name"],
                            description=repo.get("description") or repo["name"],
                            github=repo.get("html_url"),
                            demo=None
                        )
                        db.session.add(project)
                        count += 1

                if count > 0:
                    db.session.commit()
                    log_admin_action("import_github", f"Imported {count} repos from {username}")
                    flash(f"Successfully imported {count} project(s) from GitHub!", "success")
        except Exception as e:
            flash(f"Error importing repositories: {str(e)}", "danger")

    return redirect(url_for("main.dashboard"))


@main.route("/admin/edit-project/<int:id>", methods=["GET", "POST"])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)

    if request.method == "POST":
        project.title = request.form.get("title", "").strip()
        project.description = request.form.get("description", "").strip()
        project.github = request.form.get("github", "").strip()
        project.demo = request.form.get("demo", "").strip()

        image_file = request.files.get("image")
        if image_file and image_file.filename and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_file.save(
                os.path.join(current_app.config["UPLOAD_FOLDER"], "project_images", image_filename)
            )
            project.image = image_filename

        db.session.commit()
        log_admin_action("edit_project", f"Edited: {project.title}")
        flash("Project updated successfully!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("edit_project.html", project=project)


@main.route("/admin/delete-project/<int:id>", methods=["POST"])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    log_admin_action("delete_project", f"Deleted: {project.title}")
    db.session.delete(project)
    db.session.commit()
    flash("Project deleted.", "success")
    return redirect(url_for("main.dashboard"))


# ──────────────────────── Admin: Skills ────────────────────────────

@main.route("/admin/skills")
@login_required
def manage_skills():
    skills = Skill.query.all()
    return render_template("manage_skills.html", skills=skills)


@main.route("/admin/skills/add", methods=["POST"])
@login_required
def add_skill():
    skill_name = request.form.get("name", "").strip()
    if skill_name:
        skill = Skill(name=skill_name)
        db.session.add(skill)
        db.session.commit()
        flash("Skill added.", "success")
    return redirect(url_for("main.manage_skills"))


@main.route("/admin/skills/delete/<int:id>", methods=["POST"])
@login_required
def delete_skill(id):
    skill = Skill.query.get_or_404(id)
    db.session.delete(skill)
    db.session.commit()
    flash("Skill deleted.", "success")
    return redirect(url_for("main.manage_skills"))


# ──────────────────────── Admin: Experience ────────────────────────

@main.route("/admin/experience")
@login_required
def manage_experience():
    experiences = Experience.query.order_by(Experience.id.desc()).all()
    return render_template("admin_experience.html", experiences=experiences)


@main.route("/admin/experience/add", methods=["GET", "POST"])
@login_required
def add_experience():
    if request.method == "POST":
        exp = Experience(
            role=request.form.get("role", "").strip(),
            company=request.form.get("company", "").strip(),
            company_url=request.form.get("company_url", "").strip(),
            location=request.form.get("location", "").strip(),
            start_date=request.form.get("start_date", "").strip(),
            end_date=request.form.get("end_date", "").strip(),
            description=request.form.get("description", "").strip(),
        )
        db.session.add(exp)
        db.session.commit()
        log_admin_action("add_experience", f"Added: {exp.role} at {exp.company}")
        flash("Experience added!", "success")
        return redirect(url_for("main.manage_experience"))

    return render_template("add_experience.html")


@main.route("/admin/experience/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit_experience(id):
    exp = Experience.query.get_or_404(id)

    if request.method == "POST":
        exp.role = request.form.get("role", "").strip()
        exp.company = request.form.get("company", "").strip()
        exp.company_url = request.form.get("company_url", "").strip()
        exp.location = request.form.get("location", "").strip()
        exp.start_date = request.form.get("start_date", "").strip()
        exp.end_date = request.form.get("end_date", "").strip()
        exp.description = request.form.get("description", "").strip()

        db.session.commit()
        flash("Experience updated!", "success")
        return redirect(url_for("main.manage_experience"))

    return render_template("edit_experience.html", exp=exp)


@main.route("/admin/experience/delete/<int:id>", methods=["POST"])
@login_required
def delete_experience(id):
    exp = Experience.query.get_or_404(id)
    db.session.delete(exp)
    db.session.commit()
    flash("Experience deleted.", "success")
    return redirect(url_for("main.manage_experience"))


# ──────────────────────── Admin: Resume ────────────────────────────

@main.route("/admin/upload-resume", methods=["GET", "POST"])
@login_required
def upload_resume():
    if request.method == "POST":
        file = request.files.get("resume")
        if file and file.filename and allowed_file(file.filename):
            upload_path = os.path.join(
                current_app.config["UPLOAD_FOLDER"], "resumes", "resume.pdf"
            )
            file.save(upload_path)
            log_admin_action("upload_resume")
            flash("Resume uploaded successfully!", "success")
            return redirect(url_for("main.dashboard"))
        else:
            flash("Please upload a valid PDF file.", "danger")

    return render_template("upload_resume.html")


@main.route("/admin/view-resume")
@login_required
def view_resume():
    return send_from_directory(
        os.path.join(current_app.config["UPLOAD_FOLDER"], "resumes"),
        "resume.pdf",
    )


# ──────────────────────── Admin: Messages ──────────────────────────

@main.route("/admin/messages")
@login_required
def admin_messages():
    messages = Message.query.order_by(Message.id.desc()).all()
    return render_template("admin_messages.html", messages=messages)


@main.route("/admin/messages/delete/<int:id>", methods=["POST"])
@login_required
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted.", "success")
    return redirect(url_for("main.admin_messages"))


# ──────────────────────── Admin: Analytics ─────────────────────────

@main.route("/admin/analytics")
@login_required
def admin_analytics():
    total_views = PageView.query.count()
    unique_visitors = db.session.query(
        func.count(func.distinct(PageView.ip_address))
    ).scalar() or 0

    country_stats = (
        db.session.query(PageView.country, func.count(PageView.id))
        .group_by(PageView.country)
        .order_by(func.count(PageView.id).desc())
        .limit(10)
        .all()
    )

    page_stats = (
        db.session.query(PageView.page, func.count(PageView.id))
        .group_by(PageView.page)
        .order_by(func.count(PageView.id).desc())
        .limit(10)
        .all()
    )

    resume_downloads = ResumeDownload.query.count()

    return render_template(
        "admin_analytics.html",
        total_views=total_views,
        unique_visitors=unique_visitors,
        country_stats=country_stats,
        page_stats=page_stats,
        resume_downloads=resume_downloads,
    )


# ──────────────────────── Admin: Coding Profiles ──────────────────

@main.route("/admin/coding-profiles")
@login_required
def manage_coding_profiles():
    profiles = CodingProfile.query.all()
    return render_template("admin_coding_profiles.html", profiles=profiles)


@main.route("/admin/coding-profiles/add", methods=["POST"])
@login_required
def add_coding_profile():
    cp = CodingProfile(
        platform=request.form.get("platform", "").strip(),
        username=request.form.get("username", "").strip(),
        profile_url=request.form.get("profile_url", "").strip(),
        problems_solved=_safe_int(request.form.get("problems_solved", 0)),
        rating=request.form.get("rating", "").strip(),
        rank=request.form.get("rank", "").strip(),
        badge=request.form.get("badge", "").strip(),
        icon_class=request.form.get("icon_class", "").strip(),
    )
    db.session.add(cp)
    db.session.commit()
    log_admin_action("add_coding_profile", f"Added: {cp.platform}")
    flash("Coding profile added!", "success")
    return redirect(url_for("main.manage_coding_profiles"))


@main.route("/admin/coding-profiles/delete/<int:id>", methods=["POST"])
@login_required
def delete_coding_profile(id):
    cp = CodingProfile.query.get_or_404(id)
    log_admin_action("delete_coding_profile", f"Deleted: {cp.platform}")
    db.session.delete(cp)
    db.session.commit()
    flash("Coding profile deleted.", "success")
    return redirect(url_for("main.manage_coding_profiles"))


# ──────────────────────── Admin: Security (2FA) ───────────────────

@main.route("/admin/security")
@login_required
def admin_security():
    return render_template("admin_security.html")


@main.route("/admin/security/enable-2fa", methods=["POST"])
@login_required
def enable_2fa():
    import pyotp
    import qrcode
    import io
    import base64

    admin = db.session.get(Admin,current_user.id)
    if not admin.totp_secret:
        admin.totp_secret = pyotp.random_base32()
        db.session.commit()

    totp_uri = admin.get_totp_uri()

    # Generate QR code as base64 image
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    qr_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")

    return render_template(
        "admin_security.html",
        qr_code=qr_base64,
        totp_secret=admin.totp_secret,
        setup_mode=True,
    )


@main.route("/admin/security/confirm-2fa", methods=["POST"])
@login_required
def confirm_2fa():
    token = request.form.get("token", "").strip()
    admin = db.session.get(Admin,current_user.id)

    if admin.verify_totp(token):
        admin.is_2fa_enabled = True
        db.session.commit()
        log_admin_action("enable_2fa")
        flash("Two-factor authentication enabled!", "success")
    else:
        flash("Invalid code. Please try again.", "danger")

    return redirect(url_for("main.admin_security"))


@main.route("/admin/security/disable-2fa", methods=["POST"])
@login_required
def disable_2fa():
    admin = db.session.get(Admin,current_user.id)
    admin.is_2fa_enabled = False
    admin.totp_secret = None
    db.session.commit()
    log_admin_action("disable_2fa")
    flash("Two-factor authentication disabled.", "info")
    return redirect(url_for("main.admin_security"))


# ──────────────────────── Admin: Activity Log ─────────────────────

@main.route("/admin/activity-log")
@login_required
def admin_activity_log():
    logs = AdminLog.query.order_by(AdminLog.id.desc()).limit(100).all()
    return render_template("admin_activity_log.html", logs=logs)
