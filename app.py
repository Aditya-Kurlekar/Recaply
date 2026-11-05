import os
import tempfile
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

st.set_page_config(page_title="Recaply", page_icon="🧠", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg:#050812;
    --panel:#0b1020;
    --panel-2:#10172a;
    --border:rgba(148,163,184,.16);
    --muted:#91a0bb;
    --text:#f5f7ff;
    --purple:#8b5cf6;
    --cyan:#22d3ee;
}

html, body, [class*="css"] {
    font-family:'DM Sans',sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(124,58,237,.16), transparent 30%),
        radial-gradient(circle at 92% 8%, rgba(34,211,238,.12), transparent 27%),
        linear-gradient(180deg,#050812 0%,#060912 55%,#03050b 100%);
    color:var(--text);
}

.stApp::before {
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    opacity:.18;
    background-image:
        linear-gradient(rgba(139,92,246,.07) 1px,transparent 1px),
        linear-gradient(90deg,rgba(34,211,238,.05) 1px,transparent 1px);
    background-size:42px 42px;
    mask-image:linear-gradient(to bottom,black 0%,transparent 72%);
}

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#080d19 0%,#050811 100%);
    border-right:1px solid rgba(148,163,184,.12);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top:1.4rem;
}

h1,h2,h3 {
    font-family:'Space Grotesk',sans-serif !important;
    letter-spacing:-.035em;
}

.block-container {
    max-width:1120px;
    padding-top:2.2rem;
    padding-bottom:4rem;
}

.mm-brand {
    font:700 1.55rem 'Space Grotesk',sans-serif;
    color:#fff;
}

.mm-brand-sub {
    color:#7887a5;
    font-size:.66rem;
    letter-spacing:.18em;
    font-weight:700;
    margin-top:.1rem;
}

.mm-hero {
    position:relative;
    overflow:hidden;
    text-align:center;
    padding:4.2rem 2.2rem 3.2rem;
    border:1px solid rgba(139,92,246,.28);
    border-radius:28px;
    background:
        radial-gradient(circle at 50% 0%,rgba(124,58,237,.12),transparent 42%),
        linear-gradient(135deg,rgba(12,15,31,.96),rgba(7,15,27,.94));
    box-shadow:0 30px 100px rgba(0,0,0,.30);
    animation:rise .65s ease both;
}

.mm-hero::after {
    content:"";
    position:absolute;
    width:420px;
    height:420px;
    right:-220px;
    top:-260px;
    border-radius:50%;
    background:rgba(34,211,238,.10);
    filter:blur(70px);
    pointer-events:none;
}

.mm-eyebrow {
    color:#c4b5fd;
    font-size:.68rem;
    font-weight:800;
    letter-spacing:.24em;
    position:relative;
    z-index:1;
}

.mm-title {
    font:700 clamp(2.8rem,7vw,5.8rem)/.94 'Space Grotesk',sans-serif;
    letter-spacing:-.065em;
    margin:.8rem auto 1rem;
    max-width:850px;
    background:linear-gradient(105deg,#fff 8%,#ddd6fe 43%,#93c5fd 70%,#67e8f9 100%);
    -webkit-background-clip:text;
    background-clip:text;
    -webkit-text-fill-color:transparent;
    position:relative;
    z-index:1;
}

.mm-sub {
    color:#94a3b8;
    max-width:700px;
    margin:0 auto;
    line-height:1.7;
    font-size:.93rem;
    position:relative;
    z-index:1;
}

.mm-pills {
    margin-top:1.35rem;
    position:relative;
    z-index:1;
}

.mm-pill {
    display:inline-block;
    padding:.34rem .72rem;
    margin:.2rem;
    border-radius:999px;
    font-size:.62rem;
    font-weight:800;
    letter-spacing:.08em;
    color:#ddd6fe;
    background:rgba(139,92,246,.10);
    border:1px solid rgba(139,92,246,.30);
}

.mm-section {
    font:600 1.18rem 'Space Grotesk',sans-serif;
    margin:1.35rem 0 .85rem;
    color:#f5f7ff;
}

.mm-analysis {
    margin-top:1.8rem;
    padding:1.35rem;
    border:1px solid rgba(148,163,184,.14);
    border-radius:20px;
    background:rgba(9,14,27,.76);
    box-shadow:0 18px 60px rgba(0,0,0,.18);
    animation:rise .75s ease both;
}

.mm-language {
    display:flex;
    align-items:center;
    gap:.55rem;
    margin-bottom:.55rem;
}

.mm-language-label {
    color:#9aa8c2;
    font-size:.72rem;
    font-weight:700;
    letter-spacing:.08em;
    text-transform:uppercase;
}

.mm-language-help {
    color:#64748b;
    font-size:.72rem;
    margin-bottom:.8rem;
}

.mm-card {
    background:linear-gradient(145deg,rgba(15,22,39,.90),rgba(8,13,25,.92));
    border:1px solid var(--border);
    border-radius:18px;
    padding:1.15rem;
    transition:transform .22s,border-color .22s,box-shadow .22s;
    animation:rise .55s ease both;
}

.mm-card:hover {
    transform:translateY(-3px);
    border-color:rgba(139,92,246,.48);
    box-shadow:0 18px 45px rgba(60,35,130,.17);
}

.mm-label {
    color:#71819d;
    font-size:.68rem;
    text-transform:uppercase;
    letter-spacing:.13em;
    font-weight:700;
}

.mm-value {
    font:700 1.55rem 'Space Grotesk',sans-serif;
    color:#f4f6ff;
    margin-top:.35rem;
}

.mm-status {
    display:inline-flex;
    align-items:center;
    gap:.45rem;
    color:#86efac;
    font-size:.72rem;
    font-weight:700;
}

.mm-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    background:#4ade80;
    box-shadow:0 0 12px rgba(74,222,128,.8);
    animation:pulse 1.8s infinite;
}

