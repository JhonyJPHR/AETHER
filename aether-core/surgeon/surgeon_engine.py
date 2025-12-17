# aether-core/surgeon/surgeon_engine.py
import os
import shutil
import time
from colorama import Fore, Style

class Surgeon:
    def __init__(self):
        print(f"{Fore.CYAN}[SURGEON] Unidade de Intervenção V2 (com Rollback) carregada.")

    def apply_patch(self, file_path, new_code, validator_module):
        """
        Executa o ciclo completo de cirurgia segura.
        """
        print(f"{Fore.MAGENTA}[SURGEON] 🩺 Iniciando protocolo de transplante seguro...")

        # 1. VALIDAÇÃO PRÉ-OPERATÓRIA
        if not validator_module.check_integrity(new_code):
            print(f"{Fore.RED}[SURGEON] ⛔ ABORTAR! O código gerado está corrompido.")
            return False

        # 2. BACKUP
        backup_path = file_path + ".bak"
        try:
            shutil.copy(file_path, backup_path)
        except Exception:
            print(f"{Fore.RED}[SURGEON] Falha ao criar backup. Operação cancelada.")
            return False

        # 3. TRANSPLANTE
        try:
            print(f"{Fore.MAGENTA}[SURGEON] 💉 Aplicando patch...")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_code)
            
            print(f"{Fore.GREEN}{Style.BRIGHT}[SURGEON] ✅ Patch aplicado com sucesso.")
            
            # Aqui poderíamos rodar testes unitários. Se falhasse -> self.rollback()
            return True

        except Exception as e:
            print(f"{Fore.RED}[SURGEON] ❌ ERRO CRÍTICO NA ESCRITA: {e}")
            self.rollback(file_path, backup_path)
            return False

    def rollback(self, file_path, backup_path):
        """
        Restaura o arquivo original em caso de emergência.
        """
        print(f"{Fore.RED}{Style.BRIGHT}[SURGEON] ⏪ INICIANDO ROLLBACK DE EMERGÊNCIA!")
        try:
            shutil.copy(backup_path, file_path)
            print(f"{Fore.GREEN}[SURGEON] Sistema restaurado para o estado anterior.")
        except Exception as e:
            print(f"{Fore.RED}[FATAL] Falha no Rollback. Intervenção manual necessária: {e}")