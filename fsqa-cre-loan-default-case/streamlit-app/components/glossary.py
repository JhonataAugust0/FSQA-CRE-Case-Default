"""
CRE Default Dashboard — Componentes de glossário e contexto de negócio.

Responsabilidade: renderizar painéis informativos reutilizáveis.
"""

import streamlit as st


def render_glossary(items, title="📖 Legenda de Siglas"):
    """Renderiza um box de glossário sempre visível com as siglas e seus significados."""
    lis = "".join(f"<li><b>{k}</b> — {v}</li>" for k, v in items)
    st.markdown(
        f'<div class="glossary-box"><div class="gl-title">{title}</div>'
        f'<ul>{lis}</ul></div>',
        unsafe_allow_html=True)


def render_biz_context(items, title="💼 Relevância para o Negócio"):
    """Renderiza um box de contexto de negócio sempre visível."""
    lis = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(
        f'<div class="biz-box"><div class="biz-title">{title}</div>'
        f'<ul>{lis}</ul></div>',
        unsafe_allow_html=True)
