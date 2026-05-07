# 🤍 A Love That Refused to End
### Ritika & Kuldip's Love Dashboard

A beautiful, romantic Streamlit web app showcasing your love story — soft & moody aesthetic, masonry photo gallery, timeline of milestones, and a live days-together counter.

---

## 🚀 How to Deploy (Step by Step)

### Step 1 — Set up your GitHub repo
1. Go to [github.com](https://github.com) → Sign in (or create a free account)
2. Click **"New repository"** → Name it `our-love-story` → Make it **Private** (recommended) or Public
3. Click **"Create repository"**

### Step 2 — Upload your files
In your new repo, upload these files:
```
our-love-story/
├── app.py                ← the main app (provided)
├── requirements.txt      ← dependencies (provided)
└── images/               ← YOUR PHOTOS FOLDER
    ├── photo1.jpg
    ├── photo2.jpg
    ├── photo3.jpg
    ├── photo4.jpg
    ├── photo5.jpg
    ├── photo6.jpg
    └── photo7.jpg
```

### Step 3 — Name your photos correctly
Rename your photos **exactly** like this before uploading:
| File name | Which photo |
|-----------|-------------|
| `photo1.jpg` | First date / outdoor bike ride selfie |
| `photo2.jpg` | Sunday morning "Sunday" text photo |
| `photo3.jpg` | Face mask butterfly photo 🦋 |
| `photo4.jpg` | Cozy indoor warm selfie (portrait) |
| `photo5.jpg` | Indoor sideways selfie |
| `photo6.jpg` | Any other favourite |
| `photo7.jpg` | Any other favourite |

You can add more photos in `app.py` in the `gallery_photos` list!

### Step 4 — Deploy on Streamlit Cloud (FREE)
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select your repo `our-love-story`, branch `main`, file `app.py`
5. Click **"Deploy!"**
6. In ~2 minutes you'll get a live link like: `https://your-name-our-love-story.streamlit.app`

**Share that link with Kuldip 🤍**

---

## 🎨 Customizing

### Add more photos
In `app.py`, find the `gallery_photos` list and add more entries:
```python
gallery_photos = [
    ("photo1.jpg", "Your caption here"),
    ("photo8.jpg", "Pavagadh trip 🏔️"),
    ("photo9.jpg", "Statue of Unity visit"),
    # add as many as you want!
]
```

### Change the closing quote
Find `closing-quote` in the HTML and update the text to your own words.

---

## 💻 Run Locally (optional)
```bash
pip install -r requirements.txt
streamlit run app.py
```

---

*Made with 🤍 for Ritika & Kuldip*
