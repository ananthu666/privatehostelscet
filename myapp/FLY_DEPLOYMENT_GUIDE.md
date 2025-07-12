# Fly.io Deployment Guide

## Prerequisites

1. Install Fly CLI: https://fly.io/docs/hands-on/install-flyctl/
2. Sign up for Fly.io account

## Deployment Steps

### 1. Login to Fly.io

```bash
fly auth login
```

### 2. Initialize your app

```bash
cd c:\Users\sreel\OneDrive\Desktop\hostel_app\privatehostelscet\myapp
fly launch --no-deploy
```

### 3. Set up PostgreSQL database

```bash
fly postgres create --name privatehostelscet-db
fly postgres attach --app privatehostelscet privatehostelscet-db
```

### 4. Set environment variables

```bash
fly secrets set SECRET_KEY="your-secret-key-here"
fly secrets set DEBUG="False"
fly secrets set DJANGO_SETTINGS_MODULE="myapp.settings"
```

### 5. Deploy your app

```bash
fly deploy
```

### 6. Open your app

```bash
fly open
```

## Important Notes

- Your app will be available at: https://privatehostelscet.fly.dev
- Free tier includes: 3 shared CPUs, 256MB RAM
- Database will be automatically configured
- SSL is enabled by default

## Troubleshooting

- Check logs: `fly logs`
- SSH into machine: `fly ssh console`
- Check status: `fly status`
