# Vercel & Render CORS Fix Guide

This guide provides the necessary steps to ensure your Vercel frontend can communicate securely with your Render backend.

## 1. Backend Configuration (Render)

Ensure your `veteranmeet/settings.py` includes the following:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://*.vercel.app",  # Supports all Vercel deployments including previews
]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    "http://localhost:3000",
    "https://*.vercel.app",
]
```

## 2. Frontend Configuration (Vercel)

1.  **Environment Variables**:
    In your Vercel Project Settings, add:
    *   **Key**: `NEXT_PUBLIC_API_URL` (if using Next.js) or `VITE_API_URL` (if using Vite)
    *   **Value**: `https://veteranmeet-1.onrender.com`

2.  **Axios/Fetch Setup**:
    Always ensure `withCredentials: true` is set in your API calls:

    ```javascript
    import axios from 'axios';

    const api = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL,
      withCredentials: true,
    });
    ```

## 3. Verification

After deploying both:
1.  Visit your Vercel deployment URL.
2.  Open the browser console (F12) to check for any CORS errors.
3.  Test the login flow to ensure cookies are being set and sent.
