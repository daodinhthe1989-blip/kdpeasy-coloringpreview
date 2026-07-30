import io
import hashlib
import random
import requests
from PIL import Image
import streamlit as st
import replicate

# ═══════════════════════════════════════════════════════════════════
# 🔐 SECURITY SETTINGS — Edit these values to customize your app
# ═══════════════════════════════════════════════════════════════════
APP_PASSWORD = "KDPCOLOR2026"
BRAND_NAME = "KDPEasy Studio"
WELCOME_MESSAGE = "Welcome, VIP Customer!"
# ═══════════════════════════════════════════════════════════════════

AI_MODEL = "black-forest-labs/flux-kontext-pro"

COLOR_PRESETS = {
    "🌸 Pastel Dream": (
        "Colorize this black and white coloring book line art page with soft "
        "pastel colors (light pink, mint green, baby blue, lavender, soft "
        "yellow). Keep all black outlines crisp, clean, and completely "
        "unchanged. Gentle, soft shading, no gradients that obscure the "
        "linework."
    ),
    "🌈 Vibrant & Bold": (
        "Colorize this black and white coloring book line art page with "
        "vivid, highly saturated colors. Keep all black outlines crisp, "
        "clean, and completely unchanged. Bright, eye-catching, poster-like "
        "color palette."
    ),
    "🍂 Autumn Warmth": (
        "Colorize this black and white coloring book line art page with "
        "warm autumn tones: burnt orange, deep red, mustard yellow, and "
        "brown. Keep all black outlines crisp, clean, and completely "
        "unchanged."
    ),
    "🎨 Watercolor Wash": (
        "Colorize this black and white coloring book line art page in a "
        "soft watercolor painting style with gentle color bleeds and light "
        "washes. Keep the black outlines visible underneath the color. "
        "Muted, artistic color palette."
    ),
    "🌊 Ocean Cool": (
        "Colorize this black and white coloring book line art page with "
        "cool ocean tones: teal, aqua, deep blue, and seafoam green. Keep "
        "all black outlines crisp, clean, and completely unchanged."
    ),
    "🌺 Tropical Pop": (
        "Colorize this black and white coloring book line art page with "
        "bright tropical colors: hot pink, sunny orange, lime green, and "
        "turquoise. Keep all black outlines crisp, clean, and completely "
        "unchanged. Playful, energetic palette."
    ),
    "🍬 Candy Kids": (
        "Colorize this black and white coloring book line art page with "
        "cheerful, candy-bright primary and secondary colors, ideal for a "
        "children's book. Keep all black outlines crisp, clean, and "
        "completely unchanged. Simple, flat, bold color fills."
    ),
    "🌙 Midnight Fantasy": (
        "Colorize this black and white coloring book line art page with "
        "deep magical tones: midnight blue, violet, and touches of silver "
        "or gold. Keep all black outlines crisp, clean, and completely "
        "unchanged. Dreamy, fantasy-inspired palette."
    ),
    "🎄 Holiday Cheer": (
        "Colorize this black and white coloring book line art page with "
        "classic holiday colors: red, deep green, and gold. Keep all black "
        "outlines crisp, clean, and completely unchanged."
    ),
    "🌻 Sunny Meadow": (
        "Colorize this black and white coloring book line art page with "
        "warm, sunny colors: golden yellow, fresh green, and sky blue. "
        "Keep all black outlines crisp, clean, and completely unchanged. "
        "Bright, cheerful spring/summer palette."
    ),
    "✏️ Custom (write your own)": None,
}

st.set_page_config(
    page_title="KDPEasy Coloring Preview",
    page_icon="🎨",
    layout="wide",
)

