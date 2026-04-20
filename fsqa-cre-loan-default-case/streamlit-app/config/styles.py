"""
CRE Default Dashboard — Injeção de CSS global.

Responsabilidade: gerenciar todos os estilos visuais customizados do dashboard.
"""

import streamlit as st


def inject_css():
    """Injeta o CSS global no app Streamlit."""
    st.markdown("""
<style>
/* Cores Base para o Modo Claro */
:root {
    --bg-sidebar: #F0F4FA;
    --text-primary: #1F3864;
    --text-secondary: #595959;
    --border-accent: #2E75B6;
    --bg-kpi: #F0F4FA;
    --border-kpi: #2E75B6;
    --border-row: #eee;
    --bg-insight: #EFF5FB;
    --bg-limit: #FFF8E7;
    --text-limit: #664D03;
    --bg-glossary: linear-gradient(135deg,#F0F4FA 60%,#E8EFF9);
    --bg-biz: linear-gradient(135deg,#FFF8E7 60%,#FFF3CD);
}

/* Sobrescrita de Cores para o Modo Escuro */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-sidebar: #1E2129;
        --text-primary: #E2E8F0;
        --text-secondary: #A0AEC0;
        --border-accent: #63B3ED;
        --bg-kpi: #2D3748;
        --border-kpi: #63B3ED;
        --border-row: #2D3748;
        --bg-insight: #2A1F1F;
        --bg-limit: #3A2F1C;
        --text-limit: #FBD38D;
        --bg-glossary: linear-gradient(135deg,#2D3748 60%,#1A202C);
        --bg-biz: linear-gradient(135deg,#3A2F1C 60%,#2B2416);
    }
}

[data-testid="stSidebar"] { background: var(--bg-sidebar); }
.page-title  { font-size:1.9rem; font-weight:800; color:var(--text-primary); margin-bottom:0; }
.page-sub    { font-size:.95rem; color:var(--text-secondary); margin-bottom:1.2rem; }
.sec         { font-size:1.05rem; font-weight:600; color:var(--text-primary);
               border-bottom:2px solid var(--border-accent); padding-bottom:4px; margin:1.2rem 0 .8rem; }
.kpi         { background:var(--bg-kpi); border-left:4px solid var(--border-kpi);
               border-radius:8px; padding:14px 18px; }
.kpi-v       { font-size:1.8rem; font-weight:800; color:var(--text-primary); line-height:1.1; }
.kpi-l       { font-size:.78rem; color:var(--text-secondary); margin-top:2px; }
.badge-ok    { background:#D4EDDA; color:#155724; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; }
.badge-warn  { background:#FFF3CD; color:#856404; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; }
.badge-risk  { background:#F8D7DA; color:#721C24; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; }
.insight     { background:var(--bg-insight); border-left:4px solid #C00000;
               border-radius:6px; padding:10px 14px; font-size:.88rem; margin-top:8px; }
.limit-box   { background:var(--bg-limit); border-left:4px solid #FFC107;
               border-radius:6px; padding:10px 14px; font-size:.86rem; color:var(--text-limit); }
.var-row     { display:grid; grid-template-columns:160px 80px 1fr;
               gap:8px; padding:6px 0; border-bottom:1px solid var(--border-row);
               font-size:.84rem; align-items:start; }
.var-name    { font-weight:600; color:var(--text-primary); }
.var-type    { color:var(--border-accent); }
.caption     { font-size:.78rem; color:var(--text-secondary); }
.glossary-box { background:var(--bg-glossary);
               border:1px solid var(--border-kpi); border-left:4px solid var(--border-kpi);
               border-radius:8px; padding:12px 16px; font-size:.82rem;
               margin-bottom:12px; color:var(--text-primary); }
.glossary-box b { color:var(--text-primary); }
.glossary-box .gl-title { font-weight:700; font-size:.88rem; margin-bottom:6px;
                          display:flex; align-items:center; gap:6px; }
.glossary-box ul { margin:4px 0 0 8px; padding-left:14px; }
.glossary-box li { margin-bottom:3px; line-height:1.35; }
.biz-box    { background:var(--bg-biz);
              border:1px solid #FFC107; border-left:4px solid #FFC107;
              border-radius:8px; padding:12px 16px; font-size:.82rem;
              margin-bottom:12px; color:var(--text-limit); }
.biz-box b  { color:var(--text-limit); }
.biz-box .biz-title { font-weight:700; font-size:.88rem; margin-bottom:6px;
                      display:flex; align-items:center; gap:6px; }
.biz-box ul { margin:4px 0 0 8px; padding-left:14px; }
.biz-box li { margin-bottom:3px; line-height:1.35; }
</style>
""", unsafe_allow_html=True)
