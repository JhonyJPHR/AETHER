# aether-core/sentinel/sentinel_engine.py
import time
import os
import sys
from colorama import Fore, Style, init

# Configuração de Paths para importação
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Importando os Módulos
from architect.architect_engine import Architect
from surgeon.surgeon_engine import Surgeon

init(autoreset=True)

class Sentinel:
    def __init__(self, log_path, victim_path):
        self.log_path = log_path
        self.victim_path = victim_path
        self.is_running = False
        
        # Inicializa os subsistemas
        self.architect = Architect()
        self.surgeon = Surgeon()
        
        print(f"{Fore.CYAN}[SENTINEL] Sistema inicializado. Alvo: {log_path}")

    def start_monitoring(self):
        self.is_running = True
        print(f"{Fore.GREEN}[SENTINEL] 👁️  Monitoramento Ativo. Aguardando anomalias...")
        
        try:
            with open(self.log_path, 'r') as file:
                file.seek(0, 2)
                while self.is_running:
                    line = file.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    self._analyze_line(line)     
        except FileNotFoundError:
            print(f"{Fore.RED}[ERRO] Log não encontrado: {self.log_path}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[SENTINEL] Encerrando vigilância.")

    def _analyze_line(self, line):
        line = line.strip()
        if "CRITICAL_FAILURE" in line:
            self._trigger_alert(line)

    def _trigger_alert(self, error_line):
        print("\n" + "="*50)
        print(f"{Fore.RED}{Style.BRIGHT}🚨 ANOMALIA DETECTADA [NÍVEL 5]")
        print(f"{Fore.RED}RAW DATA: {error_line}")
        print("="*50)
        
        # FASE 1: DIAGNÓSTICO
        print(f"{Fore.YELLOW}>>> [FASE 1] Acionando Architect...")
        fixed_code = self.architect.diagnose_and_fix(error_line, self.victim_path)
        
        if fixed_code:
            # FASE 2: CIRURGIA
            print(f"{Fore.CYAN}>>> [FASE 2] Código recebido. Acionando Surgeon...")
            success = self.surgeon.apply_patch(self.victim_path, fixed_code)
            
            if success:
                print(f"\n{Fore.GREEN}✨ CICLO DE AUTO-CURA COMPLETO. AMEAÇA NEUTRALIZADA. ✨")
                # Pausa para não ficar detectando o mesmo erro antigo no log repetidamente
                time.sleep(2) 
        
        print("="*50 + "\n")

if __name__ == "__main__":
    LOG_FILE = "../../shared_logs/app.log"
    VICTIM_SOURCE = "../../victim-app/main.py" 
    
    bot = Sentinel(LOG_FILE, VICTIM_SOURCE)
    bot.start_monitoring()