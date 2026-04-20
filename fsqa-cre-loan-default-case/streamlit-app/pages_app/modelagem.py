"""
Página: Fase 4 — Modelagem — Comparativo de modelos e justificativa.
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

from config.theme import C_DARK, C_MID, C_RED
from components.glossary import render_glossary, render_biz_context


def render(eda):
    st.markdown('<div class="sec">Estratégia de Modelagem</div>', unsafe_allow_html=True)
    st.markdown("""
Três modelos foram treinados e comparados dentro de **pipelines sklearn** com `ColumnTransformer`
(StandardScaler nas features contínuas, passthrough nas binárias/ordinais).
A divisão treino/teste foi **80/20 estratificada** pelo target, com `random_state=42`.
""")

    # Comparativo de modelos
    st.markdown('<div class="sec">Comparativo de Modelos</div>', unsafe_allow_html=True)
    render_glossary([
        ("AUC-ROC", "Area Under the ROC Curve — probabilidade de o modelo rankear um default acima de um não-default. Quanto mais próximo de 1.0, melhor a separação."),
        ("Gini", "= 2×AUC − 1. Mede o poder discriminante acima do acaso. Gini > 0.40 é o benchmark regulatório bancário."),
        ("KS (Kolmogorov-Smirnov)", "Maior distância entre as distribuições de score de defaults e não-defaults. KS > 0.30 = o modelo separa bem os dois grupos."),
        ("Precision", "Dos alertas de default, quantos realmente o são. Precision baixa = muitos falsos alarmes (custo de análise)."),
        ("Recall", "Dos defaults reais, quantos o modelo detectou. Recall alto = poucos defaults escapam (proteção de capital)."),
        ("F1", "Média harmônica entre Precision e Recall. Equilíbrio entre custo de análise e custo de perda."),
        ("Brier Score", "Erro quadrático médio das probabilidades. Quanto menor, mais calibradas as probabilidades preditas."),
    ], title="📖 O que significa cada métrica?")
    render_biz_context([
        "<b>AUC-ROC e Gini</b> são as métricas que o regulador bancário (Basileia II/III) e auditores exigem para validar modelos de scoring de crédito.",
        "<b>KS > 0.30</b> significa que o banco pode definir uma 'linha de corte' clara para separar empréstimos de alto e baixo risco.",
        "<b>Recall é priorizado sobre Precision</b> em crédito imobiliário: o custo de um analista revisar um empréstimo saudável (~R$200 de hora-homem) é ínfimo comparado ao prejuízo de não detectar um default ($1.4M médio por empréstimo).",
        "<b>Brier Score</b> garante que quando o modelo diz '30% de chance de default', isso realmente acontece em ~30% dos casos — essencial para provisionamento contábil.",
    ])

    models_df = pd.DataFrame({
        "Modelo": ["Logistic Regression ✅", "Random Forest", "Gradient Boosting"],
        "AUC-ROC": [eda["auc"],    eda["auc_rf"],  eda["auc_gb"]],
        "Gini":    [eda["gini"],   eda["gini_rf"], eda["gini_gb"]],
        "KS":      [eda["ks"],     eda["ks_rf"],   eda["ks_gb"]],
        "Precision":[eda["prec"],  0.1686,         0.5000],
        "Recall":  [eda["rec"],    0.5414,         0.0376],
        "F1":      [eda["f1"],     0.2571,         0.0699],
        "Brier":   [eda["brier"],  0.1570,         0.0660],
    })

    fig = go.Figure()
    metrics_plot = ["AUC-ROC", "Gini", "KS", "F1"]
    colors_m = [C_DARK, C_MID, C_RED]
    for (_, row), col in zip(models_df.iterrows(), colors_m):
        fig.add_trace(go.Bar(
            name=row["Modelo"], x=metrics_plot,
            y=[row[m] for m in metrics_plot],
            marker_color=col, opacity=0.85,
            text=[f"{row[m]:.3f}" for m in metrics_plot],
            textposition="outside",
        ))
    fig.update_layout(barmode="group", height=350, yaxis=dict(range=[0,.9]),
                      legend=dict(orientation="h", y=1.1),
                      margin=dict(t=50,b=20), paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(models_df.set_index("Modelo").style.format("{:.4f}").highlight_max(axis=0, color="#D4EDDA"),
                 use_container_width=True)

    st.markdown('<div class="sec">Por que Regressão Logística?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
**Perspectiva técnica:**
- Melhor AUC-ROC no conjunto de teste (0.7335)
- Validação cruzada estável (5-fold)
- Sem overfitting significativo (gap treino-teste < 0.05)
- Coeficientes auditáveis pós-treinamento
""")
    with c2:
        st.markdown("""
**Perspectiva de negócio / regulatória:**
- Odds ratios têm interpretação direta para gestores de risco
- Alinhado com práticas de credit scoring regulatório (Basileia II/III)
- Modelo pode ser auditado por reguladores sem caixa-preta
- Gradient Boosting: Recall de apenas 3.8% — captura quase nenhum default
""")

    st.markdown('<div class="sec">Tratamento do Desbalanceamento</div>', unsafe_allow_html=True)
    st.markdown("""
Com **12.5:1 de imbalance ratio**, um modelo naive preveria "não-default" para todos e teria
92.6% de acurácia — mas capturaria zero defaults. A solução foi `class_weight='balanced'`,
que pondera os erros de classificação inversamente à frequência de cada classe durante o treinamento,
sem gerar amostras sintéticas (alternativa ao SMOTE).
""")
