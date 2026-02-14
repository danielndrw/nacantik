# app.py
# ============================================================
# ROMANTIC STREAMLIT LOVE STORY — Multi-Page Chapters (1 file)
# ============================================================
# ✅ Tidak jadi 1 halaman panjang: setiap section = 1 "chapter page"
# ✅ Navigasi pakai pill bar (klik) + tombol Next/Prev
# ✅ Palette lebih "kemerahan" (ruby/rose) daripada pink
# ✅ Animasi halus via CSS + transisi "Turning the page…" (spinner)
# ✅ Foto lokal dari ./images/ (tinggal ganti file names)
# ✅ Semua teks romantis editable di bagian atas file ini
# ============================================================

from __future__ import annotations

import html as _html
import re
import time
from pathlib import Path
from typing import Dict, List

import streamlit as st
from PIL import Image


# ============================================================
# 1) EDITABLE TEXT VARIABLES (EDIT DI SINI SAJA)
# ============================================================

PAGE_TITLE = "A Love Story 🌙"
PAGE_ICON = "💗"

# --- HERO / WELCOME ---
hero_tagline = "A DIGITAL LOVE LETTER"
hero_headline = "To My Favorite Person"
hero_subheadline = "A small, warm corner of the internet… made only for you."
hero_micro_poem = """
When the world gets loud,
you are my quiet.
"""

welcome_story_hint = """
This is not a normal website.
It’s a small story—told softly.

Take it chapter by chapter.
"""

# --- GRATITUDE ---
gratitude_text = """
I want to start with **thank you**.

Thank you for your patience, your warmth, and the way you show up—especially when it would be easier not to.
Thank you for the little things you do that you probably don’t even realize are extraordinary.

- Thank you for your honesty.
- Thank you for your gentleness.
- Thank you for choosing love, even on difficult days.

If I don’t say it enough: I see you, and I’m grateful for you.
"""

gratitude_side_title = "A soft truth"
gratitude_side_text = """
You’ve made my world calmer.
You’ve made my heart braver.
And I never want to take that for granted.
"""

# --- APOLOGY ---
apology_text = """
I’m sorry for the moments I fell short.

Sorry for the times my words didn’t reflect my feelings,
or when I didn’t listen the way you deserved to be listened to.

I’m not asking for perfection from us—only for **growth**, and for the courage to keep choosing each other.
I want to do better, not in big dramatic promises… but in the everyday ways that matter most.
"""

apology_side_title = "What I’m learning"
apology_side_text = """
Love is not just how we feel.
It’s how we speak.
How we pause.
How we repair.
How we return.
"""

# --- LOVE & DEVOTION ---
love_text = """
I love you—deeply, quietly, completely.

I love the way you think.
I love the way you care.
I love the way your presence can make a hard day feel survivable.

When I picture “home,” I don’t picture a place.
I picture **you**.

And if loving you is a choice, then it’s the easiest one I’ll ever make.
"""

love_side_title = "My devotion"
love_side_text = """
I’ll keep choosing you:

- when it’s easy
- when it’s hard
- when it’s ordinary
- when it’s beautiful

I’m here. I’m staying.
"""

# --- FUTURE & MARRIAGE ---
future_text = """
I don’t just want a future *near* you.
I want a future **with** you.

A life built from simple things:
morning light, shared meals, inside jokes, honest conversations,
and hands reaching for each other without thinking.

If marriage is a promise, then I want mine to sound like this:
*I will protect our love. I will nurture our peace. I will keep showing up.*
"""

future_side_title = "A gentle dream"
future_side_text = """
Someday, I want to look at you and know:

We did it the right way.
With kindness.
With intention.
With love that kept becoming more.
"""

# --- MEMORIES ---
memories_intro_text = """
Here are a few memories—little frames of time I never want to forget.

(Replace the images in the /images folder to make this gallery yours.)
"""

# --- VALENTINE’S & FUTURE DAYS ---
valentines_text = """
Not just Valentine’s Day—**every** day.

Let’s celebrate the small days too:
the random Tuesdays, the quiet nights, the “I’m proud of you” moments,
the “I’m here” moments.

And for the future days—birthdays, anniversaries, new chapters—
I want us to meet them hand-in-hand, with love that feels safe and alive.
"""

