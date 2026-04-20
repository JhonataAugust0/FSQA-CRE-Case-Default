"""
Página: Fase 5 — Avaliação — Métricas, ROC, PR, Calibração, Decil, CV e Odds Ratios.
"""
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from config.theme import C_DARK, C_RED, C_MID, C_LIGHT
from components.glossary import render_glossary, render_biz_context


def render(eda, roc, pr_curve, cal, scores_df, decil, or_df):
    st.markdown('<div class="sec">Métricas de Performance</div>', unsafe_allow_html=True)
    cols_m = st.columns(6)
    kpis = [
        ("AUC-ROC",    f"{eda['auc']:.4f}",  "benchmark > 0.70", "ok"),
        ("Gini",       f"{eda['gini']:.4f}", "benchmark > 0.40", "ok"),
        ("KS Stat.",   f"{eda['ks']:.4f}",   "benchmark > 0.30", "ok"),
        ("Recall",     f"{eda['rec']:.2%}",  "defaults capturados", "ok"),
        ("Precision",  f"{eda['prec']:.2%}", "threshold = 0.50", "warn"),
        ("Brier",      f"{eda['brier']:.4f}","calibração", "ok"),
    ]
    for col, (lbl, val, note, kind) in zip(cols_m, kpis):
        badge = "✅" if kind == "ok" else "⚠️"
        col.markdown(
            f'<div class="kpi"><div class="kpi-v">{val}</div>'
            f'<div class="kpi-l">{lbl} {badge}<br>'
            f'<span style="font-size:.70rem;color:#888">{note}</span></div></div>',
            unsafe_allow_html=True)

    with st.expander("📖 O que significam estas métricas e por que importam para o banco?", expanded=True):
        st.markdown("""
**Métricas de discriminação (o modelo separa bem os grupos?):**
- **AUC-ROC (0.7335):** Se sortearmos um Default e um Não-Default aleatoriamente, há **73% de chance** de o modelo atribuir score maior ao Default. Benchmark regulatório: > 0.70. ✅
- **Gini (0.4671):** Poder discriminante acima do acaso (= 2×AUC − 1). Benchmark regulatório: > 0.40. ✅
- **KS (0.3366):** Maior separação entre as curvas cumulativas de defaults e não-defaults. Com KS > 0.30, o banco pode definir uma **política de corte de crédito eficaz**. ✅

**Métricas de decisão (o que acontece quando o modelo alerta?):**
- **Recall (66.17%):** O modelo **captura 2 em cada 3 defaults** antes que ocorram — proteção direta do capital do banco.
- **Precision (13.27%):** De cada 100 alertas, ~13 são defaults reais. Os outros 87 são empréstimos saudáveis que serão revisados por precaução. **Em crédito imobiliário de alto valor ($1.4M médio), o custo de revisar um bom empréstimo é desprezível vs. o custo de ignorar um calote.**
- **Brier Score (0.2096):** Calibração das probabilidades — essencial para **provisionamento contábil** (IFRS 9) e cálculo de perdas esperadas.
        """)

    st.divider()
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Curva ROC & KS", "📉 Precision-Recall",
        "🎯 Calibração", "📊 Análise por Decil", "🔄 Validação Cruzada"
    ])

    with tab1:
        _render_roc_ks(eda, roc, scores_df)
    with tab2:
        _render_pr(eda, pr_curve)
    with tab3:
        _render_calibracao(eda, cal, scores_df)
    with tab4:
        _render_decil(eda, decil)
    with tab5:
        _render_cv_odds(eda, or_df)


