import threading
import requests as http_requests
from flask import request, current_app
from .models import PageView, ResumeDownload
from .extensions import db

# Simple in-memory cache for IP->country lookups
_country_cache = {}


def get_country_from_ip(ip_address):
    """Use ip-api.com (free, no key needed) to resolve country from IP."""
    if ip_address in ("127.0.0.1", "::1", "localhost", None, "Unknown"):
        return "Local"

    if ip_address in _country_cache:
        return _country_cache[ip_address]

    try:
        resp = http_requests.get(
            f"http://ip-api.com/json/{ip_address}",
            params={"fields": "country"},
            timeout=1,
        )
        if resp.status_code == 200:
            country = resp.json().get("country", "Unknown")
            _country_cache[ip_address] = country
            return country
    except Exception:
        pass
    return "Unknown"


def _do_track_page_view(app, page, ip, user_agent):
    """Background worker for tracking page views."""
    with app.app_context():
        try:
            country = get_country_from_ip(ip)
            pv = PageView(
                page=page,
                ip_address=ip,
                country=country,
                user_agent=user_agent[:500],
            )
            db.session.add(pv)
            db.session.commit()
        except Exception as e:
            # Log but don't crash - analytics is non-critical
            app.logger.debug(f"Failed to track page view: {e}")


def track_page_view(page):
    """Record a page view in the database (non-blocking)."""
    ip = request.remote_addr or "Unknown"
    user_agent = str(request.user_agent) if request.user_agent else ""
    app = current_app._get_current_object()

    t = threading.Thread(target=_do_track_page_view, args=(app, page, ip, user_agent))
    t.daemon = True
    t.start()


def _do_track_resume_download(app, ip):
    """Background worker for tracking resume downloads."""
    with app.app_context():
        try:
            country = get_country_from_ip(ip)
            rd = ResumeDownload(ip_address=ip, country=country)
            db.session.add(rd)
            db.session.commit()
        except Exception as e:
            # Log but don't crash - analytics is non-critical
            app.logger.debug(f"Failed to track resume download: {e}")


def track_resume_download():
    """Record a resume download (non-blocking)."""
    ip = request.remote_addr or "Unknown"
    app = current_app._get_current_object()

    t = threading.Thread(target=_do_track_resume_download, args=(app, ip))
    t.daemon = True
    t.start()
