from flask import Flask, render_template, request, jsonify
import requests
import os
from datetime import datetime
from instrumentation import configure_telemetry
import urllib3

# Desabilitar avisos de SSL não verificado
urllib3.disable_warnings()

app = Flask(__name__)

# Configuração de telemetria (traces, métricas e logs)
logger, metrics = configure_telemetry(app)

# === CONFIGURAÇÕES ===
app.config['JSON_AS_ASCII'] = False  # Permite caracteres não-ASCII no JSON
ENVIRONMENT = os.getenv('ENVIRONMENT', 'staging')
LOGIN_MERCADO_BITCOIN = os.getenv('MB_LOGIN', "b131d9c70e9a73e299a53203b50289f4dc2b2a1e41780c810ebcabd83da5d011")
PASSWORD_MERCADO_BITCOIN = os.getenv('MB_PASSWORD', "daf39bec7a6ef9fc61304bea46db3be769b872600535052c59e2a3e1648ff09b")
AUTH_URL = "https://api.mercadobitcoin.net/api/v4/authorize"

# === LISTA DE PARES SUPORTADOS ===
AVAILABLE_PAIRS = [
    {"symbol": "BTC-BRL", "desc": "Bitcoin"},
    {"symbol": "ETH-BRL", "desc": "Ethereum"},
    {"symbol": "XRP-BRL", "desc": "XRP"},
    {"symbol": "LTC-BRL", "desc": "Litecoin"},
    {"symbol": "SOL-BRL", "desc": "Solana"},
]

def authenticate():
    """Obtém token de acesso da API"""
    try:
        logger.info("Tentando autenticar na API do Mercado Bitcoin")
        response = requests.post(
            AUTH_URL,
            json={
                "login": LOGIN_MERCADO_BITCOIN,
                "password": PASSWORD_MERCADO_BITCOIN
            },
            headers={"Content-Type": "application/json"},
            timeout=10,
            verify=False  # Ignorar verificação SSL
        )
        response.raise_for_status()
        auth_data = response.json()
        logger.info("Autenticação bem sucedida")
        return auth_data
        
    except Exception as e:
        logger.error(f"Falha na autenticação: {str(e)}", exc_info=True)
        return {"error": True, "message": f"Falha na autenticação: {str(e)}"}

def get_ticker_data(symbol):
    """Consulta o ticker na API com autenticação"""
    auth_result = authenticate()
    if auth_result.get('error'):
        return auth_result
    
    access_token = auth_result.get('access_token')
    if not access_token:
        logger.error("Falha ao obter token de acesso")
        return {"error": True, "message": "Falha ao obter token de acesso"}
    
    try:
        logger.info(f"Consultando ticker para o par {symbol}")
        url = f"https://api.mercadobitcoin.net/api/v4/tickers?symbols={symbol}"
        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            timeout=10,
            verify=False  # Ignorar verificação SSL
        )
        response.raise_for_status()
        
        ticker_list = response.json()
        if not ticker_list:  # Se a lista estiver vazia
            logger.warning(f"Ticker não encontrado para o par {symbol}")
            return {"error": True, "message": "Erro na consulta: ticker não encontrado"}
            
        ticker_data = ticker_list[0]  # Pega o primeiro item da lista de tickers
        logger.info(f"Dados do ticker obtidos com sucesso para {symbol}")
        return {
            "high": ticker_data.get("high"),
            "low": ticker_data.get("low"),
            "vol": ticker_data.get("vol"),
            "last": ticker_data.get("last"),
            "buy": ticker_data.get("buy"),
            "sell": ticker_data.get("sell"),
            "open": ticker_data.get("open"),
            "date": ticker_data.get("date"),
            "pair": symbol,
            "error": False
        }
        
    except requests.exceptions.HTTPError as err:
        logger.error(f"Erro HTTP ao consultar ticker: {err.response.text}", exc_info=True)
        return {"error": True, "message": f"Erro HTTP: {err.response.text}"}
    except Exception as err:
        logger.error(f"Erro ao consultar ticker: {str(err)}", exc_info=True)
        return {"error": True, "message": "Erro na consulta: ticker não encontrado"}

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_pair = request.form.get("pair") if request.method == 'POST' else None
    ticker_data = None
    error_message = None

    if request.method == 'POST':
        logger.info(f"Requisição POST recebida para o par {selected_pair}")
        pair_info = next((p for p in AVAILABLE_PAIRS if p['symbol'] == selected_pair), None)
        if not pair_info:
            error_message = "Par inválido"
            logger.warning(f"Tentativa de acesso com par inválido: {selected_pair}")
        else:
            result = get_ticker_data(selected_pair)
            if result.get('error'):
                error_message = result.get('message')
            else:
                ticker_data = result
                ticker_data['pair'] = selected_pair

    return render_template('index.html',
                           available_pairs=AVAILABLE_PAIRS,
                           selected_pair=selected_pair,
                           ticker_data=ticker_data,
                           error_message=error_message)

@app.route('/ticker/<pair>')
@metrics.counter('ticker_api_requests_total', 'Number of requests to the ticker API',
                labels={'pair': lambda: request.view_args['pair']})
def api_ticker(pair):
    logger.info(f"Requisição API recebida para o par {pair}")
    result = get_ticker_data(pair)
    
    if result.get('error'):
        logger.error(f"Erro ao processar requisição API para {pair}: {result.get('message')}")
        return jsonify(result), 500
    
    if 'error' in result:
        del result['error']
    
    response = {
        "environment": ENVIRONMENT,
        "ticker": [result]
    }
    
    logger.info(f"Resposta API enviada com sucesso para {pair}")
    return jsonify(response)

@app.route('/health')
@metrics.counter('health_check_total', 'Number of health check requests')
def health():
    """Endpoint de health check"""
    logger.debug("Health check solicitado")
    return jsonify({"status": "healthy", "environment": ENVIRONMENT})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Iniciando aplicação na porta {port}")
    app.run(host='0.0.0.0', port=port) 