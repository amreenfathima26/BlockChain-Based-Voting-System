# Deployment Guide

This guide will help you deploy your Django application to Render with a free PostgreSQL database.

## Prerequisites

1.  **GitHub Account**: You need a GitHub account to host your code.
2.  **Render Account**: You need a Render.com account to host the application and database.

## Step 1: Push to GitHub

1.  Initialize a Git repository (if you haven't already):
    ```bash
    git init
    ```
2.  Add files to staging:
    ```bash
    git add .
    ```
3.  Commit your changes:
    ```bash
    git commit -m "Prepare for deployment"
    ```
4.  Create a new repository on GitHub (do not initialize with README/gitignore, just empty).
5.  Link your local repository to GitHub:
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
    git branch -M main
    git push -u origin main
    ```

## Step 2: Deploy to Render (The Easy Way with Blueprints)

Since we created a `render.yaml` file, you can use Render Blueprints for automatic setup.

1.  Go to your [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** and select **Blueprint**.
3.  Connect your GitHub account and select your repository.
4.  Render will automatically detect the `render.yaml` file and show you the resources it will create:
    -   **Service**: `secure-vote` (Web Service)
    -   **Database**: `secure-vote-db` (PostgreSQL)
5.  Click **Apply**.
6.  Render will start building and deploying your application. It will also create the database and automatically link it to your app.

## Step 3: Verify Deployment

1.  Wait for the build to finish. It might take a few minutes.
2.  Once deployed, you will see a URL (e.g., `https://secure-vote.onrender.com`).
3.  Click the URL to access your live application.

## Troubleshooting

-   **Database Connection**: The application is configured to automatically use the Render database when deployed. If you have issues, check the `Environment` tab in Render to ensure `DATABASE_URL` is set.
-   **Static Files**: We configured `Whitenoise` to serve static files. If styles are missing, check the build logs for `python manage.py collectstatic` errors.
-   **Admin User**: You will need to create a superuser on the production database. You can do this via the Render Shell:
    1.  Go to your Web Service in Render.
    2.  Click **Shell**.
    3.  Run: `python manage.py createsuperuser`
