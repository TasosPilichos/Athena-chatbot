import streamlit as st
import anthropic

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Athena Chat", page_icon="🦉", layout="centered")

# ── Hidden system instruction ─────────────────────────────────────────────────
SYSTEM_PROMPT = """You are a knowledgeable, patient, and encouraging teacher. Your role is to guide learners of all levels with clarity, warmth, and genuine enthusiasm for their growth.

Tone & Style:
- Be encouraging and positive — celebrate effort, not just correct answers.
- Use clear, accessible language, and adapt your explanations to the learner's level.
- Ask thoughtful follow-up questions to deepen understanding rather than just providing answers.

Ethical Guidelines:
- Always provide honest, accurate information. If you're unsure about something, say so openly.
- Never shame or belittle a learner for mistakes — treat errors as learning opportunities.
- Avoid sharing harmful, misleading, or inappropriate content under any circumstances.
- Respect the learner's autonomy; guide them toward their own conclusions rather than imposing your views.

Teaching Approach:
- Break down complex topics into manageable steps.
- Use examples, analogies, and real-world connections to make concepts stick.
- Encourage curiosity — remind learners that questions are a sign of engagement, not weakness.
- When a learner is struggling, offer alternative explanations rather than repeating the same one."""

# ── Athena SVG — Lilo & Stitch cartoon aesthetic ─────────────────────────────
# Big expressive eyes, rounded chunky shapes, warm colours, playful proportions
ATHENA_SVG_LARGE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 140 180" width="130" height="165">
  <!-- Soft glow halo -->
  <circle cx="70" cy="72" r="55" fill="#5b9bd5" opacity="0.18"/>

  <!-- Helmet — chunky & rounded like Lilo's hair bows -->
  <ellipse cx="70" cy="44" rx="36" ry="13" fill="#d4a017"/>
  <path d="M34 44 Q33 12 70 9 Q107 12 106 44 Z" fill="#f0c040"/>
  <!-- Helmet shine -->
  <ellipse cx="58" cy="22" rx="10" ry="5" fill="white" opacity="0.25" transform="rotate(-20,58,22)"/>
  <!-- Helmet ridge -->
  <rect x="65" y="7" width="10" height="20" rx="5" fill="#d4a017"/>
  <!-- Big fluffy plume — Lilo-style rounded -->
  <ellipse cx="70" cy="5" rx="9" ry="14" fill="#ff6b6b"/>
  <ellipse cx="70" cy="3" rx="6" ry="9" fill="#ff8e8e"/>

  <!-- Cheek guards — rounded -->
  <path d="M36 48 Q26 64 32 80 Q38 68 40 56 Z" fill="#f0c040"/>
  <path d="M104 48 Q114 64 108 80 Q102 68 100 56 Z" fill="#f0c040"/>

  <!-- Face — big round Lilo-style head -->
  <ellipse cx="70" cy="74" rx="30" ry="32" fill="#fde7c0"/>
  <!-- Rosy cheeks — big & cartoonish -->
  <ellipse cx="48" cy="82" rx="10" ry="7" fill="#ffb3a0" opacity="0.6"/>
  <ellipse cx="92" cy="82" rx="10" ry="7" fill="#ffb3a0" opacity="0.6"/>

  <!-- BIG expressive eyes — Lilo & Stitch signature -->
  <!-- Eye whites — large oval -->
  <ellipse cx="58" cy="70" rx="10" ry="11" fill="white"/>
  <ellipse cx="82" cy="70" rx="10" ry="11" fill="white"/>
  <!-- Iris — big & colourful -->
  <circle cx="59" cy="71" r="7.5" fill="#4a90d9"/>
  <circle cx="83" cy="71" r="7.5" fill="#4a90d9"/>
  <!-- Pupil -->
  <circle cx="60" cy="72" r="4.5" fill="#1a1a2e"/>
  <circle cx="84" cy="72" r="4.5" fill="#1a1a2e"/>
  <!-- Big eye shine — Lilo style -->
  <circle cx="63" cy="68" r="2.5" fill="white"/>
  <circle cx="87" cy="68" r="2.5" fill="white"/>
  <circle cx="57" cy="74" r="1.2" fill="white" opacity="0.7"/>
  <circle cx="81" cy="74" r="1.2" fill="white" opacity="0.7"/>
  <!-- Eyelashes — thick & expressive -->
  <path d="M50 63 Q54 59 58 62" stroke="#3a2800" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M66 62 Q70 59 74 63" stroke="#3a2800" stroke-width="2.5" fill="none" stroke-linecap="round"/>

  <!-- Eyebrows — thick expressive Lilo brows -->
  <path d="M49 60 Q58 55 67 59" stroke="#5a3a10" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M73 59 Q82 55 91 60" stroke="#5a3a10" stroke-width="3" fill="none" stroke-linecap="round"/>

  <!-- Cute button nose -->
  <ellipse cx="70" cy="80" rx="4" ry="3" fill="#f0b090" opacity="0.7"/>
  <circle cx="68" cy="80" r="1.2" fill="#d4886a" opacity="0.5"/>
  <circle cx="72" cy="80" r="1.2" fill="#d4886a" opacity="0.5"/>

  <!-- Big happy Lilo-style smile -->
  <path d="M55 90 Q70 103 85 90" stroke="#d4786a" stroke-width="3" fill="none" stroke-linecap="round"/>
  <!-- Teeth hint -->
  <path d="M59 91 Q70 100 81 91" fill="white" opacity="0.6"/>

  <!-- Body — chunky rounded Lilo-style robe -->
  <path d="M40 104 Q28 122 24 155 Q42 148 70 149 Q98 148 116 155 Q112 122 100 104 Q86 115 70 116 Q54 115 40 104Z" fill="#3a8fd4"/>
  <!-- Robe folds -->
  <path d="M55 110 Q52 130 50 149" stroke="#5aaae8" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M70 116 L68 149" stroke="#5aaae8" stroke-width="2" fill="none" opacity="0.5"/>
  <path d="M85 110 Q88 130 90 149" stroke="#5aaae8" stroke-width="2" fill="none" opacity="0.5"/>
  <!-- Gold neckline with pattern -->
  <path d="M48 104 Q70 118 92 104" stroke="#f0c040" stroke-width="3.5" fill="none"/>
  <path d="M52 107 Q70 120 88 107" stroke="#f8d860" stroke-width="1.5" fill="none" opacity="0.5"/>

  <!-- Cute owl — Lilo & Stitch big-eyed style -->
  <ellipse cx="107" cy="118" rx="13" ry="15" fill="#8b6914"/>
  <ellipse cx="107" cy="110" rx="11" ry="9" fill="#b08a28"/>
  <!-- Owl face -->
  <circle cx="103" cy="109" r="5" fill="white"/>
  <circle cx="111" cy="109" r="5" fill="white"/>
  <circle cx="103" cy="109" r="3.5" fill="#2a1800"/>
  <circle cx="111" cy="109" r="3.5" fill="#2a1800"/>
  <circle cx="104.5" cy="107.5" r="1.5" fill="white"/>
  <circle cx="112.5" cy="107.5" r="1.5" fill="white"/>
  <!-- Owl beak -->
  <path d="M105 113 L107 116 L109 113" fill="#d4a020"/>
  <!-- Owl ear tufts -->
  <path d="M98 104 Q100 98 103 103" fill="#8b6914"/>
  <path d="M116 104 Q114 98 111 103" fill="#8b6914"/>

  <!-- Shield — chunky cartoon style -->
  <ellipse cx="31" cy="128" rx="11" ry="14" fill="#d4a017"/>
  <ellipse cx="31" cy="128" rx="8" ry="11" fill="#f0c040"/>
  <circle cx="31" cy="128" r="4" fill="#d4a017"/>
  <path d="M28 124 L34 132 M34 124 L28 132" stroke="#a07010" stroke-width="1.8"/>

  <!-- Sparkles — Lilo style star doodles -->
  <text x="6" y="35" font-size="14" fill="#f0c040" opacity="0.8">✦</text>
  <text x="118" y="50" font-size="11" fill="#7ec8e3" opacity="0.8">✦</text>
  <text x="4" y="95" font-size="8" fill="#f0c040" opacity="0.5">✦</text>
  <text x="122" y="100" font-size="8" fill="#ff8e8e" opacity="0.6">✦</text>
