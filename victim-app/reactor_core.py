# victim-app/reactor_core.py
import logging
import time
import random
from fastapi import FastAPI, HTTPException

# Importando o sistema de resfriamento (Dependência Crítica)
from cooling_system import CoolingPump

# Configuração de Logs Centralizada
logging.basicConfig(
    filename='../shared_logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- CONSTANTES DE ENGENHARIA E SEGURANÇA ---
# CORREÇÃO CRÍTICA: Definição do protocolo correto conforme cooling_system.py
SECURITY_PROTOCOL_CODE = "ALPHA-9" 
MAX_SAFE_TEMPERATURE = 1000
MIN_SENSOR_RANGE = 800
MAX_SENSOR_RANGE = 1500

app = FastAPI(title="Nuclear Reactor Control - Recovery Mode")

# Inicialização do Hardware
pump = CoolingPump()

@app.get("/status")
def check_core():
    """
    Monitora a temperatura do núcleo e aciona subsistemas de segurança.
    Implementa lógica defensiva e tratamento de exceções granulares.
    """
    # Simulação de telemetria do sensor
    temp = random.randint(MIN_SENSOR_RANGE, MAX_SENSOR_RANGE)
    logging.info(f"Telemetry Reading - Core Temperature: {temp}C")
    
    # Verifica limite de segurança operacional
    if temp > MAX_SAFE_TEMPERATURE:
        logging.warning(f"THRESHOLD EXCEEDED: Temp {temp}C > {MAX_SAFE_TEMPERATURE}C. Initiating countermeasures.")
        
        try:
            # CORREÇÃO APLICADA:
            # 1. Uso do código 'ALPHA-9' em vez de 'GUEST-USER'.
            # 2. Verificação explícita do retorno da ativação.
            
            logging.info(f"Attempting cooling pump activation with protocol: {SECURITY_PROTOCOL_CODE}")
            
            # Tenta ativar a bomba
            pump.activate(SECURITY_PROTOCOL_CODE)
            
            # Validação Defensiva: Confirmar se o estado interno mudou, se possível
            if pump.status != "ACTIVE":
                raise RuntimeError("Hardware Error: Pump accepted command but status remains OFF.")
            
            logging.info("Cooling System: ENGAGED successfully.")
            return {
                "status": "COOLING_ACTIVATED", 
                "temp": temp, 
                "protocol_used": "SECURE"
            }
            
        except PermissionError as perm_err:
            # Captura específica para falha de credenciais (O erro original)
            error_msg = f"SECURITY CRITICAL: Protocol Rejected by Hardware. {str(perm_err)}"
            logging.critical(error_msg)
            # Em sistema real: Acionar SCRAM (Desligamento de Emergência)
            raise HTTPException(status_code=503, detail="CRITICAL ERROR: Security Protocol Mismatch. SCRAM Initiated.")
            
        except Exception as e:
            # Captura genérica para falhas mecânicas ou desconhecidas
            error_msg = f"HARDWARE FAILURE: Cooling system unresponsive. {str(e)}"
            logging.critical(error_msg)
            raise HTTPException(status_code=500, detail="MELTDOWN IMMINENT - EVACUATE FACILITY")
            
    # Estado Nominal
    return {"status": "NORMAL", "temp": temp, "integrity": "STABLE"}