Dashboard Panut Brasil 🏢

Sistema de gestão empresarial para a Panut Brasil, empresa alemã de produtos automotivos e indústria química.
📊 Funcionalidades

    Dashboard interativo com métricas em tempo real
    Gestão de vendas por filial (Brasil 🇧🇷, Alemanha 🇩🇪, EUA 🇺🇸)
    Controle de estoque distribuído
    Análise de vendas com gráficos dinâmicos
    Sistema de registro de vendas
    Gerenciamento de produtos e estoque

🚀 Tecnologias

    Python 3.8+
    Flask (Backend)
    Streamlit (Frontend)
    Plotly (Visualização de dados)
    Pandas (Análise de dados)

⚙️ Instalação

com a pasta baixada siga estes passos:

    Crie um ambiente virtual python -m venv venv

    Ative o ambiente virtual
    Windows

venv\Scripts\activate

    Instale as dependências pip install -r requirements.txt

🎯 Como Usar? 1)Inicie o servidor backend (Flask) python app.py simultaneamente inicie em outro terminal dentro do seu editor de código o Frontend do Python:] streamlit run dash.py Pronto! o terminal do frontend lhe dará os links de acesso ao servidor web e poderá ver a aplicação funcionando!

ESTRUTURA DAS PASTAS:

panut-dashboard/ ├── app.py # Backend Flask ├── dash.py # Frontend Streamlit ├── requirements.txt └── README.md

crie um arquivo chamado requirements.txt
📝 Documentação para o GitHub

Vou te ajudar a criar uma documentação completa para o repositório. Primeiro, vamos criar o arquivo README.md:

# Dashboard Panut Brasil 🏢

Sistema de gestão empresarial para a Panut Brasil, empresa alemã de produtos automotivos e indústria química.

## 📊 Funcionalidades

- Dashboard interativo com métricas em tempo real
- Gestão de vendas por filial (Brasil 🇧🇷, Alemanha 🇩🇪, EUA 🇺🇸)
- Controle de estoque distribuído
- Análise de vendas com gráficos dinâmicos
- Sistema de registro de vendas
- Gerenciamento de produtos e estoque

## 🚀 Tecnologias

- Python 3.8+
- Flask (Backend)
- Streamlit (Frontend)
- Plotly (Visualização de dados)
- Pandas (Análise de dados)

## ⚙️ Instalação

1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/panut-dashboard.git
cd panut-dashboard

    Crie um ambiente virtual

python -m venv venv

    Ative o ambiente virtual

# Windows
venv\Scripts\activate

    Instale as dependências

pip install -r requirements.txt

🎯 Como Usar

    Inicie o servidor backend (Flask)

python app.py

    Em outro terminal, inicie o frontend (Streamlit)

streamlit run dash.py

    Acesse o dashboard em http://localhost:8501

📁 Estrutura do Projeto

panut-dashboard/
├── app.py          # Backend Flask
├── dash.py         # Frontend Streamlit
├── requirements.txt
└── README.md

📋 Requisitos

Crie um arquivo requirements.txt:

# filepath: /c:/Users/Cesar/OneDrive/Área de Trabalho/dash/requirements.txt
flask==2.0.1
flask-cors==3.0.10
pandas==1.3.3
numpy==1.21.2
streamlit==1.11.0
plotly==5.3.1
requests==2.26.0

📊 Imagens do Sistema

[Adicione screenshots do dashboard aqui]
👥 Contribuições

    Faça um Fork do projeto
    Crie uma branch para sua feature (git checkout -b feature/NovaFeature)
    Commit suas mudanças (git commit -m 'Adicionando nova feature')
    Push para a branch (git push origin feature/NovaFeature)
    Abra um Pull Request

📜 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
✨ Autor

Desenvolvido por Cezi Cola Tecnologia


### 🔄 Para inicializar o git:

```bash
cd "C:\Users\Cesar\OneDrive\Área de Trabalho\dash"
git init
git add .
git commit -m "Primeira versão do Dashboard Panut Brasil"

📝 Para criar um novo repositório no GitHub:

    Acesse github.com
    Clique em "New repository"
    Nome: panut-dashboard
    Descrição: "Dashboard empresarial para Panut Brasil"
    Deixe público
    Não inicialize com README
    Execute no terminal:

git remote add origin https://github.com/seu-usuario/panut-dashboard.git
git branch -M main
git push -u origin main

⚠️ Não esqueça de:

    Adicionar screenshots do dashboard no README
    Atualizar os links do repositório
    Criar arquivo .gitignore:

venv/
__pycache__/
*.pyc
.env
.streamlit/

Aqui estão todos os passos que fiz para construir essa aplicação em Python Backend e Frontend.