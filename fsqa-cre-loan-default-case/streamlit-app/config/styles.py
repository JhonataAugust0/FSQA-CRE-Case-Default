"""
CRE Default Dashboard — Injeção de CSS global.

Responsabilidade: gerenciar todos os estilos visuais customizados do dashboard.
"""

import streamlit as st


def inject_css():
    """Injeta o CSS global no app Streamlit."""
    st.markdown("""
<style>
/* Reset de propriedades para mesclar com o tema Light/Dark nativo do Streamlit */
[data-testid="stSidebar"] { 
    /* O Streamlit gerencia a cor do sidebar. Apenas o deixamos nativo. */
}

.page-title  { font-size:1.9rem; font-weight:800; color:var(--text-color); margin-bottom:0; }
.page-sub    { font-size:.95rem; color:var(--text-color); opacity: 0.8; margin-bottom:1.2rem; }

.sec         { font-size:1.05rem; font-weight:600; color:var(--text-color);
               border-bottom:2px solid var(--primary-color); padding-bottom:4px; margin:1.2rem 0 .8rem; }

.kpi         { background: rgba(100, 100, 100, 0.05); border-left:4px solid var(--primary-color);
               border-radius:8px; padding:14px 18px; }
.kpi-v       { font-size:1.8rem; font-weight:800; color:var(--text-color); line-height:1.1; }
.kpi-l       { font-size:.78rem; color:var(--text-color); opacity: 0.8; margin-top:2px; }

/* Badges de risco adaptativos com fundos translúcidos */
.badge-ok    { background:rgba(40, 167, 69, 0.15); color:#28a745; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; border:1px solid rgba(40,167,69,0.3); }
.badge-warn  { background:rgba(255, 193, 7, 0.15); color:#e0a800; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; border:1px solid rgba(255,193,7,0.3); }
.badge-risk  { background:rgba(220, 53, 69, 0.15); color:#dc3545; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; border:1px solid rgba(220,53,69,0.3); }

.insight     { background: rgba(220, 53, 69, 0.05); border-left:4px solid #dc3545;
               border-radius:6px; padding:10px 14px; font-size:.88rem; margin-top:8px; 
               color: var(--text-color); }

.limit-box   { background: rgba(255, 193, 7, 0.05); border-left:4px solid #FFC107;
               border-radius:6px; padding:10px 14px; font-size:.86rem; color: var(--text-color); }

.var-row     { display:grid; grid-template-columns:160px 80px 1fr;
               gap:8px; padding:6px 0; border-bottom:1px solid rgba(150, 150, 150, 0.2);
               font-size:.84rem; align-items:start; }
.var-name    { font-weight:600; color:var(--text-color); }
.var-type    { color:var(--primary-color); }
.caption     { font-size:.78rem; color:var(--text-color); opacity: 0.7; }

/* Caixas Glossário e Business com fundos translúcidos e adaptativos */
.glossary-box { background: rgba(100, 100, 100, 0.05);
               border:1px solid var(--primary-color); border-left:4px solid var(--primary-color);
               border-radius:8px; padding:12px 16px; font-size:.82rem;
               margin-bottom:12px; color:var(--text-color); }
.glossary-box b { color:var(--text-color); }
.glossary-box .gl-title { font-weight:700; font-size:.88rem; margin-bottom:6px;
                          display:flex; align-items:center; gap:6px; }
.glossary-box ul { margin:4px 0 0 8px; padding-left:14px; }
.glossary-box li { margin-bottom:3px; line-height:1.35; }

.biz-box    { background: rgba(255, 193, 7, 0.05);
              border:1px solid rgba(255, 193, 7, 0.3); border-left:4px solid #ffc107;
              border-radius:8px; padding:12px 16px; font-size:.82rem;
              margin-bottom:12px; color:var(--text-color); }
.biz-box b  { color:var(--text-color); }
.biz-box .biz-title { font-weight:700; font-size:.88rem; margin-bottom:6px;
                      display:flex; align-items:center; gap:6px; }
.biz-box ul { margin:4px 0 0 8px; padding-left:14px; }
.biz-box li { margin-bottom:3px; line-height:1.35; }
</style>
""", unsafe_allow_html=True)
