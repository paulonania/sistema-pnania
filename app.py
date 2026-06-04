import streamlit as st
import pandas as pd
# Importando explicitamente o pyplot para garantir que o NameError não ocorra
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Relatório de Desempenho")

# Estrutura básica para coletar dados sem travar
lista = []
for l in range(1, 3):
    for p in range(1, 3):
        with st.expander(f"Linha {l} - Ponto {p}"):
            c = st.columns(3)
            q1 = c[0].number_input(f"Q1_{l}_{p}", 0.0, 15.0, 4.0)
            q2 = c[1].number_input(f"Q2_{l}_{p}", 0.0, 15.0, 5.5)
            q3 = c[2].number_input(f"Q3_{l}_{p}", 0.0, 15.0, 7.2)
            lista.append({"Q1": q1, "Q2": q2, "Q3": q3})

df = pd.DataFrame(lista)

# Gráfico simples
if not df.empty:
    m = [df["Q1"].mean(), df["Q2"].mean(), df["Q3"].mean()]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot([0, 1, 2], m, marker='o')
    st.pyplot(fig)
else:
    st.write("Aguardando dados...")
