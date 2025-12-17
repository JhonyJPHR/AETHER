# aether-core/validator/validator_engine.py
import ast
import traceback
from colorama import Fore, Style

class Validator:
    def __init__(self):
        print(f"{Fore.CYAN}[VALIDATOR] Escudo de Integridade de Código carregado.")

    def check_integrity(self, code_string):
        """
        Analisa se o código gerado pela IA é sintaticamente válido em Python.
        Isso impede que erros de sintaxe (SyntaxError) quebrem a produção.
        """
        print(f"{Fore.BLUE}[VALIDATOR] 🛡️ Verificando integridade sintática (AST Analysis)...")
        
        try:
            # Tenta fazer o parse do código para uma árvore sintática (AST)
            # Se a IA esqueceu um ':', um ')' ou indentação, isso explode aqui.
            ast.parse(code_string)
            print(f"{Fore.GREEN}[VALIDATOR] ✅ Código Aprovado: Sintaxe Válida.")
            return True
            
        except SyntaxError as e:
            print(f"{Fore.RED}[VALIDATOR] ❌ CÓDIGO REJEITADO! A IA gerou código inválido.")
            print(f"{Fore.RED}Detalhe: {e}")
            return False
        except Exception as e:
            print(f"{Fore.RED}[VALIDATOR] ❌ Erro desconhecido na validação: {e}")
            return False