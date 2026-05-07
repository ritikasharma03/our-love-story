import streamlit as st
from datetime import date
import base64
from pathlib import Path

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="A Love That Refused to End",
    page_icon="🤍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Helper: load image as base64 ───────────────────────────────────────────────
def img_to_b64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

# ── Days together counter ──────────────────────────────────────────────────────
first_date = date(2020, 1, 10)
days_together = (date.today() - first_date).days
years = days_together // 365
months = (days_together % 365) // 30

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=DM+Sans:wght@300;400&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0d0b0e !important;
    color: #e8ddd4 !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] > .main > div { padding: 0 !important; }
[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
section.main > div.block-container { padding: 0 !important; max-width: 100% !important; }
.stMarkdown { width: 100%; }

/* ── Grain overlay ── */
body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.04'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 9999;
    opacity: 0.35;
}

/* ── Hero ── */
.hero {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 60px 20px;
    overflow: hidden;
    background: radial-gradient(ellipse at 30% 20%, #3d1a2a 0%, transparent 55%),
                radial-gradient(ellipse at 70% 80%, #1a1a2e 0%, transparent 55%),
                #0d0b0e;
}

.hero::after {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, transparent 40%, #0d0b0e 100%);
    pointer-events: none;
}

.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-weight: 300;
    font-size: clamp(0.65rem, 1.5vw, 0.8rem);
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c9a882;
    margin-bottom: 28px;
    position: relative;
    z-index: 2;
    animation: fadeUp 1.2s ease both;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 7vw, 5.5rem);
    font-weight: 700;
    line-height: 1.1;
    color: #f5ede3;
    margin-bottom: 12px;
    position: relative;
    z-index: 2;
    animation: fadeUp 1.2s 0.15s ease both;
}

.hero-title em {
    font-style: italic;
    color: #e8c4a0;
}

.hero-sub {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1rem, 2.5vw, 1.35rem);
    font-style: italic;
    color: #a8967e;
    margin-bottom: 48px;
    position: relative;
    z-index: 2;
    animation: fadeUp 1.2s 0.3s ease both;
}

.hero-hashtag {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.2em;
    color: #6e5a4e;
    position: relative;
    z-index: 2;
    animation: fadeUp 1.2s 0.45s ease both;
}

.hero-photos {
    display: flex;
    gap: 16px;
    align-items: flex-end;
    justify-content: center;
    flex-wrap: wrap;
    margin: 48px 0 40px;
    position: relative;
    z-index: 2;
    animation: fadeUp 1.2s 0.6s ease both;
}

.hero-photo-wrap {
    position: relative;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0,0,0,0.6);
    transition: transform 0.4s ease;
}
.hero-photo-wrap:hover { transform: translateY(-8px) scale(1.02); }

.hero-photo-wrap:nth-child(1) { width: 180px; height: 260px; transform: rotate(-3deg); }
.hero-photo-wrap:nth-child(2) { width: 220px; height: 310px; }
.hero-photo-wrap:nth-child(3) { width: 175px; height: 250px; transform: rotate(2.5deg); }

.hero-photo-wrap img {
    width: 100%; height: 100%;
    object-fit: cover;
    object-position: top center;
    filter: sepia(15%) contrast(1.05) brightness(0.92);
}

.hero-photo-wrap::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(13,11,14,0.4) 0%, transparent 50%);
}

/* Stats ribbon */
.stats-ribbon {
    width: 100%;
    background: rgba(255,255,255,0.03);
    border-top: 1px solid rgba(201,168,130,0.15);
    border-bottom: 1px solid rgba(201,168,130,0.15);
    padding: 40px 20px;
    display: flex;
    justify-content: center;
    gap: clamp(24px, 6vw, 100px);
    flex-wrap: wrap;
}

.stat-item { text-align: center; }
.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2rem, 5vw, 3.5rem);
    font-weight: 600;
    color: #e8c4a0;
    line-height: 1;
}
.stat-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #6e5a4e;
    margin-top: 8px;
}

/* ── Section base ── */
.section {
    padding: clamp(60px, 10vw, 120px) clamp(20px, 8vw, 120px);
    max-width: 1300px;
    margin: 0 auto;
}

.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: #c9a882;
    margin-bottom: 18px;
}

.section-heading {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.8rem, 4vw, 3rem);
    font-weight: 600;
    color: #f5ede3;
    margin-bottom: 48px;
    line-height: 1.2;
}

/* ── Story section ── */
.story-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 64px;
    align-items: center;
}

@media (max-width: 768px) {
    .story-grid { grid-template-columns: 1fr; gap: 32px; }
    .hero-photo-wrap:nth-child(1), .hero-photo-wrap:nth-child(3) { transform: none !important; }
}

.story-text {
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.05rem, 1.8vw, 1.25rem);
    line-height: 1.9;
    color: #c5b5a5;
    font-weight: 300;
}

.story-img {
    border-radius: 4px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 30px 80px rgba(0,0,0,0.5);
}
.story-img img {
    width: 100%; display: block;
    filter: sepia(10%) contrast(1.05) brightness(0.9);
    transition: transform 0.6s ease;
}
.story-img:hover img { transform: scale(1.03); }

/* ── Timeline ── */
.timeline { position: relative; padding-left: 40px; }
.timeline::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 1px;
    background: linear-gradient(to bottom, transparent, #c9a882 20%, #c9a882 80%, transparent);
}

.timeline-item {
    position: relative;
    margin-bottom: 52px;
    animation: fadeUp 0.8s ease both;
}

.timeline-item::before {
    content: '';
    position: absolute;
    left: -44px; top: 6px;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #c9a882;
    box-shadow: 0 0 12px rgba(201,168,130,0.5);
}

.timeline-date {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #c9a882;
    margin-bottom: 8px;
}

.timeline-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #f5ede3;
    margin-bottom: 8px;
}

.timeline-desc {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    color: #9a8878;
    line-height: 1.7;
    font-style: italic;
}

/* ── Gallery ── */
.gallery-masonry {
    columns: 3;
    column-gap: 16px;
}

@media (max-width: 900px) { .gallery-masonry { columns: 2; } }
@media (max-width: 500px) { .gallery-masonry { columns: 1; } }

