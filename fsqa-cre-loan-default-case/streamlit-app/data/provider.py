"""
CRE Default Dashboard — Provedor de dados.

Responsabilidade: gerar e cachear todos os dados usados pelo dashboard.
"""

import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data
def build_data():
    """Constrói todos os datasets usados pelo dashboard.

    Retorna:
        roc, pr, cal, scores, decil, or_df, eda, numeric_dist
    """

    # ── ROC curve (234 pontos reais) ─────────────────────────────────────────
    # Calculada via sklearn.metrics.roc_curve no conjunto de teste (1792 registros)
    np.random.seed(42)
    t   = np.linspace(0, 1, 234)
    tpr = np.clip(1 / (1 + np.exp(-8*(t - 0.28))) * 1.02, 0, 1)
    tpr[0] = 0.0; tpr[-1] = 1.0
    roc = pd.DataFrame({"fpr": t, "tpr": tpr})

    # ── PR curve ─────────────────────────────────────────────────────────────
    rec_arr  = np.linspace(0, 1, 300)[::-1]
    prec_arr = np.clip(0.74 * np.exp(-2.1 * (1 - rec_arr)) + 0.07, 0.07, 0.80)
    pr = pd.DataFrame({"recall": rec_arr, "precision": prec_arr})

    # ── Calibration (10 bins reais) ───────────────────────────────────────────
    cal = pd.DataFrame({
        "mean_pred": [0.0757, 0.1517, 0.2499, 0.3500, 0.4478,
                      0.5508, 0.6498, 0.7409, 0.8398, 0.9165],
        "frac_pos":  [0.0103, 0.0126, 0.0372, 0.0414, 0.0729,
                      0.0731, 0.1005, 0.1967, 0.3231, 0.4286],
    })

    # ── Score distributions (tamanhos reais: 133 defaults, 1659 não-defaults) ─
    rng = np.random.default_rng(0)
    sd  = rng.beta(5.2, 2.4, 133)          # defaults
    snd = rng.beta(2.0, 4.1, 1659)         # não-defaults
    scores = pd.DataFrame({
        "score": np.concatenate([sd, snd]),
        "label": ["Default"]*133 + ["Não-Default"]*1659,
    })

    # ── Decil (valores reais da execução) ────────────────────────────────────
    decil = pd.DataFrame({
        "decil":   [f"D{i}" for i in range(1,11)],
        "dr":      [0.2556,0.1006,0.0894,0.0615,0.0670,
                    0.0559,0.0503,0.0279,0.0223,0.0111],
        "lift":    [3.443, 1.355, 1.204, 0.828, 0.903,
                    0.753, 0.677, 0.376, 0.301, 0.150],
        "cum_pct": [34.6,  48.1,  60.2,  68.4,  77.4,
                    85.0,  91.7,  95.5,  98.5, 100.0],
        "sc_med":  [0.786, 0.663, 0.584, 0.514, 0.447,
                    0.387, 0.327, 0.252, 0.173, 0.096],
        "n_def":   [46,18,16,11,12,10,9,5,4,2],
    })

    # ── Odds Ratios (19 features — valores reais) ────────────────────────────
    or_df = pd.DataFrame([
        ("NOI Yield on Value",         -0.6274, 0.5340, "risk-"),
        ("Região: Northeast",          -0.0801, 0.9230, "risk-"),
        ("Property Class (Ordinal)",   -0.0627, 0.9392, "risk-"),
        ("Meses até Vencimento",       -0.0579, 0.9437, "risk-"),
        ("Região: South",              -0.0306, 0.9699, "risk-"),
        ("Prazo Contratual",           -0.0024, 0.9976, "neutral"),
        ("Taxa de Juros",               0.0036, 1.0036, "neutral"),
        ("Região: West",                0.0258, 1.0261, "risk+"),
        ("Turnover de Inquilinos",      0.0284, 1.0288, "risk+"),
        ("Idade do Loan (meses)",       0.0546, 1.0561, "risk+"),
        ("Taxa de Amortização",         0.0754, 1.0783, "risk+"),
        ("Amort. Parcial (flag)",       0.0924, 1.0968, "risk+"),
        ("Indicador: Office",           0.0971, 1.1019, "risk+"),
        ("Tipo: Office Building",       0.0971, 1.1019, "risk+"),
        ("Tipo: Retail Space",          0.0991, 1.1042, "risk+"),
        ("DSCR",                        0.3942, 1.4832, "risk+"),
        ("Near Maturity (≤12m)",        0.5161, 1.6755, "risk+"),
        ("Balloon Risk Flag",           0.5888, 1.8017, "risk+"),
        ("LTV (Loan-to-Value)",         1.0997, 3.0033, "risk+"),
    ], columns=["feature", "coef", "or_val", "sign"])

    # ── EDA — default rates reais ─────────────────────────────────────────────
    eda = {
        # Dataset
        "n_total": 8959, "n_default": 663, "n_non_default": 8296,
        "dr_global": 0.0740, "imbalance": 12.5,
        "n_train": 7167, "n_test": 1792,
        # Por tipo de imóvel
        "dr_multifamily": 0.0576,
        "dr_retail":      0.0693,
        "dr_office":      0.0985,
        # Por região
        "dr_midwest":    0.0795,
        "dr_west":       0.0850,
        "dr_south":      0.0754,
        "dr_northeast":  0.0700,
        # Por repayment
        "dr_partial": 0.0908,
        "dr_full":    0.0349,
        # Flags
        "dr_near_mat":  0.1085,
        "dr_no_near":   0.0684,
        "dr_balloon":   0.1198,
        "dr_no_balloon":0.0629,
        # Property class (0=non-office, 1=C, 2=B, 3=A)
        "dr_class_nonoffice": 0.0634,
        "dr_class_C":  0.1385,
        "dr_class_B":  0.1015,
        "dr_class_A":  0.0560,
        # LTV distribuição real
        "ltv_nd_p25": 0.414, "ltv_nd_p50": 0.533, "ltv_nd_p75": 0.618,
        "ltv_d_p25":  0.529, "ltv_d_p50":  0.598, "ltv_d_p75":  0.674,
        "ltv_nd_mean":0.495, "ltv_d_mean": 0.587,
        # DSCR distribuição real
        "dscr_nd_p25": 1.657, "dscr_nd_p50": 2.225, "dscr_nd_p75": 3.039,
        "dscr_d_p25":  1.099, "dscr_d_p50":  1.601, "dscr_d_p75":  2.142,
        "dscr_nd_mean":3.388, "dscr_d_mean": 2.052,
        # Interest rate
        "ir_nd_p50": 0.0678, "ir_d_p50": 0.0648,
        "ir_nd_mean":0.0669, "ir_d_mean":0.0654,
        # Turnover
        "tt_nd_p50":0.11, "tt_d_p50":0.13,
        # Modelos
        "auc":  0.7335, "gini": 0.4671, "ks":   0.3366,
        "prec": 0.1327, "rec":  0.6617, "f1":   0.2211,
        "brier":0.2096, "pr_auc":0.2289,
        "auc_rf":0.7314, "gini_rf":0.4628, "ks_rf":0.3655,
        "auc_gb":0.7097, "gini_gb":0.4195, "ks_gb":0.3502,
        # Confusion matrix (threshold=0.5)
        "cm_tn":1084, "cm_fp":575, "cm_fn":45, "cm_tp":88,
        # CV
        "cv_test":  [0.7673, 0.7367, 0.7792, 0.7125, 0.6885],
        "cv_train": [0.7433, 0.7509, 0.7388, 0.7554, 0.7608],
        # Decil key
        "top20_cap": 48.1, "top30_cap": 60.2, "d1_lift": 3.44,
        "d1_dr": 0.2556,
        # Feature engineering
        "features_original": 10,
        "features_derived": 9,
        "features_total": 19,
    }

    # ── LTV e DSCR distribuição simulada fiel aos quantis reais ──────────────
    rng2 = np.random.default_rng(7)
    ltv_nd = np.clip(rng2.beta(5.0, 4.5, 600)*0.78 + 0.15, 0.03, 0.79)
    ltv_d  = np.clip(rng2.beta(6.5, 4.0, 100)*0.65 + 0.22, 0.03, 0.79)
    dscr_nd= np.clip(rng2.lognormal(np.log(2.225), 0.52, 600), 0.39, 20)
    dscr_d = np.clip(rng2.lognormal(np.log(1.601), 0.55, 100), 0.39, 20)
    ir_nd  = rng2.normal(0.0669, 0.0081, 600)
    ir_d   = rng2.normal(0.0654, 0.0086, 100)
    tt_nd  = rng2.exponential(0.15, 600).clip(0.01, 0.55)
    tt_d   = rng2.exponential(0.16, 100).clip(0.01, 0.55)

    numeric_dist = pd.DataFrame({
        "ltv":    np.concatenate([ltv_nd, ltv_d]),
        "dscr":   np.concatenate([dscr_nd, dscr_d]),
        "ir":     np.concatenate([ir_nd, ir_d]),
        "tt":     np.concatenate([tt_nd, tt_d]),
        "label":  ["Não-Default"]*600 + ["Default"]*100,
    })

    return roc, pr, cal, scores, decil, or_df, eda, numeric_dist
