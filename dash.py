import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
import numpy as np
import time

# Configurações da página
st.set_page_config(
    page_title="Panut Brasil Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Cache de dados
@st.cache_data(ttl=300)
def carregar_dados():
    try:
        response = requests.get('http://localhost:5000/api/dados')
        return response.json()
    except:
        st.error('Erro ao carregar dados')
        return {
            'produtos': {},
            'filiais': [],
            'vendas': [],
            'analytics': {
                'total_vendas': 0,
                'faturamento_total': 0,
                'produto_mais_vendido': "Sem dados",
                'faturamento_fevereiro': 0
            }
        }

# Carregamento inicial
dados = carregar_dados()

# Cabeçalho
st.title("🏢 Dashboard Panut Brasil")
st.markdown("### *Empresa Alemã de produtos automotivos e indústria Química*")

# Menu lateral
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione:",
    ["Dashboard", "Adicionar Venda", "Gerenciar Produtos e Estoque"]
)

if pagina == "Dashboard":
    tab1, tab2, tab3 = st.tabs(["📊 Vendas", "📦 Estoque", "🏢 Filiais"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Faturamento Total", f"R$ {dados['analytics']['faturamento_total']:,.2f}")
        with col2:
            st.metric("Produto Mais Vendido", dados['analytics']['produto_mais_vendido'])
        with col3:
            st.metric("Faturamento Fevereiro", f"R$ {dados['analytics']['faturamento_fevereiro']:,.2f}")
        
        if dados['vendas']:
            df_vendas = pd.DataFrame(dados['vendas'])
            df_vendas['data'] = pd.to_datetime(df_vendas['data'])
            
            fig_linha = px.line(
                df_vendas.groupby('data')['valor'].sum().reset_index(),
                x='data',
                y='valor',
                title='Evolução de Vendas',
                template='plotly_dark'
            )
            st.plotly_chart(fig_linha, use_container_width=True)
    
    with tab2:
        produtos_df = pd.DataFrame([(k, v['estoque']) for k, v in dados['produtos'].items()], 
                                columns=['produto', 'estoque'])
        fig_pizza = px.pie(
            produtos_df,
            values='estoque',
            names='produto',
            title='Distribuição de Estoque',
            template='plotly_dark'
        )
        st.plotly_chart(fig_pizza, use_container_width=True)
    
    with tab3:
        if dados['vendas']:
            df_vendas = pd.DataFrame(dados['vendas'])
            df_vendas['data'] = pd.to_datetime(df_vendas['data'])
            
            cores_filiais = {
                'Brasil': '#00FF00',
                'EUA': '#0000FF',
                'Alemanha': '#FF0000'
            }
            
            df_grouped = df_vendas.groupby(['data', 'filial'])['valor'].agg([
                ('min', 'min'),
                ('max', 'max'),
                ('open', 'first'),
                ('close', 'last')
            ]).reset_index()
            
            fig_candle = go.Figure()
            
            for filial in ['Brasil', 'Alemanha', 'EUA']:
                filial_data = df_grouped[df_grouped['filial'] == filial]
                
                if not filial_data.empty:
                    fig_candle.add_trace(
                        go.Candlestick(
                            x=filial_data['data'],
                            open=filial_data['open'],
                            high=filial_data['max'],
                            low=filial_data['min'],
                            close=filial_data['close'],
                            name=filial,
                            increasing_line_color=cores_filiais[filial],
                            decreasing_line_color=cores_filiais[filial],
                            showlegend=True
                        )
                    )
            
            fig_candle.update_layout(
                title='Análise de Vendas por Filial',
                template='plotly_dark',
                xaxis_title='Data',
                yaxis_title='Valor (R$)',
                showlegend=True,
                legend_title='Filiais',
                height=600,
                xaxis_rangeslider_visible=False,
                yaxis_tickprefix='R$ ',
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            st.plotly_chart(fig_candle, use_container_width=True)
            
            col1, col2, col3 = st.columns(3)
            vendas_por_filial = df_vendas.groupby('filial')['valor'].sum()
            
            with col1:
                st.metric(
                    "Brasil 🇧🇷",
                    f"R$ {vendas_por_filial.get('Brasil', 0):,.2f}",
                    "Líder em vendas"
                )
            with col2:
                st.metric(
                    "EUA 🇺🇸",
                    f"R$ {vendas_por_filial.get('EUA', 0):,.2f}"
                )
            with col3:
                st.metric(
                    "Alemanha 🇩🇪",
                    f"R$ {vendas_por_filial.get('Alemanha', 0):,.2f}"
                )

elif pagina == "Adicionar Venda":
    st.header("Registrar Nova Venda")
    
    with st.form(key="form_venda"):
        produtos_disponiveis = list(dados.get('produtos', {}).keys())
        produto = st.selectbox(
            "Produto",
            options=produtos_disponiveis,
            index=0 if produtos_disponiveis else None
        )
        
        filiais = ['Brasil', 'Alemanha', 'EUA']
        filial = st.selectbox(
            "Filial",
            options=filiais,
            index=0
        )
        
        quantidade = st.number_input(
            "Quantidade",
            min_value=1,
            value=1
        )
        
        data_venda = st.date_input("Data da Venda")
        
        submit_button = st.form_submit_button("Registrar Venda")
        
        if submit_button:
            try:
                venda_data = {
                    'data': data_venda.strftime('%Y-%m-%d'),
                    'produto': produto,
                    'filial': filial,
                    'quantidade': int(quantidade)
                }
                
                response = requests.post(
                    'http://127.0.0.1:5000/api/vendas',
                    json=venda_data,
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    st.success("✅ Venda registrada com sucesso!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"❌ Erro ao registrar venda: {response.text}")
                    
            except Exception as e:
                st.error(f"❌ Erro de conexão: {str(e)}")

elif pagina == "Gerenciar Produtos e Estoque":
    st.header("Gestão de Estoque")
    
    tab_estoque, tab_adicionar = st.tabs(["📦 Estoque Atual", "➕ Adicionar/Atualizar Produtos"])
    
    with tab_estoque:
        st.subheader("Estoque Disponível")
        
        estoque_df = pd.DataFrame([
            {
                'Produto': produto,
                'Preço': f'R$ {dados["produtos"][produto]["preco"]:.2f}',
                'Estoque': dados["produtos"][produto]["estoque"],
                'Valor Total': f'R$ {dados["produtos"][produto]["preco"] * dados["produtos"][produto]["estoque"]:.2f}'
            }
            for produto in dados["produtos"]
        ])
        
        st.dataframe(
            estoque_df,
            column_config={
                "Produto": st.column_config.TextColumn("Produto", width="medium"),
                "Preço": st.column_config.TextColumn("Preço", width="small"),
                "Estoque": st.column_config.NumberColumn("Quantidade", width="small"),
                "Valor Total": st.column_config.TextColumn("Valor Total", width="medium")
            },
            hide_index=True,
            use_container_width=True
        )
        
        fig_estoque = px.bar(
            estoque_df,
            x='Produto',
            y='Estoque',
            title='Quantidade em Estoque por Produto',
            template='plotly_dark',
            color='Estoque',
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_estoque, use_container_width=True)
    
    with tab_adicionar:
        st.subheader("Adicionar Novo Produto ou Atualizar Estoque")
        
        with st.form(key="form_produto"):
            opcao = st.radio(
                "Escolha uma opção:",
                ["Atualizar Produto Existente", "Adicionar Novo Produto"]
            )
            
            if opcao == "Atualizar Produto Existente":
                produto = st.selectbox(
                    "Selecione o Produto",
                    list(dados["produtos"].keys())
                )
                nova_quantidade = st.number_input(
                    "Quantidade a Adicionar",
                    min_value=1,
                    value=1
                )
                novo_preco = st.number_input(
                    "Atualizar Preço (opcional)",
                    min_value=0.0,
                    value=float(dados["produtos"][produto]["preco"]),
                    format="%.2f"
                )
            else:
                produto = st.text_input("Nome do Novo Produto")
                nova_quantidade = st.number_input(
                    "Quantidade Inicial",
                    min_value=1,
                    value=1
                )
                novo_preco = st.number_input(
                    "Preço do Produto",
                    min_value=0.01,
                    value=1.0,
                    format="%.2f"
                )
            
            submit_button = st.form_submit_button("Salvar")
            
            if submit_button:
                try:
                    if opcao == "Atualizar Produto Existente":
                        response = requests.post(
                            'http://127.0.0.1:5000/api/produtos',
                            json={
                                'nome': produto,
                                'preco': novo_preco,
                                'estoque': nova_quantidade,
                                'atualizar': True
                            }
                        )
                    else:
                        if produto in dados["produtos"]:
                            st.error("❌ Este produto já existe!")
                        else:
                            response = requests.post(
                                'http://127.0.0.1:5000/api/produtos',
                                json={
                                    'nome': produto,
                                    'preco': novo_preco,
                                    'estoque': nova_quantidade,
                                    'atualizar': False
                                }
                            )
                    
                    if response.status_code == 200:
                        st.success("✅ Operação realizada com sucesso!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(f"❌ Erro: {response.text}")
                        
                except Exception as e:
                    st.error(f"❌ Erro de conexão: {str(e)}")

# Rodapé
st.markdown("""
---
Desenvolvido orgulhosamente por Cezi Cola Tecnologia  
Tecnologia puramente em Python – Todos os direitos reservados 2025.
""")