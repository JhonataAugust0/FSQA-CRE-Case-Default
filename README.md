# CRE Loan Default — Modelagem Preditiva de Risco de Crédito Imobiliário

> **Oliver Wyman · FSQA Take-Home Case · Campus Recruiting 2026**

Modelo preditivo para estimar a probabilidade de **default em empréstimos comerciais imobiliários (CRE)** no horizonte de 12 meses, construído sobre uma amostra de 8.959 empréstimos históricos de um banco. O projeto cobre o pipeline completo de Data Science — da limpeza de dados brutos até um dashboard interativo de análise.

---

## Resultados Principais

| Métrica | Valor | Benchmark da indústria |
|---------|-------|----------------------|
| AUC-ROC | **0.7335** | > 0.70 ✅ |
| Gini | **0.4671** | > 0.40 ✅ |
| KS Statistic | **0.3366** | > 0.30 ✅ |
| Recall (threshold=0.5) | **66.2%** | — |
| Brier Score | 0.2096 | — |

**Poder operacional:** revisando os 30% da carteira com maior score de risco, o modelo captura **60% de todos os defaults** — o dobro da eficiência de uma revisão aleatória.

---

## Estrutura do Repositório

```
fsqa-cre-loan-default-case/
│
├── data/
│   ├── raw/                        ← colocar o CSV original aqui (ver abaixo)
│   └── processed/                  ← gerado automaticamente pelos notebooks
│
├── notebooks/
│   ├── 01_ETL.ipynb                ← Fase 1: limpeza e padronização dos dados
│   ├── 02_EDA.ipynb                ← Fase 2: análise exploratória de dados
│   ├── 03_features.ipynb           ← Fase 3: feature engineering
│   ├── 04_modeling.ipynb           ← Fase 4: treinamento e comparação de modelos
│   └── 05_evaluation.ipynb         ← Fase 5: avaliação completa de performance
│
├── outputs/
│   ├── eda/                        ← figuras geradas pelo NB02
│   └── evaluation/                 ← figuras da avaliação final (NB05)
│   ├── features/                   ← figuras geradas pelo NB03
│   ├── modeling/                   ← figuras e tabela comparativa (NB04)
│   ├── models/                     ← modelos serializados (.joblib)
│
├── streamlit-app/                  ← Dashboard Streamlit modularizado
│   ├── components/                 ← Componentes visuais e auxiliares
│   ├── config/                     ← Configurações de tema e estilização
│   ├── data/                       ← Carregamento e cache dos dados
│   ├── pages_app/                  ← Telas/Páginas individuais do dashboard
│   └── app.py                      ← Ponto de entrada da aplicação Streamlit
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Pré-requisitos

- Python 3.10+
- pip

---

## Instalação

```bash
git clone https://github.com/JhonataAugust0/FSQA-CRE-Case-Default.git
cd FSQA-CRE-Case-Default/

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

---

## Executando os Notebooks

Execute os notebooks **em ordem** — cada um depende do output do anterior:

```bash
jupyter notebook
```

| Notebook | Input | Output |
|----------|-------|--------|
| `01_ETL.ipynb` | `data/raw/*.csv` | `data/processed/df_clean.csv` |
| `02_EDA.ipynb` | `df_clean.csv` | figuras em `outputs/eda/` |
| `03_features.ipynb` | `df_clean.csv` | `data/processed/df_features.csv` |
| `04_modeling.ipynb` | `df_features.csv` | modelos em `outputs/models/` |
| `05_evaluation.ipynb` | `df_features.csv` + modelos | figuras em `outputs/evaluation/` |

---

## Dashboard Interativo (Streamlit)

O dashboard apresenta todos os resultados do projeto de forma interativa, organizado em 8 seções navegáveis.

### Rodando localmente

```bash
streamlit run app.py
```

O app abre automaticamente em `http://localhost:8501`.

### Seções do Dashboard

