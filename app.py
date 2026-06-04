import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata
from fpdf import FPDF
import io
import os

# CONFIGURAÇÃO DA PÁGINA WEB
st.set_page_config(page_title="Sistema Pnania Premium", layout="wide")

st.title("📊 Gerador de Relatórios — Método Pnania")
st.markdown("Configure a malha de amostragem da pista e preencha os dados abaixo.")

# ==============================================================================
# 1. IDENTIFICAÇÃO E CONFIGURAÇÃO DA MALHA (BARRA LATERAL)
# ==============================================================================
with st.sidebar:
    st.header("📋 Identificação do Relatório")
    nome_fazenda = st.text_input("Nome da Fazenda / Haras", "Fazenda Calunga")
    nome_pista = st.text_input("Nome da Pista / Picadeiro", "Picadeiro Coberto")
    dimensao_pista = st.text_input("Dimensão da Pista", "30x50m")
    data_coleta = st.text_input("Data da Coleta", "04/06/2026")
    
    st.divider()
    st.header("🎯 Parâmetros Ideais da Pista")
    ideal_umi = st.text_input("Faixa Ideal de Umidade", "4.0% - 6.0%")
    ideal_esp = st.text_input("Espessura Ideal (cm)", "12 cm")
    
    st.divider()
    st.header("📝 Notas de Consultoria")
    txt_obs = st.text_area(
        "Manejo Prévio (O que foi feito antes)", 
        "Ex: Irrigado por 10 minutos, passou o rastelo com as hastes a 2 polegadas."
    )
    txt_parecer = st.text_area(
        "Diagnóstico e Parecer Técnico",
        "Ex: Após a escarificação a pista ficou muito solta, indicando a necessidade de passar o rastelo..."
    )
    
    st.divider()
    st.header("📐 Configuração da Grade")
    n_linhas = st.number_input("Número de Linhas (Eixo X)", min_value=2, max_value=10, value=4, step=1)
    n_pontos = st.number_input("Pontos por Linha (Eixo Y)", min_value=2, max_value=10, value=5, step=1)
    
    st.divider()
    st.header("⚙️ Opções de Entrada de Dados")
    coletou_umidade = st.checkbox("Coletar Umidade por Ponto", value=True)
    coletou_espessura = st.checkbox("Coletar Espessura por Ponto", value=True)
    
    st.markdown("---")
    st.markdown("**Valores Gerais da Pista (Caso não colete por ponto):**")
    global_umi = st.number_input("Umidade Geral Declarada (%)", min_value=0.0, max_value=100.0, value=4.5, step=0.1)
    global_esp = st.number_input("Espessura Geral Declarada (cm)", min_value=0, max_value=50, value=12, step=1)

# ==============================================================================
# 2. ENTRADA DE DADOS - Dados Coletados
# ==============================================================================
st.header("📋 Dados Coletados")
st.markdown("Insira os valores coletados para cada ponto da grade:")

lista_dados = []
abas = st.tabs([f"Linha {l}" for l in range(1, n_linhas + 1)])

for l_idx, aba in enumerate(abas):
    l = l_idx + 1
    with aba:
        for p in range(1, n_pontos + 1):
            st.markdown(f"**📍 Ponto {p}**")
            
            colunas_ativas = ["1ª Queda (cm)", "2ª Queda (cm)", "3ª Queda (cm)"]
            if coletou_umidade: colunas_ativas.append("Umidade (%)")
            if coletou_espessura: colunas_ativas.append("Espessura (cm)")
            
            cols = st.columns(len(colunas_ativas))
            with cols[0]: q1 = st.number_input("1ª Queda", min_value=0.0, max_value=15.0, value=4.0, step=0.1, key=f"q1_{l}_{p}")
            with cols[1]: q2 = st.number_input("2ª Queda", min_value=0.0, max_value=15.0, value=5.5, step=0.1, key=f"q2_{l}_{p}")
            with cols[2]: q3 = st.number_input("3ª Queda", min_value=0.0, max_value=15.0, value=7.2, step=0.1, key=f"q3_{l}_{p}")
            
            umi = global_umi
            esp = global_esp
            curr_idx = 3
            if coletou_umidade:
                with cols[curr_idx]: umi = st.number_input("Umidade (%)", min_value=0.0, max_value=100.0, value=4.5, step=0.1, key=f"umi_{l}_{p}")
                curr_idx += 1
            if coletou_espessura:
                with cols[curr_idx]: esp = st.number_input("Espessura (cm)", min_value=0, max_value=50, value=12, step=1, key=f"esp_{l}_{p}")
                
            lista_dados.append({
                "Haras": nome_fazenda, "Pista": nome_pista, "Dimensão": dimensao_pista, "Data": data_coleta, 
                "Linha": f"Linha {l}", "Ponto": f"Ponto {p}", "X": l, "Y": p, 
                "1ª Queda": q1, "2ª Queda": q2, "3ª Queda": q3, "Umidade": umi, "Espessura": esp
            })

