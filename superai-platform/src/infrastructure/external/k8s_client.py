"""Kubernetes client — cluster introspection and workload management."""
from __future__ import annotations

import os
from typing import Any

import structlog

logger = structlog.get_logger(__name__)


class K8sClient:
    """Lightweight Kubernetes API client for admin operations.

    Uses the official kubernetes-client when available, falls back to
    httpx calls against the in-cluster API server.
    """

    def __init__(self) -> None:
        self._client: Any = None
        self._available = False
        self._init_client()

    def _init_client(self) -> None:
        try:
            from kubernetes import client, config

            if os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token"):
                config.load_incluster_config()
            else:
                config.load_kube_config()

            self._client = client
            self._available = True
            logger.info("k8s_client_initialized", in_cluster=os.path.exists(
                "/var/run/secrets/kubernetes.io/serviceaccount/token"
            ))
        except Exception as exc:
            logger.warning("k8s_client_unavailable", error=str(exc))
            self._available = False

    @property
    def is_available(self) -> bool:
        return self._available

    # ------------------------------------------------------------------
    # Namespace operations
    # ------------------------------------------------------------------

    def list_namespaces(self) -> list[dict[str, Any]]:
        if not self._available:
            return []
        v1 = self._client.CoreV1Api()
        ns_list = v1.list_namespace()
        return [
            {
                "name": ns.metadata.name,
                "status": ns.status.phase,
                "created_at": ns.metadata.creation_timestamp.isoformat()
                if ns.metadata.creation_timestamp else None,
                "labels": dict(ns.metadata.labels or {}),
            }
            for ns in ns_list.items
        ]

    # ------------------------------------------------------------------
    # Pod operations
    # ------------------------------------------------------------------

    def list_pods(self, namespace: str = "default") -> list[dict[str, Any]]:
        if not self._available:
            return []
        v1 = self._client.CoreV1Api()
        pod_list = v1.list_namespaced_pod(namespace=namespace)
        return [
            {
                "name": pod.metadata.name,
                "namespace": pod.metadata.namespace,
                "status": pod.status.phase,
                "node": pod.spec.node_name,
                "ip": pod.status.pod_ip,
                "containers": [
                    {
                        "name": c.name,
                        "image": c.image,
                        "ready": any(
                            cs.name == c.name and cs.ready
                            for cs in (pod.status.container_statuses or [])
                        ),
                    }
                    for c in pod.spec.containers
                ],
                "created_at": pod.metadata.creation_timestamp.isoformat()
                if pod.metadata.creation_timestamp else None,
            }
            for pod in pod_list.items
        ]

    def get_pod_logs(
        self, name: str, namespace: str = "default", tail_lines: int = 100
    ) -> str:
        if not self._available:
            return ""
        v1 = self._client.CoreV1Api()
        return v1.read_namespaced_pod_log(
            name=name,
            namespace=namespace,
            tail_lines=tail_lines,
        )

    # ------------------------------------------------------------------
    # Deployment operations
    # ------------------------------------------------------------------

    def list_deployments(self, namespace: str = "default") -> list[dict[str, Any]]:
        if not self._available:
            return []
        apps = self._client.AppsV1Api()
        dep_list = apps.list_namespaced_deployment(namespace=namespace)
        return [
            {
                "name": dep.metadata.name,
                "namespace": dep.metadata.namespace,
                "replicas": dep.spec.replicas,
                "ready_replicas": dep.status.ready_replicas or 0,
                "available_replicas": dep.status.available_replicas or 0,
                "strategy": dep.spec.strategy.type if dep.spec.strategy else "Unknown",
                "images": [
                    c.image for c in dep.spec.template.spec.containers
                ],
                "created_at": dep.metadata.creation_timestamp.isoformat()
                if dep.metadata.creation_timestamp else None,
            }
            for dep in dep_list.items
        ]

    def scale_deployment(
        self, name: str, replicas: int, namespace: str = "default"
    ) -> dict[str, Any]:
        if not self._available:
            return {"error": "k8s client not available"}
        apps = self._client.AppsV1Api()
        body = {"spec": {"replicas": replicas}}
        result = apps.patch_namespaced_deployment_scale(
            name=name,
            namespace=namespace,
            body=body,
        )
        logger.info("deployment_scaled", name=name, namespace=namespace, replicas=replicas)
        return {
            "name": name,
            "namespace": namespace,
            "replicas": result.spec.replicas,
        }

    def restart_deployment(self, name: str, namespace: str = "default") -> dict[str, Any]:
        if not self._available:
            return {"error": "k8s client not available"}
        from datetime import datetime, timezone

        apps = self._client.AppsV1Api()
        now = datetime.now(timezone.utc).isoformat()
        body = {
            "spec": {
                "template": {
                    "metadata": {
                        "annotations": {
                            "kubectl.kubernetes.io/restartedAt": now,
                        }
                    }
                }
            }
        }
        apps.patch_namespaced_deployment(name=name, namespace=namespace, body=body)
        logger.info("deployment_restarted", name=name, namespace=namespace)
        return {"name": name, "namespace": namespace, "restarted_at": now}

    # ------------------------------------------------------------------
    # Service operations
    # ------------------------------------------------------------------

    def list_services(self, namespace: str = "default") -> list[dict[str, Any]]:
        if not self._available:
            return []
        v1 = self._client.CoreV1Api()
        svc_list = v1.list_namespaced_service(namespace=namespace)
        return [
            {
                "name": svc.metadata.name,
                "namespace": svc.metadata.namespace,
                "type": svc.spec.type,
                "cluster_ip": svc.spec.cluster_ip,
                "ports": [
                    {
                        "name": p.name,
                        "port": p.port,
                        "target_port": p.target_port,
                        "protocol": p.protocol,
                    }
                    for p in (svc.spec.ports or [])
                ],
            }
            for svc in svc_list.items
        ]

    # ------------------------------------------------------------------
    # Node operations
    # ------------------------------------------------------------------

    def list_nodes(self) -> list[dict[str, Any]]:
        if not self._available:
            return []
        v1 = self._client.CoreV1Api()
        node_list = v1.list_node()
        results = []
        for node in node_list.items:
            conditions = {
                c.type: c.status
                for c in (node.status.conditions or [])
            }
            results.append({
                "name": node.metadata.name,
                "ready": conditions.get("Ready", "Unknown"),
                "os": node.status.node_info.os_image if node.status.node_info else "Unknown",
                "kubelet_version": node.status.node_info.kubelet_version
                if node.status.node_info else "Unknown",
                "cpu_capacity": node.status.capacity.get("cpu", "0")
                if node.status.capacity else "0",
                "memory_capacity": node.status.capacity.get("memory", "0")
                if node.status.capacity else "0",
            })
        return results

    # ------------------------------------------------------------------
    # Cluster health
    # ------------------------------------------------------------------

    def cluster_health(self) -> dict[str, Any]:
        if not self._available:
            return {"status": "unavailable", "message": "Kubernetes client not configured"}
        try:
            nodes = self.list_nodes()
            ready_count = sum(1 for n in nodes if n["ready"] == "True")
            return {
                "status": "healthy" if ready_count == len(nodes) else "degraded",
                "total_nodes": len(nodes),
                "ready_nodes": ready_count,
                "nodes": nodes,
            }
        except Exception as exc:
            logger.error("k8s_health_check_failed", error=str(exc))
            return {"status": "error", "message": str(exc)}


__all__ = ["K8sClient"]