</svg>"""

# Small version for chat avatar (32x32 viewbox crop of face only)
ATHENA_SVG_SMALL = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="20 40 100 100" width="36" height="36">
  <circle cx="70" cy="72" r="55" fill="#5b9bd5" opacity="0.18"/>
  <ellipse cx="70" cy="44" rx="36" ry="13" fill="#d4a017"/>
  <path d="M34 44 Q33 12 70 9 Q107 12 106 44 Z" fill="#f0c040"/>
  <rect x="65" y="7" width="10" height="20" rx="5" fill="#d4a017"/>
  <ellipse cx="70" cy="5" rx="9" ry="14" fill="#ff6b6b"/>
  <path d="M36 48 Q26 64 32 80 Q38 68 40 56 Z" fill="#f0c040"/>
  <path d="M104 48 Q114 64 108 80 Q102 68 100 56 Z" fill="#f0c040"/>
  <ellipse cx="70" cy="74" rx="30" ry="32" fill="#fde7c0"/>
  <ellipse cx="48" cy="82" rx="10" ry="7" fill="#ffb3a0" opacity="0.6"/>
  <ellipse cx="92" cy="82" rx="10" ry="7" fill="#ffb3a0" opacity="0.6"/>
  <ellipse cx="58" cy="70" rx="10" ry="11" fill="white"/>
  <ellipse cx="82" cy="70" rx="10" ry="11" fill="white"/>
  <circle cx="59" cy="71" r="7.5" fill="#4a90d9"/>
  <circle cx="83" cy="71" r="7.5" fill="#4a90d9"/>
  <circle cx="60" cy="72" r="4.5" fill="#1a1a2e"/>
  <circle cx="84" cy="72" r="4.5" fill="#1a1a2e"/>
  <circle cx="63" cy="68" r="2.5" fill="white"/>
  <circle cx="87" cy="68" r="2.5" fill="white"/>
  <path d="M49 60 Q58 55 67 59" stroke="#5a3a10" stroke-width="3" fill="none" stroke-linecap="round"/>
  <path d="M73 59 Q82 55 91 60" stroke="#5a3a10" stroke-width="3" fill="none" stroke-linecap="round"/>
  <ellipse cx="70" cy="80" rx="4" ry="3" fill="#f0b090" opacity="0.7"/>
  <path d="M55 90 Q70 103 85 90" stroke="#d4786a" stroke-width="3" fill="none" stroke-linecap="round"/>
</svg>"""

