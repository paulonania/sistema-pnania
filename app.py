import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import griddata

# CONFIGURAÇÃO DA PÁGINA WEB
st.set_page_config(page_title="Sistema Pnania Premium", layout="wide")

st.title("📊 Gerador de Relatórios — Método Pnania")
st.markdown("Configure a malha de amostragem da pista e preencha os dados abaixo. O sistema gera os mapas contínuos na hora!")

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
# 2. ENTRADA DE DADOS ORGANIZADA POR ABAS (PONTOS PUROS)
# ==============================================================================
st.header("📋 Coleta de Campo — Malha Dinâmica")
st.markdown("Insira os valores coletados de forma direta para cada ponto da grade:")

lista_dados = []
abas = st.tabs([f"Linha {l}" for l in range(1, n_linhas + 1)])

for l_idx, aba in enumerate(abas):
    l = l_idx + 1
    with aba:
        for p in range(1, n_pontos + 1):
            # RÓTULO 100% LIMPO: APENAS O NÚMERO DO PONTO
            st.markdown(f"**📍 Ponto {p}**")
            
            colunas_ativas = ["1ª Queda (cm)", "2ª Queda (cm)", "3ª Queda (cm)"]
            if coletou_umidade: colunas_ativas.append("Umidade (%)")
            if coletou_espessura: colunas_ativas.append("Espessura (cm)")
            
            cols = st.columns(len(colunas_ativas))
            with cols[0]: q1 = st.number_input("1ª Queda (cm)", min_value=0.0, max_value=15.0, value=4.0, step=0.1, key=f"q1_{l}_{p}")
            with cols[1]: q2 = st.number_input("2ª Queda (cm)", min_value=0.0, max_value=15.0, value=5.5, step=0.1, key=f"q2_{l}_{p}")
            with cols[2]: q3 = st.number_input("3ª Queda (cm)", min_value=0.0, max_value=15.0, value=7.2, step=0.1, key=f"q3_{l}_{p}")
            
            umi, esp = 4.5, 12
            curr_idx = 3
            if coletou_umidade:
                with cols[curr_idx]: umi = st.number_input("Umidade (%)", min_value=0.0, max_value=100.0, value=4.5, step=0.1, key=f"umi_{l}_{p}")
                curr_idx += 1
            if coletou_espessura:
                with cols[curr_idx]: esp = st.number_input("Espessura (cm)", min_value=0, max_value=50, value=12, step=1, key=f"esp_{l}_{p}")
                
            lista_dados.append({
                "Haras": nome_fazenda, 
                "Pista": nome_pista, 
                "Dimensão": dimensao_pista, 
                "Data": data_coleta, 
                "Linha": f"Linha {l}", 
                "Ponto": f"Ponto {p}", 
                "X": l, 
                "Y": p, 
                "1ª Queda": q1, 
                "2ª Queda": q2, 
                "3ª Queda": q3, 
                "Umidade": umi, 
                "Espessura": esp
            })

df_dados = pd.DataFrame(lista_dados)

with st.sidebar:
    st.divider()
    st.header("💾 Arquivamento e Backup")
    df_exportar = df_dados.drop(columns=["X", "Y"]).rename(columns={
        "1ª Queda": "1ª Queda - Amortecimento (cm)", 
        "2ª Queda": "2ª