.gallery-item {
    break-inside: avoid;
    margin-bottom: 16px;
    position: relative;
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 8px 30px rgba(0,0,0,0.4);
}

.gallery-item img {
    width: 100%; display: block;
    filter: sepia(8%) contrast(1.04) brightness(0.88);
    transition: transform 0.5s ease, filter 0.5s ease;
}
.gallery-item:hover img {
    transform: scale(1.04);
    filter: sepia(0%) contrast(1.06) brightness(0.95);
}

.gallery-caption {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, rgba(13,11,14,0.85) 0%, transparent 100%);
    padding: 32px 16px 16px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.9rem;
    font-style: italic;
    color: #d4c4b4;
    transform: translateY(100%);
    transition: transform 0.4s ease;
}
.gallery-item:hover .gallery-caption { transform: translateY(0); }

/* ── Closing quote ── */
.closing {
    text-align: center;
    padding: clamp(80px, 15vw, 160px) 20px;
    background: radial-gradient(ellipse at center top, #2a0f1c 0%, transparent 60%), #0d0b0e;
    position: relative;
}

.closing-quote {
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.5rem, 4vw, 3rem);
    font-style: italic;
    font-weight: 400;
    color: #e8ddd4;
    max-width: 800px;
    margin: 0 auto 32px;
    line-height: 1.5;
}

.closing-names {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.8rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c9a882;
}

.divider {
    width: 60px; height: 1px;
    background: linear-gradient(to right, transparent, #c9a882, transparent);
    margin: 0 auto 48px;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}


.accident-section {{
    padding: clamp(60px, 10vw, 120px) clamp(20px, 8vw, 120px);
    background: radial-gradient(ellipse at 60% 50%, #2a0f1c 0%, transparent 65%), #0d0b0e;
    position: relative;
    overflow: hidden;
}}

.accident-section::before {{
    content: '"';
    position: absolute;
    top: 20px; left: clamp(20px, 6vw, 100px);
    font-family: 'Playfair Display', serif;
    font-size: 18rem;
    color: rgba(201,168,130,0.04);
    line-height: 1;
    pointer-events: none;
}}

.accident-inner {{
    max-width: 1300px;
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 64px;
    align-items: center;
}}

@media (max-width: 768px) {{
    .accident-inner {{ grid-template-columns: 1fr; gap: 32px; }}
}}

.accident-photos {{
    display: flex;
    gap: 12px;
    align-items: flex-end;
}}

.accident-photo {{
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 24px 60px rgba(0,0,0,0.6);
    flex: 1;
    transition: transform 0.4s ease;
}}
.accident-photo:first-child {{
    transform: rotate(-2deg);
    flex: 0.85;
}}
.accident-photo:last-child {{
    transform: rotate(1.5deg);
}}
.accident-photo:hover {{ transform: rotate(0) scale(1.02) !important; }}
.accident-photo img {{
    width: 100%; display: block;
    filter: sepia(20%) contrast(1.05) brightness(0.85);
}}

.accident-text {{ position: relative; z-index: 2; }}

.accident-eyebrow {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: #c9a882;
    margin-bottom: 18px;
}}

.accident-heading {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.8rem, 3.5vw, 2.8rem);
    font-style: italic;
    font-weight: 600;
    color: #f5ede3;
    line-height: 1.2;
    margin-bottom: 28px;
}}

.accident-body {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.05rem, 1.8vw, 1.2rem);
    line-height: 1.9;
    color: #c5b5a5;
    font-weight: 300;
    margin-bottom: 32px;
}}

.accident-pullquote {{
    border-left: 2px solid #c9a882;
    padding-left: 20px;
    font-family: 'Playfair Display', serif;
    font-size: clamp(1rem, 1.8vw, 1.2rem);
    font-style: italic;
    color: #e8c4a0;
    line-height: 1.6;
}}


.home-section {{
    padding: clamp(60px, 10vw, 120px) clamp(20px, 8vw, 120px);
    background:
        radial-gradient(ellipse at 80% 30%, #1a1a2e 0%, transparent 55%),
        radial-gradient(ellipse at 20% 70%, #1e0f1a 0%, transparent 50%),
        #0d0b0e;
}}
.home-inner {{ max-width: 1300px; margin: 0 auto; }}

.home-bento {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    grid-template-rows: 280px 280px;
    gap: 10px;
    margin-top: 48px;
}}
@media (max-width: 900px) {{
    .home-bento {{
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: auto;
    }}
    .home-bento-span2, .home-bento-tall {{ grid-column: span 1 !important; grid-row: span 1 !important; }}
}}

.home-bento-item {{
    border-radius: 6px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 8px 30px rgba(0,0,0,0.5);
    background: #131013;
}}
.home-bento-span2 {{ grid-column: span 2; }}
.home-bento-tall   {{ grid-row: span 2; }}

.home-bento-item img {{
    width: 100%; height: 100%; display: block;
    object-fit: cover;
    object-position: top center;
    filter: sepia(8%) contrast(1.04) brightness(0.88);
    transition: transform 0.5s ease, filter 0.4s ease;
}}
.home-bento-item:hover img {{
    transform: scale(1.05);
    filter: sepia(0%) contrast(1.06) brightness(0.96);
}}

.home-bento-label {{
    position: absolute; bottom: 0; left: 0; right: 0;
    padding: 28px 14px 12px;
    background: linear-gradient(to top, rgba(0,0,0,0.75), transparent);
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.88rem;
    font-style: italic;
    color: #d4c4b4;
    opacity: 0;
    transition: opacity 0.4s ease;
}}
.home-bento-item:hover .home-bento-label {{ opacity: 1; }}

.home-quote-strip {{
    margin-top: 56px;
    border: 1px solid rgba(201,168,130,0.15);
    border-radius: 4px;
    padding: 40px 48px;
    display: flex;
    align-items: center;
    gap: 40px;
    background: rgba(255,255,255,0.02);
    flex-wrap: wrap;
}}
.home-quote-icon {{
    font-family: 'Playfair Display', serif;
    font-size: 5rem;
    color: rgba(201,168,130,0.2);
    line-height: 1;
    flex-shrink: 0;
}}
.home-quote-text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1.1rem, 2vw, 1.4rem);
    font-style: italic;
    color: #c5b5a5;
    line-height: 1.8;
}}
.home-quote-text strong {{
    font-style: normal;
    font-weight: 600;
    color: #e8c4a0;
}}