valentines_side_title = "A simple vow"
valentines_side_text = """
I’ll love you loudly in the ways that matter,
and softly in the ways you need.

Happy Valentine’s—today, and all the days ahead.
"""

# --- FOOTER ---
closing_footer_text = "Built with love, for you. 💗"


# ============================================================
# 2) PHOTO GALLERY (EDIT FILE NAMES + CAPTIONS DI SINI)
# ============================================================

PHOTO_ITEMS: List[Dict[str, str]] = [
    {"file": "photo1.jpg", "caption": "A moment I still replay in my mind."},
    {"file": "photo2.jpg", "caption": "Where everything felt a little softer."},
    {"file": "photo3.jpg", "caption": "Proof that the ordinary can be magical."},
    {"file": "photo4.jpg", "caption": "One of my favorite days with you."},
    {"file": "photo5.jpg", "caption": "A memory that feels like warm light."},
    {"file": "photo6.jpg", "caption": "Us—exactly as we are."},
]

GALLERY_COLUMNS = 3  # ubah jadi 2/4 sesuai selera


# ============================================================
# 3) STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

APP_DIR = Path(__file__).resolve().parent
IMAGES_DIR = APP_DIR / "images"


# ============================================================
# 4) QUERY PARAM HELPERS (agar klik nav terasa seperti “page”)
# ============================================================

def _get_query_page(default: str = "welcome") -> str:
    """Get ?page=... robustly across Streamlit versions."""
    try:
        qp = st.query_params  # type: ignore[attr-defined]
        page = qp.get("page", default)
        if isinstance(page, list):
            return page[0] if page else default
        return page if page else default
    except Exception:
        qp = st.experimental_get_query_params()
        return qp.get("page", [default])[0]


def _set_query_page(page: str) -> None:
    """Set ?page=... robustly across Streamlit versions."""
    try:
        st.query_params["page"] = page  # type: ignore[attr-defined]
    except Exception:
        st.experimental_set_query_params(page=page)


def _rerun() -> None:
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


# ============================================================
# 5) STYLING — Ruby / Red Romantic Theme (lebih kemerahan)
# ============================================================

