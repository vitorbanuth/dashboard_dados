#!/bin/bash
# Criação e ativação do ambiente virtual para o projeto Streamlit

echo "🔧 Criando ambiente virtual..."
python3 -m venv venv

echo "✅ Ativando ambiente virtual..."
source venv/bin/activate

echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🎉 Ambiente pronto! Para ativar depois, use:"
echo "source venv/bin/activate"