.adventure-section {{
    padding: clamp(60px, 10vw, 120px) clamp(20px, 8vw, 120px);
    background:
        radial-gradient(ellipse at 30% 0%, #0f1e2a 0%, transparent 55%),
        radial-gradient(ellipse at 70% 100%, #1a0f1a 0%, transparent 50%),
        #0d0b0e;
}}
.adventure-inner {{ max-width: 1300px; margin: 0 auto; }}

/* Rose & Chai hero moment */
.rose-moment {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 48px;
    align-items: center;
    margin-bottom: 72px;
}}
@media(max-width:768px) {{ .rose-moment {{ grid-template-columns: 1fr; }} }}

.rose-photos {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}}
.rose-photo {{
    border-radius: 5px;
    overflow: hidden;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    position: relative;
}}
.rose-photo img {{
    width: 100%; display: block;
    object-fit: cover;
    height: 280px;
    filter: sepia(8%) contrast(1.04) brightness(0.88);
    transition: transform 0.5s ease;
}}
.rose-photo:hover img {{ transform: scale(1.04); }}
.rose-photo-tall img {{ height: 572px !important; }}

.rose-text {{ }}
.rose-eyebrow {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: #c9a882;
    margin-bottom: 18px;
}}
.rose-heading {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.6rem, 3vw, 2.5rem);
    font-weight: 600;
    color: #f5ede3;
    line-height: 1.2;
    margin-bottom: 24px;
}}
.rose-body {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1rem, 1.7vw, 1.18rem);
    line-height: 1.9;
    color: #a89888;
    font-style: italic;
    margin-bottom: 32px;
}}
.rose-detail {{
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 0;
    border-top: 1px solid rgba(201,168,130,0.1);
}}
.rose-detail-icon {{ font-size: 1.2rem; }}
.rose-detail-text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    color: #c5b5a5;
}}

/* Kayak gallery */
.kayak-heading {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.4rem, 2.5vw, 2rem);
    font-style: italic;
    color: #f5ede3;
    margin-bottom: 28px;
    text-align: center;
}}

.kayak-strip {{
    display: grid;
    grid-template-columns: 1.6fr 1fr 1fr;
    grid-template-rows: 260px 260px;
    gap: 10px;
}}
@media(max-width:768px) {{
    .kayak-strip {{ grid-template-columns: 1fr 1fr; grid-template-rows: auto; }}
    .kayak-big {{ grid-row: span 1 !important; grid-column: span 2 !important; }}
}}
.kayak-big {{ grid-row: span 2; }}

.kayak-photo {{
    border-radius: 5px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 8px 28px rgba(0,0,0,0.5);
}}
.kayak-photo img {{
    width: 100%; height: 100%;
    object-fit: cover;
    object-position: center top;
    filter: sepia(5%) contrast(1.05) brightness(0.87) saturate(1.1);
    transition: transform 0.5s ease, filter 0.4s ease;
}}
.kayak-photo:hover img {{
    transform: scale(1.04);
    filter: sepia(0%) contrast(1.07) brightness(0.95) saturate(1.15);
}}
.kayak-label {{
    position: absolute; bottom:0; left:0; right:0;
    background: linear-gradient(to top, rgba(0,0,0,0.7), transparent);
    padding: 22px 12px 10px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.85rem;
    font-style: italic;
    color: #d4c4b4;
    opacity: 0;
    transition: opacity 0.4s;
}}
.kayak-photo:hover .kayak-label {{ opacity: 1; }}


.dates-section {{
    padding: clamp(60px, 10vw, 120px) clamp(20px, 8vw, 120px);
    background:
        radial-gradient(ellipse at 20% 50%, #1a0f20 0%, transparent 55%),
        radial-gradient(ellipse at 80% 10%, #0f1520 0%, transparent 50%),
        #0d0b0e;
}}
.dates-inner {{ max-width: 1300px; margin: 0 auto; }}

/* Date cards grid */
.date-cards {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 56px;
}}
@media(max-width:900px) {{ .date-cards {{ grid-template-columns: 1fr 1fr; }} }}
@media(max-width:500px) {{ .date-cards {{ grid-template-columns: 1fr; }} }}

.date-card {{
    border-radius: 6px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
    background: #111;
    cursor: pointer;
}}
.date-card img {{
    width: 100%; display: block;
    height: 320px;
    object-fit: cover;
    object-position: top center;
    filter: sepia(8%) contrast(1.04) brightness(0.86);
    transition: transform 0.5s ease, filter 0.4s ease;
}}
.date-card:hover img {{
    transform: scale(1.05);
    filter: sepia(0%) contrast(1.07) brightness(0.95);
}}
.date-card-info {{
    position: absolute; bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, rgba(13,11,14,0.92) 0%, transparent 100%);
    padding: 40px 18px 18px;
    transform: translateY(100%);
    transition: transform 0.4s ease;
}}
.date-card:hover .date-card-info {{ transform: translateY(0); }}
.date-card-title {{
    font-family: 'Playfair Display', serif;
    font-size: 1rem;
    font-weight: 600;
    color: #f5ede3;
    margin-bottom: 4px;
}}
.date-card-sub {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.85rem;
    font-style: italic;
    color: #9a8878;
}}
.date-card-badge {{
    position: absolute;
    top: 14px; left: 14px;
    background: rgba(13,11,14,0.7);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(201,168,130,0.25);
    border-radius: 20px;
    padding: 4px 12px;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #c9a882;
}}

/* Pink outfit hero */
.pink-hero {{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 10px;
    margin-bottom: 16px;
    height: 480px;
}}
@media(max-width:768px) {{
    .pink-hero {{ grid-template-columns: 1fr 1fr; height: auto; }}
    .pink-center {{ display: none; }}
}}
.pink-photo {{
    border-radius: 5px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}}
.pink-photo img {{
    width:100%; height:100%;
    object-fit:cover;
    object-position: top center;
    filter: sepia(5%) contrast(1.05) brightness(0.88);
    transition: transform 0.5s ease;
}}
.pink-photo:hover img {{ transform: scale(1.04); }}