def inject_css(reduce_motion: bool = False) -> None:
    extra_motion_css = ""
    if reduce_motion:
        extra_motion_css = """
        * { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
        """

    st.markdown(
        f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root{{
  --cream: #FFF4EC;
  --warm-beige: #F1E0D2;
  --rose: #C85C6E;         /* lebih merah */
  --ruby: #A83A4B;         /* accent utama */
  --burgundy: #7A1F2C;
  --muted-gold: #C7A65B;

  --ink: #2B2B2B;
  --ink-soft: rgba(43,43,43,0.78);

  --glass: rgba(255,255,255,0.54);
  --glass-strong: rgba(255,255,255,0.70);
  --stroke: rgba(199,166,91,0.25);
  --shadow: 0 18px 70px rgba(0,0,0,0.09);
}}

/* Background: cream + ruby glow + warm beige */
.stApp{{
  background:
    radial-gradient(900px 650px at 18% 16%, rgba(168,58,75,0.22) 0%, rgba(168,58,75,0.00) 60%),
    radial-gradient(900px 650px at 82% 18%, rgba(199,166,91,0.18) 0%, rgba(199,166,91,0.00) 60%),
    radial-gradient(1100px 900px at 50% 105%, rgba(122,31,44,0.12) 0%, rgba(122,31,44,0.00) 55%),
    linear-gradient(135deg, var(--cream) 0%, rgba(200,92,110,0.18) 36%, rgba(168,58,75,0.10) 58%, var(--warm-beige) 100%);
  background-attachment: fixed;
}}

section.main .block-container{{
  max-width: 1120px;
  padding-top: 1.7rem;
  padding-bottom: 3rem;
  animation: pageFade .60s ease both;
}}

#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

html, body, [class*="css"]{{
  font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
  color: var(--ink);
}}

h1, h2, h3, h4{{
  font-family: "Playfair Display", Georgia, serif;
  letter-spacing: 0.2px;
}}

p, li{{
  color: var(--ink-soft);
  line-height: 1.85;
  font-size: 1.05rem;
}}

/* Top header card */
.topbar{{
  background: linear-gradient(180deg, var(--glass-strong), rgba(255,255,255,0.40));
  border: 1px solid rgba(199,166,91,0.22);
  box-shadow: 0 16px 56px rgba(0,0,0,0.06);
  border-radius: 22px;
  padding: 1.05rem 1.15rem;
  overflow: hidden;
  position: relative;
}}
.topbar::before{{
  content:"";
  position:absolute;
  inset:-2px;
  background:
    radial-gradient(520px 220px at 20% 25%, rgba(168,58,75,0.18), transparent 60%),
    radial-gradient(460px 220px at 80% 22%, rgba(199,166,91,0.16), transparent 60%);
  pointer-events:none;
}}

.brand{{
  display:flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
}}
.brand .title{{
  font-family: "Playfair Display", Georgia, serif;
  font-size: 1.35rem;
  color: rgba(43,43,43,0.88);
}}
.brand .subtitle{{
  font-size: 0.95rem;
  color: rgba(43,43,43,0.62);
}}
.brand .accent{{
  color: rgba(168,58,75,0.92);
}}

/* Nav pills */
.navbar{{
  display:flex;
  flex-wrap: wrap;
  gap: .5rem;
  margin-top: .75rem;
}}
.nav-pill{{
  display:inline-flex;
  align-items:center;
  gap:.45rem;
  padding: .52rem .85rem;
  border-radius: 999px;
  background: rgba(255,255,255,0.56);
  border: 1px solid rgba(199,166,91,0.22);
  box-shadow: 0 12px 34px rgba(0,0,0,0.05);
  text-decoration:none;
  font-size: .95rem;
  color: rgba(43,43,43,0.86);
  transition: transform .16s ease, background .16s ease, border .16s ease;
}}
.nav-pill:hover{{
  transform: translateY(-2px);
  background: rgba(255,255,255,0.72);
  border: 1px solid rgba(168,58,75,0.20);
}}
.nav-pill.active{{
  background: linear-gradient(180deg, rgba(168,58,75,0.18), rgba(255,255,255,0.70));
  border: 1px solid rgba(168,58,75,0.28);
}}

/* Progress line */
.progress-wrap{{
  margin-top: .85rem;
  display:flex;
  gap:.75rem;
  align-items:center;
  flex-wrap: wrap;
}}
.progress-track{{
  height: 8px;
  width: 240px;
  border-radius: 999px;
  background: rgba(43,43,43,0.08);
  overflow:hidden;
  border: 1px solid rgba(199,166,91,0.14);
}}
.progress-fill{{
  height: 100%;
  border-radius: 999px;
  background: linear-gradient(90deg, rgba(168,58,75,0.70), rgba(199,166,91,0.70));
  box-shadow: 0 10px 26px rgba(168,58,75,0.18);
}}
.progress-text{{
  font-size: 0.93rem;
  color: rgba(43,43,43,0.62);
}}

/* Hero */
.hero{{
  background: linear-gradient(180deg, var(--glass-strong), rgba(255,255,255,0.40));
  border: 1px solid rgba(199,166,91,0.24);
  box-shadow: var(--shadow);
  border-radius: 28px;
  padding: 2.15rem 2.25rem;
  overflow: hidden;
  position: relative;
  animation: fadeUp .65s ease both;
}}
.hero::before{{
  content:"";
  position:absolute;
  inset:-2px;
  background:
    radial-gradient(650px 260px at 18% 26%, rgba(168,58,75,0.22), transparent 62%),
    radial-gradient(540px 240px at 82% 20%, rgba(199,166,91,0.16), transparent 62%);
  pointer-events:none;
}}
.hero .tag{{
  font-size:1.00rem;
  letter-spacing:.10em;
  color: rgba(43,43,43,0.62);
}}
.hero h1{{
  font-size: 3.1rem;
  margin: 0.25rem 0 0.25rem 0;
}}
.hero .sub{{
  font-size: 1.15rem;
  color: rgba(43,43,43,0.72);
}}
.hero .micro{{
  margin-top: 1.2rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(199,166,91,0.20);
  font-style: italic;
  color: rgba(43,43,43,0.70);
}}

/* Chapter header */
.chapter{{
  margin-top: 1.35rem;
  margin-bottom: 0.65rem;
}}
.chapter h2{{
  font-size: 2.05rem;
  margin-bottom: .2rem;
}}
.chapter .line{{
  height: 1px;
  background: linear-gradient(90deg, rgba(168,58,75,0.00), rgba(168,58,75,0.42), rgba(199,166,91,0.42), rgba(199,166,91,0.00));
  margin-top: .75rem;
  opacity: .85;
}}

/* Soft divider */
.soft-divider{{
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(168,58,75,0.35), rgba(199,166,91,0.40), transparent);
  margin: 1.25rem 0;
  opacity: 0.8;
}}

