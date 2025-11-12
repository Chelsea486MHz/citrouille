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
    #
    # format_deployments
    # Formats a list of deployments as a CLI table with columns for name, namespace, images, created date, and replicas
    #
    @staticmethod
    def format_deployments(deployments: List[Dict[str, Any]]) -> str:
        if not deployments:
            return "No deployments found."

        # Calculate column widths
        max_name = max(len(d["name"]) for d in deployments)
        max_namespace = max(len(d["namespace"]) for d in deployments)
        max_images = max(
            len(", ".join(d["images"])) if d["images"] else 0 for d in deployments
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
            images_str = (
                ", ".join(deployment["images"]) if deployment["images"] else "None"
            )
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

    #
    # _format_timestamp
    # Converts a datetime object to a formatted date string (YYYY-MM-DD)
    #
    @staticmethod
    def _format_timestamp(timestamp: datetime) -> str:
        if timestamp is None:
            return "Unknown"
        return timestamp.strftime("%Y-%m-%d")

    #
    # format_comparison
    # Formats namespace comparison results as a CLI report showing missing, extra, and changed deployments
    #
    @staticmethod
    def format_comparison(
        comparison: Dict[str, List[Dict[str, Any]]], namespace1: str, namespace2: str
    ) -> str:
        lines = []
        lines.append(f"\nComparing namespaces: '{namespace1}' vs '{namespace2}'\n")
        lines.append("=" * 80)

        missing = comparison.get("missing", [])
        if missing:
            lines.append(
                f"\n[-] Missing in '{namespace2}' ({len(missing)} deployment(s)):"
            )
            lines.append("-" * 80)
            for dep in missing:
                images_str = ", ".join(dep["images"]) if dep["images"] else "None"
                lines.append(f"  Name:     {dep['name']}")
                lines.append(f"  Images:   {images_str}")
                lines.append(f"  Replicas: {dep['replicas']}")
                lines.append("")

        extra = comparison.get("extra", [])
        if extra:
            lines.append(f"\n[+] Extra in '{namespace2}' ({len(extra)} deployment(s)):")
            lines.append("-" * 80)
            for dep in extra:
                images_str = ", ".join(dep["images"]) if dep["images"] else "None"
                lines.append(f"  Name:     {dep['name']}")
                lines.append(f"  Images:   {images_str}")
                lines.append(f"  Replicas: {dep['replicas']}")
                lines.append("")

        changed = comparison.get("changed", [])
        if changed:
            lines.append(
                f"\n[~] Changed between namespaces ({len(changed)} deployment(s)):"
            )
            lines.append("-" * 80)
            for change in changed:
                lines.append(f"  Name: {change['name']}")
                differences = change.get("differences", {})

                if "images" in differences:
                    images_ns1 = (
                        ", ".join(differences["images"]["ns1"])
                        if differences["images"]["ns1"]
                        else "None"
                    )
                    images_ns2 = (
                        ", ".join(differences["images"]["ns2"])
                        if differences["images"]["ns2"]
                        else "None"
                    )
                    lines.append("    Images:")
                    lines.append(f"      {namespace1}: {images_ns1}")
                    lines.append(f"      {namespace2}: {images_ns2}")

                if "replicas" in differences:
                    lines.append("    Replicas:")
                    lines.append(
                        f"      {namespace1}: {differences['replicas']['ns1']}"
                    )
                    lines.append(
                        f"      {namespace2}: {differences['replicas']['ns2']}"
                    )

                lines.append("")

        if not missing and not extra and not changed:
            lines.append("\nNo differences found. Namespaces are identical.")
        else:
            lines.append("=" * 80)
            lines.append(
                f"Summary: {len(missing)} missing, {len(extra)} extra, {len(changed)} changed"
            )

        return "\n".join(lines)


class JSONFormatter:
    #
    # format_deployments
    # Formats a list of deployments as JSON with datetime objects converted to ISO format strings
    #
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

    #
    # format_comparison
    # Formats namespace comparison results as JSON with datetime objects converted and summary statistics
    #
    @staticmethod
    def format_comparison(
        comparison: Dict[str, List[Dict[str, Any]]], namespace1: str, namespace2: str
    ) -> str:
        output = {
            "namespace1": namespace1,
            "namespace2": namespace2,
            "missing": [],
            "extra": [],
            "changed": [],
        }

        for dep in comparison.get("missing", []):
            serializable_dep = dep.copy()
            if dep.get("created"):
                serializable_dep["created"] = dep["created"].isoformat()
            output["missing"].append(serializable_dep)

        for dep in comparison.get("extra", []):
            serializable_dep = dep.copy()
            if dep.get("created"):
                serializable_dep["created"] = dep["created"].isoformat()
            output["extra"].append(serializable_dep)

        for change in comparison.get("changed", []):
            serializable_change = {
                "name": change["name"],
                "differences": change["differences"],
                "ns1": change["ns1"].copy(),
                "ns2": change["ns2"].copy(),
            }

            if change["ns1"].get("created"):
                serializable_change["ns1"]["created"] = change["ns1"][
                    "created"
                ].isoformat()
            if change["ns2"].get("created"):
                serializable_change["ns2"]["created"] = change["ns2"][
                    "created"
                ].isoformat()

            output["changed"].append(serializable_change)

        output["summary"] = {
            "missing_count": len(output["missing"]),
            "extra_count": len(output["extra"]),
            "changed_count": len(output["changed"]),
            "identical": (
                len(output["missing"]) == 0
                and len(output["extra"]) == 0
                and len(output["changed"]) == 0
            ),
        }

        return json.dumps(output, indent=2)
