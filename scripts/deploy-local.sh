#!/usr/bin/env bash
# deploy-local.sh — ALL-LOCAL deploy: build images and apply to a local Kubernetes.
# No GHCR, no cloud registry, no cloud runners.
#
# Usage:
#   ./scripts/deploy-local.sh                 # build + apply to local cluster
#   ./scripts/deploy-local.sh --skip-build    # apply only (reuse local images)
set -euo pipefail

NAMESPACE=${K8S_NAMESPACE:-mlops-production}
IMAGE_TAG="local-$(git rev-parse --short HEAD 2>/dev/null || echo dev)"
REGISTRY="local"
IMAGE_REF="${REGISTRY}/mlops-api:${IMAGE_TAG}"

echo "==> All-local deploy (image: ${IMAGE_REF})"

if [[ "${1:-}" != "--skip-build" ]]; then
  echo "==> Building API image"
  docker build -f docker/Dockerfile.api -t "${IMAGE_REF}" .
fi

kubectl get namespace "${NAMESPACE}" >/dev/null 2>&1 || kubectl create namespace "${NAMESPACE}"

echo "==> Applying kustomize overlay"
kustomize build k8s/overlays/production | \
  sed "s#mlops-api:local#${IMAGE_REF}#g" | \
  kubectl apply -f -

echo "==> Waiting for rollout"
kubectl rollout status deployment/mlops-api --namespace="${NAMESPACE}" --timeout=300s

echo "==> Health check"
kubectl get pods --namespace="${NAMESPACE}" -l app=mlops-api
kubectl get hpa --namespace="${NAMESPACE}"

echo "==> Done (all-local)"