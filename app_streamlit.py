import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import time
import os

# Configurações da página
st.set_page_config(
    page_title="Panut Brasil Dashboard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa o estado da sessão, se necessário
if 'produtos' not in st.session_state:
    st.session_state.produtos = {
        'Graxas': {'preco': 50.00, 'estoque': 1000},
        'Pastas': {'preco': 100.00, 'estoque': 5000},
        'Óleos': {'preco': 200.00, 'estoque': 2000},
        'Produtos de limpeza': {'preco': 200.00, 'estoque': 5000},
        'Produtos de manutenção': {'preco': 100.00, 'estoque': 1000}
    }

if 'filiais' not in st.session_state:
    st.session_state.filiais = ['Brasil', 'Alemanha', 'EUA']

if 'vendas' not in st.session_state:
    st.session_state.vendas = []
    # Função para gerar dados iniciais
    hoje = datetime.now()
    for _ in range(50):
        data = hoje - timedelta(days=np.random.randint(0, 30))
        produto = np.random.choice(list(st.session_state.produtos.keys()))
        filial = np.random.choice(st.session_state.filiais, p=[0.6, 0.2, 0.2])
        quantidade = np.random.randint(1, 10)
        st.session_state.vendas.append({
            'data': data.strftime('%Y-%m-%d'),
            'produto': produto,
            'filial': filial,
            'quantidade': quantidade,
            'valor': st.session_state.produtos[produto]['preco'] * quantidade
        })

# Funções auxiliares
def calcular_analytics():
    """Calcula métricas analíticas baseadas nas vendas atuais"""
    if not st.session_state.vendas:
        return {
            'total_vendas': 0,
            'faturamento_total': 0,
            'produto_mais_vendido': "Sem vendas",
            'faturamento_fevereiro': 0
        }
    
    df = pd.DataFrame(st.session_state.vendas)
    
    # Encontra o produto mais vendido
    if not df.empty:
        produto_mais_vendido = df.groupby('produto')['quantidade'].sum().idxmax()
    else:
        produto_mais_vendido = "Sem vendas"
    
    # Calcula faturamento de fevereiro
    faturamento_fevereiro = sum(v['valor'] for v in st.session_state.vendas 
        if datetime.strptime(v['data'], '%Y-%m-%d').month == 2)
    
    return {
        'total_vendas': len(st.session_state.vendas),
        'faturamento_total': sum(v['valor'] for v in st.session_state.vendas),
        'produto_mais_vendido': produto_mais_vendido,
        'faturamento_fevereiro': faturamento_fevereiro
    }

def adicionar_venda(data, produto, filial, quantidade):
    """Adiciona uma nova venda"""
    if st.session_state.produtos[produto]['estoque'] >= quantidade:
        venda = {
            'data': data,
            'produto': produto,
            'filial': filial,
            'quantidade': quantidade,
            'valor': st.session_state.produtos[produto]['preco'] * quantidade
        }
        
        st.session_state.produtos[produto]['estoque'] -= quantidade
        st.session_state.vendas.append(venda)
        return True, "✅ Venda registrada com sucesso!"
    else:
        return False, "❌ Estoque insuficiente"

def gerenciar_produto(nome, preco, estoque, atualizar=False):
    """Adiciona ou atualiza um produto"""
    if atualizar:
        if nome not in st.session_state.produtos:
            return False, "❌ Produto não encontrado"
        
        st.session_state.produtos[nome]['estoque'] += estoque
        st.session_state.produtos[nome]['preco'] = preco
        return True, "✅ Produto atualizado com sucesso!"
    else:
        if nome in st.session_state.produtos:
            return False, "❌ Este produto já existe!"
        
        st.session_state.produtos[nome] = {
            'preco': preco,
            'estoque': estoque
        }
        return True, "✅ Produto adicionado com sucesso!"

# Cabeçalho
st.title("🏢 Dashboard Panut Brasil")
st.markdown("### *Empresa Alemã de produtos automotivos e indústria Química*")

# Menu lateral
st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Selecione:",
    ["Dashboard", "Adicionar Venda", "Gerenciar Produtos e Estoque"]
)

# Página principal - Dashboard
if pagina == "Dashboard":
    tab1, tab2, tab3 = st.tabs(["📊 Vendas", "📦 Estoque", "🏢 Filiais"])
    
    analytics = calcular_analytics()
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Faturamento Total", f"R$ {analytics['faturamento_total']:,.2f}")
        with col2:
            st.metric("Produto Mais Vendido", analytics['produto_mais_vendido'])
        with col3:
            st.metric("Faturamento Fevereiro", f"R$ {analytics['faturamento_fevereiro']:,.2f}")
        
        if st.session_state.vendas:
            df_vendas = pd.DataFrame(st.session_state.vendas)
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
        produtos_df = pd.DataFrame([(k, v['estoque']) for k, v in st.session_state.produtos.items()], 
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
        if st.session_state.vendas:
            df_vendas = pd.DataFrame(st.session_state.vendas)
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

# Página - Adicionar Venda
elif pagina == "Adicionar Venda":
    st.header("Registrar Nova Venda")
    
    with st.form(key="form_venda"):
        produtos_disponiveis = list(st.session_state.produtos.keys())
        produto = st.selectbox(
            "Produto",
            options=produtos_disponiveis,
            index=0 if produtos_disponiveis else None
        )
        
        filiais = st.session_state.filiais
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
            success, mensagem = adicionar_venda(
                data_venda.strftime('%Y-%m-%d'),
                produto,
                filial,
                int(quantidade)
            )
            
            if success:
                st.success(mensagem)
                time.sleep(1)
                st.rerun()
            else:
                st.error(mensagem)

# Página - Gerenciar Produtos e Estoque
elif pagina == "Gerenciar Produtos e Estoque":
    st.header("Gestão de Estoque")
    
    tab_estoque, tab_adicionar = st.tabs(["📦 Estoque Atual", "➕ Adicionar/Atualizar Produtos"])
    
    with tab_estoque:
        st.subheader("Estoque Disponível")
        
        estoque_df = pd.DataFrame([
            {
                'Produto': produto,
                'Preço': f'R$ {st.session_state.produtos[produto]["preco"]:.2f}',
                'Estoque': st.session_state.produtos[produto]["estoque"],
                'Valor Total': f'R$ {st.session_state.produtos[produto]["preco"] * st.session_state.produtos[produto]["estoque"]:.2f}'
            }
            for produto in st.session_state.produtos
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
                    list(st.session_state.produtos.keys())
                )
                nova_quantidade = st.number_input(
                    "Quantidade a Adicionar",
                    min_value=1,
                    value=1
                )
                novo_preco = st.number_input(
                    "Atualizar Preço (opcional)",
                    min_value=0.0,
                    value=float(st.session_state.produtos[produto]["preco"]),
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
                success, mensagem = gerenciar_produto(
                    produto,
                    float(novo_preco),
                    int(nova_quantidade),
                    opcao == "Atualizar Produto Existente"
                )
                
                if success:
                    st.success(mensagem)
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(mensagem)

# Rodapé
st.markdown("""
---
Desenvolvido orgulhosamente por Cezi Cola Tecnologia  
Tecnologia puramente em Python – Todos os direitos reservados 2025.
""") 