/* Food strip */
.food-strip {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 10px;
}}
@media(max-width:600px) {{ .food-strip {{ grid-template-columns: 1fr 1fr; }} }}
.food-photo {{
    border-radius: 5px;
    overflow: hidden;
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}}
.food-photo img {{
    width:100%; height: 180px;
    object-fit:cover;
    filter: sepia(5%) contrast(1.08) brightness(0.9) saturate(1.15);
    transition: transform 0.4s ease;
}}
.food-photo:hover img {{ transform: scale(1.06); }}

.dates-subheading {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.3rem, 2.2vw, 1.8rem);
    font-style: italic;
    color: #e8c4a0;
    margin: 48px 0 24px;
}}


.car-section {{
    padding: clamp(60px, 10vw, 120px) clamp(20px, 8vw, 120px);
    background:
        radial-gradient(ellipse at 50% 0%, #1a1220 0%, transparent 60%),
        #0d0b0e;
    overflow: hidden;
}}
.car-inner {{ max-width: 1300px; margin: 0 auto; }}

.car-hero-strip {{
    position: relative;
    border-radius: 6px;
    overflow: hidden;
    height: 420px;
    margin-bottom: 48px;
    box-shadow: 0 24px 60px rgba(0,0,0,0.6);
}}
.car-hero-strip img {{
    width: 100%; height: 100%;
    object-fit: cover;
    object-position: center 30%;
    filter: sepia(10%) contrast(1.05) brightness(0.82);
    transition: transform 0.6s ease;
}}
.car-hero-strip:hover img {{ transform: scale(1.03); }}
.car-hero-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(to right, rgba(13,11,14,0.75) 0%, transparent 50%, rgba(13,11,14,0.4) 100%);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 48px;
}}
.car-hero-quote {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.4rem, 3vw, 2.2rem);
    font-style: italic;
    color: #f5ede3;
    max-width: 500px;
    line-height: 1.4;
    margin-bottom: 12px;
}}
.car-hero-tag {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.68rem;
    letter-spacing: 0.35em;
    text-transform: uppercase;
    color: #c9a882;
}}
.car-hands-row {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 12px;
}}
.car-small-row {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 48px;
}}
@media(max-width:768px) {{
    .car-hands-row {{ grid-template-columns: 1fr 1fr; }}
    .car-small-row  {{ grid-template-columns: 1fr 1fr; }}
}}
.car-photo {{
    border-radius: 5px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 8px 28px rgba(0,0,0,0.5);
    background:#111;
}}
.car-photo img {{
    width:100%; display:block;
    object-fit:cover;
    filter: sepia(8%) contrast(1.04) brightness(0.87);
    transition: transform 0.5s ease, filter 0.4s ease;
}}
.car-photo:hover img {{
    transform: scale(1.05);
    filter: sepia(0%) contrast(1.06) brightness(0.95);
}}
.car-hands-row .car-photo img {{ height: 300px; }}
.car-small-row  .car-photo img {{ height: 220px; }}
.car-caption {{
    position: absolute; bottom:0; left:0; right:0;
    background: linear-gradient(to top, rgba(0,0,0,0.75), transparent);
    padding: 24px 12px 10px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.85rem;
    font-style: italic;
    color: #d4c4b4;
    opacity: 0;
    transition: opacity 0.4s;
}}
.car-photo:hover .car-caption {{ opacity: 1; }}
.car-text-row {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 40px;
    align-items: start;
}}
@media(max-width:768px) {{ .car-text-row {{ grid-template-columns: 1fr; }} }}
.car-paragraph {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1rem, 1.7vw, 1.18rem);
    line-height: 1.9;
    color: #a89888;
    font-style: italic;
    font-weight: 300;
}}
.car-fact {{
    border: 1px solid rgba(201,168,130,0.12);
    border-radius: 4px;
    padding: 28px 32px;
    background: rgba(255,255,255,0.02);
}}
.car-fact-label {{
    font-family: 'DM Sans', sans-serif;
    font-size: 0.65rem;
    letter-spacing: 0.4em;
    text-transform: uppercase;
    color: #c9a882;
    margin-bottom: 12px;
}}
.car-fact-items {{
    list-style: none;
    padding: 0; margin: 0;
}}
.car-fact-items li {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.05rem;
    color: #c5b5a5;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex;
    align-items: center;
    gap: 12px;
}}
.car-fact-items li:last-child {{ border-bottom: none; }}
.car-fact-items li span {{ color: #c9a882; font-size: 1rem; }}


.cafe-section {{
    padding: clamp(60px, 10vw, 120px) clamp(20px, 8vw, 120px);
    background:
        radial-gradient(ellipse at 20% 80%, #1a2a1a 0%, transparent 50%),
        radial-gradient(ellipse at 80% 20%, #2a1a0f 0%, transparent 50%),
        #0d0b0e;
    position: relative;
    overflow: hidden;
}}

.cafe-inner {{ max-width: 1300px; margin: 0 auto; }}

.cafe-header {{ margin-bottom: 56px; }}

.cafe-title-row {{
    display: flex;
    align-items: baseline;
    gap: 20px;
    flex-wrap: wrap;
    margin-bottom: 16px;
}}

.cafe-hindi {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.2rem, 5vw, 4rem);
    font-weight: 700;
    color: #f5ede3;
    line-height: 1;
}}

.cafe-sub-text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1rem, 1.8vw, 1.2rem);
    font-style: italic;
    color: #9a8878;
    line-height: 1.8;
    max-width: 560px;
    margin-bottom: 48px;
}}

.cafe-grid {{
    display: grid;
    grid-template-columns: 1.2fr 0.8fr 0.8fr;
    grid-template-rows: auto auto;
    gap: 12px;
}}

@media (max-width: 768px) {{
    .cafe-grid {{ grid-template-columns: 1fr 1fr; }}
    .cafe-big {{ grid-column: span 2 !important; }}
}}

.cafe-big {{ grid-row: span 2; }}

.cafe-photo {{
    border-radius: 4px;
    overflow: hidden;
    position: relative;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5);
}}

.cafe-photo img {{
    width: 100%; height: 100%; display: block;
    object-fit: cover;
    filter: sepia(12%) contrast(1.05) brightness(0.88) saturate(1.1);
    transition: transform 0.5s ease, filter 0.5s ease;
}}
.cafe-photo:hover img {{
    transform: scale(1.04);
    filter: sepia(0%) contrast(1.07) brightness(0.95) saturate(1.15);
}}

