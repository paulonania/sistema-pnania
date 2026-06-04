import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from fpdf import FPDF
import io
import os

st.set_page_config(page_title="Sistema Pnania Premium", layout="wide")
st.title("📊 Relatório de Desempenho — Método Pnania")

# SIDEBAR CONFIG
with st.sidebar:
    nome_fazenda = st.text_input("Fazenda / Haras", "Fazenda Calunga")
    nome_pista = st.text_input("Pista", "Picadeiro")
    data_coleta = st.text_input("Data", "04/06/2026")
    n_linhas = st.number_input("Linhas (X)", 2, 10, 4)
    n_pontos = st.number_input("Pontos (Y)", 2, 10, 5)

# DADOS
lista = []
for l in range(1, n_linhas + 1):
    for p in range(1, n_pontos + 1):
        with st.expander(f"Linha {l} - Ponto {p}"):
            cols = st.columns(3)
            q1 = cols[0].number_input(f"Q1_{l}_{p}", 0.0, 15.0, 4.0)
            q2 = cols[1].number_input(f"Q2_{l}_{p}", 0.0, 15.0, 5.5)
            q3 = cols[2].number_input(f"Q3_{l}_{p}", 0.0, 15.0, 7.2)
            lista.append({"Linha": l, "Ponto": p, "Q1": q1, "Q2": q2, "Q3": q3})

df = pd.DataFrame(lista)

# CÁLCULOS
m_q1, m_q2, m_q3 = df["Q1"].mean(), df["Q2"].mean(), df["Q3"].mean()
io_q1 = (df["Q1"].std() / m_q1) * 100 if m_q1 > 0 else 0
io_q2 = (df["Q2"].std() / m_q2) * 100 if m_q2 > 0 else 0
io_q3 = (df["Q3"].std() / m_q3) * 100 if m_q3 > 0 else 0

# GRÁFICO
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([0, 1, 2], [m_q1, m_q2, m_q3], marker='o', linewidth=3, color='#0f3a61')
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amort.', 'Trans.', 'Suporte'])
ax.set_ylim(0, 10)
ax.grid(axis='y', linestyle=':')

# TABELA
tab_data = [[f"{m_q1:.1f}", f"{m_q2:.1f}", f"{m_q3:.1f}"], [f"{io_q1:.1f}%", f"{io_q2:.1f}%", f"{io_q3:.1f}%"]]
plt.table(cellText=tab_data, rowLabels=['Médias', 'IO'], colLabels=['Amort.', 'Trans.', 'Suporte'], loc='bottom', bbox=[0, -0.4, 1, 0.3])
plt.subplots_adjust(bottom=0.3)

st.pyplot(fig)

# LEGENDA
st.markdown("""
<div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px;">
    <strong>Legenda IO:</strong> 🟢 < 10% (Exc.) | 🟡 10-15% (Alerta) | 🔴 > 15% (Crítico)
</div>
""", unsafe_html=True)

# PDF
if st.sidebar.button("Gerar PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Relatorio Pnania", ln=True, align='C')
    img_buf = io.BytesIO()
    fig.savefig(img_buf, format='png')
    pdf.image(img_buf, x=10, y=30, w=180)
    st.sidebar.download_button("Baixar PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="laudo.pdf")
