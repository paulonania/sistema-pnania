import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from fpdf import FPDF
import io
import os

st.set_page_config(layout="wide")
st.title("📊 Relatório de Desempenho")

with st.sidebar:
    st.header("Configurações")
    nome_f = st.text_input("Fazenda", "Fazenda Calunga")
    data = st.text_input("Data", "04/06/2026")
    n_l = st.number_input("Linhas", 2, 10, 4)
    n_p = st.number_input("Pontos", 2, 10, 5)

lista = []
for l in range(1, n_l + 1):
    for p in range(1, n_p + 1):
        with st.expander(f"L{l}-P{p}"):
            c = st.columns(3)
            q1 = c[0].number_input(f"Q1_{l}_{p}", 0.0, 15.0, 4.0)
            q2 = c[1].number_input(f"Q2_{l}_{p}", 0.0, 15.0, 5.5)
            q3 = c[2].number_input(f"Q3_{l}_{p}", 0.0, 15.0, 7.2)
            lista.append({"L": l, "P": p, "Q1": q1, "Q2": q2, "Q3": q3})

df = pd.DataFrame(lista)
m = [df["Q1"].mean(), df["Q2"].mean(), df["Q3"].mean()]
io = [(df["Q1"].std()/m[0])*100, (df["Q2"].std()/m[1])*100, (df["Q3"].std()/m[2])*100]

fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([0,1,2], m, marker='o', color='#0f3a61', lw=3)
ax.set_xticks([0,1,2])
ax.set_xticklabels(['Amort.', 'Trans.', 'Suporte'])
ax.set_ylim(0, 10)
ax.grid(axis='y', linestyle=':')

tab_txt = [[f"{v:.1f}" for v in m], [f"{v:.1f}%" for v in io]]
plt.table(cellText=tab_txt, rowLabels=['Média', 'IO'], 
          colLabels=['Amort.', 'Trans.', 'Suporte'], 
          loc='bottom', bbox=[0, -0.5, 1, 0.3])
plt.subplots_adjust(bottom=0.3)

st.pyplot(fig)

st.markdown("""
<div style="background:#f0f2f6; padding:10px; border-radius:5px;">
    <strong>Legenda:</strong> 🟢 < 10% | 🟡 10-15% | 🔴 > 15%
</div>
""", unsafe_html=True)

if st.sidebar.button("Gerar PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"Laudo {nome_f} - {data}", ln=True, align='C')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    pdf.image(buf, x=10, y=30, w=150)
    st.sidebar.download_button("Baixar PDF", pdf.output(dest='S').encode('latin-1'), "laudo.pdf", "application/pdf")
