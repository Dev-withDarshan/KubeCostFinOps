#!/bin/bash
export KUBECONFIG=/root/.kube/config

forward_ksm() {
  while true; do
    kubectl -n monitoring port-forward svc/kube-state-metrics 8080:8080 --address 0.0.0.0
    sleep 2
  done
}

forward_prom() {
  while true; do
    kubectl -n monitoring port-forward svc/prometheus-server 9090:9090 --address 0.0.0.0
    sleep 2
  done
}

forward_opencost() {
  while true; do
    kubectl -n monitoring port-forward svc/opencost 9003:9003 --address 0.0.0.0
    sleep 2
  done
}

forward_ksm &
forward_prom &
forward_opencost &
wait

