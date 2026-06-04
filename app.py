import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fpdf import FPDF
import io

# [BLOCO 1: CONFIG E DADOS]
st.set_page_config(layout="wide")
st.title("📊 Relatório de Desempenho")
lista = []
for l in range(1, 5):
    for p in range(1, 6):
        with st.expander(f"L{l}-P{p}"):
            c = st.columns(3)
            q1 = c[0].number_input(f"Q1_{l}_{p}", 0.0, 15.0, 4.0)
            q2 = c[1].number_input(f"Q2_{l}_{p}", 0.0, 15.0, 5.5)
            q3 = c[2].number_input(f"Q3_{l}_{p}", 0.0, 15.0, 7.2)
            lista.append({"Q1":q1, "Q2":q2, "Q3":q3})
df = pd.DataFrame(lista)

# [BLOCO 2: GRÁFICO E IO]
m = [df["Q1"].mean(), df["Q2"].mean(), df["Q3"].mean()]
io = [(df["Q1"].std()/m[0])*100, (df["Q2"].std()/m[1])*100, (df["Q3"].std()/m[2])*100]
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot([0,1,2], m, marker='o', color='#0f3a61', lw=3)
ax.set_xticks([0,1,2])
ax.set_xticklabels(['Amort.', 'Trans.', 'Suporte'])
ax.grid(axis='y', linestyle=':')
st.pyplot(fig)

# [BLOCO 3: LEGENDA E PDF]
st.markdown("🟢 < 10% | 🟡 10-15% | 🔴 > 15%")
if st.button("Gerar PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Relatorio", ln=True, align='C')
    img = io.BytesIO()
    fig.savefig(img, format='png')
    pdf.image(img, x=10, y=30, w=150)
    st.download_button("Baixar", pdf.output(dest='S').encode('latin-1'), "laudo.pdf")
