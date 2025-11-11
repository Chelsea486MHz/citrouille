import argparse
import sys
from pathlib import Path

from citrouille.kube_client import K8sClient
from citrouille.formatters import TableFormatter, JSONFormatter


__version__ = "0.1"


def create_parser():
    parser = argparse.ArgumentParser(
        prog="citrouille",
        description="Kubernetes deployment inventory and security analysis tool",
        epilog="For more information, visit: https://github.com/Chelsea486MHz/citrouille"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--kubeconfig",
        type=str,
        default=None,
        metavar="PATH",
        help="Path to kubeconfig file (default: ~/.kube/config)"
    )

    parser.add_argument(
        "--context",
        type=str,
        default=None,
        metavar="NAME",
        help="Kubernetes context to use (default: current-context)"
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        choices=["table", "json"],
        default="table",
        metavar="FORMAT",
        help="Output format: table, json (default: table)"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands",
        required=False
    )

    inventory_parser = subparsers.add_parser(
        "inventory",
        help="List deployments in a namespace",
        description="Generate an inventory of deployments with their images and timestamps"
    )

    inventory_parser.add_argument(
        "namespace",
        type=str,
        nargs="?",
        default="default",
        help="Target namespace (default: default)"
    )

    inventory_parser.add_argument(
        "-A", "--all-namespaces",
        action="store_true",
        help="List deployments across all namespaces"
    )

    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare two namespaces",
        description="Compare deployments between two namespaces to identify drift"
    )

    compare_parser.add_argument(
        "namespace1",
        type=str,
        help="First namespace (source)"
    )

    compare_parser.add_argument(
        "namespace2",
        type=str,
        help="Second namespace (target)"
    )

    security_parser = subparsers.add_parser(
        "security",
        help="Perform security analysis",
        description="Analyze deployments for security vulnerabilities and misconfigurations"
    )

    security_parser.add_argument(
        "namespace",
        type=str,
        nargs="?",
        default="default",
        help="Target namespace (default: default)"
    )

    security_parser.add_argument(
        "--scan-vulnerabilities",
        action="store_true",
        help="Run Trivy vulnerability scan on container images"
    )

    security_parser.add_argument(
        "--check-config",
        action="store_true",
        help="Perform configuration security checks"
    )

    security_parser.add_argument(
        "--check-network",
        action="store_true",
        help="Analyze network security"
    )

    security_parser.add_argument(
        "--generate-sbom",
        action="store_true",
        help="Generate Software Bill of Materials (SBOM) using Trivy"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.kubeconfig:
        kubeconfig_path = Path(args.kubeconfig).expanduser()
        if not kubeconfig_path.exists():
            print(f"Error: kubeconfig file not found: {args.kubeconfig}", file=sys.stderr)
            sys.exit(1)

    if args.command == "inventory":
        handle_inventory(args)
    elif args.command == "compare":
        handle_compare(args)
    elif args.command == "security":
        handle_security(args)


def handle_inventory(args):
    try:
        k8s = K8sClient(kubeconfig=args.kubeconfig, context=args.context)

        if args.all_namespaces:
            deployments = k8s.get_all_deployments()
        else:
            deployments = k8s.get_deployments(namespace=args.namespace)

        if args.output == "json":
            output = JSONFormatter.format_deployments(deployments)
        else:
            output = TableFormatter.format_deployments(deployments)

        print(output)

    except ConnectionError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def handle_compare(args):
    print("[compare] Command not yet implemented")


def handle_security(args):
    print("[security] Command not yet implemented")


if __name__ == "__main__":
    main()
