from typing import Optional, List, Dict, Any
from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

#
# kube_client.py
#
# This file is used for a Kubernetes wrapper that we use in the rest of the code.
#


class K8sClient:
    def __init__(self, kubeconfig: Optional[str] = None, context: Optional[str] = None):
        self.kubeconfig = kubeconfig
        self.context = context
        self._apps_v1 = None
        self._core_v1 = None
        self._load_config()

    def _load_config(self):
        try:
            if self.kubeconfig:
                config.load_kube_config(
                    config_file=self.kubeconfig, context=self.context
                )
            else:
                config.load_kube_config(context=self.context)

            self._apps_v1 = client.AppsV1Api()
            self._core_v1 = client.CoreV1Api()

        except config.ConfigException as e:
            raise ConnectionError(f"Failed to load kubeconfig: {e}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Kubernetes: {e}")

    def get_namespaces(self) -> List[str]:
        try:
            namespaces = self._core_v1.list_namespace()
            return [ns.metadata.name for ns in namespaces.items]
        except ApiException as e:
            raise ApiException(f"Failed to list namespaces: {e}")

    def get_deployments(self, namespace: str = "default") -> List[Dict[str, Any]]:
        try:
            deployments = self._apps_v1.list_namespaced_deployment(namespace)
            result = []

            for deployment in deployments.items:
                images = []
                if deployment.spec.template.spec.containers:
                    images = [
                        container.image
                        for container in deployment.spec.template.spec.containers
                    ]

                result.append(
                    {
                        "name": deployment.metadata.name,
                        "namespace": deployment.metadata.namespace,
                        "images": images,
                        "created": deployment.metadata.creation_timestamp,
                        "replicas": deployment.spec.replicas or 0,
                    }
                )

            return result

        except ApiException as e:
            raise ApiException(
                f"Failed to list deployments in namespace {namespace}: {e}"
            )

    def get_all_deployments(self) -> List[Dict[str, Any]]:
        try:
            deployments = self._apps_v1.list_deployment_for_all_namespaces()
            result = []

            for deployment in deployments.items:
                images = []
                if deployment.spec.template.spec.containers:
                    images = [
                        container.image
                        for container in deployment.spec.template.spec.containers
                    ]

                result.append(
                    {
                        "name": deployment.metadata.name,
                        "namespace": deployment.metadata.namespace,
                        "images": images,
                        "created": deployment.metadata.creation_timestamp,
                        "replicas": deployment.spec.replicas or 0,
                    }
                )

            return result

        except ApiException as e:
            raise ApiException(f"Failed to list deployments across all namespaces: {e}")