CUSTOM_CSS = """
<style>
    .main > div { padding-top: 2rem; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf3 100%); }
    .block-container { max-width: 1200px; }
    h1 { color: #1f2937; font-weight: 700; }
    .stButton>button {
        background-color: #4f46e5;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #4338ca; color: white; }
    .stDownloadButton>button {
        background-color: #10b981;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }
    .stDownloadButton>button:hover { background-color: #059669; color: white; }
    div[data-testid="stFileUploader"] {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        border: 2px dashed #cbd5e1;
    }
    .info-card {
        background: white;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        border-left: 4px solid #4f46e5;
        margin-bottom: 1rem;
    }
    .login-card {
        background: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        max-width: 480px;
        margin: 3rem auto;
        text-align: center;
    }
    .login-card h2 { color: #1f2937; margin-bottom: 0.5rem; }
    .login-card .brand { color: #4f46e5; font-weight: 700; font-size: 1.1rem; margin-bottom: 1.5rem; }
    .login-card .desc { color: #64748b; font-size: 0.95rem; margin-bottom: 1.5rem; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# 🔐 PASSWORD GATE
# ═══════════════════════════════════════════════════════════════════
def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.markdown(
        f"""
        <div class='login-card'>
            <h2>🔐 {WELCOME_MESSAGE}</h2>
            <div class='brand'>✨ {BRAND_NAME} ✨</div>
            <div class='desc'>
                This is an exclusive tool for our valued customers.<br>
                Please enter your access password to continue.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        password = st.text_input(
            "🔑 Access Password",
            type="password",
            placeholder="Enter your password here...",
            key="password_input",
        )
        if st.button("🚀 Unlock App", width="stretch"):
            if password == APP_PASSWORD:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("❌ Incorrect password. Please contact support if you need access.")

        st.markdown(
            "<p style='text-align:center;color:#94a3b8;font-size:0.85rem;margin-top:2rem;'>"
            "💡 Don't have a password? This tool is exclusive to our email subscribers.<br>"
            "Contact us to get access."
            "</p>",
            unsafe_allow_html=True,
        )
    return False


if not check_password():
    st.stop()


# ═══════════════════════════════════════════════════════════════════
# 🎨 CORE LOGIC
# ═══════════════════════════════════════════════════════════════════
def get_image_hash(img_bytes: bytes, suffix: str = "") -> str:
    return hashlib.md5(img_bytes + suffix.encode()).hexdigest()


def colorize_image(image_bytes: bytes, prompt: str, seed: int | None = None) -> bytes:
    """Colorize a line art image using FLUX.1 Kontext via Replicate API."""
    api_token = st.secrets.get("REPLICATE_API_TOKEN", None)
    if not api_token:
        raise ValueError("AI service is not configured. Please contact support.")

    client = replicate.Client(api_token=api_token)

    input_params = {
        "prompt": prompt,
        "input_image": io.BytesIO(image_bytes),
        "aspect_ratio": "match_input_image",
        "output_format": "png",
    }
    if seed is not None:
        input_params["seed"] = seed

    output = client.run(AI_MODEL, input=input_params)

    if isinstance(output, list):
        output = output[0]

    if hasattr(output, "read"):
        return output.read()

    response = requests.get(str(output), timeout=120)
    response.raise_for_status()
    return response.content


def run_colorize(image_bytes: bytes, prompt: str, filename: str, force_new: bool = False):
    """Colorize an image, using the cache unless force_new is True."""
    cache_key = get_image_hash(image_bytes, prompt)
    if "colorize_cache" not in st.session_state:
        st.session_state["colorize_cache"] = {}

    if not force_new and cache_key in st.session_state["colorize_cache"]:
        result_bytes = st.session_state["colorize_cache"][cache_key]
        st.info("✨ Using a previously generated result (cached)")
    else:
        try:
            with st.spinner("🎨 AI is coloring your page... this may take 10-20 seconds."):
                seed = random.randint(1, 2_000_000_000) if force_new else None
                result_bytes = colorize_image(image_bytes, prompt, seed=seed)
                st.session_state["colorize_cache"][cache_key] = result_bytes
        except Exception as e:
            st.error(
                f"❌ Coloring failed. Please try again or contact support.  \n"
                f"Error: {str(e)[:200]}"
            )
            st.stop()

    st.session_state["colorized"] = {
        "buf": result_bytes,
        "name": filename.rsplit(".", 1)[0],
    }
    st.success(
        "✅ Done! Your colored preview is ready below. Want to preview this "
        "image in another color style? Your current preview will be "
        "replaced, so download it first if you want to keep it."
    )


