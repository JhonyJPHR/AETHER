import logging
import sys
from fastapi import FastAPI, HTTPException

# O limite de recursão foi removido/restaurado para o padrão, 
# pois a lógica foi corrigida para não estourar a pilha.

logging.basicConfig(
    filename='../shared_logs/app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(title="ChaosBank API - Target System")

@app.get("/")
def read_root():
    return {"status": "active", "system": "ChaosBank"}

# --- LÓGICA CORRIGIDA ---
def calculate_compound_interest(amount: float, periods: int = 12) -> float:
    """
    Função Corrigida: Implementa recursão com caso base (limite de profundidade).
    Calcula o valor futuro com juros de 1% por período.
    
    Args:
        amount: Valor atual.
        periods: Número de períodos restantes (condição de parada).
    """
    logging.info(f"Calculando juros. Períodos restantes: {periods}, Valor: {amount:.2f}")
    
    # 1. CASO BASE: Se os períodos acabaram, retorna o valor acumulado.
    if periods <= 0:
        return amount
    
    # 2. PASSO RECURSIVO: Calcula o próximo valor e decrementa o contador de períodos.
    # Correção Lógica: Retornamos o resultado da próxima chamada, não a soma (amount + ...),
    # para refletir corretamente o cálculo de juros compostos (Valor Final).
    return calculate_compound_interest(amount * 1.01, periods - 1)

@app.get("/investment/{amount}")
def simulate_investment(amount: float):
    logging.info(f"Iniciando simulação de investimento: ${amount}")
    
    try:
        # Define um limite seguro de iterações (ex: 12 meses)
        final_value = calculate_compound_interest(amount, periods=12)
        
        return {"original": amount, "final": round(final_value, 2)}

    except Exception as e:
        # Captura genérica para outros erros imprevistos
        error_msg = f"CRITICAL_FAILURE: {str(e)}"
        logging.error(error_msg)
        raise HTTPException(status_code=500, detail="Internal Server Error")