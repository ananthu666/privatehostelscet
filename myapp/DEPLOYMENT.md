# Hostel Management System - Deployment Guide

## Database Setup (Supabase PostgreSQL)

Your project is now configured to use PostgreSQL via Supabase.

Database URL: `postgresql://postgres:cetuioin2023@db.wfqwcucmoskkfssrtojc.supabase.co:5432/postgres`

## Environment Variables

Create a `.env` file with the following variables:

```
DATABASE_URL=postgresql://postgres:cetuioin2023@db.wfqwcucmoskkfssrtojc.supabase.co:5432/postgres
DEBUG=False
SECRET_KEY=your-secret-key-here
```

## Deployment Steps

### Option 1: Railway (Recommended)

1. Go to [railway.app](https://railway.app) and sign up
2. Click "Deploy from GitHub repo"
3. Connect your GitHub account and select this repository
4. Railway will automatically detect Django and deploy
5. Add environment variables in Railway dashboard:
   - `DATABASE_URL`: postgresql://postgres:cetuioin2023@db.wfqwcucmoskkfssrtojc.supabase.co:5432/postgres
   - `DEBUG`: False
   - `SECRET_KEY`: Generate a new secret key

### Option 2: Render

1. Go to [render.com](https://render.com) and sign up
2. Click "New Web Service"
3. Connect your GitHub repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python manage.py migrate && python manage.py collectstatic --noinput && gunicorn myapp.wsgi`
6. Add environment variables in Render dashboard

### Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add environment variables:
   ```
   heroku config:set DATABASE_URL=postgresql://postgres:cetuioin2023@db.wfqwcucmoskkfssrtojc.supabase.co:5432/postgres
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   ```
5. Deploy: `git push heroku main`

## Pre-Deployment Checklist

- ✅ PostgreSQL database configured
- ✅ Environment variables set
- ✅ Static files configuration ready
- ✅ Requirements.txt updated
- ✅ Procfile created
- ✅ Runtime.txt specified
- ✅ Security settings configured

## First-Time Setup Commands

After deployment, run these commands in your hosting platform's console:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser  # Optional: create admin user
```

## Features Included

- ✅ Complete hostel management system
- ✅ Standardized UI/UX with consistent buttons and styling
- ✅ Edit Vacancy functionality with negative value support
- ✅ Responsive design with Bootstrap 5
- ✅ Admin panel for hostel approvals
- ✅ Grievance management system
- ✅ Room booking system

## Project Structure

- **Home**: Landing page with navigation
- **Hostel Registration**: Add new hostels (admin approval required)
- **Edit Vacancy**: Manage room availability with advanced validation
- **Room Booking**: Student room request system
- **Grievance**: Complaint submission and tracking
- **Administration**: Admin panel for hostel management

Your project is production-ready! 🚀
