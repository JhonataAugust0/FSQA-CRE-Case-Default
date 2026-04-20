"""
Página: Fase 3 — Feature Engineering — Derivação de features, encoding e winsorizing.
"""

import streamlit as st
import plotly.graph_objects as go

from config.theme import C_DARK, C_RED
from components.glossary import render_glossary, render_biz_context


def render(eda, num_dist):
    st.markdown('<div class="sec">Processo de Feature Engineering</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns(3)
    c1.metric("Features originais usadas", eda["features_original"])
    c2.metric("Features derivadas", eda["features_derived"])
    c3.metric("Total no modelo", eda["features_total"])

    st.markdown('<div class="sec">Principais Features Derivadas — Distribuição por Grupo</div>', unsafe_allow_html=True)

    render_glossary([
        ("LTV", "Loan-to-Value — Saldo ÷ Valor do imóvel. Mede quanto da garantia está comprometida."),
        ("DSCR", "Debt Service Coverage Ratio — NOI ÷ Juros. Capacidade do imóvel de pagar a dívida."),
        ("NOI Yield", "Net Operating Income ÷ Valor do imóvel. Rentabilidade operacional do ativo (proxy de Cap Rate)."),
        ("Balloon Risk", "Flag: empréstimo com amortização parcial e ≤ 24 meses para vencer — risco de pagamento residual massivo."),
        ("Near Maturity", "Flag: ≤ 12 meses para o vencimento — risco iminente de refinanciamento."),
    ])
    render_biz_context([
        "<b>LTV e DSCR são os dois pilares regulatórios</b> usados por bancos e reguladores (Basileia II/III) para avaliar empréstimos imobiliários.",
        "<b>Balloon Risk e Near Maturity</b> capturam riscos de refinanciamento — quando o mutuário precisa obter novo financiamento para quitar o saldo residual, o que pode falhar em ambientes de juros altos.",
        "Essas features derivadas transformam dados brutos em <b>indicadores econômicos</b> que o modelo usa para identificar padrões de inadimplência.",
    ])

    feat_cols = st.columns(2)

    # LTV
    with feat_cols[0]:
        fig = go.Figure()
        fig.add_trace(go.Box(y=num_dist[num_dist["label"]=="Não-Default"]["ltv"],
                             name="Não-Default", marker_color=C_DARK, boxmean=True, boxpoints=False))
        fig.add_trace(go.Box(y=num_dist[num_dist["label"]=="Default"]["ltv"],
                             name="Default", marker_color=C_RED, boxmean=True, boxpoints=False))
        fig.add_hline(y=0.8, line_dash="dash", line_color="orange",
                      annotation_text="LTV=80% (limiar comum)")
        fig.update_layout(title="LTV — Loan-to-Value", height=300,
                          yaxis_title="LTV (saldo/valor imóvel)",
                          legend=dict(orientation="h"),
                          paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=10))
        st.plotly_chart(fig, use_container_width=True)

    # DSCR
    with feat_cols[1]:
        fig = go.Figure()
        fig.add_trace(go.Box(y=num_dist[num_dist["label"]=="Não-Default"]["dscr"].clip(0,12),
                             name="Não-Default", marker_color=C_DARK, boxmean=True, boxpoints=False))
        fig.add_trace(go.Box(y=num_dist[num_dist["label"]=="Default"]["dscr"].clip(0,12),
                             name="Default", marker_color=C_RED, boxmean=True, boxpoints=False))
        fig.add_hline(y=1.0, line_dash="dash", line_color="orange",
                      annotation_text="DSCR=1.0 (NOI cobre apenas os juros)")
        fig.update_layout(title="DSCR — Debt Service Coverage Ratio", height=300,
                          yaxis_title="DSCR (NOI / Juros Anuais)",
                          legend=dict(orientation="h"),
                          paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="insight">💡 <b>LTV mediano:</b> Defaults = {:.3f} vs. Não-Defaults = {:.3f} &nbsp;|&nbsp; <b>DSCR mediano:</b> Defaults = {:.3f} vs. Não-Defaults = {:.3f}</div>'.format(
        eda["ltv_d_p50"], eda["ltv_nd_p50"], eda["dscr_d_p50"], eda["dscr_nd_p50"]),
        unsafe_allow_html=True)

    st.markdown('<div class="sec">Encoding de Variáveis Categóricas</div>', unsafe_allow_html=True)
    enc_data = [
        ("Property type",              "One-Hot (drop_first=True)",       "3 categorias → 2 dummies. Evita dummy trap."),
        ("Region",                     "One-Hot (drop_first=True)",       "4 categorias → 3 dummies. Midwest = categoria base."),
        ("Principal Repayment Type",   "Label Encoding binário",          "Fully=0, Partially=1. Variável naturalmente binária."),
        ("Property Class",             "Ordinal (C=1, B=2, A=3) + NaN=0", "Preserva ordem natural de qualidade. NaN para não-Office recebe 0."),
    ]
    for var, meth, just in enc_data:
        c1, c2, c3 = st.columns([1.5, 1.5, 2])
        c1.markdown(f"**{var}**")
        c2.markdown(f"`{meth}`")
        c3.caption(just)

    st.markdown('<div class="sec">Winsorizing — Tratamento de Outliers</div>', unsafe_allow_html=True)
    st.markdown("""
Três features receberam winsorizing nos **percentis 1% e 99%** para evitar que valores extremos
distorçam os coeficientes da Regressão Logística: `ltv`, `dscr` e `noi_yield`.

O winsorizing substitui valores abaixo do p1 pelo valor do p1, e valores acima do p99 pelo p99.
Os limites são calculados apenas no conjunto de **treino** (dentro do pipeline sklearn)
para evitar data leakage para o conjunto de teste.
""")
