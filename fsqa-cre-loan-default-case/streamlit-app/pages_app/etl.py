"""
Página: Fase 1 — ETL — Problemas identificados, DQ checks e schema pós-limpeza.
"""

import pandas as pd
import streamlit as st


def render():
    st.markdown('<div class="sec">Problemas identificados no arquivo bruto</div>', unsafe_allow_html=True)

    issues = [
        ("Valores monetários",    "String com $, vírgulas e espaços", '" $1,460,057.06 "',    "float64 via regex"),
        ("Percentuais",           "String com símbolo %",             '"7.66%"',               "float / 100"),
        ("Categoriais",           "Espaços externos",                 '" Fully amortizing "', ".strip() + Categorical"),
        ("Datas",                 "String MM/DD/YYYY",                '"1/1/2020"',            "datetime64"),
        ("Property Class N/A",   "String 'N/A' para não-Office",     '"N/A"',                 "np.nan"),
        ("Encoding",              "UTF-8 com BOM (\\ufeff)",          "caractere espúrio col 1","utf-8-sig"),
    ]

    cols_hdr = st.columns([1.5, 1.5, 1.5, 1.5])
    for h, c in zip(["Problema", "Causa raiz", "Exemplo bruto", "Solução"], cols_hdr):
        c.markdown(f"**{h}**")
    for prob, causa, ex, sol in issues:
        c1, c2, c3, c4 = st.columns([1.5, 1.5, 1.5, 1.5])
        c1.markdown(prob); c2.markdown(causa)
        c3.markdown(f"`{ex}`"); c4.markdown(sol)
        st.divider()

    st.markdown('<div class="sec">DQ Checks — Resultados</div>', unsafe_allow_html=True)
    dq_results = {
        "Linhas totais":              "8.959",
        "Valores nulos (exceto P. Class)": "0",
        "Facility IDs duplicados":    "0",
        "Default flag fora de {0,1}": "0",
        "MTM > Prazo Contratual":     "0",
        "Balance > 110% do Original": "0",
        "NOI negativos":              "Documentados (plausíveis)",
        "Property Class N/A":         "6.301 (não-Office, esperado)",
    }
    c1, c2 = st.columns(2)
    items = list(dq_results.items())
    for i, (k, v) in enumerate(items):
        col = c1 if i < 4 else c2
        icon = "✅" if v not in ["Documentados (plausíveis)", "6.301 (não-Office, esperado)"] else "ℹ️"
        col.markdown(f"{icon} **{k}:** {v}")

    st.markdown('<div class="sec">Schema após ETL</div>', unsafe_allow_html=True)
    schema = pd.DataFrame({
        "Coluna": ["Facility ID","Property type","Rating snapshot date","Original Loan Amount",
                   "Principal Repayment Type","Current Loan Balance","Interest rate",
                   "Property value","Net operating income","Contractual term",
                   "Months to maturity","Annual tenant turnover","Region",
                   "Property Class","Default flag"],
        "Dtype antes": ["object"]*15,
        "Dtype depois": ["string","Categorical","datetime64","float64","Categorical",
                         "float64","float64","float64","float64","Int64",
                         "Int64","float64","Categorical","object (c/ NaN)","Int8"],
        "Nulos": [0,0,0,0,0,0,0,0,0,0,0,0,0,6301,0],
    })
    st.dataframe(schema, use_container_width=True, hide_index=True)