.cafe-big img {{ height: 480px; }}
.cafe-small img {{ height: 232px; }}

.cafe-caption {{
    position: absolute; bottom: 0; left: 0; right: 0;
    background: linear-gradient(to top, rgba(13,11,14,0.8) 0%, transparent 100%);
    padding: 28px 14px 14px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 0.88rem;
    font-style: italic;
    color: #d4c4b4;
    opacity: 0;
    transition: opacity 0.4s ease;
}}
.cafe-photo:hover .cafe-caption {{ opacity: 1; }}

.cafe-straw-row {{
    margin-top: 48px;
    display: flex;
    align-items: center;
    gap: 48px;
    flex-wrap: wrap;
}}

.cafe-straw-img {{
    flex: 0 0 280px;
    border-radius: 4px;
    overflow: hidden;
    box-shadow: 0 16px 50px rgba(0,0,0,0.5);
    transform: rotate(-1.5deg);
    transition: transform 0.4s ease;
}}
.cafe-straw-img:hover {{ transform: rotate(0) scale(1.02); }}
.cafe-straw-img img {{ width: 100%; display: block; filter: sepia(5%) brightness(0.9); }}

.cafe-straw-text {{
    flex: 1;
    min-width: 240px;
}}

.cafe-straw-heading {{
    font-family: 'Playfair Display', serif;
    font-size: clamp(1.4rem, 2.5vw, 2rem);
    font-style: italic;
    color: #f5ede3;
    margin-bottom: 16px;
    line-height: 1.3;
}}

.cafe-straw-body {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(1rem, 1.6vw, 1.15rem);
    color: #9a8878;
    line-height: 1.85;
    font-style: italic;
}}

</style>
""", unsafe_allow_html=True)


# ── Photo helper ───────────────────────────────────────────────────────────────
PHOTO_DIR = Path(__file__).parent / "images"

def photo_tag(filename: str, alt: str = "") -> str:
    path = PHOTO_DIR / filename
    b64 = img_to_b64(str(path))
    if b64:
        return f'<img src="data:image/jpeg;base64,{b64}" alt="{alt}">'
    return f'<div style="background:#1a1515;width:100%;height:200px;display:flex;align-items:center;justify-content:center;color:#4a3a34;font-size:0.8rem;">📷 {filename}</div>'


# ── HERO ───────────────────────────────────────────────────────────────────────
hero_photos = ["photo1.jpg", "photo2.jpg", "photo3.jpg"]
hero_html = '<div class="hero-photos">'
for p in hero_photos:
    hero_html += f'<div class="hero-photo-wrap">{photo_tag(p)}</div>'
hero_html += '</div>'

st.markdown(f"""
<div class="hero">
  <p class="hero-eyebrow">Since January 10, 2020 &nbsp;·&nbsp; Vadodara, India</p>
  <h1 class="hero-title">A Love That <em>Refused</em><br>to End</h1>
  <p class="hero-sub">Ritika & Kuldip — a story written in bike rides, sunrises, and unbreakable bonds</p>
  {hero_html}
  <p class="hero-hashtag">#RitikaAndKuldip &nbsp;·&nbsp; #ALoveThatRefusedToEnd</p>
</div>
""", unsafe_allow_html=True)


# ── STATS RIBBON ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stats-ribbon">
  <div class="stat-item">
    <div class="stat-number">{days_together:,}</div>
    <div class="stat-label">Days Together</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">{years}</div>
    <div class="stat-label">Years of Love</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">2</div>
    <div class="stat-label">Breakups Survived</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">∞</div>
    <div class="stat-label">Reasons to Stay</div>
  </div>
  <div class="stat-item">
    <div class="stat-number">1</div>
    <div class="stat-label">Person I'd Drive to Without Knowing the Route</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── OUR STORY ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="section">
  <p class="section-label">How it began</p>
  <h2 class="section-heading">Our Story</h2>
  <div class="story-grid">
    <div class="story-text">
      We started our journey together in 2020. Our first date was on 10 January — a simple yet special bike ride along the highway. 
      We stopped for a while, talked endlessly, and clicked a few photos. That quiet moment became the beginning of everything.<br><br>
      As time passed, we kept meeting and slowly built a world of our own. One of our favourite places became a cozy spot called <em>Cafe Local</em>, 
      where we spent countless moments together. And then Sundays turned into something magical — sitting together and watching the sunrise from the balcony. 
      Those mornings felt peaceful and beautiful in a way that's hard to describe.<br><br>
      He even showed me his new house while it was being built, letting me be a part of his dreams.
    </div>
    <div class="story-img">{photo_tag("photo4.jpg", "Ritika and Kuldip")}</div>
  </div>
  <br><br>
  <div class="story-grid" style="margin-top:0;">
    <div class="story-img">{photo_tag("photo5.jpg", "A quiet Sunday")}</div>
    <div class="story-text">
      Our relationship grew stronger with time. Even though we went through two breakups, they only made our bond deeper, stronger, and truly unbreakable.<br><br>
      There was also a moment that made me realise how much he means to me. Once, Kuldip had an accident. 
      I didn't even properly know the route, but I still drove all the way to see him. I was extremely worried and just wanted to be there for him. 
      That day showed me that no matter what, I would always find my way to him.<br><br>
      Over the years we created so many memories — celebrating birthdays, exploring different cafes, visiting Pavagadh, going bowling, and seeing the Statue of Unity. 
      In 2025, he shared our relationship with his family. From a simple bike ride to a lifetime of memories — our journey has been filled with love, growth, and countless beautiful moments.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── TIMELINE ──────────────────────────────────────────────────────────────────
timeline_events = [
    ("January 10, 2020", "The First Ride", "A bike ride along the highway. We stopped, talked endlessly, clicked a few photos. That quiet evening became the beginning of everything."),
    ("Early 2020", "Cafe Local & His Home", "Our favourite cafe became our favourite place. Then I visited his home for the first time — and Sundays became sacred."),
    ("Sunday Mornings", "Sunrise Rituals", "Sitting on his balcony, watching the sunrise together. Warm chai, soft light, and no need for words. Pure magic."),
    ("Anytime", "His New House", "He showed me the house while it was still being built. He let me into his future, brick by brick."),
    ("The Day of the Accident", "I Found My Way to You", "I didn't know the route. I went anyway. Because when it's him, I'll always find a way."),
    ("The Years Between", "Adventures Together", "Pavagadh. Bowling. Statue of Unity. Birthday celebrations. Cafes we loved and roads we discovered."),
    ("2025", "Made Official", "He told his family about us. The love that refused to hide — finally stepping into the light."),
]

tl_html = '<div class="timeline">'
for date_str, title, desc in timeline_events:
    tl_html += f"""
    <div class="timeline-item">
      <div class="timeline-date">{date_str}</div>
      <div class="timeline-title">{title}</div>
      <div class="timeline-desc">{desc}</div>
    </div>"""
tl_html += '</div>'

st.markdown(f"""
<div class="section" style="padding-top:0;">
  <p class="section-label">Our Journey</p>
  <h2 class="section-heading">Milestones</h2>
  {tl_html}
