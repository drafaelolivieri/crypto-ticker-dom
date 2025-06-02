#!/bin/bash

# Adiciona os repositórios necessários
helm repo add grafana https://grafana.github.io/helm-charts
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Cria o namespace
kubectl create namespace observability

# Instala Loki
helm install loki grafana/loki \
  -n observability -f loki-values.yaml

# Instala Promtail
helm install promtail grafana/promtail \
  -n observability -f promtail-values.yaml

# Instala Prometheus
helm install prometheus prometheus-community/prometheus \
  -n observability -f prometheus-values.yaml

# Instala Grafana
helm install grafana grafana/grafana \
  -n observability -f grafana-values.yaml

# Aguarda todos os pods estarem prontos
echo "Aguardando todos os pods iniciarem..."
kubectl wait --for=condition=ready pod --all -n observability --timeout=300s

# Obtém a senha do admin do Grafana
echo "\nSenha do admin do Grafana:"
kubectl get secret --namespace observability grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo

# Obtém o IP do LoadBalancer do Grafana
echo "\nEndereço do Grafana:"
kubectl get svc -n observability grafana -o jsonpath="{.status.loadBalancer.ingress[0].ip}" ; echo 