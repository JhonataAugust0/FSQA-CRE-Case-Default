"""
Página: Introdução — Visão geral do projeto e métricas em destaque.
"""

import streamlit as st


def render(eda):
    col_l, col_r = st.columns([1.6, 1])

    with col_l:
        st.markdown('<div class="sec">O que é este projeto?</div>', unsafe_allow_html=True)
        st.markdown("""
Empréstimos imobiliários comerciais (**CRE — Commercial Real Estate**) são financiamentos concedidos por bancos
para a aquisição ou refinanciamento de imóveis como edifícios de escritórios, espaços comerciais de varejo e
prédios residenciais multifamiliares. Esses empréstimos têm uma característica crítica: o imóvel serve como
**garantia** — se o mutuário não pagar, o banco pode executar a garantia e vender o imóvel para recuperar
o capital.

Quando um mutuário para de pagar suas obrigações contratuais, o empréstimo entra em **default** (inadimplência).
Prever quais empréstimos têm maior probabilidade de entrar em default nos próximos 12 meses é uma das tarefas
mais importantes da gestão de risco de crédito bancário. Ela permite ao banco:
""")
        for item in [
            "**Alocar capital regulatório** (Basileia II/III) de forma proporcional ao risco real de cada carteira",
            "**Priorizar revisões** e ações preventivas nos empréstimos de maior risco",
            "**Definir spreads de juros** adequados ao perfil de risco na originação de novos empréstimos",
            "**Comunicar** exposições de risco ao Conselho e aos reguladores com evidência quantitativa",
        ]:
            st.markdown(f"- {item}")

        st.markdown('<div class="sec">Objetivo deste trabalho</div>', unsafe_allow_html=True)
        st.markdown("""
A partir de uma amostra histórica de **8.959 empréstimos CRE**, este projeto constrói um modelo preditivo
capaz de estimar a probabilidade de default de cada empréstimo no horizonte de 12 meses, seguindo um pipeline
completo de Data Science em 5 fases:
""")

        phases = [
            ("Fase 1 — ETL",            "Limpeza e padronização dos dados brutos"),
            ("Fase 2 — EDA",            "Análise exploratória: drivers de default"),
            ("Fase 3 — Feature Eng.",   "Derivação de métricas financeiras (LTV, DSCR…)"),
            ("Fase 4 — Modelagem",      "Treinamento e comparação de 3 modelos"),
            ("Fase 5 — Avaliação",      "AUC-ROC, Gini, KS, calibração, decis"),
        ]
        for ph, desc in phases:
            st.markdown(f"**{ph}:** {desc}")

    with col_r:
        st.markdown('<div class="sec">Resultado em destaque</div>', unsafe_allow_html=True)

        for label, val, note in [
            ("AUC-ROC",            "0.7335", "benchmark > 0.70"),
            ("Gini",               "0.4671", "benchmark > 0.40"),
            ("KS Statistic",       "0.3366", "benchmark > 0.30"),
            ("Taxa de default",    "7.40%",  "663 de 8.959 loans"),
            ("Top 20% captura",    "48.1%",  "dos defaults da carteira"),
            ("Lift — Decil 1",     "3.44×",  "acima da média da carteira"),
        ]:
            st.markdown(
                f'<div class="kpi"><div class="kpi-v">{val}</div>'
                f'<div class="kpi-l">{label}'
                + f'<br><span style="font-size:.72rem;color:#888">{note}</span></div></div>',
                unsafe_allow_html=True)
            st.write("")

        st.markdown(
            '<div class="insight">Revisando apenas <b>30% da carteira</b> com '
            'maior score de risco, o banco capturaria <b>60% de todos os defaults</b> '
            'antes que ocorram.</div>',
            unsafe_allow_html=True)
