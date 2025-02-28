from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

app = Flask(__name__)
CORS(app)

# Dados iniciais
PRODUTOS = {
    'Graxas': {'preco': 50.00, 'estoque': 1000},
    'Pastas': {'preco': 100.00, 'estoque': 5000},
    'Óleos': {'preco': 200.00, 'estoque': 2000},
    'Produtos de limpeza': {'preco': 200.00, 'estoque': 5000},
    'Produtos de manutenção': {'preco': 100.00, 'estoque': 1000}
}

FILIAIS = ['Brasil', 'Alemanha', 'EUA']
vendas = []

def gerar_dados_iniciais():
    hoje = datetime.now()
    for _ in range(50):
        data = hoje - timedelta(days=np.random.randint(0, 30))
        produto = np.random.choice(list(PRODUTOS.keys()))
        filial = np.random.choice(FILIAIS, p=[0.6, 0.2, 0.2])
        quantidade = np.random.randint(1, 10)
        vendas.append({
            'data': data.strftime('%Y-%m-%d'),
            'produto': produto,
            'filial': filial,
            'quantidade': quantidade,
            'valor': PRODUTOS[produto]['preco'] * quantidade
        })

# Gerar dados iniciais
gerar_dados_iniciais()

@app.route('/api/dados', methods=['GET'])
def get_dados():
    df = pd.DataFrame(vendas)
    
    analytics = {
        'total_vendas': len(vendas),
        'faturamento_total': sum(v['valor'] for v in vendas) if vendas else 0,
        'produto_mais_vendido': df.groupby('produto')['quantidade'].sum().idxmax() if not df.empty else "Sem vendas",
        'faturamento_fevereiro': sum(v['valor'] for v in vendas 
            if datetime.strptime(v['data'], '%Y-%m-%d').month == 2) if vendas else 0
    }
    
    return jsonify({
        'produtos': PRODUTOS,
        'filiais': FILIAIS,
        'vendas': vendas,
        'analytics': analytics
    })

@app.route('/api/vendas', methods=['POST'])
def adicionar_venda():
    try:
        data = request.json
        print("Dados recebidos (venda):", data)
        
        if not all(k in data for k in ['data', 'produto', 'filial', 'quantidade']):
            return jsonify({"error": "Dados incompletos"}), 400
        
        venda = {
            'data': data['data'],
            'produto': data['produto'],
            'filial': data['filial'],
            'quantidade': int(data['quantidade']),
            'valor': PRODUTOS[data['produto']]['preco'] * int(data['quantidade'])
        }
        
        if PRODUTOS[data['produto']]['estoque'] >= int(data['quantidade']):
            PRODUTOS[data['produto']]['estoque'] -= int(data['quantidade'])
            vendas.append(venda)
            return jsonify({"message": "Venda registrada com sucesso!", "venda": venda})
        else:
            return jsonify({"error": "Estoque insuficiente"}), 400
        
    except Exception as e:
        print("Erro (venda):", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api/produtos', methods=['POST'])
def gerenciar_produtos():
    try:
        data = request.json
        print("Dados recebidos (produtos):", data)
        
        if data.get('atualizar'):
            # Atualizar produto existente
            if data['nome'] not in PRODUTOS:
                return jsonify({"error": "Produto não encontrado"}), 404
            
            PRODUTOS[data['nome']]['estoque'] += int(data['estoque'])
            PRODUTOS[data['nome']]['preco'] = float(data['preco'])
            
            return jsonify({
                "message": "Produto atualizado com sucesso!",
                "produto": {
                    "nome": data['nome'],
                    "preco": PRODUTOS[data['nome']]['preco'],
                    "estoque": PRODUTOS[data['nome']]['estoque']
                }
            })
        else:
            # Adicionar novo produto
            if data['nome'] in PRODUTOS:
                return jsonify({"error": "Produto já existe"}), 400
            
            PRODUTOS[data['nome']] = {
                'preco': float(data['preco']),
                'estoque': int(data['estoque'])
            }
            
            return jsonify({
                "message": "Produto adicionado com sucesso!",
                "produto": {
                    "nome": data['nome'],
                    "preco": PRODUTOS[data['nome']]['preco'],
                    "estoque": PRODUTOS[data['nome']]['estoque']
                }
            })
    
    except Exception as e:
        print("Erro (produtos):", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)