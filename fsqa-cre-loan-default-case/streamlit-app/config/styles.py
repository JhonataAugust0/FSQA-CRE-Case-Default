"""
CRE Default Dashboard — Injeção de CSS global.

Responsabilidade: gerenciar todos os estilos visuais customizados do dashboard.
"""

import streamlit as st


def inject_css():
    """Injeta o CSS global no app Streamlit."""
    st.markdown("""
<style>
[data-testid="stSidebar"] { background: #F0F4FA; }
.page-title  { font-size:1.9rem; font-weight:800; color:#1F3864; margin-bottom:0; }
.page-sub    { font-size:.95rem; color:#595959; margin-bottom:1.2rem; }
.sec         { font-size:1.05rem; font-weight:600; color:#1F3864;
               border-bottom:2px solid #2E75B6; padding-bottom:4px; margin:1.2rem 0 .8rem; }
.kpi         { background:#F0F4FA; border-left:4px solid #2E75B6;
               border-radius:8px; padding:14px 18px; }
.kpi-v       { font-size:1.8rem; font-weight:800; color:#1F3864; line-height:1.1; }
.kpi-l       { font-size:.78rem; color:#595959; margin-top:2px; }
.badge-ok    { background:#D4EDDA; color:#155724; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; }
.badge-warn  { background:#FFF3CD; color:#856404; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; }
.badge-risk  { background:#F8D7DA; color:#721C24; font-size:.72rem;
               font-weight:600; padding:2px 7px; border-radius:10px; }
.insight     { background:#EFF5FB; border-left:4px solid #C00000;
               border-radius:6px; padding:10px 14px; font-size:.88rem; margin-top:8px; }
.limit-box   { background:#FFF8E7; border-left:4px solid #FFC107;
               border-radius:6px; padding:10px 14px; font-size:.86rem; }
.var-row     { display:grid; grid-template-columns:160px 80px 1fr;
               gap:8px; padding:6px 0; border-bottom:.5px solid #eee;
               font-size:.84rem; align-items:start; }
.var-name    { font-weight:600; color:#1F3864; }
.var-type    { color:#2E75B6; }
.caption     { font-size:.78rem; color:#888; }
.glossary-box { background:linear-gradient(135deg,#F0F4FA 60%,#E8EFF9);
               border:1px solid #BDD7EE; border-left:4px solid #2E75B6;
               border-radius:8px; padding:12px 16px; font-size:.82rem;
               margin-bottom:12px; color:#1F3864; }
.glossary-box b { color:#1F3864; }
.glossary-box .gl-title { font-weight:700; font-size:.88rem; margin-bottom:6px;
                          display:flex; align-items:center; gap:6px; }
.glossary-box ul { margin:4px 0 0 8px; padding-left:14px; }
.glossary-box li { margin-bottom:3px; line-height:1.35; }
.biz-box    { background:linear-gradient(135deg,#FFF8E7 60%,#FFF3CD);
              border:1px solid #FFE69C; border-left:4px solid #FFC107;
              border-radius:8px; padding:12px 16px; font-size:.82rem;
              margin-bottom:12px; color:#664D03; }
.biz-box b  { color:#664D03; }
.biz-box .biz-title { font-weight:700; font-size:.88rem; margin-bottom:6px;
                      display:flex; align-items:center; gap:6px; }
.biz-box ul { margin:4px 0 0 8px; padding-left:14px; }
.biz-box li { margin-bottom:3px; line-height:1.35; }
</style>
""", unsafe_allow_html=True)