# Encode small SVG for use as chat avatar image src
import base64
ATHENA_AVATAR_B64 = "data:image/svg+xml;base64," + base64.b64encode(ATHENA_SVG_SMALL.encode()).decode()

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Cinzel:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Lora', serif; }

.stApp {
    background: linear-gradient(135deg, #0a1628, #0d2744, #0f3460);
    min-height: 100vh;
}

section[data-testid="stSidebar"] {
    background: rgba(10, 30, 60, 0.8) !important;
    border-right: 1px solid rgba(100, 180, 255, 0.15);
}
section[data-testid="stSidebar"] * { color: #d0e8f8 !important; }

div[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(100, 180, 255, 0.15) !important;
    border-radius: 14px !important;
    margin-bottom: 8px;
    color: #e8f4fd !important;
}

/* Black text in chat input */
div[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    border: 1px solid rgba(100, 180, 255, 0.4) !important;
    border-radius: 12px !important;
    color: #000000 !important;
    font-family: 'Lora', serif !important;
}
div[data-testid="stChatInput"] textarea::placeholder {
    color: #666666 !important;
}

h1, h2, h3 { color: #e8f4fd !important; }
p, label, .stMarkdown { color: #b8d8f0 !important; }

.stButton > button {
    background: linear-gradient(135deg, #1a6fa8, #0d4d7a) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Lora', serif !important;
    font-weight: 600 !important;
    padding: 0.4rem 1.2rem !important;
}
.stButton > button:hover { opacity: 0.85; }

/* Sticky header so Athena is always visible */
.sticky-header {
    position: sticky;
    top: 0;
    z-index: 999;
    background: linear-gradient(135deg, #0a1628ee, #0d2744ee, #0f3460ee);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(100,180,255,0.15);
    padding: 10px 0 8px 0;
    text-align: center;
}

/* Override default Streamlit assistant avatar with Athena */
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
    background: transparent !important;
    border: none !important;
}
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] svg {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ── API Key ───────────────────────────────────────────────────────────────────
try:
    api_key = st.secrets["ANTHROPIC_API_KEY"]
    key_source = "secret"
except Exception:
    api_key = None
    key_source = "sidebar"

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        f'<div style="text-align:center; padding:10px 0;">{ATHENA_SVG_LARGE}</div>',
        unsafe_allow_html=True
    )
    st.markdown("---")

    st.markdown("🔑 **Powered by Claude AI**")
    st.markdown("---")

    st.markdown("### 🎓 Teaching Assistant")
    st.markdown("*Athena guides you with patience, clarity, and wisdom.*")
    st.markdown("---")
    st.markdown(f"**Messages:** {len(st.session_state.messages)}")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# ── Sticky header — always visible while scrolling ───────────────────────────
st.markdown(f"""
<div class="sticky-header">
    <div style="display:inline-block; vertical-align:middle; margin-right:12px;">
        {ATHENA_SVG_SMALL}
    </div>
    <span style="font-family:Cinzel,serif; font-size:1.6rem; font-weight:600;
        color:#e8c55a; letter-spacing:3px; vertical-align:middle;
        text-shadow:0 0 20px rgba(232,197,90,0.4);">ATHENA</span>
    <div style="color:#7ec8e3; font-style:italic; font-size:0.85rem; margin-top:2px;">
        Your Personal Teaching Assistant
    </div>
</div>
""", unsafe_allow_html=True)

# ── Welcome intro (shown once, above chat) ────────────────────────────────────
if not st.session_state.messages:
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown(
            f'<div style="text-align:center; padding: 20px 0 10px 0;">{ATHENA_SVG_LARGE}</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<p style="text-align:center; color:#a8d8f0; font-size:0.95rem; '
            'line-height:1.7; padding: 0 10px;">'
            'Hello! I am Athena — goddess of wisdom and your guide on this learning journey. '
            'Whether you have a burning question, a tricky concept, or just curious about the world, '
            'I am here to help you discover, understand, and grow. Ask me anything! 🦉</p>',
            unsafe_allow_html=True
        )
        st.markdown(
            '<hr style="border:none; height:1px; background:linear-gradient(90deg,transparent,#e8c55a,transparent); margin:12px 0;">',
            unsafe_allow_html=True
        )

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        with st.chat_message("assistant", avatar=ATHENA_AVATAR_B64):
            st.markdown(msg["content"])
    else:
        with st.chat_message("user"):
            st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask Athena anything…"):
    if not api_key:
        st.error("⚠️ API key not configured. Please contact the administrator.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=ATHENA_AVATAR_B64):
        with st.spinner("Athena is thinking…"):
            try:
                client = anthropic.Anthropic(api_key=api_key)
                history = [
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages[:-1]
                ]
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=history + [{"role": "user", "content": prompt}],
                )
                reply = response.content[0].text
            except Exception as e:
                reply = f"⚠️ Error: {str(e)}"

        st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
