#!/usr/bin/env bash
set -euo pipefail

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm upgrade --install kube-prometheus-stack prometheus-community/kube-prometheus-stack \
  --namespace monitoring --create-namespace \
  -f values.yaml \
  --set grafana.adminPassword="${GRAFANA_ADMIN_PASSWORD:?set GRAFANA_ADMIN_PASSWORD}"

kubectl apply -f alerts.yaml

echo "Grafana:  kubectl -n monitoring port-forward svc/kube-prometheus-stack-grafana 3000:80"
echo "Prometheus: kubectl -n monitoring port-forward svc/kube-prometheus-stack-prometheus 9090:9090"
