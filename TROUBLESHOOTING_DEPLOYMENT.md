# 🆘 DEPLOYMENT TROUBLESHOOTING GUIDE

If you are seeing **"You do not have access to this app"** or **"App not found"** when trying to deploy to Streamlit Cloud, follow these steps to fix it.

## 1. The "Repo Privacy" Fix (Most Common)
Streamlit Cloud sometimes fails to see **Private** repositories if permissions aren't perfect.
*   **Fix:** Go to your GitHub Repository settings and change visibility to **Public**.
    *   *Settings -> Danger Zone -> Change repository visibility -> Make public.*
*   **Retry:** Go back to Streamlit Cloud and try to deploy again.

## 2. The "Push First" Rule
You cannot deploy if the code is only on your computer.
*   **Check:** Did you commit and push your latest code to GitHub?
*   **Fix:** Run these commands in your terminal:
    ```bash
    git add .
    git commit -m "Ready for deploy"
    git push origin main
    ```

## 3. Manual Deployment (Bypass the Button)
If clicking "Deploy" inside the app fails, do it manually:
1.  Go to **[share.streamlit.io](https://share.streamlit.io)**.
2.  Click **"New App"**.
3.  **Repository:** Select your `DecoherenceLog` repo.
4.  **Branch:** `main` (or `master`).
5.  **Main file path:** `app.py`
6.  Click **Deploy!**

## 4. The "Email Mismatch"
*   Ensure you are logging into Streamlit Cloud with the **SAME email/GitHub account** that owns the repository.
*   If you have multiple GitHub accounts, log out of everything and log back in with the correct one.

## 5. Requirements Check
Streamlit needs to know what libraries to install. We have a `requirements.txt` file, which is good.
*   **Verify:** Ensure `requirements.txt` exists in your GitHub repo.

---
**Still stuck?**
You can always run the app **LOCALLY** on your computer without internet limits:
1.  Open Terminal.
2.  Run: `streamlit run app.py`
3.  View at: `http://localhost:8501`
