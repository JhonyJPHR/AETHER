# aether-core/architect/architect_engine.py
import os
import json
from openai import OpenAI
from colorama import Fore, Style

# Tenta carregar a API Key
try:
    from dotenv import load_dotenv
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    AI_AVAILABLE = True
except:
    AI_AVAILABLE = False

class Architect:
    def __init__(self):
        print(f"{Fore.CYAN}[ARCHITECT] Módulo de Diagnóstico Inteligente carregado.")

    def diagnose_and_fix(self, error_log, file_path):
        """
        Lê o arquivo defeituoso e solicita uma correção à IA.
        """
        print(f"{Fore.YELLOW}[ARCHITECT] 🔍 Analisando código fonte em: {file_path}")
        
        # 1. Ler o código "doente" (CORREÇÃO APLICADA AQUI: encoding='utf-8')
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"{Fore.RED}[ERRO] Arquivo fonte não encontrado!")
            return None
        except Exception as e:
            print(f"{Fore.RED}[ERRO LEITURA] Não foi possível ler o arquivo: {e}")
            return None

        # 2. Montar o Prompt para a IA
        prompt = f"""
        Você é o AETHER ARCHITECT, uma IA especialista em corrigir bugs críticos em tempo real.
        
        CONTEXTO:
        O seguinte código Python gerou um erro crítico em produção.
        
        ERRO DETECTADO:
        {error_log}
        
        CÓDIGO FONTE ORIGINAL:
        ```python
        {source_code}
        ```
        
        SUA MISSÃO:
        1. Identifique a causa raiz lógica do erro (ex: divisão por zero, null pointer).
        2. Reescreva o código corrigindo o problema.
        3. Retorne APENAS o código Python corrigido. Nada de explicações.
        """

        print(f"{Fore.YELLOW}[ARCHITECT] 🧠 Consultando Núcleo de IA para solução...")

        # 3. Chamar a IA (Ou simular se não tiver chave)
        if AI_AVAILABLE and os.getenv("OPENAI_API_KEY"):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é uma IA de auto-correção de código. Retorne apenas código limpo."},
                        {"role": "user", "content": prompt}
                    ]
                )
                fixed_code = response.choices[0].message.content
                print(f"{Fore.GREEN}[ARCHITECT] 💡 Solução gerada pela IA com sucesso!")
                
                # Limpeza básica do markdown
                fixed_code = fixed_code.replace("```python", "").replace("```", "")
                return fixed_code
                
            except Exception as e:
                print(f"{Fore.RED}[ERRO AI] Falha na conexão: {e}")
                return self._simulation_mode(source_code)
        else:
            print(f"{Fore.MAGENTA}[ARCHITECT] ⚠️ Modo Simulação Ativo (Sem API Key)")
            return self._simulation_mode(source_code)

    def _simulation_mode(self, source_code):
        """
        Modo de fallback para demonstração sem internet/API.
        """
        print(f"{Fore.MAGENTA}[SIMULATION] Aplicando patch pré-definido para 'ZeroDivisionError'...")
        
        if "amount / risk_factor" in source_code:
            fixed_code = source_code.replace(
                "result = amount / risk_factor", 
                "result = amount / (risk_factor if risk_factor != 0 else 1) # Aether Fix: Prevented Division by Zero"
            )
            return fixed_code
        return source_code