# Deployment Guide

This guide explains how to deploy your NFL Analysis Dashboard to the web.

## Option 1: Streamlit Community Cloud (Recommended - FREE)

Streamlit Community Cloud is the easiest way to deploy your app for free.

### Steps:

1. **Push code to GitHub**
   ```bash
   cd /Users/csanders/Documents/llm/nflanalysis
   git init
   git add .
   git commit -m "Initial NFL analysis dashboard"
   # Create a new GitHub repository, then:
   git remote add origin https://github.com/YOUR_USERNAME/nfl-analysis.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   `https://YOUR_USERNAME-nfl-analysis.streamlit.app`

### Advantages:
- ✅ Completely FREE
- ✅ No server management
- ✅ Automatic updates from GitHub
- ✅ Built-in SSL/HTTPS
- ✅ Custom domain support

---

## Option 2: Heroku (Good for custom domains)

### Steps:

1. **Install Heroku CLI**
   ```bash
   brew tap heroku/brew && brew install heroku
   ```

2. **Create required files**

   Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

   Create `Procfile`:
   ```
   web: sh setup.sh && streamlit run app.py
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-nfl-analysis
   git push heroku main
   ```

### Cost:
- Free tier available (with some limitations)
- ~$7/month for hobby tier

---

## Option 3: AWS/Google Cloud/DigitalOcean (For full control)

### Using Docker:

1. **Create Dockerfile**
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8501

   CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **Build and run**
   ```bash
   docker build -t nfl-analysis .
   docker run -p 8501:8501 nfl-analysis
   ```

3. **Deploy to cloud**
   - AWS ECS: Deploy container to Elastic Container Service
   - Google Cloud Run: `gcloud run deploy`
   - DigitalOcean App Platform: Connect GitHub repo

---

## Option 4: Local Network (For testing)

Run locally and share on your network:

```bash
source venv/bin/activate
streamlit run app.py --server.address=0.0.0.0
```

Access from other devices on your network at: `http://YOUR_IP:8501`

---

## Custom Domain Setup

### For Streamlit Cloud:
1. Go to app settings
2. Add custom domain
3. Update your DNS:
   - CNAME: `your-app.streamlit.app`

### For Heroku:
```bash
heroku domains:add www.yourdomain.com
# Follow DNS instructions
```

---

## Environment Variables

If you need API keys or secrets:

**Streamlit Cloud:**
- Go to app settings → Secrets
- Add in TOML format

**Heroku:**
```bash
heroku config:set SECRET_KEY=your_secret
```

---

## Performance Optimization

1. **Enable caching** (already implemented with `@st.cache_data`)

2. **Limit data size**
   - Only load necessary seasons
   - Pre-aggregate data when possible

3. **Use CDN for static assets**
   - Host images on CDN
   - Minimize data loading

---

## Monitoring & Analytics

### Add Google Analytics:
```python
# In app.py, add to header:
st.markdown("""
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YOUR-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YOUR-ID');
</script>
""", unsafe_allow_html=True)
```

---

## Recommended Deployment: Streamlit Cloud

**Best for your use case because:**
1. ✅ Free tier is generous
2. ✅ Zero DevOps required
3. ✅ Automatic deploys from GitHub
4. ✅ Built for data science apps
5. ✅ Great performance
6. ✅ Custom domains supported

**Steps to go live:**
1. Push to GitHub (5 minutes)
2. Connect to Streamlit Cloud (2 minutes)
3. Share your link!

Your app will be live at a public URL you can share with anyone!
