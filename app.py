"""
app.py
Flask application for Abanum Emmanuel Ovie's portfolio site.

Run locally:
    pip install -r requirements.txt
    python app.py
Then open http://127.0.0.1:5000
"""

import os
import re
import sqlite3
from datetime import datetime, timezone

import requests
from flask import Flask, render_template, request, redirect, url_for, flash

from data import PROFILE, SKILLS_SCHEMA, PROJECTS, NAV_LINKS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "contact.db")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# --- Email notification settings (Resend HTTPS API) ------------------------
# Render's free tier blocks outbound SMTP (ports 25/465/587), so sending mail
# via smtplib to smtp.gmail.com doesn't work there. Resend sends over plain
# HTTPS instead, which isn't blocked, and the message still lands in your
# normal Gmail inbox — only the delivery transport changes.
# RESEND_API_KEY: API key from resend.com.
# NOTIFY_EMAIL: where messages should land. Defaults to the portfolio's own email.
RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
NOTIFY_EMAIL = os.environ.get("NOTIFY_EMAIL", PROFILE["email"])


def send_notification_email(name: str, sender_email: str, message: str):
    """Emails the contact-form submission to NOTIFY_EMAIL via the Resend API.
    Returns (success: bool, error: str | None). Never raises."""
    if not RESEND_API_KEY:
        return False, "Email not configured (RESEND_API_KEY not set)"

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}"},
            json={
                "from": "Portfolio Contact Form <onboarding@resend.dev>",
                "to": [NOTIFY_EMAIL],
                "reply_to": sender_email,
                "subject": f"Portfolio contact form: {name}",
                "text": f"From: {name} <{sender_email}>\n\n{message}",
            },
            timeout=10,
        )
        if response.status_code >= 400:
            return False, f"Resend API error {response.status_code}: {response.text}"
        return True, None
    except Exception as exc:  # noqa: BLE001 - we log and degrade gracefully
        return False, str(exc)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


@app.route("/")
def index():
    return render_template(
        "index.html",
        profile=PROFILE,
        skills=SKILLS_SCHEMA,
        projects=PROJECTS,
        nav_links=NAV_LINKS,
        year=datetime.now(timezone.utc).year,
    )


@app.route("/contact", methods=["POST"])
def contact():
    name = (request.form.get("name") or "").strip()
    email = (request.form.get("email") or "").strip()
    message = (request.form.get("message") or "").strip()

    errors = []
    if not name:
        errors.append("Please enter your name.")
    if not email or not EMAIL_RE.match(email):
        errors.append("Please enter a valid email address.")
    if not message:
        errors.append("Please enter a message.")

    if errors:
        for e in errors:
            flash(e, "error")
        return redirect(url_for("index") + "#contact")

    with get_db() as conn:
        conn.execute(
            "INSERT INTO messages (name, email, message, created_at) VALUES (?, ?, ?, ?)",
            (name, email, message, datetime.now(timezone.utc).isoformat()),
        )

    sent, error = send_notification_email(name, email, message)
    if not sent:
        # Message is still saved locally as a backup; log the delivery
        # failure server-side so it shows up in Render's logs without
        # exposing SMTP details to the visitor.
        app.logger.error("Contact form email notification failed: %s", error)

    flash("Message received — thanks, I'll get back to you shortly.", "success")
    return redirect(url_for("index") + "#contact")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
else:
    # Ensure the DB exists even when run via a WSGI server (e.g. gunicorn).
    init_db()
