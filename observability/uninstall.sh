#!/bin/bash

# Desinstala todos os releases
helm uninstall grafana -n observability
helm uninstall prometheus -n observability
helm uninstall promtail -n observability
helm uninstall loki -n observability

# Remove o namespace
kubectl delete namespace observability 