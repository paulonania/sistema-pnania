import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

st.title("📊 Relatório de Desempenho")

# COLETA RÁPIDA
cols = st.columns(3)
q1 = cols[0].number_input("Q1", 0.0, 15.0, 4.0)
q2 = cols[1].number_input("Q2", 0.0, 15.0, 5.5)
q3 = cols[2].number_input("Q3", 0.0, 15.0, 7.2)

# GRÁFICO SIMPLES
st.header("Penetrômetro")
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot([0, 1, 2], [q1, q2, q3], marker='o', lw=3)
ax.set_ylim(0, 10)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amort.', 'Trans.', 'Suporte'])
st.pyplot(fig)