</div>
""", unsafe_allow_html=True)


# ── GALLERY ───────────────────────────────────────────────────────────────────
gallery_photos = [
    ("photo1.jpg",              "Where it all began · Jan 10, 2020 🌿"),
    ("date2_pink_laugh.jpg",    "That laugh — always 🌸"),
    ("date2_mosaic_wall1.jpg",  "The pink day at the palace 🏛️"),
    ("date2_palace.jpg",        "Standing in front of history together"),
    ("date2_pink_hug.jpg",      "Matched in pink 🩷"),
    ("home_laugh.jpg",          "Pure joy at home"),
    ("date2_cinema_together.jpg","Cinema date 🎬"),
    ("date_vday_hats.jpg",      "Hat shopping on Valentine's Day 🤠"),
    ("date_kavish_mirror1.jpg", "Kavish Cafe pool mirror ☀️"),
    ("date2_koa_mirror.jpg",    "KOA cafe mirror selfie"),
    ("kotna_wide_selfie.jpg",   "Kotna beach — blue vests 🌊"),
    ("kotna_rose_smile.jpg",    "She gave him the rose 🌹"),
    ("car_hands1.jpg",          "Her ring, his watch 🤍"),
    ("car_bw_hearts.jpg",       "Hearts in black & white 🩶"),
    ("home_mirror1.jpg",        "The new house mirror 🪞"),
    ("home_facemask2.jpg",      "Haldi mask duo 💛"),
    ("cafe_us3.jpg",            "Café Local fairy lights ✨"),
    ("cafe_straw.jpg",          "The heart straw 🤍"),
    ("date2_pottery_done.jpg",  "Hearts they painted 🎨"),
    ("photo2.jpg",              "Sunday mornings 🌅"),
]

gallery_html = '<div class="gallery-masonry">'
for filename, caption in gallery_photos:
    gallery_html += f"""
    <div class="gallery-item">
      {photo_tag(filename)}
      <div class="gallery-caption">{caption}</div>
    </div>"""
gallery_html += '</div>'

st.markdown(f"""
<div class="section" style="padding-top:0;">
  <p class="section-label">Five years & counting</p>
  <h2 class="section-heading">Our Gallery</h2>
  {gallery_html}
