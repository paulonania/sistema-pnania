# 2. GRÁFICO PADRÃO PNANIA
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot([0, 1, 2], m, marker='o', color='#0f3a61', lw=3, markersize=8)
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(['Amortecimento', 'Transição', 'Suporte'], fontweight='bold')
ax.set_ylim(3, 8)
ax.grid(axis='y', linestyle=':', color='gray', alpha=0.6)

# TABELA DE DADOS PNANIA
tab_text = [[f"{m[0]:.1f}", f"{m[1]:.1f}", f"{m[2]:.1f}"], [f"{io[0]:.1f}%", f"{io[1]:.1f}%", f"{io[2]:.1f}%"]]
table = ax.table(cellText=tab_text, rowLabels=['Média (cm)', 'IO (%)'], 
                 colLabels=['Amort.', 'Trans.', 'Suporte'],
                 loc='bottom', bbox=[0, -0.4, 1, 0.25])
table.auto_set_font_size(False)
table.set_fontsize(10)
plt.subplots_adjust(bottom=0.3)

st.pyplot(fig)
