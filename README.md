# Zelly Website

Modern POS system website for cafes and restaurants.

## 🚀 Quick Start (Development)

### Prerequisites
- Python 3.10+
- pip

### Installation

1. Clone the repository or extract the project files

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the application:
   - Website: `http://127.0.0.1:8000/`
   - Admin Panel: `http://127.0.0.1:8000/admin-panel/`
   - Django Admin: `http://127.0.0.1:8000/django-admin/`

## 📦 Project Structure

```
Zelly-Website/
├── zelly_project/          # Django project settings
│   ├── settings.py         # Development settings
│   ├── settings_production.py  # Production settings
│   ├── urls.py
│   └── wsgi.py
├── website/                # Main application
│   ├── models.py          # Database models
│   ├── views.py           # Public views
│   ├── admin_views.py     # Admin panel views
│   └── urls.py
├── templates/             # HTML templates
│   ├── index.html        # Main website
│   └── admin/            # Admin panel templates
├── static/               # Static files (CSS, JS, images)
│   ├── styles.css
│   ├── script.js
│   └── admin/           # Admin panel assets
├── media/               # User uploaded files
├── requirements.txt     # Python dependencies
├── DEPLOYMENT.md       # Deployment guide
└── README.md          # This file
```

## 🎨 Features

### Public Website
- Modern, responsive design
- Dynamic content from database
- Partner showcase
- Customer testimonials
- Pricing plans
- Contact form

### Admin Panel
- Custom premium admin interface
- Dashboard with statistics
- CRUD operations for:
  - Partners (with logo upload)
  - Testimonials (with ratings)
  - Pricing Plans (with features)
  - Contact Requests
- Secure authentication
- Mobile responsive

## 🛠️ Technologies

- **Backend**: Django 6.0
- **Database**: SQLite (development), PostgreSQL (production recommended)
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn, Nginx, WhiteNoise

## 📚 Documentation

- [Deployment Guide](DEPLOYMENT.md) - Complete guide for deploying to production server

## 🔐 Security

- Staff-only access to admin panel
- CSRF protection
- Secure password hashing
- Production security settings included

## 📝 License

Proprietary - All rights reserved

## 👨‍💻 Development

### Adding New Features

1. Create/modify models in `website/models.py`
2. Run migrations: `python manage.py makemigrations && python manage.py migrate`
3. Update views in `website/views.py` or `website/admin_views.py`
4. Create/update templates in `templates/`
5. Add static files to `static/`

### Database Models

- **Partner**: Company partners with logos
- **Testimonial**: Customer reviews with ratings
- **PricingPlan**: Pricing tiers with features
- **ContactRequest**: Lead capture from forms

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Quick deployment checklist:
- [ ] Update SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup production database
- [ ] Run collectstatic
- [ ] Configure Gunicorn
- [ ] Setup Nginx
- [ ] Enable SSL with Let's Encrypt
