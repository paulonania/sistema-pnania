import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
st.title("📊 Relatório de Desempenho")

# COLETA DE DADOS SIMPLIFICADA
st.header("Entrada de Dados")
lista = []
# Exemplo com 3 pontos para garantir que apareça na tela
for i in range(1, 4):
    c = st.columns(3)
    q1 = c[0].number_input(f"Q1_P{i}", 0.0, 15.0, 4.0)
    q2 = c[1].number_input(f"Q2_P{i}", 0.0, 15.0, 5.5)
    q3 = c[2].number_input(f"Q3_P{i}", 0.0, 15.0, 7.2)
    lista.append({"Q1": q1, "Q2": q2, "Q3": q3})

df = pd.DataFrame(lista)
m = [df["Q1"].mean(), df["Q2"].mean(), df["Q3"].mean()]

# GRÁFICO
st.header("Gráfico de Penetrômetro")
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot([0, 1, 2], m, marker='o', color='#0f3a61', lw=3)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amort.', 'Trans.', 'Suporte'])
ax.set_ylim(0, 10)
ax.grid(axis='y', linestyle=':')
st.pyplot(fig)
