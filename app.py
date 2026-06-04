import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

st.set_page_config(layout="wide")
st.title("📊 Relatório de Desempenho Pnania")

# COLETA DE DADOS
c = st.columns(3)
q1 = c[0].number_input("Amortecimento", 0.0, 15.0, 4.0)
q2 = c[1].number_input("Transicao", 0.0, 15.0, 5.5)
q3 = c[2].number_input("Suporte", 0.0, 15.0, 7.2)

# GRÁFICO E TABELA PROFISSIONAL
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([0, 1, 2], [q1, q2, q3], marker='s', color='#0f3a61', lw=3)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amortecimento', 'Transicao', 'Suporte'])
ax.set_ylim(0, 10)
ax.grid(axis='y', linestyle=':')

# TABELA TÉCNICA
table = ax.table(cellText=[[f"{q1:.1f}", f"{q2:.1f}", f"{q3:.1f}"]],
                 colLabels=['Amort.', 'Trans.', 'Sup.'],
                 loc='bottom', bbox=[0, -0.3, 1, 0.2])
plt.subplots_adjust(bottom=0.2)

st.pyplot(fig)
