# aether-core/surgeon/surgeon_engine.py
import os
import shutil
import time
from colorama import Fore, Style

class Surgeon:
    def __init__(self):
        print(f"{Fore.CYAN}[SURGEON] Unidade de Intervenção Cirúrgica carregada.")

    def apply_patch(self, file_path, new_code):
        """
        Realiza o transplante de código:
        1. Backup do arquivo doente.
        2. Sobrescrita com o código saudável.
        """
        print(f"{Fore.MAGENTA}[SURGEON] 🩺 Iniciando procedimento em: {file_path}")
        
        # 1. Criar Backup (Segurança primeiro!)
        backup_path = file_path + ".bak"
        try:
            shutil.copy(file_path, backup_path)
            print(f"{Fore.MAGENTA}[SURGEON] 💾 Backup tático criado: {backup_path}")
        except Exception as e:
            print(f"{Fore.RED}[SURGEON] FALHA DE BACKUP. Abortando operação. Erro: {e}")
            return False

        # 2. Injetar o novo código (A Cirurgia)
        try:
            print(f"{Fore.MAGENTA}[SURGEON] 💉 Injetando patch corretivo...")
            time.sleep(1) # Drama effect (para ficar bonito no terminal)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_code)
                
            print(f"{Fore.GREEN}{Style.BRIGHT}[SURGEON] ✅ SUCESSO! Código transplantado.")
            print(f"{Fore.GREEN}[SURGEON] O sistema alvo deve reiniciar automaticamente agora.")
            return True
            
        except Exception as e:
            print(f"{Fore.RED}[SURGEON] ❌ FALHA NA ESCRITA: {e}")
            # Tenta restaurar backup
            shutil.copy(backup_path, file_path)
            print(f"{Fore.RED}[SURGEON] Backup restaurado de emergência.")
            return False