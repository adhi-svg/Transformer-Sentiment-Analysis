
import streamlit as st
from transformers import pipeline

st.set_page_config(
    page_title="Sentiment Studio",
    page_icon="◒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {
        --ink: #17211f;
        --muted: #71807a;
        --paper: #f5f6f1;
        --panel: #ffffff;
        --mint: #b9e5d2;
        --coral: #f27e68;
        --line: #dce3dc;
    }

    .stApp {
        background: var(--paper);
        color: var(--ink);
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp:before {
        content: '';
        position: fixed;
        inset: 0 0 auto 0;
        height: 7px;
        background: linear-gradient(90deg, var(--coral) 0 26%, var(--mint) 26% 74%, #f1c75b 74%);
        z-index: 10;
    }

    .block-container {
        max-width: 1180px;
        padding: 4.5rem 2rem 4rem;
    }

    .brand-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 4rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: .75rem;
        font-size: .92rem;
        font-weight: 700;
        letter-spacing: .03em;
        text-transform: uppercase;
    }

    .brand-mark {
        display: grid;
        place-items: center;
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: var(--ink);
        color: var(--mint);
        font-family: 'DM Mono', monospace;
        font-size: 1.15rem;
    }

    .status {
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        font-size: .7rem;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .status-dot {
        display: inline-block;
        width: 7px;
        height: 7px;
        margin-right: .4rem;
        border-radius: 50%;
        background: #52ad78;
    }

    .eyebrow {
        margin-bottom: .8rem;
        color: var(--coral);
        font-family: 'DM Mono', monospace;
        font-size: .72rem;
        letter-spacing: .13em;
        text-transform: uppercase;
    }

    h1 {
        max-width: 700px;
        margin: 0;
        color: var(--ink);
        font-size: clamp(3.2rem, 7vw, 6.8rem);
        font-weight: 600;
        letter-spacing: -.07em;
        line-height: .92;
    }

    .intro {
        max-width: 510px;
        margin: 1.5rem 0 3.5rem;
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.6;
    }

    .compose-panel, .result-panel {
        padding: 1.5rem;
        border: 1px solid var(--line);
        background: var(--panel);
        box-shadow: 8px 8px 0 rgba(23, 33, 31, .06);
    }

    .panel-label {
        display: flex;
        justify-content: space-between;
        margin-bottom: 1rem;
        color: var(--ink);
        font-family: 'DM Mono', monospace;
        font-size: .72rem;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .panel-label span { color: var(--muted); }

    .result-panel {
        min-height: 245px;
        background: var(--ink);
        color: #fff;
        box-shadow: 8px 8px 0 var(--mint);
    }

    .result-panel .panel-label { color: var(--mint); }
    .result-panel .panel-label span { color: #91aaa1; }

    .result-value {
        margin: 2.3rem 0 .5rem;
        color: var(--mint);
        font-size: 2.35rem;
        font-weight: 600;
        letter-spacing: -.05em;
    }

    .result-confidence {
        color: #d6e0da;
        font-family: 'DM Mono', monospace;
        font-size: .8rem;
    }

    .empty-result {
        margin-top: 4.2rem;
        color: #8ea49c;
        font-family: 'DM Mono', monospace;
        font-size: .78rem;
        line-height: 1.6;
    }

    .stTextArea textarea {
        min-height: 150px;
        border: 1px solid var(--line);
        border-radius: 0;
        background: #fbfcf9;
        color: var(--ink);
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.05rem;
    }

    .stTextArea textarea:focus, .stSelectbox div[data-baseweb='select'] > div:focus-within {
        border-color: var(--coral);
        box-shadow: 0 0 0 1px var(--coral);
    }

    .stSelectbox label, .stTextArea label {
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        font-size: .7rem;
        text-transform: uppercase;
    }

    .stSelectbox div[data-baseweb='select'] > div {
        border-radius: 0;
        border-color: var(--line);
        background: #fbfcf9;
    }

    .stButton > button {
        width: 100%;
        min-height: 48px;
        border: 0;
        border-radius: 0;
        background: var(--coral);
        color: #fff;
        font-family: 'Space Grotesk', sans-serif;
        font-size: .9rem;
        font-weight: 600;
    }

    .stButton > button:hover { background: #db6856; color: #fff; }

    @media (max-width: 760px) {
        .block-container { padding: 3rem 1rem 2.5rem; }
        .brand-row { margin-bottom: 2.5rem; }
        h1 { font-size: 3.8rem; }
        .intro { margin-bottom: 2.3rem; }
        .compose-panel, .result-panel { padding: 1rem; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="brand-row">
        <div class="brand"><span class="brand-mark">◒</span> Sentiment Studio</div>
        <div class="status"><span class="status-dot"></span> Model lab / online</div>
    </div>
    <div class="eyebrow">01 / text intelligence</div>
    <h1>Read between<br>the words.</h1>
    <p class="intro">A focused workspace for translating language into feeling. Write a thought, choose a lens, and let the model find its signal.</p>
    """,
    unsafe_allow_html=True
)

MODELS = {
    "DistilBERT": "distilbert-base-uncased-finetuned-sst-2-english",
    "RoBERTa": "cardiffnlp/twitter-roberta-base-sentiment",
    "BERT": "nlptown/bert-base-multilingual-uncased-sentiment"
}

@st.cache_resource
def load_model(model_name):
    return pipeline("sentiment-analysis", model=MODELS[model_name])

def unify_label(model_name, label):
    if model_name == "DistilBERT":
        return label

    if model_name == "RoBERTa":
        return "POSITIVE" if label == "LABEL_2" else "NEGATIVE"

    if model_name == "BERT":
        return "POSITIVE" if label in ["4 stars", "5 stars"] else "NEGATIVE"

sentence = st.text_area("Enter a sentence:")

model_choice = st.selectbox(
    "Choose a model:",
    ["DistilBERT", "RoBERTa", "BERT"]
)

if st.button("Predict"):
    if sentence.strip() == "":
        st.warning("Please enter a sentence first.")
    else:
        classifier = load_model(model_choice)
        result = classifier(sentence[:512])[0]

        final_label = unify_label(model_choice, result["label"])
        confidence = result["score"] * 100

        result_html = f"""
        <div class="result-panel">
            <div class="panel-label">Analysis complete <span>{model_choice}</span></div>
            <div class="result-value">{final_label}</div>
            <div class="result-confidence">confidence / {confidence:.2f}%</div>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div class="result-panel">
            <div class="panel-label">Analysis result <span>waiting for text</span></div>
            <div class="empty-result">Your result will appear here<br>after you run an analysis.</div>
        </div>
        """,
        unsafe_allow_html=True
    )