| Seção | Conteúdo |
|-------|----------|
| 🏠 Introdução | Contexto do problema, resultados em destaque |
| 📋 Dataset & Variáveis | Dicionário das 15 variáveis originais + 9 features derivadas |
| 📊 Fase 1 — ETL | Problemas encontrados no CSV bruto, DQ checks, schema final |
| 🔍 Fase 2 — EDA | Taxa de default por categoria, variáveis numéricas (boxplot + histograma interativo), correlações, análise temporal |
| ⚙️ Fase 3 — Features | Distribuição de LTV e DSCR por grupo, encoding, winsorizing |
| 🤖 Fase 4 — Modelagem | Comparativo de 3 modelos, justificativa da escolha, tratamento do desbalanceamento |
| 🎯 Fase 5 — Avaliação | Curva ROC, KS, PR, calibração, análise por decil (lift, gains chart), validação cruzada, odds ratios |
| ⚠️ Limitações | 7 limitações documentadas com impacto e mitigação |

### Modo standalone (sem rodar os notebooks)

O dashboard funciona **sem necessidade de rodar os notebooks** — todos os dados de análise e resultados dos modelos estão disponíveis no repositório, extraídos da execução real dos modelos. Isso permite avaliação imediata do projeto sem replicar o treinamento.

---

## Pipeline de Feature Engineering

A classe `CREFeatureEngineer` (Notebook 03) deriva 9 indicadores financeiros das variáveis originais:

| Feature | Fórmula | Interpretação |
|---------|---------|---------------|
| `ltv` | Saldo / Valor do Imóvel | Alavancagem. LTV > 1 = saldo supera a garantia |
| `dscr` | NOI / Juros Anuais | DSCR < 1 = imóvel não cobre os juros |
| `noi_yield` | NOI / Valor do Imóvel | Cap rate implícito do ativo |
| `loan_age_months` | Prazo − Meses até Vencimento | Tempo de vida do empréstimo |
| `amortization_rate` | 1 − Saldo / Valor Original | Proporção do principal já quitado |
| `near_maturity_flag` | 1 se MTM ≤ 12 meses | Risco de refinanciamento iminente |
| `balloon_risk` | 1 se Parcial E MTM ≤ 24m | Balloon payment iminente |
| `is_office` | 1 se tipo = Office | Indicador binário de tipo de ativo |
| `property_class_ord` | C=1, B=2, A=3, outros=0 | Encoding ordinal de qualidade |

---

## Modelo Selecionado

**Regressão Logística** com regularização L2 e `class_weight='balanced'`, treinada dentro de um `sklearn.Pipeline` com `ColumnTransformer` (StandardScaler nas features contínuas, passthrough nas binárias e ordinais).

A escolha prioriza **interpretabilidade** sobre performance máxima: os odds ratios permitem explicar cada predição ao gestor de risco e ao regulador, requisito para uso em ambiente bancário regulado (Basileia II/III).

### Top drivers de risco (Odds Ratios)

| Feature | Odds Ratio | Interpretação |
|---------|-----------|---------------|
| LTV | **3.003** | Maior alavancagem → mais risco |
| Balloon Risk | **1.802** | Balloon payment iminente → mais risco |
| Near Maturity | **1.676** | Vencimento próximo → mais risco |
| NOI Yield | **0.534** | Maior rentabilidade do ativo → menos risco |
| Property Class | **0.939** | Maior qualidade → menos risco |

---

## Sobre o Uso de IA Generativa

Ferramentas de IA Generativa (Claude, Anthropic) foram utilizadas nas seguintes atividades de suporte:

- Estruturação do documento executivo de planejamento metodológico
- Revisão pontual de sintaxe de bibliotecas Python (scikit-learn, imblearn, SHAP)

---

## Dependências

```
pandas>=3.0
numpy>=2.4
matplotlib>=3.10
seaborn>=0.13
scikit-learn>=1.8
joblib>=1.5
streamlit>=1.56
plotly>=6.7
jupyter>=1.1
```

---