/* Cards */
.paper, .aside{{
  border-radius: 22px;
  padding: 1.25rem 1.35rem;
  border: 1px solid rgba(199,166,91,0.22);
  box-shadow: 0 14px 52px rgba(0,0,0,0.07);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  animation: fadeUp .55s ease both;
}}
.paper{{ background: rgba(255,255,255,0.64); }}
.aside{{ background: linear-gradient(180deg, rgba(168,58,75,0.12), rgba(255,255,255,0.62)); }}
.card-title{{
  margin: 0 0 .55rem 0;
  font-size: 1.35rem;
}}
.soft-hint{{
  text-align:center;
  margin-top: .75rem;
  color: rgba(43,43,43,0.60);
  font-size: .98rem;
}}

/* Buttons */
.stButton > button{{
  border-radius: 999px !important;
  padding: .62rem 1.05rem !important;
  border: 1px solid rgba(168,58,75,0.22) !important;
  background: rgba(255,255,255,0.70) !important;
  transition: transform .16s ease, background .16s ease;
}}
.stButton > button:hover{{
  transform: translateY(-1px);
  background: rgba(255,255,255,0.86) !important;
}}

/* Images */
div[data-testid="stImage"] img{{
  border-radius: 18px;
  border: 1px solid rgba(199,166,91,0.20);
  box-shadow: 0 18px 62px rgba(0,0,0,0.12);
  transition: transform .22s ease, filter .22s ease;
}}
div[data-testid="stImage"] img:hover{{
  transform: scale(1.01);
  filter: saturate(1.03);
}}
.img-caption{{
  margin-top: .45rem;
  font-size: .95rem;
  color: rgba(43,43,43,0.68);
  font-style: italic;
}}
.missing-photo{{
  border-radius: 18px;
  padding: 1.1rem 1rem;
  border: 1px dashed rgba(168,58,75,0.35);
  background: rgba(255,255,255,0.44);
  color: rgba(43,43,43,0.70);
}}

/* Footer */
.romantic-footer{{
  margin-top: 2.2rem;
  padding: 1.2rem 1.2rem;
  text-align: center;
  border-radius: 18px;
  background: rgba(255,255,255,0.45);
  border: 1px solid rgba(199,166,91,0.16);
  color: rgba(43,43,43,0.70);
}}

/* Animations */
@keyframes fadeUp{{
  from {{opacity: 0; transform: translateY(10px);}}
  to   {{opacity: 1; transform: translateY(0);}}
}}
@keyframes pageFade{{
  from {{opacity: 0.0; transform: translateY(8px);}}
  to   {{opacity: 1.0; transform: translateY(0);}}
}}

{extra_motion_css}
</style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 6) TEXT RENDERING (Editable text -> pretty HTML)
# ============================================================

def _apply_light_formatting(escaped: str) -> str:
    """Support **bold** and *italic* markers (input already escaped)."""
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", escaped)
    return escaped


