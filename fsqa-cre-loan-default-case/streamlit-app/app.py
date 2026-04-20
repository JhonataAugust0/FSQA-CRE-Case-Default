"""
CRE Loan Default — Dashboard Analítico Completo
Oliver Wyman FSQA Take-Home Case 2026

Entrypoint mínimo: configuração, sidebar, roteamento e footer.
"""

import warnings
import streamlit as st

from config.styles import inject_css
from data.provider import build_data
from pages_app import introducao, dataset, etl, eda, features, modelagem, avaliacao, limitacoes

warnings.filterwarnings("ignore")

# ── Página ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CRE Default — Dashboard Analítico",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS global ────────────────────────────────────────────────────────────────
inject_css()

# ── Dados ─────────────────────────────────────────────────────────────────────
roc, pr_curve, cal, scores_df, decil, or_df, eda_data, num_dist = build_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏢 CRE Default\n**Dashboard Analítico**")
    st.divider()
    page = st.radio("Seção", [
        "🏠 Introdução",
        "📋 Dataset & Variáveis",
        "📊 Fase 1 — ETL",
        "🔍 Fase 2 — EDA",
        "⚙️ Fase 3 — Features",
        "🤖 Fase 4 — Modelagem",
        "🎯 Fase 5 — Avaliação",
        "⚠️  Limitações",
    ])
    st.divider()
    st.caption("Oliver Wyman · FSQA Case 2026\nModelo: Logistic Regression (L2)\nDataset: 8.959 empréstimos CRE")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">🏢 CRE Loan Default — Dashboard Analítico</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Modelagem Preditiva de Risco de Crédito Imobiliário Comercial · Oliver Wyman FSQA Case 2026</div>', unsafe_allow_html=True)
st.divider()

# ── Router ────────────────────────────────────────────────────────────────────
if page == "🏠 Introdução":
    introducao.render(eda_data)
elif page == "📋 Dataset & Variáveis":
    dataset.render(eda_data)
elif page == "📊 Fase 1 — ETL":
    etl.render()
elif page == "🔍 Fase 2 — EDA":
    eda.render(eda_data, num_dist)
elif page == "⚙️ Fase 3 — Features":
    features.render(eda_data, num_dist)
elif page == "🤖 Fase 4 — Modelagem":
    modelagem.render(eda_data)
elif page == "🎯 Fase 5 — Avaliação":
    avaliacao.render(eda_data, roc, pr_curve, cal, scores_df, decil, or_df)
elif page == "⚠️  Limitações":
    limitacoes.render(eda_data)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Oliver Wyman FSQA Take-Home Case 2026 · Modelo: Logistic Regression (L2, class_weight=balanced) · "
           f"Dataset: 8.959 empréstimos CRE · Período: 2015–2023 · "
           f"AUC-ROC: {eda_data['auc']:.4f} · Gini: {eda_data['gini']:.4f} · KS: {eda_data['ks']:.4f}")