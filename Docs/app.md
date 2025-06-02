# Crypto Ticker - Documentação Completa

# Sumário
- [Visão Geral](#visão-geral)
- [Tecnologias](#tecnologias)
- [Instalação e Configuração](#instalação-e-configuração)
- [Arquitetura](#arquitetura)
- [API](#api)
- [Interface do Usuário](#interface-do-usuário)

# Visão Geral
O Crypto Ticker é uma aplicação web desenvolvida em Python que fornece informações em tempo real sobre preços de criptomoedas através da API do Mercado Bitcoin. A aplicação oferece tanto uma interface web amigável quanto endpoints de API para consulta programática.

# Tecnologias
- Python 3.9
- Flask 2.0.1
- Docker
- Bootstrap 5.1.3

## Pares de Criptomoedas Suportados
- BTC-BRL (Bitcoin)
- ETH-BRL (Ethereum)
- XRP-BRL (XRP)
- LTC-BRL (Litecoin)
- SOL-BRL (Solana)

# Instalação e Configuração

## Pré-requisitos
- Docker instalado
- Python 3.9+ (para desenvolvimento local)
- pip (gerenciador de pacotes Python)

## Instalação

### Usando Docker (Recomendado)
1. Clone o repositório
2. No diretório raiz do projeto, execute:
```bash
docker build -t crypto-ticker ./app
docker run -p 8080:8080 crypto-ticker
```

### Instalação Local
1. Clone o repositório
2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```
3. Instale as dependências:
```bash
pip install -r app/requirements.txt
```

## Configuração

### Variáveis de Ambiente
A aplicação utiliza as seguintes variáveis de ambiente:

- `PORT`: Porta onde a aplicação será executada (padrão: 8080)
- `ENVIRONMENT`: Ambiente de execução (padrão: staging)
- `MB_LOGIN`: Login da API do Mercado Bitcoin
- `MB_PASSWORD`: Senha da API do Mercado Bitcoin

### Configuração via Docker
As variáveis de ambiente podem ser configuradas no Dockerfile ou passadas durante a execução do container:

```bash
docker run -p 8080:8080 \
  -e ENVIRONMENT=production \
  -e MB_LOGIN=seu_login \
  -e MB_PASSWORD=sua_senha \
  crypto-ticker
```

### Configuração Local
Para desenvolvimento local, você pode criar um arquivo `.env` na raiz do projeto com as variáveis necessárias.

# Arquitetura

## Visão Geral da Arquitetura
A aplicação segue uma arquitetura web simples e modular, construída com Flask. Os principais componentes são:

```
app/
├── src/
│   ├── app.py           # Aplicação principal
│   ├── test_app.py      # Testes
│   └── templates/       # Templates HTML
│       └── index.html   # Interface do usuário
├── requirements.txt     # Dependências
└── Dockerfile          # Configuração Docker
```

## Componentes Principais

### Aplicação Principal (app.py)
- **Servidor Web Flask**: Gerencia as requisições HTTP e renderiza as páginas
- **Autenticação**: Implementa autenticação com a API do Mercado Bitcoin
- **Gerenciamento de Dados**: Processa e formata dados de criptomoedas

### Camada de API
- **Endpoint `/ticker/<par>`**: Fornece dados em tempo real para pares de criptomoedas
- **Endpoint `/health`**: Monitoramento da saúde da aplicação
- **Autenticação**: Gerencia tokens de acesso para a API do Mercado Bitcoin

### Interface do Usuário
- **Template Responsivo**: Interface web construída com Bootstrap
- **Formulário de Consulta**: Permite seleção de pares de criptomoedas
- **Exibição de Dados**: Mostra informações detalhadas sobre preços e volumes

## Fluxo de Dados
1. O usuário seleciona um par de criptomoedas na interface
2. A aplicação autentica com a API do Mercado Bitcoin
3. Os dados são requisitados da API externa
4. Os resultados são processados e formatados
5. As informações são exibidas na interface ou retornadas via API

## Segurança
- Autenticação via tokens JWT
- Variáveis de ambiente para credenciais
- Sanitização de inputs
- Tratamento de erros e validações

## Monitoramento
- Endpoint de health check para monitoramento
- Logs de erros e acessos
- Métricas de performance via Docker

# API

## Visão Geral da API
A API do Crypto Ticker fornece endpoints para consulta de preços de criptomoedas em tempo real. Todos os dados são obtidos através da API do Mercado Bitcoin.

## Endpoints

### GET /ticker/{par}
Retorna informações detalhadas sobre um par de criptomoedas específico.

#### Parâmetros da URL
- `par` (obrigatório): Par de criptomoedas (exemplo: BTC-BRL)

#### Exemplo de Resposta
```json
{
    "environment": "staging",
    "ticker": [{
        "high": "150000.00000000",
        "low": "147000.00000000",
        "vol": "10.12345678",
        "last": "148500.00000000",
        "buy": "148400.00000000",
        "sell": "148600.00000000",
        "open": "147500.00000000",
        "date": "1234567890",
        "pair": "BTC-BRL"
    }]
}
```

#### Campos da Resposta
- `high`: Maior preço negociado nas últimas 24 horas
- `low`: Menor preço negociado nas últimas 24 horas
- `vol`: Volume negociado nas últimas 24 horas
- `last`: Preço da última negociação
- `buy`: Maior preço de compra das últimas 24 horas
- `sell`: Menor preço de venda das últimas 24 horas
- `open`: Preço de abertura
- `date`: Timestamp da última atualização
- `pair`: Par de criptomoedas consultado

### GET /health
Endpoint para verificação da saúde da aplicação.

#### Exemplo de Resposta
```json
{
    "status": "healthy",
    "environment": "staging"
}
```

## Tratamento de Erros
Em caso de erro, a API retorna uma resposta com a seguinte estrutura:

```json
{
    "error": true,
    "message": "Descrição detalhada do erro"
}
```

## Limites e Restrições
- Todas as requisições devem ser feitas via HTTPS
- As respostas são limitadas a 50 resultados por requisição
- Os dados são atualizados em tempo real
- O rate limit é definido pela API do Mercado Bitcoin

# Interface do Usuário

## Visão Geral da Interface
A interface do usuário do Crypto Ticker foi desenvolvida para ser intuitiva e responsiva, permitindo fácil acesso às informações de preços de criptomoedas.

## Componentes da Interface

### Seletor de Pares
- Dropdown menu com todos os pares de criptomoedas disponíveis
- Exibe nome completo e símbolo da criptomoeda
- Mantém a seleção após a consulta

### Painel de Informações
O painel principal exibe as seguintes informações para o par selecionado:

#### Preços
- **Último**: Preço da última negociação
- **Maior**: Maior preço nas últimas 24h
- **Menor**: Menor preço nas últimas 24h
- **Compra**: Melhor preço de compra atual
- **Venda**: Melhor preço de venda atual

#### Dados Adicionais
- **Volume**: Volume negociado em 24h
- **Abertura**: Preço de abertura
- **Data**: Timestamp da última atualização

### Mensagens de Erro
- Exibidas em destaque no topo da página
- Formatação em vermelho para alertas
- Mensagens claras e informativas

## Estilização
A interface utiliza o framework Bootstrap 5.1.3 para:
- Layout responsivo
- Componentes modernos
- Esquema de cores consistente
- Adaptação para diferentes tamanhos de tela

## Acessibilidade
- Labels descritivos em todos os campos
- Contraste adequado para leitura
- Navegação via teclado
- Suporte a leitores de tela

## Responsividade
A interface se adapta aos seguintes dispositivos:
- Desktop (>1200px)
- Tablet (768px - 1199px)
- Mobile (<768px)

## Boas Práticas
- Carregamento rápido
- Feedback imediato das ações
- Validação de entrada de dados
- Tratamento adequado de erros
- Cache de dados quando apropriado 