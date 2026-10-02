import streamlit as st
import pandas as pd
import pickle


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ChurnAI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOAD MODEL  (unchanged)
# ============================================================

@st.cache_resource
def load_model():

    with open("churn_stacking_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("churn_threshold.pkl", "rb") as f:
        threshold = pickle.load(f)

    return model, threshold


model, threshold = load_model()
threshold = float(threshold)


# ============================================================
# CUSTOM CSS  (Apple-style glossy glass, dark)
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --blue: #0a84ff;
        --green: #30d158;
        --red: #ff453a;
        --amber: #ff9f0a;
        --text: #f5f5f7;
        --muted: #98a1b3;
        --glass: linear-gradient(180deg, rgba(255,255,255,0.075), rgba(255,255,255,0.028));
        --glass-border: rgba(255,255,255,0.10);
        --gloss: inset 0 1px 0 rgba(255,255,255,0.16);
    }
    
    /* ---------- base ---------- */
    html, body, .stApp, button, input, select, textarea {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Segoe UI", sans-serif !important;
    }

    .stApp {
        color: var(--text);
        background:
            radial-gradient(900px 600px at 8% -5%, rgba(10,132,255,0.22), transparent 60%),
            radial-gradient(800px 600px at 100% 10%, rgba(191,90,242,0.17), transparent 60%),
            radial-gradient(900px 700px at 50% 110%, rgba(48,209,88,0.09), transparent 60%),
            #05070c;
        background-attachment: fixed;
    }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    .block-container {
        max-width: 1280px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* ---------- hero ---------- */
    .hero {
        display: flex;
        align-items: center;
        gap: 20px;
        padding: 26px 30px;
        margin-bottom: 22px;
        border-radius: 26px;
        background: var(--glass);
        border: 1px solid var(--glass-border);
        box-shadow: var(--gloss), 0 24px 60px rgba(0,0,0,0.45);
        backdrop-filter: blur(28px);
        position: relative;
        overflow: hidden;
    }
    .hero::after {
        content: "";
        position: absolute;
        inset: 0 0 55% 0;
        background: linear-gradient(180deg, rgba(255,255,255,0.07), transparent);
        pointer-events: none;
    }
    .logo {
        width: 62px; height: 62px;
        border-radius: 17px;
        display: grid; place-items: center;
        font-size: 28px; font-weight: 800; color: #fff;
        background: linear-gradient(160deg, #5ac8fa 0%, #0a84ff 45%, #5e5ce6 100%);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.5), 0 10px 28px rgba(10,132,255,0.45);
        flex-shrink: 0;
    }
    .hero-title {
        font-size: 34px; font-weight: 800; letter-spacing: -1px;
        color: #fff; line-height: 1.05; margin: 0;
    }
    .hero-sub { color: var(--muted); font-size: 15px; margin-top: 6px; }
    .chips { margin-left: auto; display: flex; gap: 8px; flex-wrap: wrap; justify-content: flex-end; }
    .chip {
        padding: 7px 13px; border-radius: 999px; font-size: 12.5px; font-weight: 600;
        color: #d7dbe5; background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.10); box-shadow: var(--gloss);
        white-space: nowrap;
    }
    .chip.live { color: #7ff0a0; background: rgba(48,209,88,0.12); border-color: rgba(48,209,88,0.30); }
    .dot {
        display: inline-block; width: 7px; height: 7px; border-radius: 50%;
        background: var(--green); margin-right: 7px;
        box-shadow: 0 0 0 0 rgba(48,209,88,0.7);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(48,209,88,0.6); }
        70% { box-shadow: 0 0 0 8px rgba(48,209,88,0); }
        100% { box-shadow: 0 0 0 0 rgba(48,209,88,0); }
    }

    .presets-label { color: var(--muted); font-size: 13px; margin: 0 0 8px 4px; }

    /* ---------- tabs ---------- */
    div[data-baseweb="tab-list"] {
        gap: 6px; padding: 5px; width: fit-content;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 15px;
    }
    div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none; }
    button[data-baseweb="tab"] {
        height: 38px; padding: 0 20px; border-radius: 11px;
        background: transparent; color: var(--muted); font-weight: 600;
        transition: all 0.2s ease;
    }
    button[data-baseweb="tab"] p { font-size: 14px; font-weight: 600; color: inherit; }
    button[data-baseweb="tab"]:hover { color: #fff; }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #fff;
        background: linear-gradient(180deg, rgba(255,255,255,0.20), rgba(255,255,255,0.08));
        box-shadow: var(--gloss), 0 4px 14px rgba(0,0,0,0.3);
    }
    div[data-baseweb="tab-panel"] {
        margin-top: 14px;
        padding: 26px 26px 14px 26px;
        border-radius: 24px;
        background: var(--glass);
        border: 1px solid var(--glass-border);
        box-shadow: var(--gloss), 0 24px 60px rgba(0,0,0,0.40);
        backdrop-filter: blur(24px);
    }

    /* ---------- widget labels ---------- */
    div[data-testid="stWidgetLabel"] p, label {
        color: #aab3c5 !important;
        font-size: 13px !important;
        font-weight: 500 !important;
    }

    /* ---------- select ---------- */
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 13px !important;
        min-height: 44px;
        color: #fff !important;
        box-shadow: var(--gloss);
        transition: border-color 0.2s, background 0.2s;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: rgba(10,132,255,0.7) !important;
        background: rgba(255,255,255,0.09) !important;
    }
    div[data-baseweb="select"] span { color: #fff !important; }
    div[data-baseweb="select"] svg { fill: #98a1b3 !important; }

    div[data-baseweb="popover"] ul, div[role="listbox"] {
        background: rgba(24,28,38,0.96) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(24px);
    }
    li[role="option"], div[role="option"] { background: transparent !important; color: #fff !important; }
    li[role="option"]:hover, div[role="option"]:hover,
    li[role="option"][aria-selected="true"] { background: rgba(10,132,255,0.28) !important; }

    /* ---------- number input ---------- */
    div[data-baseweb="input"], div[data-baseweb="base-input"] {
        background: rgba(255,255,255,0.06) !important;
        border-radius: 13px !important;
    }
    div[data-baseweb="input"] {
        border: 1px solid rgba(255,255,255,0.12) !important;
        box-shadow: var(--gloss);
        min-height: 44px;
        transition: border-color 0.2s;
    }
    div[data-baseweb="input"]:focus-within { border-color: var(--blue) !important; }
    div[data-baseweb="input"] input { color: #fff !important; background: transparent !important; }
    .stNumberInput button { background: transparent !important; color: #98a1b3 !important; }
    .stNumberInput button:hover { color: #fff !important; background: rgba(255,255,255,0.08) !important; }

    /* ---------- buttons ---------- */
    .stButton > button, button[kind], button[data-testid^="stBaseButton"] {
        border-radius: 13px;
        font-weight: 650;
        transition: transform 0.15s ease, box-shadow 0.2s ease, background 0.2s ease;
    }

    /* primary: glossy Apple blue */
    button[kind="primary"], button[data-testid="stBaseButton-primary"] {
        width: 100%;
        height: 54px;
        border: none !important;
        color: #fff !important;
        font-size: 16px;
        background: linear-gradient(180deg, #4fb0ff 0%, #0a84ff 50%, #0071e3 100%) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.45), 0 10px 28px rgba(10,132,255,0.38) !important;
    }
    button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {
        transform: translateY(-1px);
        filter: brightness(1.08);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.5), 0 14px 34px rgba(10,132,255,0.5) !important;
    }
    button[kind="primary"]:active, button[data-testid="stBaseButton-primary"]:active { transform: scale(0.985); }
    button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p { color: #fff !important; font-size: 16px; font-weight: 700; }

    /* secondary: glass pills (presets) */
    button[kind="secondary"], button[data-testid="stBaseButton-secondary"] {
        height: 42px;
        color: #e6e9f0 !important;
        background: linear-gradient(180deg, rgba(255,255,255,0.10), rgba(255,255,255,0.04)) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        box-shadow: var(--gloss);
    }
    button[kind="secondary"]:hover, button[data-testid="stBaseButton-secondary"]:hover {
        border-color: rgba(10,132,255,0.65) !important;
        background: linear-gradient(180deg, rgba(10,132,255,0.28), rgba(10,132,255,0.10)) !important;
        transform: translateY(-1px);
    }
    button[kind="secondary"] p, button[data-testid="stBaseButton-secondary"] p { font-size: 13.5px; color: inherit !important; }

    /* ---------- bordered container (run panel) ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 22px !important;
        border: 1px solid var(--glass-border) !important;
        background: var(--glass);
        box-shadow: var(--gloss), 0 20px 50px rgba(0,0,0,0.35);
        backdrop-filter: blur(24px);
    }

    /* ---------- snapshot card ---------- */
    .glass {
        padding: 22px;
        margin-bottom: 16px;
        border-radius: 24px;
        background: var(--glass);
        border: 1px solid var(--glass-border);
        box-shadow: var(--gloss), 0 24px 60px rgba(0,0,0,0.40);
        backdrop-filter: blur(24px);
    }
    .glass-title { font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 14px; }
    .tiles { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .tile {
        padding: 12px 14px; border-radius: 15px;
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.07);
        box-shadow: var(--gloss);
    }
    .tile-k { font-size: 12px; color: var(--muted); }
    .tile-v { font-size: 17px; font-weight: 700; color: #fff; margin-top: 3px; letter-spacing: -0.2px; }

    /* ---------- result: the gauge ---------- */
    @property --p { syntax: '<number>'; inherits: false; initial-value: 0; }

    .result { text-align: center; padding: 26px 22px 24px 22px; }
    .ring-wrap { display: flex; justify-content: center; margin: 4px 0 18px 0; }
    .ring {
        --p: 0; --c: #3a4254; --glow: rgba(0,0,0,0);
        position: relative;
        width: 216px; height: 216px; border-radius: 50%;
        background: conic-gradient(var(--c) calc(var(--p) * 1%), rgba(255,255,255,0.08) 0);
        filter: drop-shadow(0 0 22px var(--glow));
        animation: fillRing 1.3s cubic-bezier(0.22, 1, 0.36, 1) both;
    }
    @keyframes fillRing { from { --p: 0; } }
    .ring-inner {
        position: absolute; inset: 15px; border-radius: 50%;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background: radial-gradient(circle at 50% 25%, #1b2130 0%, #0b0f18 75%);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.12), inset 0 -20px 40px rgba(0,0,0,0.4);
    }
    .ring-pct { font-size: 50px; font-weight: 800; color: #fff; letter-spacing: -2px; line-height: 1; }
    .ring-pct span { font-size: 22px; font-weight: 700; color: var(--muted); margin-left: 2px; letter-spacing: 0; }
    .ring-cap { font-size: 12.5px; color: var(--muted); margin-top: 8px; }
    .tick { position: absolute; inset: 0; }
    .tick::before {
        content: ""; position: absolute; top: -5px; left: 50%;
        width: 4px; height: 24px; margin-left: -2px; border-radius: 3px;
        background: #fff; box-shadow: 0 0 10px rgba(255,255,255,0.7);
    }

    .churn-alert {
        color: var(--red) !important; font-size: 24px; font-weight: 800; letter-spacing: -0.4px;
        animation: churnBlink 0.65s ease-in-out 3;
    }
    @keyframes churnBlink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }
    .safe-result { color: var(--green) !important; font-size: 24px; font-weight: 800; letter-spacing: -0.4px; }
    .idle-result { color: #c9cfdb; font-size: 20px; font-weight: 700; }
    .result-description { color: var(--muted); font-size: 13.5px; margin-top: 8px; line-height: 1.45; }

    .stats { display: flex; gap: 10px; margin-top: 18px; }
    .stat {
        flex: 1; padding: 10px 12px; border-radius: 14px;
        background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.07);
    }
    .stat-k { font-size: 11.5px; color: var(--muted); }
    .stat-v { font-size: 15px; font-weight: 700; color: #fff; margin-top: 2px; }

    .stale {
        display: inline-block; margin-top: 14px; padding: 6px 12px; border-radius: 999px;
        font-size: 12.5px; font-weight: 600; color: var(--amber);
        background: rgba(255,159,10,0.12); border: 1px solid rgba(255,159,10,0.30);
    }

    .app-footer { text-align: center; color: #5d6779; font-size: 12px; margin-top: 34px; }

    /* ---------- responsive + a11y ---------- */
    @media (max-width: 900px) {
        .hero { flex-wrap: wrap; }
        .chips { margin-left: 0; justify-content: flex-start; }
    }
    @media (prefers-reduced-motion: reduce) {
        .ring, .churn-alert, .dot { animation: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True
)


def card(html: str):
    """Render an HTML block (whitespace collapsed so markdown never treats it as code)."""
    st.markdown(" ".join(html.split()), unsafe_allow_html=True)


# ============================================================
# STATE: defaults + presets
# ============================================================

DEFAULTS = {
    "gender": "Female",
    "senior": "No",
    "partner": "No",
    "dependents": "No",
    "tenure": 12,
    "phone": "Yes",
    "multi": "No",
    "internet": "DSL",
    "security": "No",
    "backup": "No",
    "protection": "No",
    "techsup": "No",
    "stv": "No",
    "smovies": "No",
    "contract": "Month-to-month",
    "paperless": "Yes",
    "payment": "Electronic check",
    "monthly": 70.0,
    "total": 1000.0,
}

PRESETS = {
    "🆕 New fiber customer": {
        "tenure": 3, "internet": "Fiber optic", "contract": "Month-to-month",
        "payment": "Electronic check", "monthly": 85.0, "total": 255.0,
    },
    "🏡 Loyal two-year": {
        "tenure": 60, "contract": "Two year", "internet": "DSL",
        "security": "Yes", "backup": "Yes", "techsup": "Yes",
        "partner": "Yes", "dependents": "Yes", "paperless": "No",
        "payment": "Credit card (automatic)", "monthly": 65.0, "total": 3900.0,
    },
    "📺 Streaming heavy": {
        "tenure": 24, "internet": "Fiber optic", "stv": "Yes", "smovies": "Yes",
        "multi": "Yes", "contract": "One year",
        "payment": "Bank transfer (automatic)", "monthly": 105.0, "total": 2520.0,
    },
    "↺ Reset": {},
}

for _k, _v in DEFAULTS.items():
    st.session_state.setdefault(f"f_{_k}", _v)


def apply_preset(name: str):
    values = {**DEFAULTS, **PRESETS[name]}
    for k, v in values.items():
        st.session_state[f"f_{k}"] = v
    st.session_state.pop("last", None)


# ============================================================
# HEADER
# ============================================================

card(
    f"""
    <div class="hero">
        <div class="logo">C</div>
        <div>
            <div class="hero-title">ChurnAI</div>
            <div class="hero-sub">Customer churn analysis and prediction</div>
        </div>
        <div class="chips">
            <div class="chip live"><span class="dot"></span>Model online</div>
            <div class="chip">Logistic Regression + Random Forest stacking</div>
            <div class="chip">Decision threshold {threshold:.2f}</div>
        </div>
    </div>
    """
)


# ============================================================
# QUICK PRESETS
# ============================================================

st.markdown('<div class="presets-label">Start from a sample customer</div>', unsafe_allow_html=True)

preset_cols = st.columns(4)
for col, name in zip(preset_cols, PRESETS):
    with col:
        st.button(name, key=f"preset_{name}", on_click=apply_preset, args=(name,), use_container_width=True)

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# ============================================================
# LAYOUT: inputs (left) | snapshot + result (right)
# ============================================================

left, right = st.columns([1.7, 1], gap="large")

with left:
    tab_profile, tab_services, tab_billing = st.tabs(
        ["👤  Customer profile", "📡  Internet & services", "💳  Account & billing"]
    )

    # ---------------- PROFILE ----------------
    with tab_profile:
        c1, c2, c3 = st.columns(3)
        with c1:
            gender = st.selectbox("Gender", ["Female", "Male"], key="f_gender")
        with c2:
            senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"], key="f_senior")
        with c3:
            partner = st.selectbox("Partner", ["No", "Yes"], key="f_partner")

        c1, c2, c3 = st.columns(3)
        with c1:
            dependents = st.selectbox("Dependents", ["No", "Yes"], key="f_dependents")
        with c2:
            tenure = st.number_input(
                "Tenure (months)", min_value=0, max_value=72, step=1, key="f_tenure"
            )
        with c3:
            phone_service = st.selectbox("Phone Service", ["Yes", "No"], key="f_phone")

    # ---------------- SERVICES ----------------
    with tab_services:
        c1, c2, c3 = st.columns(3)

        # Options adapt so impossible combos (e.g. "Yes" streaming with no internet) can't be picked
        multi_opts = ["No phone service"] if phone_service == "No" else ["No", "Yes"]

        with c1:
            internet_service = st.selectbox(
                "Internet Service", ["DSL", "Fiber optic", "No"], key="f_internet"
            )

        svc_opts = ["No internet service"] if internet_service == "No" else ["No", "Yes"]

        with c1:
            multiple_lines = st.selectbox("Multiple Lines", multi_opts, key="f_multi")
            online_security = st.selectbox("Online Security", svc_opts, key="f_security")
            online_backup = st.selectbox("Online Backup", svc_opts, key="f_backup")

        with c2:
            device_protection = st.selectbox("Device Protection", svc_opts, key="f_protection")
            tech_support = st.selectbox("Tech Support", svc_opts, key="f_techsup")
            streaming_tv = st.selectbox("Streaming TV", svc_opts, key="f_stv")

        with c3:
            streaming_movies = st.selectbox("Streaming Movies", svc_opts, key="f_smovies")
            contract = st.selectbox(
                "Contract", ["Month-to-month", "One year", "Two year"], key="f_contract"
            )
            paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"], key="f_paperless")

    # ---------------- BILLING ----------------
    with tab_billing:
        c1, c2, c3 = st.columns(3)
        with c1:
            payment_method = st.selectbox(
                "Payment Method",
                [
                    "Electronic check",
                    "Mailed check",
                    "Bank transfer (automatic)",
                    "Credit card (automatic)",
                ],
                key="f_payment",
            )
        with c2:
            monthly_charges = st.number_input(
                "Monthly Charges ($)", min_value=0.0, step=0.5, key="f_monthly"
            )
        with c3:
            total_charges = st.number_input(
                "Total Charges ($)", min_value=0.0, step=10.0, key="f_total"
            )


# ============================================================
# BUILD MODEL INPUT  (exact same features / order as training)
# ============================================================

senior_citizen_value = 1 if senior_citizen == "Yes" else 0

input_data = pd.DataFrame(
    {
        "gender": [gender],
        "SeniorCitizen": [senior_citizen_value],
        "Partner": [partner],
        "Dependents": [dependents],
        "tenure": [tenure],
        "PhoneService": [phone_service],
        "MultipleLines": [multiple_lines],
        "InternetService": [internet_service],
        "OnlineSecurity": [online_security],
        "OnlineBackup": [online_backup],
        "DeviceProtection": [device_protection],
        "TechSupport": [tech_support],
        "StreamingTV": [streaming_tv],
        "StreamingMovies": [streaming_movies],
        "Contract": [contract],
        "PaperlessBilling": [paperless_billing],
        "PaymentMethod": [payment_method],
        "MonthlyCharges": [monthly_charges],
        "TotalCharges": [total_charges],
    }
)

input_signature = str(input_data.to_dict("records")[0])


# ============================================================
# RIGHT COLUMN: snapshot, controls, result
# ============================================================

with right:

    # ---------- snapshot ----------
    addons = sum(
        1 for s in (online_security, online_backup, device_protection,
                    tech_support, streaming_tv, streaming_movies)
        if s == "Yes"
    )

    card(
        f"""
        <div class="glass">
            <div class="glass-title">Customer snapshot</div>
            <div class="tiles">
                <div class="tile"><div class="tile-k">Tenure</div><div class="tile-v">{tenure} months</div></div>
                <div class="tile"><div class="tile-k">Contract</div><div class="tile-v">{contract}</div></div>
                <div class="tile"><div class="tile-k">Monthly</div><div class="tile-v">&#36;{monthly_charges:,.2f}</div></div>
                <div class="tile"><div class="tile-k">Lifetime billed</div><div class="tile-v">&#36;{total_charges:,.0f}</div></div>
                <div class="tile"><div class="tile-k">Internet</div><div class="tile-v">{internet_service}</div></div>
                <div class="tile"><div class="tile-k">Add-ons</div><div class="tile-v">{addons} of 6</div></div>
            </div>
        </div>
        """
    )

    # ---------- controls ----------
    with st.container(border=True):
        live = st.toggle("Live prediction", key="live", help="Re-run the model on every change")
        predict_button = st.button("🔍  Predict customer churn", type="primary", key="predict")

    # ---------- prediction (logic unchanged) ----------
    if predict_button or live:

        churn_probability = model.predict_proba(input_data)[0][1]

        prediction = 1 if churn_probability >= threshold else 0

        st.session_state["last"] = {
            "sig": input_signature,
            "prob": float(churn_probability),
            "pred": prediction,
        }

    last = st.session_state.get("last")

    # ---------- result ----------
    if last is None:
        card(
            """
            <div class="glass result">
                <div class="ring-wrap">
                    <div class="ring" style="--p:0;">
                        <div class="ring-inner">
                            <div class="ring-pct">–</div>
                            <div class="ring-cap">churn probability</div>
                        </div>
                    </div>
                </div>
                <div class="idle-result">Ready when you are</div>
                <div class="result-description">
                    Set the customer details, then run the prediction.
                </div>
            </div>
            """
        )
    else:
        probability_percent = last["prob"] * 100
        is_churn = last["pred"] == 1
        color = "#ff453a" if is_churn else "#30d158"
        glow = "rgba(255,69,58,0.55)" if is_churn else "rgba(48,209,88,0.45)"
        margin = probability_percent - threshold * 100
        margin_text = f"{margin:+.1f} pts"

        if is_churn:
            verdict = """
                <div class="churn-alert">⚠ Customer likely to churn</div>
                <div class="result-description">
                    The model identifies this customer as having a higher likelihood of churn.
                </div>
            """
        else:
            verdict = """
                <div class="safe-result">✓ Customer likely to stay</div>
                <div class="result-description">
                    The model identifies this customer as having a lower likelihood of churn.
                </div>
            """

        stale = (
            '<div class="stale">Inputs changed since this result. Run the prediction again.</div>'
            if last["sig"] != input_signature else ""
        )

        card(
            f"""
            <div class="glass result">
                <div class="ring-wrap">
                    <div class="ring" style="--p:{probability_percent:.1f}; --c:{color}; --glow:{glow};">
                        <div class="tick" style="transform: rotate({threshold * 360:.1f}deg);"></div>
                        <div class="ring-inner">
                            <div class="ring-pct">{probability_percent:.1f}<span>%</span></div>
                            <div class="ring-cap">churn probability</div>
                        </div>
                    </div>
                </div>
                {verdict}
                <div class="stats">
                    <div class="stat"><div class="stat-k">Threshold</div><div class="stat-v">{threshold * 100:.1f}%</div></div>
                    <div class="stat"><div class="stat-k">Vs threshold</div><div class="stat-v">{margin_text}</div></div>
                </div>
                {stale}
            </div>
            """
        )


# ============================================================
# FOOTER
# ============================================================

card(
    """
    <div class="app-footer">
        Customer Churn Prediction • Logistic Regression + Random Forest Stacking
    </div>
    """
)