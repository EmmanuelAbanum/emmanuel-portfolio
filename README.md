# Abanum Emmanuel Ovie — Portfolio

A personal portfolio site built with **Flask, Bootstrap, HTML, and CSS**,
presenting my skills and projects as a "technical dossier" —
a schema table for skills, structured records for projects, and a
working contact form backed by SQLite.

## Run it locally

```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

The first run automatically creates `contact.db` (SQLite) to store
messages sent through the contact form — no separate database setup
needed to try it locally.

## Project structure

```
portfolio/
├── app.py                 # Flask routes: home page + contact form handling
├── data.py                # All site content (bio, skills, projects) — edit here
├── requirements.txt
├── templates/
│   ├── base.html           # Shared HTML shell, fonts, Bootstrap
│   └── index.html          # The page itself
└── static/
    ├── css/style.css        # All visual design
    └── js/script.js         # Hero "typing" animation
```


## Switching from SQLite to MySQL

The contact form uses SQLite by default so the project runs anywhere
with zero setup. To use MySQL instead (matching the rest of your
stack):

1. `pip install mysql-connector-python` (or `PyMySQL`)
2. In `app.py`, replace the `get_db()` / `init_db()` functions with
   MySQL connection logic, e.g.:

```python
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="portfolio",
    )
```

3. Create the `messages` table in MySQL using the same columns shown
   in `init_db()`.

## Getting contact form messages by email

The contact form emails you the moment someone submits it. It also
still saves a backup copy locally, but email is the reliable channel —
treat the local database as a fallback only (see the Render notes
below on why).

**Important:** this uses [Resend](https://resend.com), an email API
over HTTPS — not Gmail's SMTP servers directly. That's a deliberate
choice: Render's free tier blocks outbound SMTP traffic (the protocol
Gmail's mail servers use) to prevent spam abuse, so a direct
Gmail-SMTP approach will silently fail there with a
`Network is unreachable` error. Resend sends over plain HTTPS instead,
which isn't blocked — and the message still lands in your normal
Gmail inbox exactly the same way, since you'll set your Gmail address
as the recipient.

### 1. Create a free Resend account

Go to [resend.com](https://resend.com) and sign up using
**emmanuelovieabanum@gmail.com** — using this exact address matters
for the next step.

### 2. Create an API key

In the Resend dashboard, go to **API Keys → Create API Key**. Give it
a name like `portfolio-site`, and copy the key (it starts with `re_`
and is only shown once).

### 3. Set environment variables

```bash
export RESEND_API_KEY="re_your_key_here"
export NOTIFY_EMAIL="emmanuelovieabanum@gmail.com"   # optional, defaults to this anyway
```

On Render, add these under your service's **Environment** tab instead.

**Note on the free tier:** without verifying your own domain with
Resend, you can only send emails *to* the address you signed up with —
which is exactly what this app does, so no domain verification is
needed. If you ever want to send *from* a custom address (e.g.
`hello@yourdomain.com`) instead of Resend's shared `onboarding@resend.dev`
address, that's when domain verification becomes necessary — not
required for this use case.

**Never commit your API key to GitHub.** Treat it like a password. If
it's ever exposed, delete it from the Resend dashboard and create a
new one.

If `RESEND_API_KEY` isn't set, the form still works and still saves
messages locally — it just won't email you, and will log a warning on
the server instead.

## Deploying

This is a standard Flask app, so it deploys to any Python host
(Render, Railway, PythonAnywhere, a VPS with gunicorn, etc.). For
production:

- Set a real `SECRET_KEY` environment variable.
- Run with a production server, e.g.:
  ```bash
  pip install gunicorn
  gunicorn app:app
  ```
- Turn off debug mode (already off by default outside `python app.py`).

### Deploying to Render (free, no credit card required)

1. Push this project to a GitHub repository.
2. On [render.com](https://render.com), click **New > Web Service** and
   connect that repo.
3. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
4. Add an environment variable `SECRET_KEY` with a random value.
5. Click **Deploy**. Render gives you a live `https://your-app.onrender.com`
   URL once the build finishes.

Note: on Render's free tier, the app "sleeps" after 15 minutes of no
traffic and takes ~30–60 seconds to wake up on the next visit — normal
for a free tier, not a bug. Also note that free-tier disks are
ephemeral: the SQLite `contact.db` file resets not just on redeploy,
but every time the app spins down from inactivity and restarts —
which happens often. That's exactly why the contact form emails you
directly (see the section above) instead of relying on that file as
the only record of a message.

## Customizing the design

All visual identity lives in `static/css/style.css`, driven by CSS
variables at the top of the file (`:root { ... }`) — colors, fonts,
and spacing can be changed in one place without touching the rest of
the file.
