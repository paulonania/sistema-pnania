import streamlit as st
import matplotlib.pyplot as plt

st.title("Sistema Pnania - Base 1")

# Coleta de 3 pontos para teste
c = st.columns(3)
q1 = c[0].number_input("Amortecimento", 0.0, 15.0, 4.0)
q2 = c[1].number_input("Transição", 0.0, 15.0, 5.5)
q3 = c[2].number_input("Suporte", 0.0, 15.0, 7.2)

# Gráfico simples
fig, ax = plt.subplots(figsize=(5, 3))
ax.plot([0, 1, 2], [q1, q2, q3], marker='o', lw=3)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amort.', 'Trans.', 'Suporte'])
ax.set_ylim(0, 10)
st.pyplot(fig)
