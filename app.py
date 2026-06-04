import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

st.set_page_config(layout="wide")
st.title("📊 Relatório de Desempenho - Padrão Pnania")

# COLETA
c = st.columns(3)
q1 = c[0].number_input("Amortecimento", 0.0, 15.0, 4.0)
q2 = c[1].number_input("Transição", 0.0, 15.0, 5.5)
q3 = c[2].number_input("Suporte", 0.0, 15.0, 7.2)

# GRÁFICO PROFISSIONAL
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot([0, 1, 2], [q1, q2, q3], marker='s', markersize=10, color='#0f3a61', lw=3)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amortecimento', 'Transição', 'Suporte'], fontweight='bold')
ax.set_ylim(0, 10)
ax.grid(axis='y', linestyle=':', color='gray')
ax.set_title("ÍNDICE DE PENETRÔMETRO", fontweight='bold', color='#0f3a61')

# TABELA
tab_data = [[f"{q1:.1f}", f"{q2:.1f}", f"{q3:.1f}"]]
table = ax.table(cellText=tab_data, rowLabels=['Pista Atual'], 
                 colLabels=['Amort.', 'Trans.', 'Suporte'],
                 loc='bottom', bbox=[0, -0.35, 1, 0.2])
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.subplots_adjust(bottom=0.3)

st.pyplot(fig)
