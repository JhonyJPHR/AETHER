# victim-app/cooling_system.py
class CoolingPump:
    def __init__(self):
        self.status = "OFF"
    
    def activate(self, protocol_code):
        """
        A bomba só ativa se receber o código de segurança 'ALPHA-9'.
        Qualquer outra coisa gera erro de acesso negado.
        """
        if protocol_code != "ALPHA-9":
            raise PermissionError("INVALID SECURITY PROTOCOL: Pump Activation Denied.")
        
        self.status = "ACTIVE"
        return True