def text_to_html_blocks(text: str) -> str:
    """
    Convert simple text into HTML paragraphs + bullet lists.
    - Blank lines -> paragraph breaks
    - Lines starting '- ' or '• ' -> bullet list
    """
    raw = (text or "").strip()
    if not raw:
        return "<p></p>"

    lines = raw.splitlines()
    out: List[str] = []
    para_buf: List[str] = []
    list_buf: List[str] = []

    def flush_paragraph() -> None:
        nonlocal para_buf
        if para_buf:
            content = _html.escape("\n".join(para_buf)).replace("\n", "<br>")
            content = _apply_light_formatting(content)
            out.append(f"<p>{content}</p>")
            para_buf = []

    def flush_list() -> None:
        nonlocal list_buf
        if list_buf:
            items = []
            for item in list_buf:
                item_esc = _apply_light_formatting(_html.escape(item))
                items.append(f"<li>{item_esc}</li>")
            out.append("<ul>" + "".join(items) + "</ul>")
            list_buf = []

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            flush_paragraph()
            flush_list()
            continue

        is_bullet = stripped.startswith("- ") or stripped.startswith("• ")
        if is_bullet:
            flush_paragraph()
            list_buf.append(stripped[2:].strip())
        else:
            flush_list()
            para_buf.append(stripped)

    flush_paragraph()
    flush_list()
    return "".join(out)


# ============================================================
# 7) UI COMPONENTS
# ============================================================

@st.cache_data(show_spinner=False)
def load_image(path: Path) -> Image.Image:
    return Image.open(path)


def revealable_text_card(key: str, text: str, button_label: str) -> None:
    """
    Animation-like reveal:
    - starts with a romantic reveal button
    - after click: short spinner then text appears in a glass card
    """
    if key not in st.session_state:
        st.session_state[key] = False

    if not st.session_state[key]:
        c1, c2, c3 = st.columns([0.22, 0.56, 0.22], gap="small")
        with c2:
            pressed = st.button(button_label, key=f"{key}_btn")
        st.markdown(
            '<div class="soft-hint">Tap to unfold the words—slowly, softly.</div>',
            unsafe_allow_html=True,
        )

        if pressed:
            with st.spinner("Unfolding…"):
                time.sleep(0.35)
            st.session_state[key] = True
            if hasattr(st, "toast"):
                st.toast("💗", icon="✨")

    if st.session_state[key]:
        st.markdown(
            f'<div class="paper">{text_to_html_blocks(text)}</div>',
            unsafe_allow_html=True,
        )


def side_note_card(title: str, text: str) -> None:
    st.markdown(
        f"""
        <div class="aside">
          <div class="card-title">{_html.escape(title)}</div>
          {text_to_html_blocks(text)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def chapter_header(title: str, subtitle: str = "") -> None:
    subtitle_html = ""
    if subtitle.strip():
        subtitle_html = (
            f'<div style="color: rgba(43,43,43,0.66); font-size: 1.02rem;">'
            f"{_html.escape(subtitle)}</div>"
        )
    st.markdown(
        f"""
        <div class="chapter">
          <h2>{_html.escape(title)}</h2>
          {subtitle_html}
          <div class="line"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 8) PAGES (each section is a “chapter page”)
# ============================================================

PAGES: List[Dict[str, str]] = [
    {"id": "welcome", "label": "🌸 Welcome", "title": "Welcome"},
    {"id": "gratitude", "label": "💌 Gratitude", "title": "Gratitude"},
    {"id": "apology", "label": "🤍 Apology", "title": "Apology"},
    {"id": "love", "label": "🌹 Love", "title": "Love & Devotion"},
    {"id": "future", "label": "💍 Future", "title": "Future & Marriage"},
    {"id": "memories", "label": "📸 Memories", "title": "Our Memories"},
    {"id": "valentines", "label": "✨ Days", "title": "Valentine’s & Future Days"},
]
PAGE_IDS = {p["id"] for p in PAGES}


def page_index(page_id: str) -> int:
    for i, p in enumerate(PAGES):
        if p["id"] == page_id:
            return i
    return 0


