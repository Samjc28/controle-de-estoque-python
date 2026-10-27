"""
Sistema de Controle de Estoque com Python e SQLite
Ponto de entrada principal da aplicação.
"""
from pathlib import Path
import sys

# Adiciona o diretório 'janela' ao PATH para importação do módulo de interface
BASE_DIR = Path(__file__).resolve().parent
JANELA_DIR = BASE_DIR / "janela"
sys.path.insert(0, str(JANELA_DIR))

if __name__ == "__main__":
    import window
