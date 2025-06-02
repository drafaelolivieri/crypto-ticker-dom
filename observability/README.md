# Stack de Observabilidade

Esta stack inclui as seguintes ferramentas:
- Grafana: Visualização de métricas e logs
- Prometheus: Coleta e armazenamento de métricas
- Loki: Agregação e armazenamento de logs
- Promtail: Coleta de logs

## Pré-requisitos
- Kubernetes cluster
- Helm v3
- kubectl configurado

## Instalação

Para instalar a stack completa:
```bash
chmod +x install.sh
./install.sh
```

O script irá:
1. Adicionar os repositórios Helm necessários
2. Criar o namespace `observability`
3. Instalar todos os componentes
4. Mostrar a senha do admin do Grafana
5. Mostrar o endereço IP do Grafana

## Desinstalação

Para remover a stack completa:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

## Acessando o Grafana

1. Use o IP mostrado após a instalação
2. Login: `admin`
3. Senha: mostrada após a instalação

## Datasources configurados
- Prometheus: métricas da aplicação
- Loki: logs da aplicação

## Recursos alocados

### Grafana
- Requests: 128Mi RAM, 50m CPU
- Limits: 256Mi RAM

### Prometheus
- Requests: 128Mi RAM, 50m CPU
- Limits: 256Mi RAM

### Loki
- Requests: 128Mi RAM, 50m CPU
- Limits: 256Mi RAM

### Promtail
- Requests: 64Mi RAM, 30m CPU
- Limits: 128Mi RAM

## Observações
- Persistência desabilitada para todos os componentes
- AlertManager e PushGateway do Prometheus desabilitados
- Grafana exposto via LoadBalancer 