import pytest
from io import StringIO
from unittest.mock import patch, Mock
from datetime import datetime

from citrouille.cli import create_parser, main


class TestArgumentParser:
    def test_parser_creation(self):
        parser = create_parser()
        assert parser is not None
        assert parser.prog == "citrouille"

    def test_version_argument(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--version"])
        assert exc_info.value.code == 0

    def test_help_argument(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--help"])
        assert exc_info.value.code == 0

    def test_no_command_shows_help(self):
        with patch('sys.argv', ['citrouille']):
            with patch('sys.stdout', new_callable=StringIO):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 0


class TestGlobalOptions:
    def test_kubeconfig_option(self):
        parser = create_parser()
        args = parser.parse_args(["--kubeconfig", "/path/to/config", "inventory"])
        assert args.kubeconfig == "/path/to/config"

    def test_context_option(self):
        parser = create_parser()
        args = parser.parse_args(["--context", "my-context", "inventory"])
        assert args.context == "my-context"

    def test_output_option_table(self):
        parser = create_parser()
        args = parser.parse_args(["-o", "table", "inventory"])
        assert args.output == "table"

    def test_output_option_json(self):
        parser = create_parser()
        args = parser.parse_args(["--output", "json", "inventory"])
        assert args.output == "json"

    def test_output_default(self):
        parser = create_parser()
        args = parser.parse_args(["inventory"])
        assert args.output == "table"

    def test_invalid_output_format(self):
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--output", "yaml", "inventory"])


class TestInventoryCommand:
    def test_inventory_command(self):
        parser = create_parser()
        args = parser.parse_args(["inventory"])
        assert args.command == "inventory"
        assert args.namespace == "default"
        assert args.all_namespaces is False

    def test_inventory_with_namespace(self):
        parser = create_parser()
        args = parser.parse_args(["inventory", "production"])
        assert args.command == "inventory"
        assert args.namespace == "production"

    def test_inventory_all_namespaces(self):
        parser = create_parser()
        args = parser.parse_args(["inventory", "-A"])
        assert args.command == "inventory"
        assert args.all_namespaces is True

    def test_inventory_all_namespaces_long(self):
        parser = create_parser()
        args = parser.parse_args(["inventory", "--all-namespaces"])
        assert args.command == "inventory"
        assert args.all_namespaces is True

    def test_inventory_with_global_options(self):
        parser = create_parser()
        args = parser.parse_args([
            "--kubeconfig", "/custom/config",
            "--context", "prod-cluster",
            "-o", "json",
            "inventory",
            "kube-system"
        ])
        assert args.command == "inventory"
        assert args.namespace == "kube-system"
        assert args.kubeconfig == "/custom/config"
        assert args.context == "prod-cluster"
        assert args.output == "json"

    def test_inventory_help(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["inventory", "--help"])
        assert exc_info.value.code == 0


class TestCompareCommand:
    def test_compare_command(self):
        parser = create_parser()
        args = parser.parse_args(["compare", "production", "staging"])
        assert args.command == "compare"
        assert args.namespace1 == "production"
        assert args.namespace2 == "staging"

    def test_compare_requires_two_namespaces(self):
        parser = create_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["compare", "production"])

    def test_compare_with_global_options(self):
        parser = create_parser()
        args = parser.parse_args([
            "--kubeconfig", "/custom/config",
            "-o", "json",
            "compare",
            "ns1",
            "ns2"
        ])
        assert args.command == "compare"
        assert args.namespace1 == "ns1"
        assert args.namespace2 == "ns2"
        assert args.kubeconfig == "/custom/config"
        assert args.output == "json"

    def test_compare_help(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["compare", "--help"])
        assert exc_info.value.code == 0


class TestSecurityCommand:
    def test_security_command_default(self):
        parser = create_parser()
        args = parser.parse_args(["security"])
        assert args.command == "security"
        assert args.namespace == "default"
        assert args.scan_vulnerabilities is False
        assert args.check_config is False
        assert args.check_network is False
        assert args.generate_sbom is False

    def test_security_with_namespace(self):
        parser = create_parser()
        args = parser.parse_args(["security", "production"])
        assert args.command == "security"
        assert args.namespace == "production"

    def test_security_scan_vulnerabilities(self):
        parser = create_parser()
        args = parser.parse_args(["security", "--scan-vulnerabilities"])
        assert args.scan_vulnerabilities is True

    def test_security_check_config(self):
        parser = create_parser()
        args = parser.parse_args(["security", "--check-config"])
        assert args.check_config is True

    def test_security_check_network(self):
        parser = create_parser()
        args = parser.parse_args(["security", "--check-network"])
        assert args.check_network is True

    def test_security_generate_sbom(self):
        parser = create_parser()
        args = parser.parse_args(["security", "--generate-sbom"])
        assert args.generate_sbom is True

    def test_security_all_flags(self):
        parser = create_parser()
        args = parser.parse_args([
            "security",
            "production",
            "--scan-vulnerabilities",
            "--check-config",
            "--check-network",
            "--generate-sbom"
        ])
        assert args.command == "security"
        assert args.namespace == "production"
        assert args.scan_vulnerabilities is True
        assert args.check_config is True
        assert args.check_network is True
        assert args.generate_sbom is True

    def test_security_with_global_options(self):
        parser = create_parser()
        args = parser.parse_args([
            "--context", "prod",
            "-o", "json",
            "security",
            "kube-system",
            "--scan-vulnerabilities"
        ])
        assert args.command == "security"
        assert args.namespace == "kube-system"
        assert args.context == "prod"
        assert args.output == "json"
        assert args.scan_vulnerabilities is True

    def test_security_help(self):
        parser = create_parser()
        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["security", "--help"])
        assert exc_info.value.code == 0


