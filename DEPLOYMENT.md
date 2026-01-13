# Deployment Guide (100% Free - No Credit Card)

We will use **Neon.tech** for the Free Database (better than Render's temporary one) and **Render** for the hosting, doing it manually to avoid the payment screen.

## Step 1: Get a Free Database (Neon.tech)

1.  Go to [Neon.tech](https://neon.tech/) and Sign Up (Free).
2.  Create a new **Project**.
3.  You will be shown a **Connection String**. It looks like this:
    `postgres://user:password@ep-something.aws.neon.tech/neondb?sslmode=require`
4.  **Copy this string**. You will need it in Step 3.

## Step 2: Push Code to GitHub

(If you haven't already)
1.  Commit and push your latest changes:
    ```bash
    git add .
    git commit -m "Ready for deployment"
    git push origin main
    ```

## Step 3: Deploy to Render (Manual Method)

1.  Go to [Render Dashboard](https://dashboard.render.com/).
2.  Click **New +** -> **Web Service**.
3.  Select **Build and deploy from a Git repository**.
4.  Connect your `BlockChain-Based-Voting-System` repository.
5.  Scroll down to configure:
    -   **Name**: `secure-vote` (or anything you like)
    -   **Region**: Closest to you (e.g., Singapore or Oregon)
    -   **Branch**: `main`
    -   **Runtime**: `Python 3`
    -   **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
    -   **Start Command**: `gunicorn secure_vote.wsgi:application`  <-- **IMPORTANT: COPY THIS EXACTLY**
6.  **Instance Type**: Select **Free**.
7.  **Environment Variables** (Click "Add Environment Variable"):
    -   Key: `DATABASE_URL`
    -   Value: *(Paste the Neon Connection String)*
    -   Key: `PYTHON_VERSION`
    -   Value: `3.10.11`
    -   Key: `RENDER`
    -   Value: `true`
8.  Click **Create Web Service**.

## Step 4: Create Superuser (Admin)

Once the deployment finishes (Step 3 is green/Live):
1.  In the Render Dashboard for your service, click the **Shell** tab (on the left).
2.  Wait for the terminal to connect.
3.  Type:
    ```bash
    python manage.py createsuperuser
    ```
4.  Follow the prompts to create your admin account.

## Troubleshooting

-   **Build Fail:** Check the "Logs" tab. If it says "Module not found", make sure `requirements.txt` is updated.
-   **Database Error:** Ensure you copied the full connection string from Neon, including `sslmode=require`.