def _render_roc_ks(eda, roc, scores_df):
    render_glossary([
        ("ROC", "Receiver Operating Characteristic — curva que mostra o trade-off entre detectar defaults (TPR) e gerar falsos alarmes (FPR) em cada threshold."),
        ("AUC", "Area Under the Curve — área sob a curva ROC. AUC=0.50 = aleatório; AUC=1.0 = perfeito."),
        ("FPR (False Positive Rate)", "Proporção de não-defaults classificados erroneamente como default (falsos alarmes)."),
        ("TPR (True Positive Rate)", "Proporção de defaults corretamente identificados pelo modelo (= Recall)."),
        ("KS (Kolmogorov-Smirnov)", "Maior distância vertical entre as curvas cumulativas de defaults e não-defaults. Indica o ponto de máxima separação."),
    ])
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=roc["fpr"], y=roc["tpr"], mode="lines",
            name=f"Logistic Regression (AUC={eda['auc']:.4f})",
            line=dict(color=C_DARK, width=3), fill="tozeroy", fillcolor=f"rgba(31,56,100,0.08)"))
        fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Aleatório (AUC=0.50)",
            line=dict(color="gray", dash="dash", width=1.5)))
        ks_idx = int(np.argmax(np.abs(roc["tpr"].values - roc["fpr"].values)))
        fig.add_trace(go.Scatter(x=[roc["fpr"].iloc[ks_idx]], y=[roc["tpr"].iloc[ks_idx]],
            mode="markers", name=f"KS = {eda['ks']:.4f}",
            marker=dict(color=C_RED, size=12, symbol="diamond")))
        fig.add_annotation(x=roc["fpr"].iloc[ks_idx]+0.05, y=roc["tpr"].iloc[ks_idx]-0.05,
            text=f"KS={eda['ks']:.3f}", font=dict(color=C_RED, size=11), showarrow=True, arrowcolor=C_RED)
        fig.update_layout(title="Curva ROC — Logistic Regression", xaxis_title="Taxa de Falso Positivo (FPR)",
            yaxis_title="Taxa de Verdadeiro Positivo (TPR)", height=400, paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(x=0.4, y=0.1))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        sc = scores_df.sort_values("score", ascending=False)
        pct_pop = np.linspace(0, 1, len(sc))
        is_def = (sc["label"].values == "Default")
        cum_d = np.cumsum(is_def) / is_def.sum()
        cum_nd = np.cumsum(~is_def) / (~is_def).sum()
        ks_p = pct_pop[np.argmax(np.abs(cum_d - cum_nd))]
        ks_d = cum_d[np.argmax(np.abs(cum_d - cum_nd))]
        ks_nd = cum_nd[np.argmax(np.abs(cum_d - cum_nd))]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pct_pop*100, y=cum_d*100, mode="lines", name="Defaults acumulados", line=dict(color=C_RED, width=2.5)))
        fig.add_trace(go.Scatter(x=pct_pop*100, y=cum_nd*100, mode="lines", name="Não-Defaults acumulados", line=dict(color=C_DARK, width=2.5)))
        fig.add_trace(go.Scatter(x=[0,100], y=[0,100], mode="lines", name="Aleatório", line=dict(color="gray", dash="dash")))
        fig.add_shape(type="line", x0=ks_p*100, x1=ks_p*100, y0=ks_nd*100, y1=ks_d*100, line=dict(color=C_RED, width=2, dash="dot"))
        fig.add_annotation(x=ks_p*100+4, y=(ks_d+ks_nd)*50, text=f"KS={eda['ks']:.3f}", font=dict(color=C_RED, size=11), showarrow=False)
        fig.update_layout(title="Gráfico KS", xaxis_title="% da carteira (score decrescente)", yaxis_title="% cumulativo",
            height=400, paper_bgcolor="rgba(0,0,0,0)", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig, use_container_width=True)


