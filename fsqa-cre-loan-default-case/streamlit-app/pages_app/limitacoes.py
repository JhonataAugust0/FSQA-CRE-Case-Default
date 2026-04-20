"""
Página: Limitações — Riscos de uso em produção e recomendações.
"""
import streamlit as st


def render(eda):
    st.markdown('<div class="sec">Limitações e Riscos de Uso em Produção</div>', unsafe_allow_html=True)
    limits = [
        ("🔴", "Alto", "Ausência de variáveis macroeconômicas",
         "Taxa de vacância regional, cap rates de mercado e PIB local não estão no dataset. Esses fatores explicam parte relevante da variância residual (AUC atual de 0.73).",
         "Incorporar dados CBRE/CoStar e FRED na v2.0. AUC estimado após inclusão: 0.78+."),
        ("🔴", "Alto", "Snapshot único por loan — sem trajetória temporal",
         "Cada registro é uma fotografia em um momento. O modelo não captura deterioração gradual (NOI caindo, vacância crescente). Um modelo de sobrevivência ou LSTM com múltiplos snapshots seria mais preditivo.",
         "Coletar múltiplos snapshots por loan. Avaliar Cox Proportional Hazard ou LSTM longitudinal na v3.0."),
        ("🟡", "Médio", "DSCR simplificado — ignora amortização de principal",
         "O Debt Service foi calculado como Balance × Interest Rate. Em loans Fully Amortizing, o pagamento real inclui principal + juros, tornando o DSCR calculado mais otimista que o real.",
         "Calcular debt service completo com fórmula PMT de anuidade na próxima versão."),
        ("🟡", "Médio", "Cobertura temporal 2015–2023 — ciclo de juros sub-representado",
         "O ciclo de alta de taxas de 2022+ (Fed Funds +525bps) está parcialmente representado. O modelo pode sub-estimar risco de refinanciamento em ambiente de juros elevados.",
         "Revalidar o modelo com snapshots de 2022–2024. Incluir Fed Funds Rate como variável exógena."),
        ("🟡", "Médio", "Precision baixa (13.3%) no threshold padrão",
         "A 12.5:1 de desbalanceamento gera muitos falsos positivos. Em threshold 0.50, apenas 1 em cada 7.5 alertas é um default real.",
         "Usar threshold ótimo (≈0.47, máximo F1). Segmentar carteira por tipo de imóvel para thresholds específicos."),
        ("🟢", "Baixo-Médio", "Property Class disponível apenas para Office (~30%)",
         "Para Retail e Multifamily, a variável recebe valor 0 (ausência de informação), limitando seu poder discriminatório para esses segmentos.",
         "Solicitar classificação equivalente de qualidade para todos os tipos de imóvel."),
        ("🟢", "Baixo", "Viés de sobrevivência potencial",
         "O dataset pode não incluir loans que já defaultaram antes de 2015. Se loans de alta qualidade persistem mais tempo, a carteira observada pode sub-representar o risco real histórico.",
         "Confirmar com equipe de dados se há registros pré-2015 excluídos e incorporar na análise."),
    ]
    for icon, imp, titulo, desc, mitiga in limits:
        with st.expander(f"{icon} **{titulo}** — Impacto: {imp}"):
            st.markdown(f'<div class="limit-box">{desc}</div>', unsafe_allow_html=True)
            st.markdown(f"**💡 Mitigação sugerida:** {mitiga}")

    st.divider()
    st.markdown('<div class="sec">Recomendações ao Banco</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.info("**Uso imediato:** Implementar como ferramenta de triagem de primeira linha. Priorizar revisão dos Decis 1–3 (30% da carteira → captura 60% dos defaults). Threshold recomendado: 0.47.")
    with col_b:
        st.warning("**Roadmap:** v2 — variáveis macro + DSCR completo (6 meses). v3 — modelo longitudinal com múltiplos snapshots (12 meses). Revalidação anual com dados atualizados.")
