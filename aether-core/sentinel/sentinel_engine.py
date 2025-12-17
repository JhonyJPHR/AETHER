# aether-core/sentinel/sentinel_engine.py
import time
import os
import sys
from colorama import Fore, Style, init

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from architect.architect_engine import Architect
from surgeon.surgeon_engine import Surgeon
from validator.validator_engine import Validator

init(autoreset=True)

class Sentinel:
    def __init__(self, log_path, victim_path):
        self.log_path = log_path
        self.victim_path = victim_path
        self.is_running = False
        
        self.architect = Architect()
        self.surgeon = Surgeon()
        self.validator = Validator()
        
        # Memória de Curto Prazo para o Loop Ouroboros
        self.last_fix_time = 0
        self.last_error = None
        self.retry_count = 0
        
        print(f"{Fore.CYAN}[SENTINEL] Ouroboros System V3 Ready. Alvo: {log_path}")

    def start_monitoring(self):
        self.is_running = True
        print(f"{Fore.GREEN}[SENTINEL] 👁️  Monitoramento Permanente Iniciado.")
        
        # Cria o arquivo de log se não existir
        if not os.path.exists(self.log_path):
            open(self.log_path, 'w').close()

        with open(self.log_path, 'r') as file:
            file.seek(0, 2)
            while self.is_running:
                line = file.readline()
                if not line:
                    time.sleep(0.1)
                    continue
                self._analyze_line(line)     

    def _analyze_line(self, line):
        line = line.strip()
        if "CRITICAL_FAILURE" in line:
            self._handle_crisis(line)

    def _handle_crisis(self, error_line):
        current_time = time.time()
        
        # Verifica se é um erro recorrente (aconteceu menos de 5s depois do último fix)
        is_recurring = (current_time - self.last_fix_time) < 10
        
        print("\n" + "="*50)
        if is_recurring:
            self.retry_count += 1
            print(f"{Fore.RED}{Style.BRIGHT}🔁 FALHA NA TENTATIVA ANTERIOR! (Tentativa {self.retry_count})")
            print(f"{Fore.RED}O erro persiste ou mudou. Forçando re-análise profunda.")
            feedback = f"O erro '{error_line}' ocorreu IMEDIATAMENTE após sua correção anterior."
        else:
            self.retry_count = 0
            feedback = None
            print(f"{Fore.RED}{Style.BRIGHT}🚨 ANOMALIA DETECTADA")
        
        print(f"{Fore.RED}RAW: {error_line}")
        print("="*50)

        # Se tentou 5 vezes e não deu, aborta para não gastar API infinita
        if self.retry_count > 5:
            print(f"{Fore.RED}[FATAL] O sistema não consegue se auto-reparar. Intervenção humana necessária.")
            sys.exit(1)
        
        # FASE 1: Architect com Memória
        fixed_code = self.architect.diagnose_and_fix(error_line, self.victim_path, previous_attempt=feedback)
        
        if fixed_code:
            # FASE 2: Validator
            if self.surgeon.apply_patch(self.victim_path, fixed_code, self.validator):
                self.last_fix_time = time.time()
                print(f"\n{Fore.GREEN}✨ Patch aplicado. Monitorando estabilidade...")
                
                # Pequena pausa para o servidor reiniciar
                time.sleep(3)
        
        print("="*50 + "\n")

if __name__ == "__main__":
    LOG_FILE = "../../shared_logs/app.log"
    VICTIM_SOURCE = "../../victim-app/reactor_core.py" # Mudamos o alvo para algo complexo
    
    bot = Sentinel(LOG_FILE, VICTIM_SOURCE)
    bot.start_monitoring()