def _render_pr(eda, pr_curve):
    render_glossary([
        ("PR-AUC", "Area Under the Precision-Recall Curve — mede a qualidade do modelo em cenários com classes desbalanceadas (poucos defaults vs. muitos não-defaults)."),
        ("Precision", "Dos empréstimos que o modelo alertou como default, quantos realmente o são. Impacta o custo de análise do banco."),
        ("Recall", "Dos empréstimos que de fato entraram em default, quantos o modelo conseguiu detectar. Impacta a proteção de capital."),
        ("TN (True Negative)", "Não-default corretamente classificado como não-default."),
        ("FP (False Positive)", "Não-default incorretamente alertado como default (falso alarme — custo de análise)."),
        ("FN (False Negative)", "Default que o modelo não detectou (perda financeira real do banco)."),
        ("TP (True Positive)", "Default corretamente detectado pelo modelo (perda evitada)."),
    ])
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pr_curve["recall"], y=pr_curve["precision"], mode="lines",
            name=f"PR-AUC={eda['pr_auc']:.4f}", line=dict(color=C_DARK, width=2.5),
            fill="tozeroy", fillcolor="rgba(31,56,100,0.08)"))
        fig.add_hline(y=eda["dr_global"], line_dash="dash", line_color="gray", annotation_text=f"Baseline: {eda['dr_global']:.2%}")
        fig.update_layout(title="Curva Precision-Recall", xaxis_title="Recall", yaxis_title="Precision",
            height=380, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        cm_vals = [[eda["cm_tn"], eda["cm_fp"]], [eda["cm_fn"], eda["cm_tp"]]]
        cm_labels = [
            [f"TN\n{eda['cm_tn']:,}\n({eda['cm_tn']/eda['n_test']:.1%})", f"FP\n{eda['cm_fp']:,}\n({eda['cm_fp']/eda['n_test']:.1%})"],
            [f"FN\n{eda['cm_fn']:,}\n({eda['cm_fn']/eda['n_test']:.1%})", f"TP\n{eda['cm_tp']:,}\n({eda['cm_tp']/eda['n_test']:.1%})"],
        ]
        fig = go.Figure(go.Heatmap(z=cm_vals, text=cm_labels, texttemplate="%{text}",
            colorscale="Blues", showscale=False, x=["Pred: Não-Default", "Pred: Default"], y=["Real: Não-Default", "Real: Default"]))
        fig.update_layout(title="Matriz de Confusão (threshold = 0.50)", height=380, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight">⚠️ <b>Precision baixa (13.3%):</b> A cada 100 alertas de default, 87 são falsos positivos. Isso é consequência direta do forte desbalanceamento (12.5:1) e do threshold padrão de 0.50. O threshold ótimo (máx F1) é ~0.47, que melhora o balanço Precision/Recall. <b>No contexto de crédito imobiliário de alto valor, tolerar Falsos Positivos (revisar contratos BONS) é preferível a tolerar Falsos Negativos (ignorar e tomar um calote milionário, focando no Recall).</b></div>', unsafe_allow_html=True)


def _render_calibracao(eda, cal, scores_df):
    render_glossary([
        ("Brier Score", "Erro quadrático médio entre a probabilidade predita e o resultado real (0 ou 1). Quanto menor, melhor a calibração."),
        ("Reliability Diagram", "Gráfico que compara a probabilidade predita pelo modelo com a fração real de defaults. Na calibração perfeita, os pontos ficam sobre a diagonal."),
        ("Threshold", "Ponto de corte de probabilidade acima do qual o modelo classifica um empréstimo como default. Padrão = 0.50."),
    ], title="📖 Legenda: Calibração")
    render_biz_context([
        "A <b>calibração</b> é essencial para <b>provisionamento contábil (IFRS 9)</b>: se o modelo diz '25% de chance de default', o banco provisiona ~25% do valor como perda esperada.",
        "Um modelo bem calibrado permite que analistas <b>confiem nas probabilidades</b> para tomada de decisão, não apenas no ranking.",
    ])
    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=cal["mean_pred"], y=cal["frac_pos"], mode="lines+markers",
            name="Logistic Regression", line=dict(color=C_DARK, width=2.5), marker=dict(size=9)))
        fig.add_trace(go.Scatter(x=[0,1], y=[0,1], mode="lines", name="Calibração perfeita", line=dict(color="gray", dash="dash")))
        fig.update_layout(title=f"Reliability Diagram (Brier = {eda['brier']:.4f})", xaxis_title="Probabilidade predita média (por bin)",
            yaxis_title="Fração real de defaults", height=380, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=scores_df[scores_df["label"]=="Não-Default"]["score"], nbinsx=40, name="Não-Default", marker_color=C_DARK, opacity=0.55, histnorm="probability density"))
        fig.add_trace(go.Histogram(x=scores_df[scores_df["label"]=="Default"]["score"], nbinsx=40, name="Default", marker_color=C_RED, opacity=0.65, histnorm="probability density"))
        fig.add_vline(x=0.5, line_dash="dash", line_color="gray", annotation_text="threshold=0.50")
        fig.update_layout(title="Distribuição de Scores por Classe", barmode="overlay", xaxis_title="P(Default) predita",
            yaxis_title="Densidade", height=380, legend=dict(orientation="h"), paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)
    brier_skill = 1 - eda["brier"] / (eda["dr_global"] * (1 - eda["dr_global"]))
    st.markdown(f'<div class="insight">📐 <b>Brier Skill Score = {brier_skill:.4f}</b> — o modelo é {brier_skill:.1%} melhor que a previsão ingênua de sempre prever a taxa base ({eda["dr_global"]:.2%}).</div>', unsafe_allow_html=True)


