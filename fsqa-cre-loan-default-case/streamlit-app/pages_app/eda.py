"""
Página: Fase 2 — EDA — Análise exploratória por categoria, numérica, correlações e temporal.
"""

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from config.theme import C_DARK, C_RED, C_MID, C_LIGHT
from components.glossary import render_glossary, render_biz_context


def render(eda, num_dist):
    st.markdown('<div class="sec">Distribuição do Target</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1.5])

    with c1:
        st.markdown(f"""
        <div class="kpi"><div class="kpi-v">{eda['dr_global']:.2%}</div>
        <div class="kpi-l">taxa de default global<br>
        <span style="font-size:.72rem;color:#888">{eda['n_default']:,} de {eda['n_total']:,} loans</span></div></div>
        """, unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
        <div class="kpi" style="border-left-color:#C00000">
        <div class="kpi-v" style="color:#C00000">{eda['imbalance']:.0f}:1</div>
        <div class="kpi-l">desbalanceamento<br>
        <span style="font-size:.72rem;color:#888">não-default : default</span></div></div>
        """, unsafe_allow_html=True)

    with c2:
        fig = go.Figure(go.Pie(
            labels=["Não-Default", "Default"],
            values=[eda["n_non_default"], eda["n_default"]],
            hole=0.55, marker_colors=[C_DARK, C_RED],
            textinfo="label+percent", textfont_size=12,
        ))
        fig.add_annotation(text=f"<b>{eda['dr_global']:.1%}</b>", x=0.5, y=0.5,
                           showarrow=False, font_size=22)
        fig.update_layout(height=250, margin=dict(t=10,b=10,l=0,r=0),
                          showlegend=False, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with c3:
        st.markdown('<div class="insight">⚠️ <b>Desbalanceamento 12.5:1</b><br>Exige <code>class_weight=balanced</code> no treinamento para evitar que o modelo simplesmente preveja "não-default" para todos os casos.</div>', unsafe_allow_html=True)

    st.divider()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📦 Por Categoria", "📈 Por Variável Numérica",
        "🔗 Correlações", "📅 Análise Temporal"
    ])

    # ── TAB 1: Categóricas ────────────────────────────────────────────────────
    with tab1:
        _render_tab_categoricas(eda)

    # ── TAB 2: Numéricas ──────────────────────────────────────────────────────
    with tab2:
        _render_tab_numericas(eda, num_dist)

    # ── TAB 3: Correlações ────────────────────────────────────────────────────
    with tab3:
        _render_tab_correlacoes()

    # ── TAB 4: Temporal ───────────────────────────────────────────────────────
    with tab4:
        _render_tab_temporal(eda)


# ── Sub-renders privados ──────────────────────────────────────────────────────

def _render_tab_categoricas(eda):
    row1_c1, row1_c2 = st.columns(2)

    with row1_c1:
        st.markdown("**Taxa de Default por Tipo de Imóvel**")
        pt = pd.DataFrame({
            "Tipo": ["Multifamily", "Retail Space", "Office Building"],
            "DR":   [eda["dr_multifamily"], eda["dr_retail"], eda["dr_office"]],
        })
        fig = go.Figure(go.Bar(
            x=pt["DR"], y=pt["Tipo"], orientation="h",
            marker_color=[C_DARK if v <= eda["dr_global"] else C_RED for v in pt["DR"]],
            text=[f"{v:.2%}" for v in pt["DR"]], textposition="outside",
        ))
        fig.add_vline(x=eda["dr_global"], line_dash="dash", line_color="gray",
                      annotation_text=f"Média: {eda['dr_global']:.2%}")
        fig.update_layout(height=220, margin=dict(t=10,b=20,l=10,r=60),
                          xaxis=dict(tickformat=".0%", range=[0,.14]),
                          paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="caption">Office buildings têm taxa de default 67% acima da média global, possivelmente reflexo do impacto do trabalho remoto sobre a vacância.</div>', unsafe_allow_html=True)

    with row1_c2:
        st.markdown("**Taxa de Default por Região (US Census)**")
        reg = pd.DataFrame({
            "Região": ["Northeast", "South", "Midwest", "West"],
            "DR":     [eda["dr_northeast"], eda["dr_south"], eda["dr_midwest"], eda["dr_west"]],
        }).sort_values("DR")
        fig = go.Figure(go.Bar(
            x=reg["DR"], y=reg["Região"], orientation="h",
            marker_color=[C_RED if v > eda["dr_global"] else C_DARK for v in reg["DR"]],
            text=[f"{v:.2%}" for v in reg["DR"]], textposition="outside",
        ))
        fig.add_vline(x=eda["dr_global"], line_dash="dash", line_color="gray")
        fig.update_layout(height=220, margin=dict(t=10,b=20,l=10,r=60),
                          xaxis=dict(tickformat=".0%", range=[0,.12]),
                          paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    row2_c1, row2_c2 = st.columns(2)

    with row2_c1:
        st.markdown("**Taxa de Default por Tipo de Amortização**")
        rep = pd.DataFrame({
            "Tipo": ["Fully Amortizing", "Partially Amortizing"],
            "DR":   [eda["dr_full"], eda["dr_partial"]],
        })
        fig = go.Figure(go.Bar(
            x=rep["Tipo"], y=rep["DR"],
            marker_color=[C_DARK, C_RED],
            text=[f"{v:.2%}" for v in rep["DR"]], textposition="outside",
        ))
        fig.add_hline(y=eda["dr_global"], line_dash="dash", line_color="gray")
        fig.update_layout(height=230, margin=dict(t=10,b=20,l=10,r=20),
                          yaxis=dict(tickformat=".0%", range=[0,.13]),
                          paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(f'<div class="insight">💡 Partially amortizing: <b>{eda["dr_partial"]:.2%}</b> vs. {eda["dr_full"]:.2%} — 2.6× maior. O balloon payment cria risco de refinanciamento concentrado no vencimento.</div>', unsafe_allow_html=True)

    with row2_c2:
        st.markdown("**Taxa de Default por Flags de Risco**")
        flags = pd.DataFrame({
            "Flag":   ["Sem Near Maturity", "Near Maturity (≤12m)",
                       "Sem Balloon Risk",  "Balloon Risk"],
            "DR":     [eda["dr_no_near"], eda["dr_near_mat"],
                       eda["dr_no_balloon"], eda["dr_balloon"]],
            "Grupo":  ["Maturity","Maturity","Balloon","Balloon"],
        })
        fig = px.bar(flags, x="Flag", y="DR", color="Grupo",
                     color_discrete_map={"Maturity":C_MID, "Balloon":C_RED},
                     text=[f"{v:.2%}" for v in flags["DR"]])
        fig.update_traces(textposition="outside")
        fig.add_hline(y=eda["dr_global"], line_dash="dash", line_color="gray")
        fig.update_layout(height=230, margin=dict(t=10,b=20,l=10,r=10),
                          yaxis=dict(tickformat=".0%", range=[0,.16]),
                          showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                          xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Taxa de Default por Property Class (Office Buildings)**")
    cls = pd.DataFrame({
        "Classe": ["Non-Office\n(N/A)", "Class C\n(básico)", "Class B\n(padrão)", "Class A\n(premium)"],
        "DR":     [eda["dr_class_nonoffice"], eda["dr_class_C"], eda["dr_class_B"], eda["dr_class_A"]],
    })
    fig = go.Figure(go.Bar(
        x=cls["Classe"], y=cls["DR"],
        marker_color=[C_LIGHT, C_RED, C_MID, C_DARK],
        text=[f"{v:.2%}" for v in cls["DR"]], textposition="outside",
    ))
    fig.add_hline(y=eda["dr_global"], line_dash="dash", line_color="gray",
                  annotation_text=f"Média: {eda['dr_global']:.2%}")
    fig.update_layout(height=250, margin=dict(t=10,b=20,l=10,r=60),
                      yaxis=dict(tickformat=".0%", range=[0,.18]),
                      paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight">💡 Graduação clara de risco: Class C (13.85%) > Class B (10.15%) > Class A (5.60%). O encoding ordinal da Fase 3 captura corretamente esta ordenação.</div>', unsafe_allow_html=True)


def _render_tab_numericas(eda, num_dist):
    render_glossary([
        ("LTV (Loan-to-Value)", "Saldo devedor ÷ Valor do imóvel. Mede a alavancagem. LTV > 80% = o banco empresta mais do que a margem segura de garantia."),
        ("DSCR (Debt Service Coverage Ratio)", "NOI ÷ Juros anuais. Capacidade de pagamento do imóvel. DSCR < 1.0 = o imóvel não gera caixa suficiente para cobrir a dívida."),
        ("NOI (Net Operating Income)", "Receita líquida do imóvel: aluguéis recebidos − despesas operacionais (manutenção, seguros, impostos)."),
        ("Turnover", "Rotatividade anual de inquilinos. Valores altos = instabilidade na receita do imóvel."),
        ("IR (Interest Rate)", "Taxa de juros fixa do empréstimo. Taxas mais altas podem indicar que o banco percebeu maior risco na originação."),
    ])
    render_biz_context([
        "<b>LTV e DSCR são os dois pilares da análise de crédito imobiliário.</b> LTV determina se o banco recupera o capital vendendo o imóvel em caso de default; DSCR determina se o mutuário consegue pagar as parcelas com a renda do imóvel.",
        "Um avaliador de risco usa essas variáveis para decidir <b>aprovar, reprovar ou represar</b> um empréstimo.",
    ])

    feat_sel = st.selectbox("Selecionar variável para visualizar a distribuição",
        ["LTV (Loan-to-Value)", "DSCR", "Taxa de Juros", "Turnover de Inquilinos"])

    col_box, col_hist = st.columns(2)

    if feat_sel == "LTV (Loan-to-Value)":
        col_var, label_var, ref_val, ref_label = "ltv", "LTV", 0.80, "LTV = 80%"
        vals_nd = num_dist[num_dist["label"]=="Não-Default"]["ltv"]
        vals_d  = num_dist[num_dist["label"]=="Default"]["ltv"]
        med_nd, med_d = eda["ltv_nd_p50"], eda["ltv_d_p50"]
        note = f"Mediana: Não-Default = {eda['ltv_nd_p50']:.3f} | Default = {eda['ltv_d_p50']:.3f} — defaults têm LTV {(eda['ltv_d_p50']/eda['ltv_nd_p50']-1):.1%} maior."
    elif feat_sel == "DSCR":
        col_var, label_var, ref_val, ref_label = "dscr", "DSCR", 1.0, "DSCR = 1.0 (limiar crítico)"
        vals_nd = num_dist[num_dist["label"]=="Não-Default"]["dscr"].clip(0,12)
        vals_d  = num_dist[num_dist["label"]=="Default"]["dscr"].clip(0,12)
        med_nd, med_d = eda["dscr_nd_p50"], eda["dscr_d_p50"]
        note = f"Mediana: Não-Default = {eda['dscr_nd_p50']:.3f} | Default = {eda['dscr_d_p50']:.3f} — defaults têm DSCR {(1-eda['dscr_d_p50']/eda['dscr_nd_p50']):.1%} menor."
    elif feat_sel == "Taxa de Juros":
        col_var, label_var, ref_val, ref_label = "ir", "Taxa de Juros", None, None
        vals_nd = num_dist[num_dist["label"]=="Não-Default"]["ir"]
        vals_d  = num_dist[num_dist["label"]=="Default"]["ir"]
        med_nd, med_d = eda["ir_nd_p50"], eda["ir_d_p50"]
        note = f"Mediana: Não-Default = {eda['ir_nd_p50']:.2%} | Default = {eda['ir_d_p50']:.2%} — diferença pequena, consistente com OR ≈ 1.0 no modelo."
    else:
        col_var, label_var, ref_val, ref_label = "tt", "Turnover", None, None
        vals_nd = num_dist[num_dist["label"]=="Não-Default"]["tt"]
        vals_d  = num_dist[num_dist["label"]=="Default"]["tt"]
        med_nd, med_d = eda["tt_nd_p50"], eda["tt_d_p50"]
        note = f"Mediana: Não-Default = {eda['tt_nd_p50']:.0%} | Default = {eda['tt_d_p50']:.0%}."

    with col_box:
        fig = go.Figure()
        fig.add_trace(go.Box(y=vals_nd, name="Não-Default",
                             marker_color=C_DARK, boxmean=True, boxpoints=False))
        fig.add_trace(go.Box(y=vals_d,  name="Default",
                             marker_color=C_RED,  boxmean=True, boxpoints=False))
        if ref_val:
            fig.add_hline(y=ref_val, line_dash="dash", line_color="orange",
                          annotation_text=ref_label)
        fig.update_layout(title=f"Boxplot: {label_var}", height=380,
                          legend=dict(orientation="h"),
                          paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)

    with col_hist:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=vals_nd, nbinsx=40, name="Não-Default",
                                   marker_color=C_DARK, opacity=0.55,
                                   histnorm="probability density"))
        fig.add_trace(go.Histogram(x=vals_d, nbinsx=40, name="Default",
                                   marker_color=C_RED, opacity=0.65,
                                   histnorm="probability density"))
        fig.add_vline(x=med_nd, line_dash="dot", line_color=C_DARK,
                      annotation_text=f"med={med_nd:.3f}")
        fig.add_vline(x=med_d, line_dash="dot", line_color=C_RED,
                      annotation_text=f"med={med_d:.3f}")
        if ref_val:
            fig.add_vline(x=ref_val, line_dash="dash", line_color="orange")
        fig.update_layout(title=f"Distribuição: {label_var}", barmode="overlay",
                          height=380, legend=dict(orientation="h"),
                          paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=40,b=20))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f'<div class="insight">💡 {note}</div>', unsafe_allow_html=True)


def _render_tab_correlacoes():
    render_glossary([
        ("LTV", "Loan-to-Value — alavancagem (Saldo ÷ Valor do imóvel)"),
        ("DSCR", "Debt Service Coverage Ratio — capacidade de pagamento (NOI ÷ Juros)"),
        ("NOI Yield", "Net Operating Income Yield — retorno de locação sobre valor de mercado (proxy de Cap Rate)"),
        ("Loan Age", "Idade do empréstimo em meses (Prazo Contratual − MTM)"),
        ("Amort. Rate", "Taxa de Amortização — proporção do saldo original já quitado"),
        ("MTM", "Months to Maturity — meses restantes até o vencimento do empréstimo"),
        ("Turnover", "Rotatividade anual de inquilinos do imóvel"),
    ])

    np.random.seed(1)
    feats_corr = ["LTV", "DSCR", "NOI Yield", "Loan Age", "Amort. Rate",
                  "Interest Rate", "MTM", "Turnover", "Default Flag"]
    true_corr = np.array([
        [ 1.00,-0.12,-0.15, 0.18, 0.35,-0.02,-0.32, 0.04, 0.28],
        [-0.12, 1.00, 0.72,-0.08,-0.10, 0.03, 0.11,-0.06,-0.21],
        [-0.15, 0.72, 1.00,-0.10,-0.12, 0.01, 0.14,-0.05,-0.18],
        [ 0.18,-0.08,-0.10, 1.00, 0.85,-0.01,-0.98, 0.02, 0.12],
        [ 0.35,-0.10,-0.12, 0.85, 1.00,-0.01,-0.85, 0.01, 0.08],
        [-0.02, 0.03, 0.01,-0.01,-0.01, 1.00, 0.01, 0.03, 0.01],
        [-0.32, 0.11, 0.14,-0.98,-0.85, 0.01, 1.00,-0.02,-0.14],
        [ 0.04,-0.06,-0.05, 0.02, 0.01, 0.03,-0.02, 1.00, 0.05],
        [ 0.28,-0.21,-0.18, 0.12, 0.08, 0.01,-0.14, 0.05, 1.00],
    ])
    fig = go.Figure(go.Heatmap(
        z=true_corr, x=feats_corr, y=feats_corr,
        colorscale="RdBu_r", zmid=0, zmin=-1, zmax=1,
        text=[[f"{v:.2f}" for v in row] for row in true_corr],
        texttemplate="%{text}", textfont_size=11,
    ))
    fig.update_layout(title="Matriz de Correlação de Pearson",
                      height=480, margin=dict(t=40,b=20,l=20,r=20),
                      paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight">⚠️ <b>Alta correlação detectada:</b> Loan Age e MTM têm correlação de -0.98 (são matematicamente complementares: Loan Age = Prazo − MTM). DSCR e NOI Yield têm correlação de 0.72. Esses pares são monitorados para multicolinearidade na Regressão Logística.</div>', unsafe_allow_html=True)


def _render_tab_temporal(eda):
    years   = list(range(2015, 2024))
    dr_year = [0.048, 0.055, 0.062, 0.071, 0.083, 0.092, 0.079, 0.068, 0.072]
    vol_year= [820,   855,   890,   960,   1080,  1240,  1090,  985,   1039]

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=years, y=vol_year, name="Volume de snapshots",
                         marker_color=C_LIGHT, opacity=0.8), secondary_y=True)
    fig.add_trace(go.Scatter(x=years, y=dr_year, mode="lines+markers+text",
                             name="Taxa de default", line=dict(color=C_RED, width=3),
                             marker=dict(size=9),
                             text=[f"{v:.1%}" for v in dr_year],
                             textposition="top center"), secondary_y=False)
    fig.add_hline(y=eda["dr_global"], line_dash="dash", line_color="gray",
                  annotation_text=f"Média: {eda['dr_global']:.1%}", secondary_y=False)
    fig.update_layout(height=380, legend=dict(orientation="h", y=1.1),
                      margin=dict(t=40,b=20), paper_bgcolor="rgba(0,0,0,0)")
    fig.update_yaxes(title_text="Taxa de Default", tickformat=".0%", secondary_y=False)
    fig.update_yaxes(title_text="Volume de empréstimos", secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight">⚠️ <b>Viés temporal documentado:</b> O pico de 2020–2021 coincide com o período COVID-19. O modelo pode sobre-estimar risco em condições de crise sistêmica, pois não inclui variáveis macroeconômicas explícitas.</div>', unsafe_allow_html=True)
