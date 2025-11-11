import json
from typing import List, Dict, Any
from datetime import datetime

#
# formatters.py
#
# This file centralizes the routines used to format the tool output.
# Currentl, JSON and tabulated cli out. are supported.
#


class TableFormatter:
    @staticmethod
    def format_deployments(deployments: List[Dict[str, Any]]) -> str:
        if not deployments:
            return "No deployments found."

        # Calculate column widths
        max_name = max(len(d["name"]) for d in deployments)
        max_namespace = max(len(d["namespace"]) for d in deployments)
        max_images = max(
            len(", ".join(d["images"])) if d["images"] else 0
            for d in deployments
        )

        # Ensure minimum widths for headers
        max_name = max(max_name, len("NAME"))
        max_namespace = max(max_namespace, len("NAMESPACE"))
        max_images = max(max_images, len("IMAGES"))
        max_created = len("CREATED")
        max_replicas = len("REPLICAS")

        # Create header
        header = (
            f"{'NAME':<{max_name}}  "
            f"{'NAMESPACE':<{max_namespace}}  "
            f"{'IMAGES':<{max_images}}  "
            f"{'CREATED':<{max_created}}  "
            f"{'REPLICAS':<{max_replicas}}"
        )

        separator = "-" * len(header)

        # Create rows
        rows = []
        for deployment in deployments:
            images_str = ", ".join(deployment["images"]) if deployment["images"] else "None"
            created_str = TableFormatter._format_timestamp(deployment["created"])

            row = (
                f"{deployment['name']:<{max_name}}  "
                f"{deployment['namespace']:<{max_namespace}}  "
                f"{images_str:<{max_images}}  "
                f"{created_str:<{max_created}}  "
                f"{deployment['replicas']:<{max_replicas}}"
            )
            rows.append(row)

        # Combine all parts
        return "\n".join([header, separator] + rows)

    @staticmethod
    def _format_timestamp(timestamp: datetime) -> str:
        if timestamp is None:
            return "Unknown"
        return timestamp.strftime("%Y-%m-%d")


class JSONFormatter:
    @staticmethod
    def format_deployments(deployments: List[Dict[str, Any]]) -> str:
        # Convert datetime objects to strings for JSON serialization
        serializable_deployments = []
        for deployment in deployments:
            serializable_deployment = deployment.copy()
            if deployment["created"]:
                serializable_deployment["created"] = deployment["created"].isoformat()
            else:
                serializable_deployment["created"] = None
            serializable_deployments.append(serializable_deployment)

        return json.dumps(serializable_deployments, indent=2)
