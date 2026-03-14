# Portfolio Flask

A modern, professional developer portfolio web application built with Flask.

## Features

### Public Portfolio
- **Hero Section** - Profile image, name, title, typing tagline animation, social links, resume download
- **About Section** - Bio, email, phone, location
- **Experience Timeline** - Animated timeline with company links
- **Skills Section** - Animated skill badges with scroll-triggered effects
- **Coding Profiles** - LeetCode, HackerRank, Codeforces, GeeksForGeeks stats cards
- **Projects Grid** - Card layout with images, GitHub & demo links, hover animations
- **Contact Form** - CSRF-protected with email notifications
- **AI Chatbot** - OpenAI-powered chat widget that answers questions about you
- **Dark Mode** - Toggle with system preference detection and localStorage persistence
- **SEO Optimized** - Meta tags, OpenGraph, Twitter Cards, JSON-LD structured data, sitemap, robots.txt
- **Modern Animations** - AOS scroll animations, parallax hero, page loader, typing effect

### Admin Dashboard
- **Full CMS** - Manage all portfolio content from one place
- **Profile Management** - Edit name, title, bio, profile image, social links
- **Projects CRUD** - Add/edit/delete projects with image uploads
- **Skills Management** - Add/remove skills displayed as badges
- **Experience CRUD** - Manage work experience entries
- **Coding Profiles** - Manage coding platform stats (LeetCode, HackerRank, etc.)
- **Contact Messages** - View and manage visitor messages
- **Resume Upload** - Upload PDF resume for visitor download
- **Analytics Dashboard** - Page views, unique visitors, country breakdown, resume downloads
- **Activity Log** - Track all admin actions with timestamps and IPs

### Security
- **2FA Authentication** - TOTP-based (Google Authenticator) with QR code setup
- **Login Rate Limiting** - 5 attempts per minute
- **JWT API Authentication** - Token-based auth for REST API
- **CSRF Protection** - All forms protected with Flask-WTF
- **Password Hashing** - Werkzeug secure password hashing
- **Admin Activity Logging** - Track login, content changes, and security events

### REST API
- `GET /api/profile` - Get profile data
- `GET /api/projects` - List all projects
- `GET /api/skills` - List all skills
- `GET /api/experience` - List all experience
- `POST /api/auth/login` - Get JWT token
- `POST /api/chat` - AI chatbot endpoint

## Tech Stack

- **Backend:** Flask, Flask-Login, Flask-SQLAlchemy, Flask-Migrate, Flask-WTF, Flask-Mail, Flask-JWT-Extended, Flask-Limiter, Flask-CORS
- **Frontend:** Bootstrap 5.3, Bootstrap Icons, AOS (Animate On Scroll), Jinja2
- **Database:** MySQL (via PyMySQL)
- **AI:** OpenAI GPT-3.5 Turbo
- **Security:** pyotp (2FA), qrcode (QR generation)
- **Testing:** pytest, pytest-flask
- **Deployment:** Gunicorn, Docker, GitHub Actions CI/CD

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd portfolio-flask
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
MYSQL_USER=root
MYSQL_PASSWORD=your-password
MYSQL_HOST=localhost
MYSQL_DB=portfolio_db
MYSQL_PORT=3306

# Email notifications
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
ADMIN_EMAIL=your-email@gmail.com

# AI Chatbot (optional)
OPENAI_API_KEY=your-openai-api-key

# JWT Secret
JWT_SECRET_KEY=your-jwt-secret

# Site URL (for SEO)
SITE_URL=https://yourdomain.com
```

### 5. Initialize the database

```bash
flask db init        # Only if migrations/ doesn't exist
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Create admin user

```bash
python -c "
from run import app
from app.extensions import db
from app.models import Admin
with app.app_context():
    admin = Admin(username='admin')
    admin.set_password('your-password')
    db.session.add(admin)
    db.session.commit()
    print('Admin user created!')
"
```

### 7. Run the application

```bash
python run.py
```

Visit `http://localhost:5000` for the portfolio and `http://localhost:5000/admin/login` for the admin panel.

## Docker

### Quick Start

```bash
docker-compose up --build
```

### Production Build

```bash
docker build -t portfolio-flask .
docker run -p 5000:5000 --env-file .env portfolio-flask
```

## Testing

```bash
pytest tests/ -v
```

## Custom Domain Setup

### Render

1. Go to your Render dashboard > your service > Settings
2. Under "Custom Domains", click "Add Custom Domain"
3. Enter your domain (e.g., `rahuldadge.dev`)
4. Add the CNAME record shown by Render to your DNS provider
5. Wait for DNS propagation and SSL certificate provisioning (automatic via Let's Encrypt)

### Railway

1. Go to your Railway project > Settings > Domains
2. Click "Add Domain" and enter your custom domain
3. Copy the CNAME target provided by Railway
4. Add a CNAME record in your DNS provider pointing to Railway's target
5. SSL is automatically provisioned

### DNS Configuration

- **Subdomain** (e.g., portfolio.yourdomain.com): Add a CNAME record pointing to your hosting provider's URL
- **Root domain** (e.g., yourdomain.com): Some providers require an A record or ALIAS record instead of CNAME

### Environment Variable

Set `SITE_URL` to your custom domain for correct SEO canonical URLs:

```
SITE_URL=https://rahuldadge.dev
```

## Deployment

### Render / Railway

1. Push your code to GitHub
2. Connect your repository to Render or Railway
3. Set environment variables in the platform dashboard
4. The `Procfile` and `runtime.txt` are already configured

### PythonAnywhere

1. Upload your code or clone from GitHub
2. Set up a MySQL database
3. Configure the WSGI file to point to `run:app`
4. Set environment variables in the `.env` file

## Project Structure

```
portfolio-flask/
├── app/
│   ├── __init__.py              # Application factory
│   ├── extensions.py            # Flask extensions (db, jwt, limiter, cors, etc.)
│   ├── models.py                # 11 database models
│   ├── analytics.py             # Page view & download tracking
│   ├── forms.py                 # WTForms definitions
│   ├── routes/
│   │   ├── __init__.py          # Blueprint exports
│   │   ├── main.py              # Main blueprint (30+ routes)
│   │   └── api.py               # REST API blueprint
│   ├── templates/
│   │   ├── base.html            # Base template with SEO, dark mode, chat
│   │   ├── index.html           # Public portfolio page
│   │   ├── dashboard.html       # Admin dashboard
│   │   ├── admin_analytics.html # Analytics dashboard
│   │   ├── admin_security.html  # 2FA settings
│   │   ├── admin_coding_profiles.html
│   │   ├── admin_activity_log.html
│   │   ├── verify_2fa.html
│   │   ├── partials/
│   │   │   └── admin_navbar.html
│   │   └── ... (13+ templates)
│   └── static/
│       ├── css/style.css        # Custom styles + dark mode
│       ├── js/main.js           # Dark mode, animations, chat widget
│       └── uploads/
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   ├── test_routes.py           # Route tests
│   ├── test_api.py              # API tests
│   └── test_models.py           # Model tests
├── .github/workflows/ci.yml    # CI/CD pipeline
├── Dockerfile
├── docker-compose.yml
├── config.py
├── run.py
├── requirements.txt
├── Procfile
├── runtime.txt
└── .gitignore
```

## License

This project is open source and available under the [MIT License](LICENSE).
