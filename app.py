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
st.markdown("Configure a malha de amostragem da pista, insira os dados no formulário e clique em Processar.")

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
    st.header("📐 Configuração da Grade")
    n_linhas = st.number_input("Número de Linhas de Coleta (Eixo X)", min_value=2, max_value=10, value=4, step=1)
    n_pontos = st.number_input("Pontos por Linha (Eixo Y)", min_value=2, max_value=10, value=5, step=1)
    
    st.divider()
    st.header("⚙️ Foco do Relatório")
    coletou_umidade = st.checkbox("Incluir Mapa de Umidade", value=True)
    coletou_espessura = st.checkbox("Incluir Mapa de Espessura", value=True)

# ==============================================================================
# 2. FORMULÁRIO DE ENTRADA DE DADOS - INICIALIZAÇÃO ZERADA
# ==============================================================================
st.header("📋 Dados Coletados")
st.markdown("Preencha as abas de cada linha abaixo. Para zerar tudo, basta atualizar a página (F5) no seu tablet ou notebook.")

lista_dados = []

# Formulário oficial que isola o cache das caixas numéricas
with st.form("formulario_coleta"):
    
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
                
                # Valores iniciais em 0.0 para garantir uma planilha limpa de cara
                with cols[0]: q1 = st.number_input("1ª Queda (cm)", min_value=0.0, max_value=15.0, value=0.0, step=0.1, key=f"q1_{l}_{p}")
                with cols[1]: q2 = st.number_input("2ª Queda (cm)", min_value=0.0, max_value=15.0, value=0.0, step=0.1, key=f"q2_{l}_{p}")
                with cols[2]: q3 = st.number_input("3ª Queda (cm)", min_value=0.0, max_value=15.0, value=0.0, step=0.1, key=f"q3_{l}_{p}")
                
                umi, esp = 0.0, 0
                curr_idx = 3
                if coletou_umidade:
                    with cols[curr_idx]: umi = st.number_input("Umidade (%)", min_value=0.0, max_value=100.0, value=0.0, step=0.1, key=f"umi_{l}_{p}")
                    curr_idx += 1
                if coletou_espessura:
                    with cols[curr_idx]: esp = st.number_input("Espessura (cm)", min_value=0, max_value=50, value=0, step=1, key=f"esp_{l}_{p}")
                    
                lista_dados.append({
                    "Haras": nome_fazenda, "Pista": nome_pista, "Dimensão": dimensao_pista, "Data": data_coleta, 
                    "Linha": f"Linha {l}", "Ponto": f"Ponto {p}", "X": l, "Y": p, 
                    "1ª Queda": q1, "2ª Queda": q2, "3ª Queda": q3, "Umidade": umi, "Espessura": esp
                })

    st.markdown("---")
    disparar_calculos = st.form_submit_button("🚀 Processar e Atualizar Relatórios", type="primary")

# ==============================================================================
# 3. PROCESSAMENTO E GERAÇÃO DOS GRÁFICOS
# ==============================================================================
df_dados = pd.DataFrame(lista_dados)
dados_inseridos = df_dados["1ª Queda"].sum() > 0

if disparar_calculos and dados_inseridos:
    med_amortecimento = df_dados["1ª Queda"].mean()
    med_transicao = df_dados["2ª Queda"].mean()
    med_suporte = df_dados["3ª Queda"].mean()
    medicao_atual = [med_amortecimento, med_transicao, med_suporte]
    
    todas_quedas = pd.concat([df_dados["1ª Queda"], df_dados["2ª Queda"], df_dados["3ª Queda"]])
    io_geral = (todas_quedas.std() / todas_quedas.mean()) * 100 if todas_quedas.mean() > 0 else 0
    umidade_media_geral = df_dados["Umidade"].mean()
    espessura_media_geral = round(df_dados["Espessura"].mean())

    fases, verde_inf, verde_sup = ['Amortecimento', 'Transição', 'Suporte'], [3.5, 5.5, 7.0], [4.5, 6.5, 8.0]
    
    fig1, plt_ax1 = plt.subplots(figsize=(9, 6.5))
    plt_ax1.set_facecolor('#f4f4f6')
    x_indices = np.arange(len(fases))
    plt_ax1.fill_between(x_indices, verde_inf, verde_sup, color='#e2f0d9', alpha=0.7, label='Método Pnania')
    plt_ax1.plot(x_indices, verde_sup, color='#a9d08e', linestyle='--', linewidth=1.2)
    plt_ax1.plot(x_indices, verde_inf, color='#a9d08e', linestyle='--', linewidth=1.2)
    plt_ax1.plot(x_indices, medicao_atual, color='#0f3a61', linewidth=3.5, marker='s', markersize=12, markerfacecolor='white', markeredgewidth=3, label=f"{nome_pista} ({data_coleta})")
    
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
    plt.title(f"{nome_fazenda} — {nome_pista} ({dimensao_pista}) — {data_coleta}", fontsize=9.5, pad=12, fontweight='bold', color='#555555')
    plt_ax1.legend(loc='upper left', frameon=True, facecolor='white', edgecolor='#e0e0e0', fontsize=9)
    
    colunas_tab = ['Amortecimento', 'Transição', 'Suporte']
    dados_linha1 = [f"{verde_inf[0]:.1f} - {verde_sup[0]:.1f}", f"{verde_inf[1]:.1f} - {verde_sup[1]:.1f}", f"{verde_inf[2]:.1f} - {verde_sup[2]:.1f}"]
    dados_linha2 = [f"{medicao_atual[0]:.1f}", f"{medicao_atual[1]:.1f}", f"{medicao_atual[2]:.1f}"]
    if coletou_umidade: colunas_tab.append('Umidade Geral'); dados_linha1.append('-'); dados_linha2.append(f"{umidade_media_geral:.1f}%")
    if coletou_espessura: colunas_tab.append('Espessura Méd.'); dados_linha1.append('-'); dados_linha2.append(f"{espessura_media_geral} cm")
    
    tabela = plt.table(cellText=[dados_linha1, dados_linha2], rowLabels=['Faixa Ideal (cm)', f'Pista (IO: {io_geral:.1f}%)'], colLabels=colunas_tab, rowColours=['#f2f7fa', '#ffffff'], colColours=['#0f3a61']*len(colunas_tab), loc='bottom', cellLoc='center', bbox=[0.0, -0.24, 1.0, 0.14])
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
        plt_ax2.set_title('MAPA DE ESPESSURA DA CAMADA (cm)', fontsize=11, fontweight='bold', color='#0f3a61', pad=12)
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
        plt_ax3.set_title('MAPA DE UMIDADE DA PISTA (%)', fontsize=11, fontweight='bold', color='#0f3a61', pad=12)
        plt_ax3.set_xlabel('Linhas de Coleta (Largura)', fontsize=9, fontweight='bold')
        plt_ax3.set_ylabel('Pontos de Coleta (Comprimento)', fontsize=9, fontweight='bold')
        plt_ax3.set_yticks(range(1, n_pontos + 1))
        plt_ax3.set_yticklabels([str(i) for i in range(1, n_pontos + 1)], fontsize=9, fontweight='bold')
        plt_ax3.set_xticks(range(1, n_linhas + 1))
        plt_ax3.set_xticklabels([f"L {i}" for i in range(1, n_linhas + 1)], fontsize=9)
        fig3.colorbar(mapa2, ax=plt_ax3).set_label('Umidade (%)', fontsize
