# Render Deployment Guide (SQLite)

This guide explains how to deploy your Django project on Render using Docker with SQLite.

## Overview

The deployment uses:

- **Dockerfile.render**: A simplified Dockerfile that uses SQLite instead of PostgreSQL
- **render.yaml**: Render configuration file (optional, can also configure via dashboard)
- Your local **db.sqlite3** database is included in the Docker image

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. Push your code to GitHub/GitLab
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Blueprint"
4. Connect your repository
5. Render will automatically detect `render.yaml` and configure the service

### Option 2: Manual Configuration

1. Push your code to GitHub/GitLab
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New +" → "Web Service"
4. Connect your repository
5. Configure:

   - **Name**: bintel-erp-backend (or your choice)
   - **Environment**: Docker
   - **Dockerfile Path**: `./Dockerfile.render`
   - **Instance Type**: Free (or your choice)

6. Add Environment Variables:

   - `JWT_SECRET`: bintel
   - `SECRET_KEY`: django-insecure-change-me-in-production
   - `DEBUG`: True
   - `DJANGO_SETTINGS_MODULE`: backend.settings_sqlite

7. Click "Create Web Service"

## Important Notes

⚠️ **Data Persistence**:

- Data will be LOST when the container restarts/redeploys
- This is expected for testing purposes
- The container starts with your local SQLite data each time

⚠️ **Security**:

- Change `SECRET_KEY` and `JWT_SECRET` for production
- Set `DEBUG=False` for production

## Testing Locally

Test the Docker image locally before deploying:

```bash
# Build the image
docker build -f Dockerfile.render -t bintel-render-test .

# Run the container
docker run -p 5100:5100 bintel-render-test

# Access at http://localhost:5100
```

## Updating Data

To update the SQLite database in the deployment:

1. Update your local `db.sqlite3` file
2. Commit and push changes
3. Render will automatically rebuild and redeploy

## API Documentation

Once deployed, access the API documentation at:

- Swagger UI: `https://your-app.onrender.com/api/schema/swagger-ui/`
- ReDoc: `https://your-app.onrender.com/api/schema/redoc/`
