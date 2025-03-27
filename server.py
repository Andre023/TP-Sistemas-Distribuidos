# O código acima implementa um servidor Flask que fornece um endpoint para obter o horário NTP.
# O cliente (cliente.py) faz uma requisição para esse servidor, enviando o tempo T1. 
# O servidor responde com os tempos T2 e T3, que são usados para calcular o offset do relógio local. 
# O cliente então ajusta seu relógio local gradualmente para sincronizá-lo com o horário correto.
import ntplib
from flask import Flask, jsonify, request
import time

app = Flask(__name__)

def get_ntp_time():
    """Obtém o horário atualizado via NTP"""
    try:
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        return response.tx_time  # Retorna o tempo correto do servidor NTP
    except Exception as e:
        print(f"Erro ao obter NTP: {e}")
        return time.time()  # Em caso de erro, retorna o tempo local como fallback

@app.route('/time', methods=['GET'])
def get_time():
    """Endpoint que retorna T2 (tempo de recebimento) e T3 (tempo de resposta)"""
    T1 = float(request.args.get('T1', time.time()))  # Obtém o T1 enviado pelo cliente
    T2 = get_ntp_time()  # Tempo de recebimento da requisição
    time.sleep(0.01)  # Simula pequeno atraso no processamento
    T3 = get_ntp_time()  # Tempo de envio da resposta
    return jsonify({'T2': T2, 'T3': T3})  # Retorna os tempos para o cliente

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Inicia o servidor Flask


