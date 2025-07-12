# Quick Setup: Neon PostgreSQL Database

## Step 1: Create Neon Account

1. Go to https://neon.tech/
2. Click "Sign Up"
3. Use your GitHub account for quick signup

## Step 2: Create Database

1. Click "Create a project"
2. Choose region (closest to you)
3. Give it a name: "privatehostelscet"
4. Click "Create project"

## Step 3: Get Connection String

1. In your Neon dashboard, click "Connection details"
2. Copy the connection string that looks like:
   ```
   postgresql://username:password@hostname/dbname?sslmode=require
   ```

## Step 4: Update Your Django App

1. Open your `.env` file
2. Replace the commented DATABASE_URL with your Neon URL:
   ```
   DATABASE_URL=your-neon-connection-string-here
   ```

## Step 5: Test Connection

```bash
python test_supabase.py
```

## Step 6: Run Migrations

```bash
python manage.py migrate
```

## Example Neon Connection String:

```
DATABASE_URL=postgresql://user123:abc123@ep-cool-cloud-123456.us-east-2.aws.neon.tech/neondb?sslmode=require
```

## Why Neon?

- ✅ Free tier is generous (512 MB)
- ✅ Fast and reliable
- ✅ Serverless PostgreSQL
- ✅ Auto-scaling
- ✅ Built-in connection pooling