def render_topbar(current_page: str) -> None:
    idx = page_index(current_page)
    total = len(PAGES)
    pct = int(((idx + 1) / total) * 100)

    nav_links = []
    for p in PAGES:
        active = "active" if p["id"] == current_page else ""
        nav_links.append(
            f'<a class="nav-pill {active}" href="?page={p["id"]}">{_html.escape(p["label"])}</a>'
        )
    nav_html = "".join(nav_links)

    st.markdown(
        f"""
        <div class="topbar">
          <div class="brand">
            <div class="title">{_html.escape(PAGE_TITLE)} <span class="accent">✦</span></div>
            <div class="subtitle">A gentle story in {total} chapters</div>
          </div>

          <div class="navbar">{nav_html}</div>

          <div class="progress-wrap">
            <div class="progress-track">
              <div class="progress-fill" style="width:{pct}%;"></div>
            </div>
            <div class="progress-text">Chapter {idx+1} of {total}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prev_next(current_page: str) -> None:
    idx = page_index(current_page)

    prev_id = PAGES[idx - 1]["id"] if idx > 0 else None
    next_id = PAGES[idx + 1]["id"] if idx < len(PAGES) - 1 else None

    left, mid, right = st.columns([1, 2, 1], gap="small")

    with left:
        if prev_id:
            if st.button("← Previous", key=f"prev_{prev_id}"):
                _set_query_page(prev_id)
                st.session_state["_transition"] = True
                _rerun()
        else:
            st.write("")

    with mid:
        st.markdown(
            '<div style="text-align:center; color: rgba(43,43,43,0.55); padding-top: .35rem;">'
            "Take your time. No rush. 💗"
            "</div>",
            unsafe_allow_html=True,
        )

    with right:
        if next_id:
            if st.button("Next →", key=f"next_{next_id}"):
                _set_query_page(next_id)
                st.session_state["_transition"] = True
                _rerun()
        else:
            st.write("")


# ============================================================
# 9) PAGE CONTENT
# ============================================================

def render_welcome() -> None:
    st.markdown(
        f"""
        <div class="hero">
          <div class="tag">{_html.escape(hero_tagline)}</div>
          <h1>{_html.escape(hero_headline)} <span style="color: rgba(168,58,75,0.92);">❤</span></h1>
          <div class="sub">{_html.escape(hero_subheadline)}</div>
          <div class="micro">{text_to_html_blocks(hero_micro_poem)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    chapter_header("A soft beginning", "A cinematic little place—built gently, with intention.")
    left, right = st.columns([1.25, 1], gap="large")
    with left:
        st.markdown(
            f'<div class="paper">{text_to_html_blocks(welcome_story_hint)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns([0.2, 0.6, 0.2], gap="small")
        with c2:
            if st.button("Start the story ✨", key="start_story"):
                _set_query_page("gratitude")
                st.session_state["_transition"] = True
                _rerun()

    with right:
        side_note_card(
            "A tiny promise",
            "This space is gentle.\nThis story is honest.\nAnd every page is written with care.",
        )


def render_gratitude() -> None:
    chapter_header("💌 Gratitude", "For the love you give—seen and unseen.")
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        revealable_text_card("reveal_gratitude", gratitude_text, "Reveal this chapter 💌")
    with right:
        side_note_card(gratitude_side_title, gratitude_side_text)


def render_apology() -> None:
    chapter_header("🤍 Apology", "Because love is also repair.")
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        revealable_text_card("reveal_apology", apology_text, "Reveal this chapter 🤍")
    with right:
        side_note_card(apology_side_title, apology_side_text)


def render_love() -> None:
    chapter_header("🌹 Love & Devotion", "Soft, steady, and real.")
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        revealable_text_card("reveal_love", love_text, "Reveal this chapter 🌹")
    with right:
        side_note_card(love_side_title, love_side_text)


def render_future() -> None:
    chapter_header("💍 Future & Marriage", "Not a fantasy—an intention.")
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        revealable_text_card("reveal_future", future_text, "Reveal this chapter 💍")
    with right:
        side_note_card(future_side_title, future_side_text)


def render_memories() -> None:
    chapter_header("📸 Our Memories", "Little frames of time I never want to lose.")
    st.markdown(
        f'<div class="paper">{text_to_html_blocks(memories_intro_text)}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

    cols = st.columns(GALLERY_COLUMNS, gap="medium")
    for i, item in enumerate(PHOTO_ITEMS):
        with cols[i % GALLERY_COLUMNS]:
            img_path = IMAGES_DIR / item["file"]
            caption = item.get("caption", "").strip()

            if img_path.exists():
                try:
                    img = load_image(img_path)
                    st.image(img, use_container_width=True)
                    if caption:
                        st.markdown(
                            f'<div class="img-caption">{_html.escape(caption)}</div>',
                            unsafe_allow_html=True,
                        )
                except Exception:
                    st.markdown(
                        f'<div class="missing-photo">Could not load <strong>{_html.escape(item["file"])}</strong>.</div>',
                        unsafe_allow_html=True,
                    )
            else:
                st.markdown(
                    f"""
                    <div class="missing-photo">
                      <strong>Missing photo:</strong> {_html.escape(item["file"])}<br>
                      Put it inside <code>/images</code> or update PHOTO_ITEMS at the top.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center; color: rgba(43,43,43,0.60); font-style: italic;">'
        "If you want—add more photos and captions. This chapter can grow with us."
        "</div>",
        unsafe_allow_html=True,
    )


def render_valentines() -> None:
    chapter_header("✨ Valentine’s & Future Days", "Not only a date—an atmosphere.")
    left, right = st.columns([1.35, 1], gap="large")
    with left:
        revealable_text_card("reveal_valentines", valentines_text, "Reveal this chapter ✨")
    with right:
        side_note_card(valentines_side_title, valentines_side_text)


RENDERERS = {
    "welcome": render_welcome,
    "gratitude": render_gratitude,
    "apology": render_apology,
    "love": render_love,
    "future": render_future,
    "memories": render_memories,
    "valentines": render_valentines,
}


# ============================================================
# 10) APP ENTRYPOINT
# ============================================================

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    reduce_motion = st.toggle("Reduce motion (accessibility)", value=False)
    st.caption("Tip: Turn off motion if you want a calmer feel.")

inject_css(reduce_motion=reduce_motion)

requested_page = _get_query_page(default="welcome")
if requested_page not in PAGE_IDS:
    requested_page = "welcome"
    _set_query_page("welcome")

# Detect page change (for smooth transition)
if "current_page" not in st.session_state:
    st.session_state["current_page"] = requested_page
elif st.session_state["current_page"] != requested_page:
    st.session_state["current_page"] = requested_page
    st.session_state["_transition"] = True

current_page = st.session_state["current_page"]

# Smooth transition cue (shows only on page change)
if st.session_state.get("_transition", False) and not reduce_motion:
    with st.spinner("Turning the page…"):
        time.sleep(0.35)
    st.session_state["_transition"] = False
    if hasattr(st, "toast"):
        st.toast("✨", icon="💗")

render_topbar(current_page)
st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)

with st.container():
    RENDERERS.get(current_page, render_welcome)()

st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
render_prev_next(current_page)

# Optional background music (COMMENTED)
# ------------------------------------------------------------
# Tips:
# 1) Buat folder: ./assets
# 2) Taruh file: ./assets/music.mp3
# 3) Uncomment block ini untuk mengaktifkan audio.
#
# ASSETS_DIR = APP_DIR / "assets"
# music_path = ASSETS_DIR / "music.mp3"
# with st.sidebar:
#     st.markdown("### 🎵 Background music")
#     if music_path.exists():
#         st.audio(music_path.read_bytes(), format="audio/mp3")
#     else:
#         st.caption("Add an MP3 at ./assets/music.mp3 to enable music.")

st.markdown(
    f"""
    <div class="romantic-footer">
      {_html.escape(closing_footer_text)}
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# INSTRUCTIONS (SINGKAT)
# ============================================================
#
# Run:
#   pip install streamlit pillow
#   streamlit run app.py
#
# Edit teks:
#   edit variabel di bagian paling atas (gratitude_text, love_text, dst)
#
# Ganti foto:
#   taruh foto di ./images/ dan edit PHOTO_ITEMS (nama file + caption)
# ============================================================