df_dados = pd.DataFrame(lista_dados)

# ==============================================================================
# 3. PROCESSAMENTO E ESTATÍSTICA (MÉTODO PNANIA)
# ==============================================================================
if not df_dados.empty:
    med_amortecimento = df_dados["1ª Queda"].mean()
    med_transicao = df_dados["2ª Queda"].mean()
    med_suporte = df_dados["3ª Queda"].mean()
    medicao_atual = [med_amortecimento, med_transicao, med_suporte]
    
    # Cálculos isolados de IO para Umidade e Espessura
    io_umidade = (df_dados["Umidade"].std() / df_dados["Umidade"].mean()) * 100 if df_dados["Umidade"].mean() > 0 and coletou_umidade else 0.0
    io_espessura = (df_dados["Espessura"].std() / df_dados["Espessura"].mean()) * 100 if df_dados["Espessura"].mean() > 0 and coletou_espessura else 0.0
    
    umidade_media_geral = df_dados["Umidade"].mean() if coletou_umidade else global_umi
    espessura_media_geral = round(df_dados["Espessura"].mean()) if coletou_espessura else global_esp

    fases, verde_inf, verde_sup = ['Amortecimento', 'Transição', 'Suporte'], [3.5, 5.5, 7.0], [4.5, 6.5, 8.0]
    
    fig1, plt_ax1 = plt.subplots(figsize=(9, 6.5))
    plt_ax1.set_facecolor('#f4f4f6')
    x_indices = np.arange(len(fases))
    plt_ax1.fill_between(x_indices, verde_inf, verde_sup, color='#e2f0d9', alpha=0.7, label='Método Pnania')
    plt_ax1.plot(x_indices, verde_sup, color='#a9d08e', linestyle='--', linewidth=1.2)
    plt_ax1.plot(x_indices, verde_inf, color='#a9d08e', linestyle='--', linewidth=1.2)
    plt_ax1.plot(x_indices, medicao_atual, color='#0f3a61', linewidth=3.5, marker='s', markersize=12, markerfacecolor='white', markeredgewidth=3, label=f"{nome_pista}")
    
    for i, txt in enumerate(medicao_atual):
        plt_ax1.annotate(f'{txt:.1f}', (x_indices[i], medicao_atual[i]), textcoords="offset points", xytext=(0, 14), ha='center', fontweight='bold', fontsize=11, color='#0f3a61')
    
    plt_ax1.set_ylim(0, 10)
    plt_ax1.set_ylabel('Profundidade (cm)', fontsize=10, fontweight='bold', color='#555555')
    plt_ax1.set_xticks(x_indices)
    plt_ax1.set_xticklabels(fases, fontsize=10, fontweight='bold')
    plt_ax1.spines['top'].set_visible(False)
    plt_ax1.spines['right'].set_visible(False)
    plt_ax1.grid(axis='y', linestyle=':', alpha=0.5, color='#cccccc')
    plt.suptitle('ÍNDICE DE PENETRÔMETRO', fontsize=13, fontweight='bold', color='#0f3a61', y=0.98)
    plt.title(f"{nome_fazenda} — {nome_pista} — {data_coleta}", fontsize=9.5, pad=12, fontweight='bold', color='#555555')
    plt_ax1.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#e0e0e0', fontsize=9)
    
    # REMOVIDO O COLUNA DO IO GERAL DA TABELA DO PENETRÔMETRO
    colunas_tab = ['Amortecimento', 'Transição', 'Suporte', 'Umidade Pista', 'Espessura Méd.']
    dados_linha1 = [f"{verde_inf[0]:.1f} - {verde_sup[0]:.1f}", f"{verde_inf[1]:.1f} - {verde_sup[1]:.1f}", f"{verde_inf[2]:.1f} - {verde_sup[2]:.1f}", f"{ideal_umi}", f"{ideal_esp}"]
    dados_linha2 = [f"{medicao_atual[0]:.1f}", f"{medicao_atual[1]:.1f}", f"{medicao_atual[2]:.1f}", f"{umidade_media_geral:.1f}%", f"{espessura_media_geral} cm"]
    
    tabela = plt.table(cellText=[dados_linha1, dados_linha2], rowLabels=['Faixa Ideal', 'Pista Atual'], colLabels=colunas_tab, rowColours=['#f2f7fa', '#ffffff'], colColours=['#0f3a61']*len(colunas_tab), loc='bottom', cellLoc='center', bbox=[0.0, -0.24, 1.0, 0.14])
    tabela.set_fontsize(9)
    for (row, col), cell in tabela.get_celld().items():
        if row == 0: cell.get_text().set_color('white'); cell.get_text().set_weight('bold')
        if row > 0 and col >= 0: cell.get_text().set_weight('bold')
    plt.subplots_adjust(bottom=0.22, top=0.88)
    
    img_penetro = io.BytesIO()
    plt.savefig(img_penetro, format='png', bbox_inches='tight', dpi=150)
    img_penetro.seek(0)

    xi = np.linspace(1, n_linhas, 100)
    yi = np.linspace(1, n_pontos, 100)
    xi, yi = np.meshgrid(xi, yi)
    
    img_espessura = io.BytesIO()
    if coletou_espessura:
        zi_espessura = griddata((df_dados['X'], df_dados['Y']), df_dados['Espessura'], (xi, yi), method='cubic')
        fig2, plt_ax2 = plt.subplots(figsize=(7, 4.2))
        mapa1 = plt_ax2.imshow(zi_espessura, extent=[1, n_linhas, 1, n_pontos], origin='lower', cmap='turbo', aspect='auto')
        
        # IO ADICIONADO DIRETAMENTE NO TÍTULO DO MAPA
        plt_ax2.set_title(f'MAPA DE ESPESSURA DA CAMADA (IO: {io_espessura:.1f}%)', fontsize=11, fontweight='bold', color='#0f3a61', pad=12)
        plt_ax2.set_xlabel('Linhas de Coleta (Largura)', fontsize=9, fontweight='bold')
        plt_ax2.set_ylabel('Pontos de Coleta (Comprimento)', fontsize=9, fontweight='bold')
        plt_ax2.set_yticks(range(1, n_pontos + 1))
        plt_ax2.set_yticklabels([str(i) for i in range(1, n_pontos + 1)], fontsize=9, fontweight='bold')
        plt_ax2.set_xticks(range(1, n_linhas + 1))
        plt_ax2.set_xticklabels([f"L {i}" for i in range(1, n_linhas + 1)], fontsize=9)
        fig2.colorbar(mapa1, ax=plt_ax2).set_label('Espessura (cm)', fontsize=9, fontweight='bold')
        plt.savefig(img_espessura, format='png', bbox_inches='tight', dpi=150)
        img_espessura.seek(0)

    img_umidade = io.BytesIO()
    if coletou_umidade:
        zi_umidade = griddata((df_dados['X'], df_dados['Y']), df_dados['Umidade'], (xi, yi), method='cubic')
        fig3, plt_ax3 = plt.subplots(figsize=(7, 4.2))
        mapa2 = plt_ax3.imshow(zi_umidade, extent=[1, n_linhas, 1, n_pontos], origin='lower', cmap='turbo', aspect='auto')
        
        # IO ADICIONADO DIRETAMENTE NO TÍTULO DO MAPA
        plt_ax3.set_title(f'MAPA DE UMIDADE DA PISTA (IO: {io_umidade:.1f}%)', fontsize=11, fontweight='bold', color='#0f3a61', pad=12)
        plt_ax3.set_xlabel('Linhas de Coleta (Largura)', fontsize=9, fontweight='bold')
        plt_ax3.set_ylabel('Pontos de Coleta (Comprimento)', fontsize=9, fontweight='bold')
        plt_ax3.set_yticks(range(1, n_pontos + 1))
        plt_ax3.set_yticklabels([str(i) for i in range(1, n_pontos + 1)], fontsize=9, fontweight='bold')
        plt_ax3.set_xticks(range(1, n_linhas + 1))
        plt_ax3.set_xticklabels([f"L {i}" for i in range(1, n_linhas + 1)], fontsize=9)
        fig3.colorbar(mapa2, ax=plt_ax3).set_label('Umidade (%)', fontsize=9, fontweight='bold')
        plt.savefig(img_umidade, format='png', bbox_inches='tight', dpi=150)
        img_umidade.seek(0)

    # EXIBIÇÃO NA TELA
    st.divider()
    st.header("📈 Relatórios")
    
    col_g1, col_g2 = st.columns([1.2, 1.0])
    with col_g1:
        st.pyplot(fig1)
    with col_g2:
        if coletou_espessura: st.pyplot(fig2)
        if coletou_umidade: st.pyplot(fig3)

    # EMISSÃO DO LAUDO EM PDF (LIMITADO A 2 PÁGINAS)
    with st.sidebar:
        st.divider()
        st.header("📄 Emissão de Documento")
        
        if st.button("✨ Gerar Relatório em PDF"):
            pdf = FPDF(orientation="P", unit="mm", format="A4")
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            
            if os.path.exists("logo.png"):
                pdf.image("logo.png", x=10, y=10, w=45)
                pdf.set_y(34)
            else:
                pdf.set_y(15)
            
            pdf.set_font("Helvetica", "B", 18)
            pdf.set_text_color(15, 58, 97)
            pdf.cell(0, 12, "RELATÓRIO DE DESEMPENHO".encode('latin-1', 'replace').decode('latin-1'), ln=True, align="C")
            
            pdf.set_draw_color(220, 222, 225)
            pdf.line(10, 48, 200, 48)
            pdf.set_y(52)
            
            pdf.set_text_color(50, 50, 50)
            pdf.set_fill_color(245, 247, 250)
            pdf.set_font("Helvetica", "B", 10)
            
            txt_quadro = "  DADOS DA PROPRIEDADE E DA COLETA"
            pdf.cell(0, 6, txt_quadro.encode('latin-1', 'replace').decode('latin-1'), ln=True, fill=True)
            
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(40, 6, " Fazenda / Haras: ", border="LT")
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(0, 6, f"{nome_fazenda}".encode('latin-1', 'replace').decode('latin-1'), border="RT", ln=True)
            
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(40, 6, " Pista / Picadeiro: ", border="L")
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(0, 6, f"{nome_pista} ({dimensao_pista})".encode('latin-1', 'replace').decode('latin-1'), border="R", ln=True)
            
            pdf.set_font("Helvetica", "", 9)
            pdf.cell(40, 6, " Data da Coleta: ", border="LB")
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(0, 6, f"{data_coleta}".encode('latin-1', 'replace').decode('latin-1'), border="RB", ln=True)
            
            if txt_obs:
                pdf.ln(2)
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(40, 6, " Manejo Prévio: ".encode('latin-1', 'replace').decode('latin-1'), border="LBT", fill=True)
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 6, f"{txt_obs}".encode('latin-1', 'replace').decode('latin-1'), border="RBT")
            
            if txt_parecer:
                pdf.ln(1)
                pdf.set_font("Helvetica", "B", 9)
                pdf.cell(40, 6, " Parecer Técnico: ".encode('latin-1', 'replace').decode('latin-1'), border="LBT", fill=True)
                pdf.set_font("Helvetica", "", 9)
                pdf.multi_cell(0, 6, f"{txt_parecer}".encode('latin-1', 'replace').decode('latin-1'), border="RBT")
            
            pdf.ln(4)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 6, "1. Perfil de Compactação (Índice de Penetrômetro)".encode('latin-1', 'replace').decode('latin-1'), ln=True)
            pdf.ln(1)
            pdf.image(img_penetro, x=15, w=180)
            
            # --- PÁGINA 2: MAPAS ---
            if coletou_espessura or coletou_umidade:
                pdf.add_page()
                if os.path.exists("logo.png"):
                    pdf.image("logo.png", x=10, y=8, w=25)
                
                pdf.line(10, 20, 200, 20)
                pdf.set_text_color(50, 50, 50)
                pdf.set_y(26)
                pdf.set_font("Helvetica", "B", 11)
                pdf.cell(0, 6, "2. Distribuição Espacial e Mapas de Calor".encode('latin-1', 'replace').decode('latin-1'), ln=True)
                pdf.ln(4)
                
                if coletou_espessura:
                    pdf.image(img_espessura, x=35, w=140)
                    pdf.ln(10)
                if coletou_umidade:
                    pdf.image(img_umidade, x=35, w=140)
            
            pdf_output = pdf.output()
            st.download_button(
                label="📥 Baixar Laudo Técnico (.PDF)", 
                data=bytes(pdf_output), 
                file_name=f"Relatorio_Desempenho_{nome_fazenda.replace(' ', '_')}.pdf", 
                mime="application/pdf"
            )

        # Botão de CSV organizado
        df_exportar = df_dados.drop(columns=["X", "Y"]).rename(columns={
            "1ª Queda": "1ª Queda - Amortecimento (cm)", 
            "2ª Queda": "2ª Queda - Transição (cm)", 
            "3ª Queda": "3ª Queda - Suporte (cm)", 
            "Umidade": "Umidade TDR (%)", 
            "Espessura": "Espessura da Camada (cm)"
        })
        csv_data = df_exportar.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Baixar Tabela de Campo (.CSV)", data=csv_data, file_name=f"Levantamento_{nome_fazenda.replace(' ', '_')}_{data_coleta.replace('/', '-')}.csv", mime='text/csv')
else:
    st.warning("A planilha está vazia!")
