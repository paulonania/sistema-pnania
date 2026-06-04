import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

st.set_page_config(layout="wide")
st.title("Relatorio de Desempenho")

cols = st.columns(3)
q1 = cols[0].number_input("Amortecimento", 0.0, 15.0, 4.0)
q2 = cols[1].number_input("Transicao", 0.0, 15.0, 5.5)
q3 = cols[2].number_input("Suporte", 0.0, 15.0, 7.2)

fig, ax = plt.subplots(figsize=(6, 3))
ax.plot([0, 1, 2], [q1, q2, q3], marker='o')
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amort', 'Trans', 'Suporte'])
ax.set_ylim(0, 10)
st.pyplot(fig)