# ═══════════════════════════════════════════════════════════════════
# 🎨 MAIN APP
# ═══════════════════════════════════════════════════════════════════
header_col1, header_col2 = st.columns([5, 1])
with header_col1:
    st.title("🎨 KDPEasy Coloring Preview")
with header_col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔒 Logout", width="stretch"):
        st.session_state["password_correct"] = False
        if "colorized" in st.session_state:
            del st.session_state["colorized"]
        st.rerun()

st.markdown(
    f"<p style='color:#64748b;font-size:1.05rem;'>"
    f"Turn a black &amp; white coloring page into an eye-catching colored "
    f"preview — perfect for Etsy, Amazon, and social media listings.<br>"
    f"<span style='color:#4f46e5;font-weight:600;'>✨ Exclusive tool by {BRAND_NAME}</span>"
    f"</p>",
    unsafe_allow_html=True,
)
st.markdown("---")

uploaded_file = st.file_uploader(
    "Upload a coloring page (JPG or PNG)",
    type=["jpg", "jpeg", "png"],
    help="Upload a single black & white line art page to colorize.",
)

if uploaded_file is None:
    st.markdown(
        "<div class='info-card'>"
        "<b>Why use this?</b><br>"
        "Marketplace listings sell better with a colored preview image next "
        "to the blank line art — but hand-coloring a sample page takes time "
        "or design skill you may not have.<br><br>"
        "<b>How it works</b><br>"
        "1. Upload a black &amp; white coloring page<br>"
        "2. Pick a color style (or write your own)<br>"
        "3. Preview the colorized result<br>"
        "4. Download it for your listing or social posts"
        "</div>",
        unsafe_allow_html=True,
    )
else:
    original_bytes = uploaded_file.getvalue()
    image = Image.open(uploaded_file)

    col_left, col_right = st.columns([1, 1], gap="large")

    with col_left:
        st.subheader("📷 Original")
        st.image(image, width="stretch")

    with col_right:
        st.subheader("⚙️ Color Style")

        style_label = st.selectbox(
            "Choose a color style",
            options=list(COLOR_PRESETS.keys()),
            index=0,
            label_visibility="collapsed",
        )

        prompt = COLOR_PRESETS[style_label]
        if prompt is None:
            prompt = st.text_area(
                "Describe how you'd like it colored",
                placeholder=(
                    "e.g. Colorize with bright rainbow colors, keep the "
                    "black outlines crisp"
                ),
                height=100,
            )

        st.markdown("")

        if st.button("✨ Colorize This Page", width="stretch"):
            if not prompt or not prompt.strip():
                st.error("Please choose a style or describe how you'd like it colored.")
            else:
                run_colorize(original_bytes, prompt, uploaded_file.name, force_new=False)

        if "colorized" in st.session_state:
            if st.button("🔄 Generate a New Variation", width="stretch"):
                if not prompt or not prompt.strip():
                    st.error("Please choose a style or describe how you'd like it colored.")
                else:
                    run_colorize(original_bytes, prompt, uploaded_file.name, force_new=True)

if "colorized" in st.session_state:
    st.markdown("---")
    st.subheader("✅ Colorized Preview")

    conv = st.session_state["colorized"]
    col_a, col_b = st.columns([1, 1], gap="large")
    with col_a:
        st.image(conv["buf"], caption="Colorized Result", width="stretch")
    with col_b:
        st.markdown(
            "<div class='info-card'>"
            "Great for:<br>"
            "• Etsy / Amazon listing thumbnails<br>"
            "• Pinterest &amp; Instagram posts<br>"
            "• Book cover mockups"
            "</div>",
            unsafe_allow_html=True,
        )
        st.download_button(
            "⬇️ Download Colorized Image",
            data=conv["buf"],
            file_name=f"{conv['name']}_colorized.png",
            mime="image/png",
            width="stretch",
        )

st.markdown("---")
st.markdown(
    f"<p style='text-align:center;color:#94a3b8;font-size:0.85rem;'>"
    f"✨ Exclusive tool by <b>{BRAND_NAME}</b> • Made for self-publishers"
    f"</p>",
    unsafe_allow_html=True,
)
