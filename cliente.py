# O cliente se conecta a um servidor Flask que fornece o horário NTP e ajusta seu relógio local gradualmente.
# O cliente simula um relógio local com um erro inicial aleatório entre -10 e +10 segundos.
# O cliente se conecta ao servidor Flask que fornece o horário NTP e ajusta seu relógio local gradualmente.
import time
import requests
import random

SERVER_URL = 'http://server:5000/time'  # URL do servidor de tempo

# Função para obter o horário do servidor e calcular o offset
def get_server_time():
    """Obtém T2 e T3 do servidor e calcula o offset"""
    T1 = time.time()  # Marca o tempo antes de enviar a requisição
    try:
        response = requests.get(SERVER_URL, params={'T1': T1}, timeout=5) 
        T4 = time.time()  # Tempo de recebimento da resposta
        data = response.json()
        T2 = data['T2']
        T3 = data['T3']
        
        # Cálculo do offset conforme o algoritmo de Cristian
        offset = ((T2 - T1) + (T3 - T4)) / 2
        estimated_time = T4 + offset  # Ajusta o tempo local com base no offset
        return estimated_time, offset
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        return time.time(), 0  # Em caso de erro, mantém o tempo local

# Função para ajustar o relógio local gradualmente
def adjust_clock(current_time, target_time):
    """Ajusta o relógio local de forma gradual"""
    step = 0.1  # Ajuste gradual de 0.1s para evitar saltos abruptos
    while abs(current_time - target_time) > step:
        if current_time < target_time:
            current_time += step
        else:
            current_time -= step
        print(f"Ajustando relógio para: {current_time:.2f}")
        time.sleep(0.1)  # Pequena pausa para simular o ajuste gradual
    return target_time

# Função principal para executar o cliente
if __name__ == '__main__':
    # Simula um relógio local com um erro inicial aleatório entre -10 e +10 segundos
    offset = random.uniform(-10, 10)
    local_time = time.time() + offset
    print(f"Horário local inicial: {local_time:.2f} (offset: {offset:.2f}s)")

    # Loop para sincronizar o relógio local com o horário do servidor
    while True:
        estimated_time, offset = get_server_time()
        print(f"Offset calculado: {offset:.2f}s, Hora estimada: {estimated_time:.2f}")
        local_time = adjust_clock(local_time, estimated_time)
        print(f"Horário local sincronizado: {local_time:.2f}")
        time.sleep(10)  # Aguarda 10 segundos antes da próxima atualização


