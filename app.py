import streamlit as st
import pandas as pd
# Importação forçada para evitar o NameError
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Relatório de Desempenho")

# 1. ENTRADA DE DADOS SIMPLIFICADA
cols = st.columns(3)
q1 = cols[0].number_input("Amortecimento", 0.0, 15.0, 4.0)
q2 = cols[1].number_input("Transição", 0.0, 15.0, 5.5)
q3 = cols[2].number_input("Suporte", 0.0, 15.0, 7.2)

# 2. GRÁFICO BLINDADO
st.header("Penetrômetro")
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([0, 1, 2], [q1, q2, q3], marker='o', color='#0f3a61', lw=3)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amort.', 'Trans.', 'Suporte'])
ax.set_ylim(0, 10)
ax.grid(axis='y', linestyle=':')

st.pyplot(fig)