</div>
""", unsafe_allow_html=True)


# ── THE DAY I FOUND MY WAY ────────────────────────────────────────────────────
st.markdown(f"""
<div class="accident-section">
  <div class="accident-inner">
    <div class="accident-photos">
      <div class="accident-photo">{photo_tag("accident1.jpg", "The day of the accident")}</div>
      <div class="accident-photo">{photo_tag("accident2.jpg", "I found my way to you")}</div>
    </div>
    <div class="accident-text">
      <p class="accident-eyebrow">The moment that said everything</p>
      <h2 class="accident-heading">The Day I Found<br>My Way to You</h2>
      <p class="accident-body">
        When Kuldip had his accident, I didn't even properly know the route.<br><br>
        But none of that mattered. I got on the road and I drove — not knowing every turn, 
        not knowing every street — just knowing that I needed to be there. 
        That I would always find a way to him, no matter what.<br><br>
        When I arrived and saw him — bandaged, tired, but smiling — I understood something 
        I hadn't put into words before. This is what love actually is. Not the easy days. 
        The days you show up anyway.
      </p>
      <div class="accident-pullquote">
        "I didn't know the route.<br>
        I went anyway.<br>
        Because when it's him — I'll always find a way."
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── HIS HOME, OUR WORLD ───────────────────────────────────────────────────────
st.markdown(f"""
<div class="home-section">
  <div class="home-inner">
    <p class="section-label">Where we are most ourselves</p>
    <h2 class="section-heading">His Home,<br>Our World</h2>

    <div class="home-bento">

      <div class="home-bento-item home-bento-tall">
        {photo_tag("home_mirror1.jpg")}
        <div class="home-bento-label">The new house mirror — where this chapter began 🤍</div>
      </div>

      <div class="home-bento-item home-bento-span2">
        {photo_tag("home_laugh.jpg")}
        <div class="home-bento-label">This laugh says everything about us</div>
      </div>

      <div class="home-bento-item">
        {photo_tag("home_mirror2.jpg")}
        <div class="home-bento-label">He's giving bunny ears 😂</div>
      </div>

      <div class="home-bento-item">
        {photo_tag("home_sunny.jpg")}
        <div class="home-bento-label">A quiet Sunday morning 🌤️</div>
      </div>

      <div class="home-bento-item">
        {photo_tag("home_facemask2.jpg")}
        <div class="home-bento-label">Haldi face mask duo 💛</div>
      </div>

      <div class="home-bento-item">
        {photo_tag("home_mirror3.jpg")}
        <div class="home-bento-label">Colour-coordinated and happy 💜</div>
      </div>

      <div class="home-bento-item">
        {photo_tag("home_kuldip_smile.jpg")}
        <div class="home-bento-label">Caught him smiling 🥹</div>
      </div>

    </div>

    <div class="home-quote-strip">
      <div class="home-quote-icon">"</div>
      <div class="home-quote-text">
        His home became <strong>our comfort place</strong> — where we could just be ourselves. 
        Face masks, lazy afternoons, mirror selfies, Sunday mornings on the balcony. 
        No performance, no pretending. Just us, at our most real, in the place that felt most like home.
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── ADVENTURES SECTION ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="adventure-section">
  <div class="adventure-inner">
    <p class="section-label">Their first trip together</p>
    <h2 class="section-heading">Adventures Together</h2>

    <!-- Rose & Chai moment -->
    <div class="rose-moment">
      <div class="rose-photos">
        <div class="rose-photo rose-photo-tall" style="grid-row: span 2;">
          {photo_tag("kotna_rose_smile.jpg")}
        </div>
        <div class="rose-photo">
          {photo_tag("kotna_rose_lap.jpg")}
        </div>
        <div class="rose-photo">
          {photo_tag("kotna_car_hands.jpg")}
        </div>
      </div>
      <div class="rose-text">
        <p class="rose-eyebrow">Kotna Beach · Their first trip</p>
        <h3 class="rose-heading">She brought him<br>a rose. He got her<br>a chiku shake. 🌹</h3>
        <p class="rose-body">
          Ritika showed up with a red rose for Kuldip — wrapped in cellophane, 
          carried all the way to Kotna. And he? He got her a chiku shake. 
          No grand plan, no occasion — just two people quietly saying 
          <em>I thought of you</em> in the simplest, sweetest ways.<br><br>
          That photo of him holding the rose and the shake — that grin says everything. 
          He knew exactly how special this day already was.
        </p>
        <div class="rose-detail">
          <span class="rose-detail-icon">📍</span>
          <span class="rose-detail-text">Kotna Beach — their first trip somewhere new together</span>
        </div>
        <div class="rose-detail">
          <span class="rose-detail-icon">🌹</span>
          <span class="rose-detail-text">Ritika brought him a red rose. He got her a chiku shake.</span>
        </div>
        <div class="rose-detail">
          <span class="rose-detail-icon">🛶</span>
          <span class="rose-detail-text">First time kayaking — together in an orange boat on open water</span>
        </div>
      </div>
    </div>

    <!-- Kayak gallery -->
    <p class="kayak-heading"><em>On the water, in blue life vests, paddling into something new</em></p>
    <div class="kayak-strip">
      <div class="kayak-photo kayak-big">
        {photo_tag("kotna_wide_selfie.jpg")}
        <div class="kayak-label">Kotna lake — kayaks & sunlight 🌊</div>
      </div>
      <div class="kayak-photo">
        {photo_tag("kotna_kayak_water.jpg")}
        <div class="kayak-label">Out on the open water</div>
      </div>
      <div class="kayak-photo">
        {photo_tag("kotna_lifevest_selfie.jpg")}
        <div class="kayak-label">Blue vests, big smiles</div>
      </div>
      <div class="kayak-photo">
        {photo_tag("kotna_together_shore.jpg")}
        <div class="kayak-label">After the kayak — colourful boats behind them</div>
      </div>
      <div class="kayak-photo">
        {photo_tag("kotna_kayak_dock1.jpg")}
        <div class="kayak-label">Ready to paddle 🚣</div>
      </div>
    </div>

  </div>
</div>
""", unsafe_allow_html=True)

# ── OUR DATES SECTION ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dates-section">
  <div class="dates-inner">
    <p class="section-label">The chapters of us</p>
    <h2 class="section-heading">Our Dates</h2>

    <!-- Date cards: themed outings -->
    <div class="date-cards">

      <div class="date-card">
        {photo_tag("date_dec_rings1.jpg")}
        <div class="date-card-badge">Dec 2025</div>
        <div class="date-card-info">
          <div class="date-card-title">Nature & Rings</div>
          <div class="date-card-sub">Green trees, their rings showing, heads together 🌿</div>
        </div>
      </div>

      <div class="date-card">
        {photo_tag("date_vday_mirror.jpg")}
        <div class="date-card-badge">Valentine's Day 2026</div>
        <div class="date-card-info">
          <div class="date-card-title">Happy Valentine's Day</div>
          <div class="date-card-sub">The rose wall, the teddy bear, the mirror selfie 🌹</div>
        </div>
      </div>

      <div class="date-card">
        {photo_tag("date_vday_hats.jpg")}
        <div class="date-card-badge">Valentine's Day 2026</div>
        <div class="date-card-info">
          <div class="date-card-title">Hat Shopping</div>
          <div class="date-card-sub">Cowboy hat + bucket hat = them 🤠🪣</div>
        </div>
      </div>

      <div class="date-card">
        {photo_tag("date_kavish_mirror1.jpg")}
        <div class="date-card-badge">Mar 2026</div>
        <div class="date-card-info">
          <div class="date-card-title">Kavish Cafe</div>
          <div class="date-card-sub">Pool, palm trees, arch mirror selfies ☀️</div>
        </div>
      </div>

      <div class="date-card">
        {photo_tag("date2_cinema_together.jpg")}
        <div class="date-card-badge">Movie Date</div>
        <div class="date-card-info">
          <div class="date-card-title">Cinema Night</div>
          <div class="date-card-sub">Red velvet seats, her leaning into him 🎬</div>
        </div>
      </div>

      <div class="date-card">
        {photo_tag("date_pottery_heart.jpg")}
        <div class="date-card-badge">Craft Date</div>
        <div class="date-card-info">
          <div class="date-card-title">Painted Hearts</div>
          <div class="date-card-sub">They painted heart pottery together 🎨</div>
        </div>
      </div>

    </div>

    <!-- Pink outfit palace shoot -->
    <p class="dates-subheading">The Pink Day — Vadodara Palace 🏛️</p>
    <div class="pink-hero">
      <div class="pink-photo">{photo_tag("date2_mosaic_wall1.jpg")}</div>
      <div class="pink-photo pink-center">{photo_tag("date2_palace.jpg")}</div>
      <div class="pink-photo">{photo_tag("date2_pink_laugh.jpg")}</div>
    </div>
    <div class="pink-hero" style="height:340px; margin-bottom:0;">
      <div class="pink-photo">{photo_tag("date2_pink_hug.jpg")}</div>
      <div class="pink-photo pink-center">{photo_tag("date2_mosaic_wall2.jpg")}</div>
      <div class="pink-photo">{photo_tag("date2_pink_cafe_selfie.jpg")}</div>
    </div>

    <!-- Food memories -->
    <p class="dates-subheading">What we ate 🍽️</p>
    <div class="food-strip">
      <div class="food-photo">{photo_tag("date2_pizza.jpg")}</div>
      <div class="food-photo">{photo_tag("date_ny_paratha.jpg")}</div>
      <div class="food-photo">{photo_tag("date2_fafda.jpg")}</div>
      <div class="food-photo">{photo_tag("date2_food_banana.jpg")}</div>
    </div>

  </div>
