# Dashboard Panut Brasil

Dashboard interativo para a empresa Panut Brasil, desenvolvido com Streamlit.

## Sobre o Projeto

Este dashboard foi desenvolvido para a Panut Brasil, uma empresa alemã especializada em produtos automotivos e indústria química. O dashboard permite visualizar dados de vendas, gerenciar estoque e registrar novas vendas.

## Funcionalidades

- **Dashboard de Vendas**: Visualização de métricas de vendas, gráficos de evolução e análise por filial.
- **Gestão de Estoque**: Visualização do estoque atual e adição/atualização de produtos.
- **Registro de Vendas**: Interface para registrar novas vendas.

## Tecnologias Utilizadas

- **Streamlit**: Framework para criação de aplicações web com Python
- **Pandas**: Manipulação e análise de dados
- **Plotly**: Visualização de dados interativa
- **NumPy**: Computação numérica

## Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone este repositório:
   ```
   git clone https://github.com/seu-usuario/panut-dashboard.git
   cd panut-dashboard
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source venv/bin/activate
     ```

4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

### Executando o Dashboard

Execute o seguinte comando:
```
streamlit run app.py
```

O dashboard será aberto automaticamente no seu navegador padrão. Se não abrir, acesse `http://localhost:8501`.

## Implantação no Streamlit Cloud

Para implantar este dashboard no Streamlit Cloud:

1. Faça o fork deste repositório para sua conta GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io/)
3. Faça login com sua conta GitHub
4. Clique em "New app"
5. Selecione o repositório, o branch (main) e o arquivo principal (app.py)
6. Clique em "Deploy"

## Estrutura do Projeto

- `app.py`: Arquivo principal do aplicativo Streamlit
- `requirements.txt`: Lista de dependências do projeto
- `.streamlit/config.toml`: Configurações do Streamlit

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

## Contato

Desenvolvido por Cezi Cola Tecnologia - [website](https://www.cezicola.com) 