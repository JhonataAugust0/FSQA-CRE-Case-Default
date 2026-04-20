"""
Página: Dataset & Variáveis — Dicionário de dados e estrutura do dataset.
"""

import pandas as pd
import streamlit as st


def render(eda):
    st.markdown('<div class="sec">Estrutura do Dataset</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total de empréstimos", f"{eda['n_total']:,}")
    c2.metric("Variáveis originais", "15")
    c3.metric("Período dos snapshots", "2015 – 2023")
    c4.metric("Target: taxa de default", f"{eda['dr_global']:.2%}")

    st.markdown('<div class="sec">Dicionário de Variáveis Originais</div>', unsafe_allow_html=True)
    st.caption("Todas as variáveis são medidas na data do snapshot, exceto o Default flag (observado nos 12 meses seguintes).")

    variables = [
        ("Facility ID",              "Texto",    "Identificador único de cada empréstimo — não tem poder preditivo, usado apenas como chave."),
        ("Property type",            "Categ.",   "Tipo do imóvel: Retail space (varejo), Office building (escritório) ou Multifamily residential (residencial multifamiliar)."),
        ("Rating snapshot date",     "Data",     "Data de referência na qual os demais campos são observados. O default flag é observado nos 12 meses seguintes a esta data."),
        ("Original loan amount",     "Moeda",    "Valor original do empréstimo no momento da originação. Pode ser maior que o saldo atual, pois o mutuário já pode ter amortizado parte do principal."),
        ("Principal repayment type", "Categ.",   "Fully amortizing: pagamentos seguem amortização linear ao longo de todo o prazo. Partially amortizing: amortização linear sobre 25 anos, mas prazo contratual pode ser menor — gera um 'balloon payment' (pagamento residual) no vencimento."),
        ("Current loan balance",     "Moeda",    "Saldo devedor atual na data do snapshot. Reflete o principal ainda em aberto após pagamentos já realizados."),
        ("Interest rate",            "% a.a.",   "Taxa de juros fixa cobrada do mutuário durante toda a vida do empréstimo. Taxas mais altas podem indicar seleção adversa — o banco cobrou mais porque percebeu maior risco na originação."),
        ("Property value",           "Moeda",    "Valor de mercado estimado do imóvel dado como garantia. Componente fundamental do LTV (alavancagem)."),
        ("Net operating income",     "Moeda",    "Receita líquida do imóvel: aluguel recebido menos despesas operacionais (manutenção, seguros, impostos, gestão). NOI negativo significa que o imóvel custa mais do que rende."),
        ("Contractual term",         "Meses",    "Prazo original do empréstimo. Após esse número de meses, qualquer saldo residual vence integralmente."),
        ("Months to maturity",       "Meses",    "Meses restantes até o vencimento na data do snapshot. MTM baixo → risco de refinanciamento iminente."),
        ("Tenant turnover",          "% a.a.",   "Rotatividade de inquilinos nos últimos 3 anos. Alta rotatividade indica instabilidade de receita do imóvel."),
        ("Region",                   "Categ.",   "Localização geográfica conforme definições do US Census Bureau: Midwest, Northeast, South, West."),
        ("Property Class",           "Categ.",   "Classificação de qualidade de edifícios Office: A (premium) > B (padrão) > C (básico). Disponível apenas para Office buildings."),
        ("Default flag",             "Binário",  "Variável resposta: 1 = o empréstimo entrou em default nos 12 meses seguintes ao snapshot; 0 = não entrou. Esta é a variável que o modelo tenta prever."),
    ]

    st.markdown("""
    <div style="display:grid;grid-template-columns:160px 65px 1fr;gap:4px 8px;
    font-size:.82rem;padding:6px 0;border-bottom:1.5px solid #2E75B6;font-weight:600;color:#1F3864">
    <span>Variável</span><span>Tipo</span><span>Descrição</span></div>
    """, unsafe_allow_html=True)
    for nm, tp, desc in variables:
        color = "#EFF5FB" if nm == "Default flag" else "transparent"
        st.markdown(
            f'<div class="var-row" style="background:{color}">'
            f'<span class="var-name">{nm}</span>'
            f'<span class="var-type">{tp}</span>'
            f'<span>{desc}</span></div>',
            unsafe_allow_html=True)

    st.markdown('<div class="sec">Variáveis Derivadas na Fase 3</div>', unsafe_allow_html=True)
    st.caption("Criadas a partir das variáveis originais para capturar relações econômicas que as variáveis isoladas não capturam.")
    derived = [
        ("LTV",                "Saldo / Valor do Imóvel",       "Alavancagem. LTV > 100% = saldo supera a garantia."),
        ("DSCR",               "NOI / Juros Anuais",            "DSCR < 1 = imóvel não gera renda suficiente para cobrir os juros."),
        ("NOI Yield",          "NOI / Valor do Imóvel",         "Cap rate implícito. Proxy da rentabilidade do ativo."),
        ("Loan Age (meses)",   "Prazo Contratual − MTM",        "Tempo de vida do empréstimo desde a originação."),
        ("Amortization Rate",  "1 − Saldo / Valor Original",    "Proporção do principal já quitado."),
        ("Near Maturity Flag", "1 se MTM ≤ 12 meses",          "Indica risco de refinanciamento iminente."),
        ("Balloon Risk",       "1 se Parcial E MTM ≤ 24m",     "Balloon payment iminente em loan partially amortizing."),
        ("is_office",          "1 se Property type = Office",   "Indicador binário de tipo de ativo."),
        ("property_class_ord", "C=1, B=2, A=3, outros=0",      "Encoding ordinal da qualidade do edifício."),
    ]
    st.markdown("""
    <div style="display:grid;grid-template-columns:160px 180px 1fr;gap:4px 8px;
    font-size:.82rem;padding:6px 0;border-bottom:1.5px solid #2E75B6;font-weight:600;color:#1F3864">
    <span>Feature</span><span>Fórmula</span><span>Interpretação</span></div>
    """, unsafe_allow_html=True)
    for nm, fm, desc in derived:
        st.markdown(
            f'<div style="display:grid;grid-template-columns:160px 180px 1fr;gap:4px 8px;'
            f'padding:5px 0;border-bottom:.5px solid #eee;font-size:.82rem">'
            f'<span style="font-weight:600;color:#1F3864">{nm}</span>'
            f'<span style="font-family:monospace;font-size:.78rem;color:#2E75B6">{fm}</span>'
            f'<span>{desc}</span></div>',
            unsafe_allow_html=True)
