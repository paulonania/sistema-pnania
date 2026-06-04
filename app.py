# GRÁFICO PADRÃO PNANIA
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot([0, 1, 2], [q1, q2, q3], marker='s', markersize=10, color='#0f3a61', lw=3)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amortecimento', 'Transição', 'Suporte'], fontweight='bold')
ax.set_ylim(0, 10)
ax.grid(axis='y', linestyle=':', color='gray')
ax.set_title("ÍNDICE DE PENETRÔMETRO", fontweight='bold', color='#0f3a61')

# TABELA DE DADOS
tab_data = [[f"{q1:.1f}", f"{q2:.1f}", f"{q3:.1f}"]]
plt.table(cellText=tab_data, rowLabels=['Pista Atual'], 
          colLabels=['Amort.', 'Trans.', 'Suporte'],
          loc='bottom', bbox=[0, -0.4, 1, 0.2])
plt.subplots_adjust(bottom=0.3)
st.pyplot(fig)
