# Zelly Website - Server Deployment Guide

## 📋 Prerequisites

- Ubuntu 20.04+ or similar Linux server
- Python 3.10+
- Domain name pointed to your server
- SSH access to your server

---

## 🚀 Deployment Steps

### 1. Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Install PostgreSQL (recommended for production)
sudo apt install postgresql postgresql-contrib -y
```

### 2. Create Database (PostgreSQL)

```bash
sudo -u postgres psql

# In PostgreSQL shell:
CREATE DATABASE zelly_db;
CREATE USER zelly_user WITH PASSWORD 'your_secure_password';
ALTER ROLE zelly_user SET client_encoding TO 'utf8';
ALTER ROLE zelly_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE zelly_user SET timezone TO 'Asia/Tashkent';
GRANT ALL PRIVILEGES ON DATABASE zelly_db TO zelly_user;
\q
```

### 3. Upload Project to Server

```bash
# On your local machine, create a zip of the project
# Or use git to clone the repository

# On server:
cd /var/www/
sudo mkdir zelly
sudo chown $USER:$USER zelly
cd zelly

# Upload your project files here
```

### 4. Setup Python Environment

```bash
cd /var/www/zelly

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install psycopg2-binary  # For PostgreSQL
```

### 5. Configure Environment Variables

```bash
# Create .env file
nano .env

# Add these variables:
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=postgresql://zelly_user:your_secure_password@localhost:5432/zelly_db
STATIC_ROOT=/var/www/zelly/staticfiles/
MEDIA_ROOT=/var/www/zelly/media/
```

### 6. Update Settings for Production

```bash
# Edit zelly_project/settings.py to use production settings
nano zelly_project/settings.py

# Add at the top:
import os
from dotenv import load_dotenv
load_dotenv()

# Or use settings_production.py:
# Rename settings.py to settings_dev.py
# Rename settings_production.py to settings.py
```

### 7. Run Migrations and Collect Static Files

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Set permissions
sudo chown -R www-data:www-data /var/www/zelly/
sudo chmod -R 755 /var/www/zelly/
```

### 8. Configure Gunicorn

```bash
# Create gunicorn service file
sudo nano /etc/systemd/system/zelly.service
```

Add this content:

```ini
[Unit]
Description=Zelly Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/zelly
Environment="PATH=/var/www/zelly/venv/bin"
ExecStart=/var/www/zelly/venv/bin/gunicorn --workers 3 --bind unix:/var/www/zelly/zelly.sock zelly_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable the service
sudo systemctl start zelly
sudo systemctl enable zelly
sudo systemctl status zelly
```

### 9. Configure Nginx

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/zelly
```

Add this content:

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 10M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/zelly/staticfiles/;
    }

    location /media/ {
        alias /var/www/zelly/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/zelly/zelly.sock;
    }
}
```

```bash
# Enable the site
sudo ln -s /etc/nginx/sites-available/zelly /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 10. Setup SSL with Let's Encrypt (Optional but Recommended)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal is configured automatically
```

---

## 🔄 Updating the Application

```bash
# SSH to server
cd /var/www/zelly
source venv/bin/activate

# Pull latest changes (if using git)
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart zelly
sudo systemctl restart nginx
```

---

## 🛠️ Troubleshooting

### Check Gunicorn logs:
```bash
sudo journalctl -u zelly -f
```

### Check Nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Restart services:
```bash
sudo systemctl restart zelly
sudo systemctl restart nginx
```

### Check service status:
```bash
sudo systemctl status zelly
sudo systemctl status nginx
```

---

## 📝 Important Notes

1. **Security**: 
   - Change SECRET_KEY in production
   - Set DEBUG=False
   - Use strong database passwords
   - Keep dependencies updated

2. **Backups**:
   - Regularly backup your database
   - Backup media files
   - Keep a copy of .env file securely

3. **Monitoring**:
   - Set up monitoring for your application
   - Monitor disk space and server resources
   - Set up email notifications for errors

4. **Performance**:
   - Consider using Redis for caching
   - Optimize database queries
   - Use CDN for static files if needed

---

## 🌐 Access Points After Deployment

- **Main Website**: `https://your-domain.com`
- **Admin Panel**: `https://your-domain.com/admin-panel/`
- **Django Admin**: `https://your-domain.com/django-admin/`

---

## 📞 Support

For issues or questions, refer to:
- Django Documentation: https://docs.djangoproject.com/
- Nginx Documentation: https://nginx.org/en/docs/
- Gunicorn Documentation: https://docs.gunicorn.org/
