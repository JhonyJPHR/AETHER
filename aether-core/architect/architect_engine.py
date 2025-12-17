# aether-core/architect/architect_engine.py
import os
import google.generativeai as genai
from colorama import Fore
from dotenv import load_dotenv
import glob

load_dotenv()

class Architect:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.ai_available = False
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-3-pro-preview')
            self.ai_available = True
            print(f"{Fore.CYAN}[ARCHITECT] 🧠 Gemini Pro: Modo Multi-Contexto Ativado.")

    def get_project_context(self, victim_path):
        """
        Lê TODOS os arquivos Python do diretório alvo para entender dependências.
        Isso é crucial para sistemas complexos.
        """
        folder = os.path.dirname(victim_path)
        context = ""
        # Pega todos os .py da pasta
        files = glob.glob(os.path.join(folder, "*.py"))
        
        for file in files:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    filename = os.path.basename(file)
                    context += f"\n--- ARQUIVO: {filename} ---\n{content}\n"
            except:
                pass
        return context

    def diagnose_and_fix(self, error_log, file_path, previous_attempt=None):
        print(f"{Fore.YELLOW}[ARCHITECT] 🔍 Escaneando contexto global do projeto...")
        
        # 1. Obter o código de TODO o projeto, não só do arquivo quebrado
        project_context = self.get_project_context(file_path)
        
        # 2. Ler o arquivo específico do erro para referência
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                target_code = f.read()
        except:
            return None

        # 3. Prompt de Engenharia de Sistemas Críticos
        extra_instruction = ""
        if previous_attempt:
            extra_instruction = f"""
            ATENÇÃO: VOCÊ JÁ TENTOU CORRIGIR ISSO E FALHOU.
            SUA TENTATIVA ANTERIOR CAUSOU ESTE NOVO ERRO:
            "{previous_attempt}"
            NÃO COMETA O MESMO ERRO. ANALISE PROFUNDAMENTE.
            """

        prompt = f"""
        Você é uma IA de Recuperação de Desastres para Sistemas Críticos (Nível NASA).
        
        CONTEXTO DO PROJETO (Outros arquivos para entender dependências):
        {project_context}
        
        ARQUIVO ALVO (Onde o erro explodiu):
        ```python
        {target_code}
        ```
        
        ERRO CRÍTICO REPORTADO:
        "{error_log}"
        
        {extra_instruction}
        
        MISSÃO:
        1. Analise a interação entre os arquivos. O erro pode ser uma dependência mal injetada ou lógica cruzada.
        2. Reescreva o ARQUIVO ALVO inteiro corrigindo a falha.
        3. Seja defensivo: Adicione validações extras.
        4. Retorne APENAS o código Python do ARQUIVO ALVO.
        """

        print(f"{Fore.YELLOW}[ARCHITECT] 🧠 Processando lógica complexa no Gemini...")

        if self.ai_available:
            try:
                response = self.model.generate_content(prompt)
                fixed_code = response.text
                if "```python" in fixed_code:
                    fixed_code = fixed_code.split("```python")[1].split("```")[0]
                elif "```" in fixed_code:
                    fixed_code = fixed_code.replace("```", "")
                
                print(f"{Fore.GREEN}[ARCHITECT] 💡 Solução arquitetural gerada.")
                return fixed_code.strip()
            except Exception as e:
                print(f"{Fore.RED}[ERRO AI] {e}")
                return None
        return None