.stTabs [data-baseweb="tab-list"] {
    gap:.35rem;
    background:transparent;
    border-bottom:1px solid rgba(148,163,184,.13);
}

.stTabs [data-baseweb="tab"] {
    color:#7f8da8;
    font-weight:700;
    font-size:.78rem;
    padding:.7rem .8rem;
}

.stTabs [aria-selected="true"] {
    color:#fff !important;
}

.stTabs [data-baseweb="tab-highlight"] {
    background:linear-gradient(90deg,#8b5cf6,#22d3ee);
    height:2px;
}

.stButton > button,
.stDownloadButton > button {
    border:1px solid rgba(167,139,250,.34);
    border-radius:12px;
    background:linear-gradient(105deg,#7c3aed 0%,#6366f1 52%,#299fd6 100%);
    color:white;
    font-weight:800;
    min-height:2.8rem;
    transition:all .2s ease;
    box-shadow:0 8px 28px rgba(99,102,241,.16);
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    transform:translateY(-2px);
    box-shadow:0 14px 35px rgba(99,102,241,.30);
    border-color:rgba(196,181,253,.65);
}

.stTextInput input,
.stSelectbox [data-baseweb="select"] > div {
    background:#0d1424 !important;
    border:1px solid rgba(148,163,184,.18) !important;
    border-radius:11px !important;
    color:#fff !important;
}

.stTextInput input:focus {
    border-color:rgba(139,92,246,.75) !important;
    box-shadow:0 0 0 1px rgba(139,92,246,.25) !important;
}

[data-testid="stFileUploader"] {
    border:1px dashed rgba(167,139,250,.42);
    border-radius:14px;
    background:rgba(13,20,36,.58);
}

[data-testid="stFileUploader"] section {
    background:transparent;
}

.stProgress > div > div {
    background:linear-gradient(90deg,#8b5cf6,#6366f1,#22d3ee);
}

[data-testid="stAlert"] {
    border-radius:12px;
}

@keyframes rise {
    from { opacity:0; transform:translateY(14px); }
    to { opacity:1; transform:translateY(0); }
}

@keyframes pulse {
    0%,100% { transform:scale(1); opacity:.8; }
    50% { transform:scale(1.35); opacity:1; }
}

@media (max-width: 800px) {
    .block-container { padding:1rem 1rem 3rem; }
    .mm-hero { padding:3rem 1.1rem 2.5rem; border-radius:22px; }
    .mm-title { font-size:3.1rem; }
}

@media (prefers-reduced-motion:reduce) {
    *,*::before,*::after {
        animation-duration:.01ms !important;
        transition-duration:.01ms !important;
    }
}
</style>
""", unsafe_allow_html=True)

for key, default in {"result": None, "chat_history": [], "last_source": ""}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def run_pipeline(source: str, language: str, source_label: str):
    progress = st.progress(0, text="Preparing your meeting...")
    status = st.empty()
    try:
        status.info("Processing audio...")
        chunks = process_input(source)
        progress.progress(15, text="Audio ready")

        transcript = transcribe_all(chunks, language)
        if not transcript or not transcript.strip():
            raise ValueError("No speech was detected. Try a clearer recording.")
        progress.progress(35, text="Transcription complete")

        title = generate_title(transcript)
        progress.progress(48, text="Meeting title generated")

        meeting_summary = summarize(transcript)
        progress.progress(65, text="Summary generated")

        action_items = extract_action_items(transcript)
        decisions = extract_key_decisions(transcript)
        questions = extract_questions(transcript)
        progress.progress(83, text="Meeting insights extracted")

        rag_chain = build_rag_chain(transcript)
        progress.progress(100, text="Analysis complete")

        st.session_state.result = {
            "title": title,
            "transcript": transcript,
            "summary": meeting_summary,
            "action_items": action_items,
            "key_decisions": decisions,
            "open_questions": questions,
            "rag_chain": rag_chain,
        }
        st.session_state.chat_history = []
        st.session_state.last_source = source_label
        status.success("Your meeting intelligence is ready.")
    except Exception as exc:
        status.error(f"Analysis failed: {exc}")
        st.exception(exc)


def build_report_text(r):
    return (
        f"Recaply — MEETING REPORT\n\nTITLE\n{r['title']}\n\n"
        f"SUMMARY\n{r['summary']}\n\nACTION ITEMS\n{r['action_items']}\n\n"
        f"KEY DECISIONS\n{r['key_decisions']}\n\nOPEN QUESTIONS\n{r['open_questions']}\n\n"
        f"TRANSCRIPT\n{r['transcript']}\n"
    )


with st.sidebar:
    st.markdown(
        "<div class='mm-brand'>✦ Recaply</div>"
        "<div class='mm-brand-sub'>MEETING INTELLIGENCE</div>",
        unsafe_allow_html=True,
    )
    st.divider()
    st.caption("Turn conversations into searchable intelligence.")

    if st.session_state.result:
        st.markdown(
            "<div class='mm-status'><span class='mm-dot'></span> Meeting analysed</div>",
            unsafe_allow_html=True,
        )
        st.write("")
        if st.button("＋ New meeting", use_container_width=True):
            st.session_state.result = None
            st.session_state.chat_history = []
            st.rerun()

st.markdown("""
<div class="mm-hero">
    <div class="mm-eyebrow">✦ AI MEETING INTELLIGENCE</div>
    <div class="mm-title">Every conversation.<br>One clear picture.</div>
    <div class="mm-sub">
        Turn recordings into structured intelligence — searchable transcripts,
        decisions, action items and answers, all in one workspace.
    </div>
    <div class="mm-pills">
        <span class="mm-pill">MULTILINGUAL</span>
        <span class="mm-pill">AI SUMMARIES</span>
        <span class="mm-pill">RAG Q&amp;A</span>
        <span class="mm-pill">PDF + TXT EXPORT</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="mm-section">Start a new analysis</div>', unsafe_allow_html=True)

st.markdown('<div class="mm-analysis">', unsafe_allow_html=True)

st.markdown(
    '<div class="mm-language">'
    '<span class="mm-language-label">Transcription language</span>'
    '</div>',
    unsafe_allow_html=True,
)

language = st.selectbox(
    "Language",
    ["english", "hinglish"],
    index=0,
    format_func=lambda x: "🇬🇧  English" if x == "english" else "🇮🇳  Hindi / Hinglish",
    label_visibility="collapsed",
)

st.markdown(
    '<div class="mm-language-help">'
    'English uses local Whisper. Hindi / Hinglish uses the Sarvam transcription route.'
    '</div>',
    unsafe_allow_html=True,
)

url_tab, file_tab = st.tabs(["🔗 YouTube link", "📁 Upload recording"])

with url_tab:
    url = st.text_input(
        "YouTube URL",
        placeholder="Paste a YouTube video URL...",
        label_visibility="collapsed",
    )

    if st.button("Analyse YouTube link →", use_container_width=True, key="run_url"):
        if not url.strip():
            st.warning("Paste a YouTube URL first.")
        else:
            st.session_state.result = None
            run_pipeline(url.strip(), language, "YouTube video")

with file_tab:
    uploaded = st.file_uploader(
        "Choose an audio or video file",
        type=["mp3", "wav", "m4a", "mp4", "mov", "mkv", "webm", "mpeg", "mpga"],
    )

    if uploaded:
        st.caption(f"{uploaded.name} · {uploaded.size / (1024 * 1024):.1f} MB")

    if st.button(
        "Analyse recording →",
        use_container_width=True,
        key="run_file",
        disabled=uploaded is None,
    ):
        temp_path = None
        try:
            suffix = Path(uploaded.name).suffix or ".mp4"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp:
                temp.write(uploaded.getbuffer())
                temp_path = temp.name

            st.session_state.result = None
            run_pipeline(temp_path, language, uploaded.name)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

st.markdown('</div>', unsafe_allow_html=True)

r = st.session_state.result

if r:
    st.write("")
    st.markdown('<div class="mm-section">Meeting intelligence</div>', unsafe_allow_html=True)
    st.markdown(f"### {r['title']}")
    st.caption(f"Source: {st.session_state.last_source}")

    a, b, c = st.columns(3)

    for col, label, value in [
        (a, "Transcript characters", f"{len(r['transcript']):,}"),
        (b, "Analysis modules", "5 complete"),
        (c, "Meeting Q&A", "Ready"),
    ]:
        with col:
            st.markdown(
                f"<div class='mm-card'>"
                f"<div class='mm-label'>{label}</div>"
                f"<div class='mm-value'>{value}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.write("")

    summary_tab, action_tab, decision_tab, question_tab, transcript_tab, chat_tab = st.tabs(
        [
            "✦ Summary",
            "✓ Action items",
            "◇ Decisions",
            "? Open questions",
            "≡ Transcript",
            "◎ Ask your meeting",
        ]
    )

    with summary_tab:
        st.markdown('<div class="mm-section">Executive summary</div>', unsafe_allow_html=True)
        st.markdown(r["summary"])

    with action_tab:
        st.markdown('<div class="mm-section">Action items</div>', unsafe_allow_html=True)
        st.markdown(r["action_items"])

    with decision_tab:
        st.markdown('<div class="mm-section">Key decisions</div>', unsafe_allow_html=True)
        st.markdown(r["key_decisions"])

    with question_tab:
        st.markdown('<div class="mm-section">Unresolved questions</div>', unsafe_allow_html=True)
        st.markdown(r["open_questions"])

    with transcript_tab:
        st.text_area("Full transcript", r["transcript"], height=420)
        st.download_button(
            "Download transcript (.txt)",
            r["transcript"].encode("utf-8"),
            "meetmind_transcript.txt",
            "text/plain",
        )

    with chat_tab:
        st.markdown(
            '<div class="mm-section">Ask anything about this meeting</div>',
            unsafe_allow_html=True,
        )
        st.caption(
            "Answers are grounded in the transcript indexed by your ChromaDB RAG pipeline."
        )

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        prompt = st.chat_input("What were the main decisions?")

        if prompt:
            st.session_state.chat_history.append(
                {"role": "user", "content": prompt}
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Searching your meeting..."):
                    try:
                        answer = ask_question(r["rag_chain"], prompt)
                    except Exception as exc:
                        answer = f"Unable to answer: {exc}"

                st.markdown(answer)

            st.session_state.chat_history.append(
                {"role": "assistant", "content": answer}
            )

    st.divider()
    st.markdown('<div class="mm-section">Export meeting report</div>', unsafe_allow_html=True)

    report = build_report_text(r)

    st.download_button(
        "↓ Download full report (.txt)",
        report.encode("utf-8"),
        "meetmind_meeting_report.txt",
        "text/plain",
        use_container_width=True,
    )

    try:
        from io import BytesIO
        from xml.sax.saxutils import escape
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import mm

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=18 * mm,
            rightMargin=18 * mm,
            topMargin=18 * mm,
            bottomMargin=18 * mm,
        )

        styles = getSampleStyleSheet()

        story = [
            Paragraph("Recaply — Meeting Report", styles["Title"]),
            Spacer(1, 8),
            Paragraph(escape(r["title"]), styles["Heading2"]),
        ]

        for heading, key in [
            ("Summary", "summary"),
            ("Action Items", "action_items"),
            ("Key Decisions", "key_decisions"),
            ("Open Questions", "open_questions"),
            ("Transcript", "transcript"),
        ]:
            story.extend(
                [
                    Spacer(1, 10),
                    Paragraph(heading, styles["Heading2"]),
                    Paragraph(
                        escape(str(r[key])).replace("\n", "<br/>"),
                        styles["BodyText"],
                    ),
                ]
            )

        doc.build(story)

        st.download_button(
            "↓ Download full report (.pdf)",
            buffer.getvalue(),
            "meetmind_meeting_report.pdf",
            "application/pdf",
            use_container_width=True,
        )

    except ImportError:
        st.info("To enable PDF export, run: python -m pip install reportlab")

else:
    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown(
            """
            <div class="mm-card" style="text-align:center;padding:2.4rem 1.4rem;margin-top:2rem">
                <div style="font-size:2.4rem">✦</div>
                <div style="font:600 1.3rem Space Grotesk,sans-serif;color:#f3f5ff">
                    Your next meeting starts here
                </div>
                <p style="color:#8997b2;line-height:1.7">
                    Add a YouTube link or upload a recording to generate searchable notes,
                    clear decisions and practical next steps.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