</div>
""", unsafe_allow_html=True)

# ── CAR RIDES SECTION ─────────────────────────────────────────────────────────
st.markdown(f"""
<div class="car-section">
  <div class="car-inner">
    <p class="section-label">Our moving world</p>
    <h2 class="section-heading">Somewhere Between<br>Here & There</h2>

    <div class="car-hero-strip">
      {photo_tag("car_drive_together.jpg")}
      <div class="car-hero-overlay">
        <p class="car-hero-quote">"Some of our best conversations happened<br>going nowhere in particular."</p>
        <p class="car-hero-tag">Every drive, a little world of our own</p>
      </div>
    </div>

    <div class="car-hands-row">
      <div class="car-photo">
        {photo_tag("car_hands1.jpg")}
        <div class="car-caption">Her ring. His watch. Fingers interlaced. 🤍</div>
      </div>
      <div class="car-photo">
        {photo_tag("car_hands2.jpg")}
        <div class="car-caption">Held together even in traffic</div>
      </div>
      <div class="car-photo">
        {photo_tag("car_hands3.jpg")}
        <div class="car-caption">Three different shots of the same truth</div>
      </div>
    </div>

    <div class="car-small-row">
      <div class="car-photo">
        {photo_tag("car_bw_hearts.jpg")}
        <div class="car-caption">Hearts floating around them 🩶</div>
      </div>
      <div class="car-photo">
        {photo_tag("car_ritika_rain.jpg")}
        <div class="car-caption">Ritika, rain on the window, lost in thought</div>
      </div>
      <div class="car-photo">
        {photo_tag("car_kuldip_ganpati.jpg")}
        <div class="car-caption">Kuldip placing the Ganpati idol 🙏</div>
      </div>
      <div class="car-photo">
        {photo_tag("car_selfie_main.jpg")}
        <div class="car-caption">White shirt, coral dress — Feb 2026 ✨</div>
      </div>
    </div>

    <div class="car-text-row">
      <p class="car-paragraph">
        Every car ride became a small adventure. Sometimes going somewhere — 
        a trip, a cafe, a new place. Sometimes just driving, windows down, music on, 
        no destination needed.<br><br>
        Ritika staring out at the rain. Kuldip's eyes on the road, one hand reaching for hers.
        The Ganpati idol watching over the dashboard.
        Not just commutes — conversations, confessions, comfortable silences.
      </p>
      <div class="car-fact">
        <p class="car-fact-label">Things that happened in the car</p>
        <ul class="car-fact-items">
          <li><span>🚗</span> Long talks about the future</li>
          <li><span>🌧️</span> Watching rain on a quiet road</li>
          <li><span>🤝</span> Hands held at every red light</li>
          <li><span>📸</span> Candid photos when the other wasn't looking</li>
          <li><span>🙏</span> A Ganpati blessing for every journey</li>
          <li><span>🖤</span> Black & white selfies with floating hearts</li>
        </ul>
      </div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── CAFE LOCAL SECTION ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cafe-section">
  <div class="cafe-inner">
    <div class="cafe-header">
      <p class="section-label">Our favourite place in the world</p>
      <div class="cafe-title-row">
        <h2 class="section-heading" style="margin-bottom:0;">Café Local</h2>
        <span class="cafe-hindi">· काफे लोकल</span>
      </div>
      <p class="cafe-sub-text">
        Some places become more than places. They become the backdrop of your memories, 
        the smell you'll remember for years, the corner where you first felt completely at ease 
        with someone. Café Local is that place for us.
      </p>
    </div>

    <div class="cafe-grid">
      <div class="cafe-photo cafe-big">
        {photo_tag("cafe_us3.jpg", "Our corner at Café Local")}
        <div class="cafe-caption">The fairy lights, the wooden tables — always us here 🤍</div>
      </div>
      <div class="cafe-photo cafe-small">
        {photo_tag("cafe_interior.jpg", "Inside Café Local")}
        <div class="cafe-caption">The teal sofas we loved sitting on</div>
      </div>
      <div class="cafe-photo cafe-small">
        {photo_tag("cafe_us1.jpg", "Laughing together")}
        <div class="cafe-caption">Can't stop laughing — as always</div>
      </div>
      <div class="cafe-photo cafe-small">
        {photo_tag("cafe_us2.jpg", "Kuldip at the cafe")}
        <div class="cafe-caption">His smile that says he's happy here</div>
      </div>
      <div class="cafe-photo cafe-small">
        {photo_tag("cafe_sign1.jpg", "Cafe Local sign")}
        <div class="cafe-caption">Makarpura, Vadodara — our place</div>
      </div>
    </div>

    <div class="cafe-straw-row">
      <div class="cafe-straw-img">{photo_tag("cafe_straw.jpg", "Heart straw")}</div>
      <div class="cafe-straw-text">
        <h3 class="cafe-straw-heading">The heart-shaped straw<br>that said everything</h3>
        <p class="cafe-straw-body">
          We didn't need grand gestures. We had a heart-shaped straw, 
          a milkshake between us, and wooden tables that had heard a hundred 
          of our conversations.<br><br>
          Café Local wasn't just where we ate. It was where we talked about 
          everything and nothing. Where silences felt comfortable. 
          Where we just… were.
        </p>
      </div>
    </div>

  </div>
</div>
""", unsafe_allow_html=True)

# ── CLOSING ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="closing">
  <div class="divider"></div>
  <p class="closing-quote">
    "Through breakups and beginnings, through accidents and sunrises,<br>
    through every route I didn't know — I always found my way back to you."
  </p>
  <div class="divider"></div>
  <p class="closing-names">Ritika &nbsp;🤍&nbsp; Kuldip &nbsp;·&nbsp; #ALoveThatRefusedToEnd</p>
</div>
""", unsafe_allow_html=True)