class TestMainFunction:
    def test_main_with_nonexistent_kubeconfig(self):
        with patch('sys.argv', ['citrouille', '--kubeconfig', '/nonexistent/path', 'inventory']):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "kubeconfig file not found" in mock_stderr.getvalue()

    @patch('citrouille.cli.K8sClient')
    def test_main_inventory_table_output(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s
        mock_k8s.get_deployments.return_value = [{
            "name": "nginx",
            "namespace": "default",
            "images": ["nginx:1.21"],
            "created": datetime(2024, 11, 11, 10, 30, 0),
            "replicas": 3
        }]
        with patch('sys.argv', ['citrouille', 'inventory', 'default']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "nginx" in output
                assert "default" in output
                assert "nginx:1.21" in output

    @patch('citrouille.cli.K8sClient')
    def test_main_inventory_json_output(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s
        mock_k8s.get_deployments.return_value = [{
            "name": "nginx",
            "namespace": "default",
            "images": ["nginx:1.21"],
            "created": datetime(2024, 11, 11, 10, 30, 0),
            "replicas": 3
        }]
        with patch('sys.argv', ['citrouille', '-o', 'json', 'inventory', 'default']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert '"name": "nginx"' in output
                assert '"namespace": "default"' in output

    @patch('citrouille.cli.K8sClient')
    def test_main_inventory_all_namespaces(self, mock_kube_client):
        mock_k8s = Mock()
        mock_kube_client.return_value = mock_k8s
        mock_k8s.get_all_deployments.return_value = []
        with patch('sys.argv', ['citrouille', 'inventory', '-A']):
            main()
            mock_k8s.get_all_deployments.assert_called_once()

    @patch('citrouille.cli.K8sClient')
    def test_main_inventory_connection_error(self, mock_kube_client):
        mock_kube_client.side_effect = ConnectionError("Failed to connect")
        with patch('sys.argv', ['citrouille', 'inventory']):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1
                assert "Error:" in mock_stderr.getvalue()

    def test_main_compare_placeholder(self):
        with patch('sys.argv', ['citrouille', 'compare', 'ns1', 'ns2']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "[compare]" in output
                assert "not yet implemented" in output

    def test_main_security_placeholder(self):
        with patch('sys.argv', ['citrouille', 'security']):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                assert "[security]" in output
                assert "not yet implemented" in output