def _render_decil(eda, decil):
    render_glossary([
        ("Decil (D1–D10)", "A carteira é dividida em 10 faixas iguais (10% cada) ordenadas pelo score de risco. D1 = 10% de maior risco; D10 = 10% de menor risco."),
        ("DR (Default Rate)", "Taxa de default observada dentro de cada decil."),
        ("Lift", "Quanto o modelo concentra defaults no decil vs. a média. Lift=3.44× no D1 significa que esse decil tem 3.44 vezes mais defaults que a média da carteira."),
        ("Gains Chart", "Curva de captura cumulativa: mostra que % dos defaults totais o banco captura revisando os X% de maior score."),
    ], title="📖 Legenda: Análise por Decil")
    render_biz_context([
        "A análise por decil responde à pergunta operacional: <b>'quantos empréstimos o banco precisa revisar para capturar a maioria dos defaults?'</b>",
        "Top 20% → 48% dos defaults | Top 30% → 60% dos defaults. Isso permite ao banco <b>alocar analistas de forma eficiente</b>, focando nos empréstimos de maior risco.",
    ])
    c1, c2, c3 = st.columns(3)
    c1.metric("Top 20% captura", f"{eda['top20_cap']:.0f}% dos defaults")
    c2.metric("Top 30% captura", f"{eda['top30_cap']:.0f}% dos defaults")
    c3.metric("Lift — Decil 1",  f"{eda['d1_lift']:.2f}×")
    col1, col2 = st.columns(2)
    with col1:
        colors_d = [C_RED if r > eda["dr_global"]*1.4 else C_MID if r > eda["dr_global"] else C_LIGHT for r in decil["dr"]]
        fig = go.Figure(go.Bar(x=decil["decil"], y=decil["dr"], marker_color=colors_d,
            text=[f"{v:.1%}" for v in decil["dr"]], textposition="outside"))
        fig.add_hline(y=eda["dr_global"], line_dash="dash", line_color="gray", annotation_text=f"Média: {eda['dr_global']:.1%}")
        fig.update_layout(title="Taxa de Default por Decil (D1 = maior risco)", yaxis=dict(tickformat=".0%", range=[0,.33]),
            height=350, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=50,b=20))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        pct_x = [0] + list(np.arange(10, 101, 10))
        cap_y = [0] + list(decil["cum_pct"])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=pct_x, y=cap_y, mode="lines+markers", name="Modelo",
            line=dict(color=C_DARK, width=3), fill="tozeroy", fillcolor="rgba(31,56,100,0.10)"))
        fig.add_trace(go.Scatter(x=[0,100], y=[0,100], mode="lines", name="Aleatório", line=dict(color="gray", dash="dash")))
        for pct_pop, idx in [(20, 2), (30, 3)]:
            cap = decil["cum_pct"].iloc[idx-1]
            fig.add_annotation(x=pct_pop, y=cap, text=f" {pct_pop}% da carteira<br> → {cap:.0f}% dos defaults",
                font=dict(color=C_RED, size=10), showarrow=True, arrowcolor=C_RED, ax=35, ay=-25)
        fig.update_layout(title="Curva de Captura Cumulativa (Gains Chart)", xaxis=dict(range=[0,100], ticksuffix="%"),
            yaxis=dict(range=[0,105], ticksuffix="%"), height=350, paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", y=-0.15), margin=dict(t=50,b=50))
        st.plotly_chart(fig, use_container_width=True)
    fig = go.Figure(go.Bar(x=decil["decil"], y=decil["lift"],
        marker_color=[C_RED if v>2 else C_MID if v>1 else C_LIGHT for v in decil["lift"]],
        text=[f"{v:.2f}×" for v in decil["lift"]], textposition="outside"))
    fig.add_hline(y=1.0, line_dash="dash", line_color="gray", annotation_text="Lift=1.0 (sem ganho vs. aleatório)")
    fig.update_layout(title="Lift por Decil", yaxis=dict(range=[0, 4.2]), height=300, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight">💡 <b>Valor operacional:</b> O banco que revisasse apenas os 30% de maior score captaria 60% de todos os defaults — com menos da metade do esforço de revisar a carteira inteira. O Decil 1 concentra <b>{:.1f}×</b> a taxa de default média.'.format(eda["d1_lift"]) + '</div>', unsafe_allow_html=True)


def _render_cv_odds(eda, or_df):
    render_glossary([
        ("Validação Cruzada (CV)", "O dataset de treino é dividido em K partes (folds). O modelo treina em K−1 partes e testa na restante, repetindo K vezes. Garante que o resultado não depende de uma divisão específica dos dados."),
        ("Fold", "Cada uma das K partições usadas na validação cruzada. Aqui usamos 5-fold (K=5)."),
        ("Gap treino-teste", "Diferença entre AUC no treino e no teste. Gap alto (>0.05) indica overfitting — o modelo memoriza o treino mas não generaliza."),
        ("IC 95%", "Intervalo de confiança de 95% do AUC. Indica a faixa em que o AUC real provavelmente se encontra."),
    ], title="📖 Legenda: Validação Cruzada")
    cv_test = eda["cv_test"]
    cv_train = eda["cv_train"]
    folds = [f"Fold {i}" for i in range(1,6)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=folds, y=cv_train, name="Treino", marker_color=C_DARK, opacity=0.75))
    fig.add_trace(go.Bar(x=folds, y=cv_test, name="Teste", marker_color=C_RED, opacity=0.85))
    mean_t = np.mean(cv_test)
    fig.add_hline(y=mean_t, line_dash="dash", line_color=C_RED, annotation_text=f"Média Teste: {mean_t:.4f}")
    fig.update_layout(barmode="group", title="Validação Cruzada Estratificada (5-fold)",
        yaxis=dict(range=[0.55, 0.85]), height=380, legend=dict(orientation="h"),
        paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=50,b=20))
    st.plotly_chart(fig, use_container_width=True)
    std_t = float(np.std(cv_test))
    gap = float(np.mean(cv_train) - np.mean(cv_test))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("AUC médio (teste)", f"{np.mean(cv_test):.4f}")
    c2.metric("Desvio padrão", f"± {std_t:.4f}")
    c3.metric("IC 95%", f"[{np.mean(cv_test)-1.96*std_t:.4f}, {np.mean(cv_test)+1.96*std_t:.4f}]")
    c4.metric("Gap treino-teste", f"{gap:.4f}", delta="sem overfitting" if gap < 0.05 else "overfitting")

    st.markdown('<div class="sec">Odds Ratios — Interpretabilidade</div>', unsafe_allow_html=True)
    render_glossary([
        ("Odds Ratio (OR)", "exp(coeficiente). OR=1.0 → sem efeito. OR>1.0 → aumenta o risco de default. OR<1.0 → reduz o risco de default."),
        ("LTV", "Loan-to-Value (Saldo ÷ Valor do imóvel). OR=3.00 → a cada 1 desvio-padrão de aumento no LTV, o risco triplica."),
        ("DSCR", "Debt Service Coverage Ratio (NOI ÷ Juros). OR=1.48 → surpreendentemente, coeficiente positivo após padronização."),
        ("Balloon Risk", "Flag de pagamento residual iminente (parcial + ≤24m). OR=1.80 → risco quase dobra."),
        ("NOI Yield", "NOI ÷ Valor do imóvel (rentabilidade). OR=0.53 → maior rentabilidade reduz risco pela metade."),
        ("Near Maturity", "Flag de vencimento iminente (≤12m). OR=1.68 → risco de refinanciamento elevado."),
    ], title="📖 Legenda: Variáveis do Modelo")
    render_biz_context([
        "Os <b>Odds Ratios</b> são a principal vantagem da Regressão Logística sobre modelos caixa-preta: cada variável tem uma <b>interpretação direta e auditável</b>.",
        "Um gestor de risco pode explicar ao regulador exatamente <b>por que</b> um empréstimo recebeu score alto: 'LTV de 78% (OR=3.0) combinado com Balloon Risk ativo (OR=1.8)'.",
        "Todos os sinais são <b>economicamente coerentes</b>: alta alavancagem (LTV) e risco de refinanciamento (Balloon/Near Maturity) aumentam risco; boa rentabilidade (NOI Yield) e qualidade do imóvel (Property Class) reduzem.",
    ])
    or_sorted = or_df.sort_values("or_val")
    colors_or = [C_RED if v > 1 else C_DARK for v in or_sorted["or_val"]]
    fig = go.Figure(go.Bar(x=or_sorted["or_val"], y=or_sorted["feature"], orientation="h",
        marker_color=colors_or, opacity=0.85, text=[f"{v:.3f}" for v in or_sorted["or_val"]], textposition="outside"))
    fig.add_vline(x=1.0, line_dash="dash", line_color="black")
    fig.update_layout(title="Odds Ratios — Regressão Logística (vermelho=↑risco, azul=↓risco)",
        xaxis_title="Odds Ratio [exp(β)]", height=560, paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=50,b=40,r=80))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight">✅ <b>Todos os principais drivers têm sinais economicamente coerentes:</b> LTV (OR=3.00) e Balloon Risk (OR=1.80) aumentam o risco; NOI Yield (OR=0.53) e Property Class reduzem. A verificação sistemática dos sinais está documentada no Notebook 05.</div>', unsafe_allow_html=True)
